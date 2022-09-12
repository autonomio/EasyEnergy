import os
import torch
from pytorch_lightning import LightningModule, Trainer
from torch.nn import functional as F
from torch.utils.data import DataLoader
from torchvision import transforms
from torchvision.datasets import MNIST
from easyenergy.callbacks.pytorch_lightning import TestBatchCallback


PATH_DATASETS = os.environ.get("PATH_DATASETS", ".")
BATCH_SIZE = 256


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

    def test_step(self, batch, batch_idx):
        inputs, classes = batch
        logits = self(inputs)
        print(logits)


test_ds = MNIST(PATH_DATASETS, train=False,
                download=False,
                transform=transforms.ToTensor())
test_loader = DataLoader(test_ds, batch_size=BATCH_SIZE)

cb = TestBatchCallback()
trainer = Trainer(callbacks=[cb])

mnist_model = MNISTModel()
model = mnist_model.load_from_checkpoint('mnist.ckpt')

test = trainer.test(model, test_loader)
