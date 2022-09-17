from easyenergy.machine_energy import MachineEnergy
import json

with open('config.json', 'r') as f:
    config = json.load(f)


def train_method():
    import os
    import torch
    from pytorch_lightning import LightningModule, Trainer
    from pytorch_lightning.callbacks.progress import TQDMProgressBar

    from torch.nn import functional as F
    from torch.utils.data import DataLoader
    from torchvision import transforms
    from torchvision.datasets import MNIST

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

    PATH_DATASETS = os.environ.get("PATH_DATASETS", ".")
    BATCH_SIZE = 256 if torch.cuda.is_available() else 64
    # Init our model
    mnist_model = MNISTModel()

    # Init DataLoader from MNIST Dataset
    train_ds = MNIST(PATH_DATASETS,
                     train=True,
                     download=True,
                     transform=transforms.ToTensor())
    train_loader = DataLoader(train_ds, batch_size=BATCH_SIZE)

    # Initialize a trainer
    trainer = Trainer(
        accelerator="auto",
        devices=1 if torch.cuda.is_available() else None,
        max_epochs=3,
        callbacks=[TQDMProgressBar(refresh_rate=20)],
    )

    # Train the model ⚡
    trainer.fit(mnist_model, train_loader)


def test_custom_func_machine_energy():
    MachineEnergy(config, train_func=train_method)
