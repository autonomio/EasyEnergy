from tensorflow.keras.callbacks import Callback
import time
from codecarbon import EmissionsTracker
import os

'''
Callback class to pass as arguments for model.predict() in Keras.
Runs Codecarbon tracking per every batch while predicting.
'''


class PredictBatchCallback(Callback):
    def __init__(self, output_dir='energy_results'):
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)
        filename = time.strftime('%D%H%M%S').replace('/', '')
        filename = filename + '_predict_batch_results.csv'
        self.output_file = filename
        self.output_dir = output_dir

    def on_predict_batch_begin(self, batch, logs=None):
        self.codecarbon_tracker = EmissionsTracker(
            output_dir=self.output_dir,
            output_file=self.output_file
            )
        self.codecarbon_tracker.start()

    def on_predict_batch_end(self, batch, logs=None):
        self.codecarbon_tracker.stop()
