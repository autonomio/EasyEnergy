import os


def docker_install_commands(self):
    '''commands to install docker in a machine'''

    commands = ['curl -fsSL https://get.docker.com -o get-docker.sh',
                'sh get-docker.sh']

    return commands


def write_shell_script(self):
    '''write docker commands to shell script'''

    commands = docker_install_commands(self)
    experiment_name = self.experiment_name

    with open('/tmp/{}/easyenergy_docker.sh'.format(
            experiment_name), 'w') as f:

        for command in commands:
            f.write(command + '\n')


def write_dockerfile(self):
    framework = self.framework
    experiment_name = self.experiment_name

    if framework == 'keras':
        filename = 'easyenergy_mnist_keras.py'

    elif framework == 'pl':
        filename = 'easyenergy_mnist_pl.py'

    else:
        filename = 'easyenergy_custom_model.py'

    commands = ['FROM abhijithneilabraham/easyenergy_docker_image',

                'RUN mkdir -p /tmp/',

                'COPY {} /tmp/{}'.format(filename, filename),


                'COPY easyenergy_config.json /tmp/easyenergy_config.json',

                'CMD python3 /tmp/{}'.format(filename),

                'RUN chmod -R 777 /tmp/'
                ]

    with open('/tmp/{}/Dockerfile'.format(
            experiment_name), 'w') as f:

        for command in commands:
            f.write(command + '\n')


def docker_ssh_file_transfer(self, client):
    '''Transfer the docker scripts to the remote machines'''

    experiment_name = self.experiment_name
    dest_dir = self.dest_dir

    write_dockerfile(self)

    sftp = client.open_sftp()

    try:
        sftp.chdir(self.dest_dir)  # Test if dest dir exists

    except IOError:
        sftp.mkdir(self.dest_dir)  # Create dest dir
        sftp.chdir(self.dest_dir)

    docker_files = ['easyenergy_docker.sh', 'Dockerfile']

    for file in os.listdir("/tmp/{}".format(experiment_name)):
        if file in docker_files:
            sftp.put("/tmp/{}/".format(
                experiment_name) + file, dest_dir + file)

    sftp.close()
