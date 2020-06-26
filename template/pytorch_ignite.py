""" pytorch-ignite template """

from logging import Logger
# torch
import torch.nn as nn
from torch.utils.tensorboard import SummaryWriter
# ignite
from ignite.contrib.handlers import ProgressBar
from ignite.engine import Engine, Events
from ignite.metrics import RunningAverage
from ignite.handlers import Checkpoint, EarlyStopping, Timer

def write_metrics():
    # summry to tensorboard etc...
    pass


def prepare_loaders():
    # prepare dataloaders
    return train_loader, test_loader

# early stopping
def score_function(engine):
    return score

def train(): 
    # tensor board
    writer = SummaryWriter(log_dir='xxx')
    device = torch.device('cuda')

    # prepare dataset
    train_loader, test_loader = prepare_loaders()

    # prepare model
    model = Model()

    # prepare optimizers, etc
    loss = nn.CrossEntropyLoss()
    optimizer = Adam()

    # train iteration
    def train_step(engine: Engine, x: torch.Tensor):
        model.train()
        optimizer.zero_grad()

        y: torch.Tensor = model(x)

        loss.backward()
        optimizer.step()

        # return metrics
        return {
            'nll': loss.item()
        }
    
    # validate iteration
    def validate_step(engine: Engine, x: torch.Tensor):
        model.eval()
        with torch.no_grad():
            y: torch.Tensor = model(x)

            return {
                'nll': loss(y).item(),
            }

    # custom trainer, validator
    trainer = Engine(train_step)
    validator = Engine(test_step)
    
    # metrics
    nll_metric = RunningAverage(alpha=options.alpha, output_transform=lambda output: output['nll'])
    nll_metric.attach(trainer, 'nll')

    bar = ProgressBar()
    desc = 'Epoch {} Iteration {} - nll: {:.2f}'
    bar.attach(trainer, metric_names=['nll'])

    # pytorch_ignite handlers
    logger.info(f'- add handlers ...')


    # model saver
    checkpoint_handler = Checkpoint(model, n_saved=3)
    trainer.add_event_handler(Events.EPOCH_COMPLETED, checkpoint_handler)

    early_stop_handler = EarlyStopping(patience=5, score_function=score_function, trainer=trainer)
    evaluator.add_event_handler(Events.EPOCH_COMPLETED, early_stop_handler)

    # called every iteration
    @trainer.on(Events.ITERATION_COMPLETED(every=10))
    def log_training_loss(engine: Engine):
        nll = engine.state.output['nll']
        bar.desc = desc.format(engine.state.epoch, engine.state.iteration, nll)
    
    # called every epoch
    @trainer.on(Events.EPOCH_COMPLETED)
    def train_result(engine: Engine):
        evaluator.run(train_loader)
        write_metrics(mode='train')

    # validate
    @trainer.on(Events.EPOCH_COMPLETED)
    def test_result(engine: Engine):
        evaluator.run(test_loader)
        write_metrics(mode='test')

    # gracelly stop
    @trainer.on(Events.EXCEPTION_RAISED)
    def handle_exception(engine, e):
        if isinstance(e, KeyboardInterrupt) and (engine.state.iteration > 1):
            engine.terminate()

            # model save, etc...

            logger.warning('KeyboardInterrupt caught. Exiting gracefully.')
        else:
            logger.error(e)

    # called when train has finished
    @trainer.on(Events.COMPLETED)
    def handle_completed(engine: Engine):
        pass

    # training
    trainer.run(train_loader, max_epochs=100)
