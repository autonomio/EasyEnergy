import paramiko
from inspect import getsource


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

        if framework == 'keras':
            from .models import mnist_keras
            filestr = getsource(mnist_keras)

            with open("/tmp/{}/mnist_keras.py".format(
                    experiment_name), "w") as f:
                f.write(filestr)

        elif framework == 'pl':
            from .models import mnist_pl
            filestr = getsource(mnist_pl)
            with open("/tmp/{}/mnist_pl.py".format(
                    experiment_name), "w") as f:
                f.write(filestr)
