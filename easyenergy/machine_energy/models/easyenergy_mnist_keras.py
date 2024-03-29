from easyenergy.callbacks.keras import TrainCallback


def mnist_keras():

    import tensorflow as tf

    mnist = tf.keras.datasets.mnist

    (x_train, y_train), (x_test, y_test) = mnist.load_data()
    x_train, x_test = x_train / 255.0, x_test / 255.0

    model = tf.keras.models.Sequential(
        [
            tf.keras.layers.Flatten(input_shape=(28, 28)),
            tf.keras.layers.Dense(128, activation="relu"),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.Dense(10),
        ]
    )

    loss_fn = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)

    model.compile(optimizer="adam", loss=loss_fn, metrics=["accuracy"])
    res_path = '/tmp/energy_results'
    cb = TrainCallback(res_path)
    history = model.fit(x_train, y_train, epochs=3, callbacks=[cb])
    return history


if __name__ == "__main__":
    mnist_keras()
