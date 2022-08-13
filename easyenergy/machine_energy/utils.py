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


def create_temp_file(self, train_func=None,
                     framework='keras'):
    experiment_name = self.experiment_name

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


def ssh_file_transfer(self, client, machine_id):
    '''Transfer the current talos script to the remote machines'''

    sftp = client.open_sftp()

    try:
        sftp.chdir(self.dest_dir)  # Test if dest dir exists

    except IOError:
        sftp.mkdir(self.dest_dir)  # Create dest dir
        sftp.chdir(self.dest_dir)

    create_temp_file(self)
    files = ['easyenergy_mnist_keras.py',
             'easyenergy_mnist_pl.py']

    for file in sftp.listdir('/tmp/{}'.format(
            self.experiment_name)):
        if file.startswith('easyenergy'):
            sftp.remove('/tmp/{}/'.format(self.experiment_name) + file)

    for file in os.listdir('/tmp/{}'.format(self.experiment_name)):
        if file in files:
            sftp.put('/tmp/{}/'.format(self.experiment_name) + file, file)
    sftp.close()
