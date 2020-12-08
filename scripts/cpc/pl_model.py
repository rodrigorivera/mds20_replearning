from collections import OrderedDict

import pytorch_lightning as pl
from torch.optim import Adam

from cpc.model import CPC
import torch


class CPCModel(pl.LightningModule):
    def __init__(self, vocab_size, emb_dim, enc_dim, ar_dim, kernel_size, lr):
        super(CPCModel, self).__init__()
        self.save_hyperparameters()
        self.cpc = CPC(vocab_size=vocab_size,
                       emb_dim=emb_dim,
                       enc_dim=enc_dim,
                       ar_dim=ar_dim,
                       kernel_size=kernel_size)

        self.lr = lr

    def configure_optimizers(self):
        return Adam(self.parameters(), lr=self.lr)

    def forward(self, batch):
        return self.cpc(batch)

    def training_step(self, batch, batch_idx):
        text_batch = batch
        info_nce_loss = self.cpc(text_batch)
        self.log('info_nce', info_nce_loss)
        torch.cuda.empty_cache()
        return info_nce_loss

    def validation_step(self, batch, batch_idx):
        text_batch = batch
        info_nce_loss = self.cpc(text_batch)

        self.log('val_info_nce', info_nce_loss)
        torch.cuda.empty_cache()