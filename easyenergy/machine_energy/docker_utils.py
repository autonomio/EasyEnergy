def docker_install_commands(self):
    '''commands to install docker in a machine'''

    commands = ['curl -fsSL https://get.docker.com -o get-docker.sh',
                'sh get-docker.sh']

    return commands


def write_shell_script(self):
    '''write docker commands to shell script'''
    commands = docker_install_commands(self)

    with open('/tmp/{}/jako_docker.sh'.format(
            self.experiment_name), 'w') as f:
        for command in commands:
            f.write(command + '\n')
