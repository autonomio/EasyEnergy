import json
import os
from .tracker_run import tracker_run


class MachineEnergy:
    '''
    Handles all arguments and data organising and runs `tracker_run()`.
    '''

    def __init__(self, config, experiment_name='machine_energy',
                 framework='keras',
                 train_func=None,
                 ):
        self.experiment_name = experiment_name

        # directory to save files in destination machines
        self.dest_dir = '/tmp/{}/'.format(experiment_name)

        # directory to save data files in all machines
        data_dir = '/tmp/{}/energy_results/'.format(experiment_name)
        self.data_dir = data_dir

        # directory to get files to local machine
        local_dir = '/tmp/{}/machine_energy_results'.format(experiment_name)
        self.local_dir = local_dir

        if not os.path.exists(self.dest_dir):
            os.mkdir(self.dest_dir)

        if not os.path.exists(self.data_dir):
            os.mkdir(self.data_dir)

        if not os.path.exists(local_dir):
            os.mkdir(local_dir)

        for f in os.listdir(local_dir):
            if f.endswith('.csv'):
                os.remove(os.path.join(local_dir, f))

        self.framework = framework
        self.train_func = train_func

        # Handle the case when `config` is a filepath
        if isinstance(config, str):

            with open(config, 'r') as f:
                self.config_data = json.load(f)

        # Handle the case when `config` is dict
        elif isinstance(config, dict):
            self.config_data = config

        with open('/tmp/{}/easyenergy_config.json'.format(experiment_name),
                  'w') as outfile:
            json.dump(self.config_data, outfile, indent=2)

        if 'run_local' in config.keys():
            run_local = config['run_local']
            self.run_local = run_local
        else:
            self.run_local = False

        docker = False
        if 'run_docker' in config.keys():
            docker = config['run_docker']

        tracker_run(self, docker=docker)
