def mnist_pl():
    import os
    import torch
    from pytorch_lightning import LightningModule, Trainer
    from pytorch_lightning.callbacks.progress import TQDMProgressBar
    from torch.nn import functional as F
    from torch.utils.data import DataLoader
    from torchvision import transforms
    from torchvision.datasets import MNIST
    from easyenergy.callbacks.pytorch_lightning import TrainCallback

    PATH_DATASETS = os.environ.get("PATH_DATASETS", ".")
    BATCH_SIZE = 256 if torch.cuda.is_available() else 64

    class MNISTModel(LightningModule):
        def __init__(self):
            super().__init__()
            self.l1 = torch.nn.Linear(28 * 28, 10)

        def forward(self, x):
            return torch.relu(self.l1(x.view(x.size(0), -1)))

        def training_step(self, batch, batch_nb):
            x, y = batch
            loss = F.cross_entropy(self(x), y)
            return loss

        def configure_optimizers(self):
            return torch.optim.Adam(self.parameters(), lr=0.02)

    # Init the model
    mnist_model = MNISTModel()
    # Use the easyenergy Callback for tracking energy during training
    cb = TrainCallback()

    # Init DataLoader from MNIST Dataset
    train_ds = MNIST(PATH_DATASETS, train=True,
                     download=True,
                     transform=transforms.ToTensor())
    train_loader = DataLoader(train_ds, batch_size=BATCH_SIZE)

    # Initialize a trainer
    trainer = Trainer(
        accelerator="auto",
        devices=None,
        max_epochs=3,
        callbacks=[TQDMProgressBar(refresh_rate=20), cb],
    )

    # Train the model ⚡
    trainer.fit(mnist_model, train_loader)
    return trainer


def mnist_keras():
    from easyenergy.callbacks.keras import TrainCallback
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

    cb = TrainCallback()
    history = model.fit(x_train, y_train, epochs=3, callbacks=[cb])
    return history
