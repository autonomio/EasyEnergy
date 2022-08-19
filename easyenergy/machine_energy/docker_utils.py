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
