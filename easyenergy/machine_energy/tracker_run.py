from .utils import ssh_connect


def tracker_run(self):
    clients = ssh_connect(self)
    