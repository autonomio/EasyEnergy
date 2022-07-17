from .gridsearch_run import search
import os
import json
import time


class GridSearch:
    def __init__(self,
                 model_fn,
                 x_train,
                 y_train,
                 params,
                 epochs=None,
                 project_name='grid_search'):
        best_params, emissions = search(model_fn, x_train, y_train, params)
        save_timestamp = time.strftime('%D%H%M%S').replace('/', '')
        self.save_timestamp = save_timestamp

        if not os.path.exists(project_name):
            os.mkdir(project_name)

        best_params_file = '{}/{}_best_params.json'.format(project_name,
                                                           save_timestamp)
        emissions_file = '{}/{}_emissions.json'.format(project_name,
                                                       save_timestamp)
        with open(best_params_file, 'w') as f:
            json.dump(best_params_file, f, indent=2)

        with open(emissions_file, 'w') as f:
            json.dump(emissions_file, f, indent=2)
