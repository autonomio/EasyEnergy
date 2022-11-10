from .utils import ssh_connect, ssh_file_transfer, ssh_run, run__tracker_local
from .utils import ssh_get_files, compare_results

from .docker_utils import write_shell_script, write_dockerfile
from .docker_utils import docker_ssh_file_transfer, docker_image_setup
from .docker_utils import docker_machine_run

import threading


def tracker_run(self, docker=False):
    '''
    Handles all the steps to run the MachineEnergy features

    Parameters
    ----------
    docker : TYPE: Bool, optional
        DESCRIPTION. The default is False.
        If set to true, pulls docker image to the remote machine
        and runs as a docker container

    Returns
    -------
    None.

    '''

    run_local = self.run_local
    threads = []

    clients = ssh_connect(self)

    for machine_id, client in clients.items():

        ssh_file_transfer(self, client, machine_id)

        if not docker:
            args = (self, client, machine_id)
            thread = threading.Thread(target=ssh_run, args=args)
            thread.start()
            threads.append(thread)

        else:
            write_shell_script(self)
            docker_ssh_file_transfer(self, client)
            docker_image_setup(self, client, machine_id)
            args = (self, client, machine_id)
            thread = threading.Thread(target=docker_machine_run, args=args)
            thread.start()
            threads.append(thread)

    if run_local:
        args = (self, )
        thread = threading.Thread(target=run__tracker_local, args=args)
        thread.start()
        threads.append(thread)

    for t in threads:
        t.join()

    clients = ssh_connect(self)
    for machine_id, client in clients.items():
        ssh_get_files(self, client, machine_id)

    compare_results(self)
