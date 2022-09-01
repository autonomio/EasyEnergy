from easyenergy.machine_energy import MachineEnergy
import json


with open('config.json', 'r') as f:
    config = json.load(f)

me = MachineEnergy(config)
