from .gridsearch_run import search


class GridSearch:
    def __init__(self,
                 model_fn,
                 x_train,
                 y_train,
                 params,
                 epochs=None,
                 project_name='grid_search'):
        best_params, emissions = search(model_fn, x_train, y_train, params)
