from .utils import ssh_connect, ssh_file_transfer, ssh_run
import threading


def tracker_run(self):

    clients = ssh_connect(self)
    threads = []
    for machine_id, client in clients.items():
        ssh_file_transfer(self, client, machine_id)

        args = (self, client, machine_id)
        thread = threading.Thread(target=ssh_run, args=args)
        thread.start()
        threads.append(thread)

    for t in threads:
        t.join()
