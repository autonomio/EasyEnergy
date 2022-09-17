from easyenergy.machine_energy import MachineEnergy
import json

with open('config.json', 'r') as f:
    config = json.load(f)


def test_machine_energy():
    MachineEnergy(config)


test_machine_energy()
