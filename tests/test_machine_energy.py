from easyenergy.machine_energy import MachineEnergy
import json
import shutil


# shutil.copy('../autonomio-dev.pem', 'autonomio-dev.pem')

with open('config.json', 'r') as f:
    config = json.load(f)

def test_machine_energy():
    me = MachineEnergy(config)

