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


def write_dockerfile(self, platform='amd'):
    framework = self.framework
    experiment_name = self.experiment_name

    if framework == 'keras':
        filename = 'easyenergy_mnist_keras.py'

    elif framework == 'pl':
        filename = 'easyenergy_mnist_pl.py'

    else:
        filename = 'easyenergy_custom_model.py'

    if platform == 'amd':
        image_name = 'abhijithneilabraham/easyenergy_docker_image_amd64'
    else:
        image_name = 'abhijithneilabraham/easyenergy_docker_image'

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

    execute_str = 'sudo docker'
    execute_strings = []
    stdin, stdout, stderr = client.exec_command(execute_str)
    stdout = str(stdout.read())
    stderr = str(stderr.read())

    dockerflag = True

    if stdout:
        if 'command not found' in stdout:
            dockerflag = False
    if stderr:
        if 'command not found' in stderr:
            dockerflag = False

    if not dockerflag:

        install = ['chmod +x /tmp/{}/easyenergy_docker.sh'.format(
            self.experiment_name),
            'sh /tmp/{}/easyenergy_docker.sh'.format(
                self.experiment_name)]

        execute_strings += install

    image_name = self.image_name
    pullstr = 'sudo docker pull {}'.format(image_name)

    pull = [pullstr]
    execute_strings += pull

    for execute_str in execute_strings:
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


def docker_machine_run(self, client, machine_id):
    ''' Run EasyEnergy using docker'''
    machine_id = str(machine_id)
    experiment_name = self.experiment_name
    print('started experiment in machine id {}'.format(machine_id))
    rm_container = ['sudo docker stop easyenergy_docker_remote',
                    'sudo docker rm easyenergy_docker_remote']
    build = ['sudo docker build -t easyenergy_docker_remote -f /tmp/' +
             experiment_name + '/Dockerfile /tmp/' + experiment_name + '/']
    execute_strings = [

        'sudo docker run  --name {} {}'.format(
            'easyenergy_docker_remote', 'easyenergy_docker_remote'),

        'sudo docker container cp -a {}:/tmp/{}/ /tmp/{}/'.format(
            'easyenergy_docker_remote', experiment_name,
            experiment_name),
        'sudo docker stop easyenergy_docker_remote',
        'sudo docker rm easyenergy_docker_remote']

    cmd_strings = rm_container + build + execute_strings
    execute_strings = []

    for string in cmd_strings:
        string = string.replace('easyenergy_docker_remote',
                                'easyenergy_docker_remote_' + experiment_name)
        execute_strings.append(string)

    for execute_str in execute_strings:
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

    print('Completed experiment in machine id {}'.format(machine_id))
