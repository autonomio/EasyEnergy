import json
import os
from .tracker_run import tracker_run


class MachineEnergy:
    def __init__(self, config, experiment_name='machine_energy',
                 framework='keras',
                 train_func=None):
        self.experiment_name = experiment_name
        self.dest_dir = '/tmp/{}/'.format(experiment_name)

        if not os.path.exists(self.dest_dir):
            os.mkdir(self.dest_dir)

        self.framework = framework
        self.train_func = train_func
        # Handle the case when `config` is a filepath
        if isinstance(config, str):

            with open(config, 'r') as f:
                self.config_data = json.load(f)

            with open('/tmp/{}/easyenergy_config.json'.format(experiment_name),
                      'w') as outfile:
                json.dump(self.config_data, outfile, indent=2)

        # Handle the case when `config` is dict
        elif isinstance(config, dict):
            self.config_data = config
            with open('/tmp/{}/easyenergy_config.json'.format(experiment_name),
                      'w') as outfile:
                json.dump(self.config_data, outfile, indent=2)

        tracker_run(self)
