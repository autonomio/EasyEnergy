import os
from .utils import check_architecture, get_stdout, detect_machine


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


def write_dockerfile(self, arch):
    '''
    write Dockerfile for building docker images inside each machine
    '''
    framework = self.framework
    experiment_name = self.experiment_name
    train_func = self.train_func

    if not train_func:
        if framework == 'keras':
            filename = 'easyenergy_mnist_keras.py'

        elif framework == 'pl':
            filename = 'easyenergy_mnist_pl.py'
    else:
        filename = 'easyenergy_custom_model.py'

    if arch == 'amd':
        image_name = 'abhijithneilabraham/easyenergy_docker_image_amd64'
    else:
        image_name = 'abhijithneilabraham/easyenergy_docker_image_arm64'

    self.image_name = image_name
    config_name = 'easyenergy_config.json'

    commands = ['FROM ubuntu:20.04',

                'FROM {}'.format(image_name),

                'RUN mkdir /tmp/{}/'.format(experiment_name),

                'COPY {} /tmp/{}/{}'.format(filename,
                                            experiment_name,
                                            filename),

                'COPY {} /tmp/{}/{}'.format(config_name,
                                            experiment_name,
                                            config_name),

                'CMD python3.9 /tmp/{}/{}'.format(experiment_name,
                                                  filename),

                ]

    with open('/tmp/{}/Dockerfile'.format(
            experiment_name), 'w') as f:

        for command in commands:
            f.write(command + '\n')


def docker_ssh_file_transfer(self, client):
    '''Transfer the docker scripts to the remote machines'''

    experiment_name = self.experiment_name
    arch = check_architecture(self, client)

    write_dockerfile(self, arch)

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
                experiment_name) + file,
                file)

    sftp.close()


def amazon_linux_docker_cmds(self):
    '''commands to install docker in amazon linux'''
    cmds = ['sudo yum update -y',
            'sudo amazon-linux-extras install docker',
            'sudo service docker start',
            ]
    return cmds


def docker_install(self, client):

    execute_str = 'sudo docker'
    '''execute commands to install docker across any platform'''

    stdin, stdout, stderr = client.exec_command(execute_str)
    dockerflag = True
    out = get_stdout(self, stdout, stderr)

    if out == "docker_error":
        dockerflag = False

    self.machine_spec = detect_machine(self, client)

    if not dockerflag:
        install = ['chmod +x /tmp/{}/easyenergy_docker.sh'.format(
            self.experiment_name),
            'sh /tmp/{}/easyenergy_docker.sh'.format(
                self.experiment_name)]

        for execute_str in install:
            stdin, stdout, stderr = client.exec_command(execute_str)
            out = get_stdout(self, stdout, stderr)

        if self.machine_spec == 'amazon_linux':
            cmds = [
                'sudo yum update -y',
                'sudo yum install amazon-linux-extras',
                'sudo amazon-linux-extras install docker',
                'sudo service docker start',
                'sudo groupadd docker',
                'sudo usermod -aG docker $USER']

            for cmd in cmds:
                _, stdout, stderr = client.exec_command(cmd)
                get_stdout(self, stdout, stderr)


def docker_image_setup(self, client, machine_id):
    '''Run the transmitted script remotely without args and show its output.

    Parameters
    ----------
    client | `Object` | paramiko ssh client object
    machine_id | `int`| Machine id for each of the distribution machines

    Returns
    -------
    None.

    '''

    execute_strings = []

    docker_install(self, client)

    image_name = self.image_name
    pullstr = 'sudo docker pull {}'.format(image_name)
    execute_strings.append(pullstr)

    for execute_str in execute_strings:
        stdin, stdout, stderr = client.exec_command(execute_str)
        get_stdout(self, stdout, stderr)


def docker_machine_run(self, client, machine_id):
    ''' Run EasyEnergy using docker'''
    machine_id = str(machine_id)
    experiment_name = self.experiment_name
    train_func = self.train_func

    print('started experiment in machine id {}'.format(machine_id))
    rm_container = ['sudo docker stop easyenergy_docker_remote',
                    'sudo docker rm easyenergy_docker_remote']
    build = ['sudo docker build -t easyenergy_docker_remote -f /tmp/' +
             experiment_name + '/Dockerfile /tmp/' + experiment_name + '/']
    cp_str = '/tmp/{}/energy_results/'.format(experiment_name)

    if train_func:
        cp_str = 'sudo docker container cp -a {}:/tmp/{}/{}/ /tmp/{}/'.format(
            'easyenergy_docker_remote',
            experiment_name,
            'energy_results',
            experiment_name)
    else:
        cp_str = 'sudo docker container cp -a {}:/tmp/{}/ /tmp/{}/'.format(
            'easyenergy_docker_remote',
            'energy_results',
            experiment_name)
    execute_strings = [

        'sudo docker run  --name {} {}'.format(
            'easyenergy_docker_remote', 'easyenergy_docker_remote'),
        cp_str,
        'sudo docker stop easyenergy_docker_remote',
        'sudo docker rm easyenergy_docker_remote',
        'sudo docker system prune -af']

    cmd_strings = rm_container + build + execute_strings
    execute_strings = []

    for string in cmd_strings:
        string = string.replace('easyenergy_docker_remote',
                                'easyenergy_docker_remote_' + experiment_name)
        execute_strings.append(string)

    for execute_str in execute_strings:
        stdin, stdout, stderr = client.exec_command(execute_str)
        get_stdout(self, stdout, stderr)

    print('Completed experiment in machine id {}'.format(machine_id))
