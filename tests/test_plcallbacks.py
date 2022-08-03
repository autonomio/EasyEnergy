import os
import torch
from pytorch_lightning import LightningModule, Trainer
from pytorch_lightning.callbacks.progress import TQDMProgressBar
from torch.nn import functional as F
from torch.utils.data import DataLoader
from torchvision import transforms
from torchvision.datasets import MNIST
from easyenergy.callbacks.pytorch_lightning import TrainCallback
from easyenergy.callbacks.pytorch_lightning import TrainBatchCallback
from easyenergy.callbacks.pytorch_lightning import PredictCallback
from easyenergy.callbacks.pytorch_lightning import PredictBatchCallback


PATH_DATASETS = os.environ.get("PATH_DATASETS", ".")


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

test_ds = MNIST(PATH_DATASETS, train=False,
                download=False,
                transform=transforms.ToTensor())


def test_traincallback():

    cb = TrainCallback()
    BATCH_SIZE = 256
    train_loader = DataLoader(train_ds, batch_size=BATCH_SIZE)
    trainer = Trainer(
        accelerator="auto",
        devices=None,
        max_epochs=2,
        callbacks=[TQDMProgressBar(refresh_rate=20), cb],
    )

    trainer.fit(mnist_model, train_loader)
    trainer.save_checkpoint('mnist.ckpt')


def test_trainbatchcallback():
    BATCH_SIZE = 10000
    train_loader = DataLoader(train_ds, batch_size=BATCH_SIZE)
    cb = TrainBatchCallback()
    trainer = Trainer(
        accelerator="auto",
        devices=None,
        max_epochs=2,
        callbacks=[TQDMProgressBar(refresh_rate=20), cb],
    )

    trainer.fit(mnist_model, train_loader)


def test_predictcallback():
    BATCH_SIZE = 10000
    test_loader = DataLoader(test_ds, batch_size=BATCH_SIZE)
    test_list = [t[0] for t in test_loader]

    cb = PredictCallback()
    trainer = Trainer(callbacks=[cb])
    model = mnist_model.load_from_checkpoint('mnist.ckpt')
    trainer.predict(model, test_list)


def test_predictbatchcallback():
    BATCH_SIZE = 10000
    test_loader = DataLoader(test_ds)
    test_list = [t[0] for t in test_loader]
    test_dl = DataLoader(test_list, batch_size=BATCH_SIZE)

    cb = PredictBatchCallback()
    trainer = Trainer(callbacks=[cb])
    model = mnist_model.load_from_checkpoint('mnist.ckpt')
    trainer.predict(model, test_dl)


test_traincallback()
test_trainbatchcallback()
test_predictcallback()
test_predictbatchcallback()
