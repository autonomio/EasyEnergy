from pytorch_lightning.callbacks import Callback
from codecarbon import EmissionsTracker
import os
import time


class TrainCallback(Callback):
    def __init__(self, output_dir='energy_results'):
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)
        filename = time.strftime('%D%H%M%S').replace('/', '')
        filename = filename + '_train_results.csv'
        self.output_dir = output_dir
        self.output_file = filename
        self.codecarbon_tracker = EmissionsTracker(
            output_dir=self.output_dir,
            output_file=self.output_file
        )

    def on_train_start(self, trainer, pl_module):

        self.codecarbon_tracker.start()

    def on_train_end(self, trainer, pl_module):
        self.codecarbon_tracker.stop()
