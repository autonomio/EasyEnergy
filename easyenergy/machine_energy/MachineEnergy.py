import json
from .tracker_run import tracker_run


class MachineEnergy:
    def __init__(self, config):
        # Handle the case when `config` is a filepath
        if isinstance(config, str):
            with open(config, 'r') as f:
                self.config_data = json.load(f)

        # Handle the case when `config` is dict
        elif isinstance(config, dict):
            self.config_data = config
            with open('config.json', 'w') as outfile:
                json.dump(self.config_data, outfile, indent=2)

        tracker_run(self)
