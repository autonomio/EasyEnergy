from .utils import ssh_connect, ssh_file_transfer, ssh_run
from .utils import ssh_get_files, compare_results

from .docker_utils import write_shell_script, write_dockerfile
from .docker_utils import docker_ssh_file_transfer, docker_image_setup
from .docker_utils import docker_machine_run

import threading


def tracker_run(self, docker=False):

    clients = ssh_connect(self)
    threads = []

    for machine_id, client in clients.items():

        ssh_file_transfer(self, client, machine_id)

        if not docker:
            args = (self, client, machine_id)
            thread = threading.Thread(target=ssh_run, args=args)
            thread.start()
            threads.append(thread)

        else:
            write_shell_script(self)
            write_dockerfile(self)
            docker_ssh_file_transfer(self, client)
            docker_image_setup(self, client, machine_id)
            args = (self, client, machine_id)
            thread = threading.Thread(target=docker_machine_run, args=args)
            thread.start()
            threads.append(thread)

    for t in threads:
        t.join()

    clients = ssh_connect(self)
    for machine_id, client in clients.items():
        ssh_get_files(self, client, machine_id)

    compare_results(self)
