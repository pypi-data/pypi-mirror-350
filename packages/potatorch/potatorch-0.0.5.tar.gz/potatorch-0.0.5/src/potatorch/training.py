from typing import Optional
import torch
from torch import nn, Tensor
from torch.utils.data import DataLoader
from torch.optim.lr_scheduler import LinearLR, ReduceLROnPlateau
from potatorch.datasets.utils import split_dataset
from potatorch.datasets.utils import RandomSubsetSampler
from potatorch.datasets.utils import UnbatchedDataloader
from contextlib import ExitStack
from potatorch.utils import to_device
import numpy as np
import gc

def make_optimizer(optimizer_init: callable, *args, **kwargs):
    return lambda m: optimizer_init(m.parameters(), *args, **kwargs)

# TODO: args filter for evaluation metrics
class TrainingLoop():
    def __init__(
            self,
            model,
            dataset,
            loss_fn,
            optimizer,
            train_p=0.7,
            val_p=0.15,
            test_p=0.15,
            random_split=True,
            batch_size:int | None = 1024,
            shuffle=False,
            random_subsampling=None,
            augmenter=None,
            filter_fn=None,
            num_workers=4,
            mixed_precision=False,
            loss_arg_filter=None,
            pin_memory=True,
            callbacks=[],
            val_metrics={},
            device='cpu',
            seed=42):

        self.model = model
        self.dataset = dataset
        self.loss_fn = loss_fn
        # self.optimizer_fn = optimizer_fn
        self.optimizer = optimizer
        self.train_p = train_p
        self.val_p = val_p
        self.test_p = test_p
        self.random_split = random_split
        self.batch_size = batch_size
        self.shuffle = shuffle
        self.random_subsampling = random_subsampling
        self.augmenter = augmenter
        self.filter_fn = filter_fn
        self.num_workers = num_workers
        self.device = device
        self.mixed_precision = mixed_precision
        self.loss_arg_filter = loss_arg_filter
        self.pin_memory = pin_memory
        self.callbacks = callbacks
        self.val_metrics = val_metrics
        self.seed = 42

        # Pytorch auto scaler for mixed precision training (no-ops if not enabled)
        self.scaler = torch.GradScaler(self.device, enabled=self.mixed_precision)
        
        if not self.loss_arg_filter:
            self.loss_arg_filter = lambda x, pred, y: (pred, *y)

        self._clear_state()
        self._init_dataloaders()

    def _clear_state(self):
        """ Clear internal training state """
        self.state = {}
        self.metrics = {}

    def _init_dataloaders(self):
        # TODO: maybe use an other class for evaluation?
        self.train_dataloader, self.val_dataloader, self.test_dataloader = self._make_dataloaders(
                self.dataset,
                self.train_p,
                self.val_p,
                self.test_p)

    def _collate_fn(self, batch):
        if self.filter_fn:
            batch = [data for data in batch if self.filter_fn(data)]
        return torch.utils.data.default_collate(batch)

    def _make_dataloaders(self, dataset, train_p, val_p, test_p):
        shuffle = self.shuffle and self.random_subsampling is not None

        train_ds, val_ds, test_ds = split_dataset(dataset,
                train_p, val_p, test_p, random=self.random_split,
                seed=self.seed)

        sampler = None
        if self.random_subsampling is not None:
            sampler = RandomSubsetSampler(train_ds, self.random_subsampling, replace=False)

        if self.augmenter is not None:
            train_ds = self.augmenter(train_ds)
        
        dataloader_fn = DataLoader if self.batch_size else UnbatchedDataloader

        train_dl = dataloader_fn(train_ds,
                batch_size=self.batch_size,
                shuffle=shuffle,
                sampler=sampler,
                collate_fn=self._collate_fn,
                pin_memory=self.pin_memory,
                num_workers=self.num_workers,
                # prefetch_factor=(self.num_workers*2 if self.num_workers > 0 else None),
                prefetch_factor=2,
                # TODO: how to pass worker_init_fn
                # worker_init_fn=dataset.worker_init_fn,
                persistent_workers=True)
        val_dl = dataloader_fn(val_ds,
                batch_size=self.batch_size*2 if self.batch_size else None,
                collate_fn=self._collate_fn,
                shuffle=False,
                pin_memory=self.pin_memory,
                num_workers=self.num_workers,
                prefetch_factor=2,
                persistent_workers=False)
        test_dl = dataloader_fn(test_ds,
                batch_size=self.batch_size,
                collate_fn=self._collate_fn,
                shuffle=False,
                pin_memory=self.pin_memory,
                num_workers=4)

        return train_dl, val_dl, test_dl

    # TODO: type annotation: can accept anything in input I guess
    def preprocess_batch(self, inputs, *args, **kwargs):
        return to_device(*inputs, device=self.device, non_blocking=True)

    def forward(self, inputs, *args, **kwargs) -> Tensor:
        (X, *ys) = inputs
        X = X.float()
        pred = self.model(X)
        return pred

    def compute_loss(self, inputs, pred, *args, **kwargs) -> Tensor:
        (X, *ys) = inputs
        X = X.float()
        return self.loss_fn(*self.loss_arg_filter(X, pred, ys))

    def backward(self, loss):
        self.scaler.scale(loss).backward()
        self.scaler.step(self.optimizer)
        self.scaler.update()

    def _train(self, epochs):
        if self.train_dataloader is None or self.val_dataloader is None:
            self._init_dataloaders()

        num_batches = len(self.train_dataloader)
        self.update_state('batches', num_batches)
        
        self.on_train_start()
        initial_epoch = self.get_state('epoch', 1)

        for epoch in range(initial_epoch, initial_epoch + epochs):
            self.on_train_epoch_start(epoch)

            self.model.train()
            for batch, inputs in enumerate(self.train_dataloader):
                self.on_train_batch_start(batch)

                # Clear gradients
                self.optimizer.zero_grad(set_to_none=True)

                # Forward pass
                with torch.autocast(device_type=self.device, enabled=self.mixed_precision):
                    inputs = self.preprocess_batch(inputs)
                    pred = self.forward(inputs)
                    loss = self.compute_loss(inputs, pred)

                # Backpropagation
                self.backward(loss)
                self.on_train_batch_end(batch, loss.detach())

            with torch.autocast(device_type=self.device, enabled=self.mixed_precision):
                val_loss, other_metrics = self._test(self.val_dataloader, self.val_metrics)
            self.on_validation_end(val_loss, other_metrics)
            self.on_train_epoch_end(epoch)

        self.on_train_end()

    def _test(self, dataloader, metrics, verbose = False):
        num_batches = len(dataloader)
        self.model.eval()
        test_loss = 0.0
        test_metrics = dict.fromkeys(metrics.keys(), 0.0)
        with torch.no_grad():
            for batch, inputs in enumerate(dataloader):
                if verbose:
                    print(f'Processing batch: {batch + 1}/{num_batches}')
                inputs = self.preprocess_batch(inputs)
                pred = self.forward(inputs)
                loss = self.compute_loss(inputs, pred).detach()
                test_loss = test_loss + (loss - test_loss) / (batch + 1)

                for name, fn in metrics.items():
                    v = test_metrics[name]
                    new = fn(pred, inputs).detach() 
                    test_metrics[name] = v + (new - v) / (batch + 1)

        test_metrics = {k: v for k, v in test_metrics.items()}
        return test_loss, test_metrics

    def predict(self, data):
        """ Run inference over a set of datapoints,
            returning the predicted values.
            `data` can be any iterable complying with the model input.
        """
        self.model.eval()
        h = []
        with torch.no_grad():
            for inputs in data:
                inputs = self.preprocess_batch(inputs)
                pred = self.forward(inputs)
                h = np.concatenate((h, pred.cpu().detach().numpy()), axis=None)

        return h
    
    def run(self, epochs=10, verbose=1):
        self.update_state('verbose', verbose)
        try:
            self._train(epochs)
        except KeyboardInterrupt:
            print('Terminating training loop...')

        return self.model

    def clear(self):
        del self.train_dataloader
        del self.val_dataloader
        del self.test_dataloader
        self._clear_state()
    
    def dump_state(self):
        """ Produces a snapshot dictionary containing all information
            to restore the current state of the TrainingLoop sometime in the
            future.
        """
        assert self.model is not None, "Model not initialized"
        return {
                'model_state_dict': self.model.state_dict(),
                'optimizer_state_dict': self.optimizer.state_dict(),
                'training_loop_state_dict': self.get_states(),
                'training_loop_metrics': self.get_last_metrics(),
                'callbacks_state_dict': [c.state_dict() for c in self.callbacks],
                # 'train_dataloader': self.train_dataloader,
                # 'val_dataloader': self.val_dataloader,
                # 'test_dataloader': self.test_dataloader
                }

    def load_state(self, model, dump):
        """ Loads a TrainingLoop snapshot produced by a call to dump_state. """
        self.model = model
        self.model.load_state_dict(dump['model_state_dict'])
        self.optimizer.load_state_dict(dump['optimizer_state_dict'])
        self.state = dump['training_loop_state_dict']
        self.metrics = dump['training_loop_metrics']

        for i, d in enumerate(dump['callbacks_state_dict']):
            self.callbacks[i].load_state_dict(d)

    def get_last_metric(self, metric, default=None):
        """ Get last computed metric """
        return self.metrics.get(metric, default)

    def get_last_metrics(self):
        return self.metrics.copy()

    def update_metric(self, metric, value):
        """ Update the given metric with the current value
            The method automatically tracks min and max values of the metric
        """
        if torch.is_tensor(value):
            value = value.item()
        min_v = self.get_last_metric(f'min-{metric}')
        max_v = self.get_last_metric(f'max-{metric}')
        self.metrics[metric] = value
        if min_v is None or value < min_v:
            self.metrics[f'min-{metric}'] = value
        if max_v is None or value > max_v:
            self.metrics[f'max-{metric}'] = value

    def update_state(self, key, value):
        self.state[key] = value

    def get_state(self, key, default=None):
        return self.state.get(key, default)

    def get_states(self):
        return self.state.copy()

    """ Callback hooks """
    def on_train_start(self):
        for c in self.callbacks: c.on_train_start(self)

    def on_train_end(self):
        for c in self.callbacks: c.on_train_end(self)

    def on_train_batch_start(self, batch_num):
        self.update_state('batch', batch_num)
        for c in self.callbacks: c.on_train_batch_start(self)

    def on_train_batch_end(self, batch_num, batch_loss):
        # Update current batch loss
        self.update_metric('loss', batch_loss)
        # Current mean loss (default 0 if None)
        mean_loss = self.get_last_metric('mean_loss', 0.0)
        # Running mean loss update
        mean_loss = mean_loss + (batch_loss - mean_loss)/(batch_num + 1)
        self.update_metric('mean_loss', mean_loss)

        # Log current learning rate
        self.update_state('lr', self.optimizer.param_groups[0]['lr'])

        for c in self.callbacks: c.on_train_batch_end(self)

    def on_train_epoch_start(self, epoch_num):
        self.update_metric('mean_loss', 0.0)
        self.update_state('epoch', epoch_num)
        for c in self.callbacks: c.on_train_epoch_start(self)

    def on_train_epoch_end(self, epoch_num):
        # setting epoch + 1 on epoch end is necessary for cases in which
        # the training stopped mid-epoch
        self.update_state('epoch', epoch_num + 1)
        for c in self.callbacks: c.on_train_epoch_end(self)

    def on_validation_batch_start(self):
        for c in self.callbacks: c.on_validation_batch_start(self)

    def on_validation_batch_end(self):
        for c in self.callbacks: c.on_validation_batch_end(self)

    def on_validation_start(self):
        for c in self.callbacks: c.on_validation_start(self)

    def on_validation_end(self, val_loss, other_metrics):
        self.update_metric('val_loss', val_loss)

        for metric, value in other_metrics.items():
            self.update_metric(f'val_{metric}', value)
        for c in self.callbacks: c.on_validation_end(self)
    
    def on_evaluation_end(self, test_loss, other_metrics):
        self.update_metric('test_loss', test_loss)

        for metric, value in other_metrics.items():
            self.update_metric(f'test_{metric}', value)
        for c in self.callbacks: c.on_evaluation_end(self)

    # TODO: maybe use an other class for evaluation?
    # TODO: verbose
    def evaluate(self, metrics, use_test = True, verbose = False):
        with torch.autocast(device_type=self.device, enabled=self.mixed_precision):
            loss, other_metrics = self._test(self.test_dataloader if use_test else self.val_dataloader, metrics, verbose=verbose)

        # self.on_evaluation_end(loss, other_metrics)
        return {'loss': loss, **other_metrics}
