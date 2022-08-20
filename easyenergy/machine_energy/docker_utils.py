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


def docker_image_setup(self, client, machine_id, db_machine=False):
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
    dockerflag = True

    if stdout:
        if 'command not found' in stdout:
            dockerflag = False
    if stderr:
        if 'command not found' in stdout:
            dockerflag = False

    if not dockerflag:
        install = ['chmod +x /tmp/{}/easyenergy_docker.sh'.format(
            self.experiment_name),
            '/tmp/{}/easyenergy_docker.sh'.format(
                self.experiment_name)]
        execute_strings += install

    pull = ['sudo docker pull abhijithneilabraham/easyenergy_docker_image']
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
