from easyenergy.machine_energy import MachineEnergy
import json

with open('config.json', 'r') as f:
    config = json.load(f)

experiment_name = 'machine_energy'
framework = 'keras'

me = MachineEnergy(config,
                   experiment_name=experiment_name,
                   framework=framework
                   )
