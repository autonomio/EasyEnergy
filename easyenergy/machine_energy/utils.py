import paramiko
from inspect import getsource
import os


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

    if not train_func:
        # if custom train function is not added.
        if framework == 'keras':
            from .models import mnist_keras
            filestr = getsource(mnist_keras)

            with open("/tmp/{}/easyenergy_mnist_keras.py".format(
                    experiment_name), "w") as f:
                f.write(filestr)

        elif framework == 'pl':
            from .models import mnist_pl
            filestr = getsource(mnist_pl)
            with open("/tmp/{}/easyenergy_mnist_pl.py".format(
                    experiment_name), "w") as f:
                f.write(filestr)
    else:
        filestr = getsource(train_func)
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
                 'easyenergy_mnist_pl.py']
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
