from easyenergy.callbacks.pytorch_lightning import TrainCallback


def mnist_pl():
    import os
    import torch
    from pytorch_lightning import LightningModule, Trainer
    from pytorch_lightning.callbacks.progress import TQDMProgressBar
    from torch.nn import functional as F
    from torch.utils.data import DataLoader
    from torchvision import transforms
    from torchvision.datasets import MNIST

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


if __name__ == "__main__":
    mnist_pl()
