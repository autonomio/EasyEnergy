from sklearn.model_selection import GridSearchCV
from tensorflow.keras.wrappers.scikit_learn import KerasClassifier
from codecarbon import EmissionsTracker


def search(model_fn, x_train, y_train, params, epochs=None,
           project_name='grid_search'):

    if epochs is None:
        model = KerasClassifier(build_fn=model_fn)
    else:
        model = KerasClassifier(build_fn=model_fn, epochs=epochs)

    model = KerasClassifier(build_fn=model_fn, epochs=epochs)
    param_grid = params
    grid = GridSearchCV(estimator=model, param_grid=param_grid)

    tracker = EmissionsTracker(project_name=project_name)
    tracker.start()
    grid_result = grid.fit(x_train, y_train)
    emissions = tracker.stop()

    print(f'''Best Accuracy : {grid_result.best_score_}
          using {grid_result.best_params_}''')
    print(f"Emissions : {emissions} kg CO₂")

    return grid_result.best_params_, emissions
