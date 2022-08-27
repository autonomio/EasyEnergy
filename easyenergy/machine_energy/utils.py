import paramiko
from inspect import getsource
import os
import shutil
import pandas as pd
import time


def ssh_connect(self):
    '''
    Returns
    -------
    clients | `list` | List of client objects of machines after connection.

    '''

    configs = self.config_data['machines']
    clients = {}

    for config in configs:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        host = config['MACHINE_IP_ADDRESS']
        port = config['MACHINE_PORT']
        username = config['MACHINE_USER']

        if 'MACHINE_PASSWORD' in config.keys():
            password = config['MACHINE_PASSWORD']
            client.connect(host, port, username, password)

        elif 'MACHINE_KEY_FILENAME' in config.keys():
            client.connect(host, port, username,
                           key_filename=config['MACHINE_KEY_FILENAME'])

        clients[config['machine_id']] = client

    return clients


def create_temp_file(self):

    experiment_name = self.experiment_name
    train_func = self.train_func
    framework = self.framework
    currpath = os.path.dirname(__file__)
    modelpath = currpath + '/models/'

    if not train_func:
        # if custom train function is not added.
        if framework == 'keras':
            shutil.copyfile(modelpath + 'easyenergy_mnist_keras.py',
                            '/tmp/{}/easyenergy_mnist_keras.py'.format(
                                experiment_name))

        elif framework == 'pl':
            shutil.copyfile(modelpath + 'easyenergy_mnist_pl.py',
                            '/tmp/{}/easyenergy_mnist_pl.py'.format(
                                experiment_name))
    else:
        filestr = getsource(train_func)
        func_name = train_func.__name__
        run_command = func_name + '()'
        filestr = filestr + '\n' + run_command
        with open("/tmp/{}/easyenergy_custom_model.py".format(
                experiment_name), "w") as f:
            f.write(filestr)


def ssh_file_transfer(self, client, machine_id):
    '''Transfer the model script to the remote machines'''

    sftp = client.open_sftp()

    try:
        sftp.chdir(self.dest_dir)  # Test if dest dir exists

    except IOError:
        sftp.mkdir(self.dest_dir)  # Create dest dir
        sftp.chdir(self.dest_dir)

    create_temp_file(self)

    if not self.train_func:
        files = ['easyenergy_mnist_keras.py',
                 'easyenergy_mnist_pl.py',
                 'easyenergy_config.json']
    else:
        files = ['easyenergy_custom_model.py']

    for file in sftp.listdir('/tmp/{}'.format(
            self.experiment_name)):
        if file.startswith('easyenergy'):
            sftp.remove('/tmp/{}/'.format(self.experiment_name) + file)

    for file in os.listdir('/tmp/{}'.format(self.experiment_name)):
        if file in files:
            sftp.put('/tmp/{}/'.format(self.experiment_name) + file, file)
    sftp.close()


def ssh_run(self, client, machine_id):
    '''Run the transmitted script remotely

    Parameters
    ----------
    client | `Object` | paramiko ssh client object
    machine_id | `int`| Machine id for each of the machines

    Returns
    -------
    None.

    '''
    if not self.train_func:

        if self.framework == 'keras':
            execute_str = 'python3 /tmp/{}/easyenergy_mnist_keras.py'.format(
                self.experiment_name)
        elif self.framework == 'pl':
            execute_str = 'python3 /tmp/{}/easyenergy_mnist_pl.py'.format(
                self.experiment_name)

    else:
        execute_str = 'python3 /tmp/{}/easyenergy_custom_model.py'.format(
            self.experiment_name)

    stdin, stdout, stderr = client.exec_command(execute_str)

    if stderr:
        for line in stderr:
            try:
                # Process each error line in the remote output
                print(line)
            except Exception as e:
                print(e)

    for line in stdout:
        try:
            # Process each line in the remote output
            print(line)
        except Exception as e:
            print(e)


def ssh_get_files(self, client, machine_id):
    '''Get files via ssh from a machine'''
    experiment_name = self.experiment_name
    sftp = client.open_sftp()
    data_dir = '/tmp/{}/energy_results/'.format(experiment_name)
    local_dir = '/tmp/{}/machine_energy_results'.format(experiment_name)
    self.local_dir = local_dir

    try:
        sftp.chdir(data_dir)  # Test if dest dir exists

    except IOError:
        sftp.mkdir(data_dir)  # Create dest dir
        sftp.chdir(data_dir)

    for f in os.listdir(local_dir):
        if f.endswith('.csv'):
            os.remove(os.path.join(local_dir, f))

    execute_str = 'sudo chmod 777 -R /tmp'
    stdin, stdout, stderr = client.exec_command(execute_str)

    for file in sftp.listdir(data_dir):
        if file.endswith('.csv'):
            sftp.get(data_dir + file, '/tmp/{}/{}/'.format(
                self.experiment_name,
                'machine_energy_results') + 'machine_' +
                str(machine_id) + '_' + file)

    files = sftp.listdir(path=data_dir)
    for file in files:
        sftp.remove(data_dir + file)

    sftp.close()


def compare_results(self):
    local_dir = self.local_dir
    emissions = []
    energy_consumption = []
    machine_ids = []
    for f in os.listdir(local_dir):
        if f.endswith('.csv'):
            data = pd.read_csv(local_dir + '/' + f)
            machine_id = int(f.split('_')[1])
            emissions.append(data['emissions'])
            energy_consumption.append(data['energy_consumed'])
            machine_ids.append(machine_id)
    res = pd.DataFrame({'machine_id': machine_ids,
                        'emissions': emissions,
                        'energy_consumption': energy_consumption})

    save_folder = 'machine_energy_comparison/'

    if not os.path.exists(save_folder):
        os.mkdir(save_folder)

    filename = time.strftime('%D%H%M%S').replace('/', '')
    filename = filename + '_results.csv'

    res.to_csv(save_folder + '/' + filename)

    return res
