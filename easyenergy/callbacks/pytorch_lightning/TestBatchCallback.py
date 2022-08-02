from pytorch_lightning.callbacks import Callback
from codecarbon import EmissionsTracker
import os
import time


class TestBatchCallback(Callback):
    def __init__(self, output_dir='energy_results'):
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)
        filename = time.strftime('%D%H%M%S').replace('/', '')
        filename = filename + '_predict_batch_results.csv'
        self.output_file = filename
        self.output_dir = output_dir

    def on_test_batch_start(self, model, pl_module,
                            batch, batch_idx, dataloader_idx):
        self.codecarbon_tracker = EmissionsTracker(
            output_dir=self.output_dir,
            output_file=self.output_file
            )
        self.codecarbon_tracker.start()

    def on_test_batch_end(self, model, pl_module,
                          batch, batch_idx, dataloader_idx,
                          logs=None):
        self.codecarbon_tracker.stop()
