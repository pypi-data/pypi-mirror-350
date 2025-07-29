from typing import List, Tuple
import torch
from state_of_the_art.relevance_model.dataset import Dataset
from state_of_the_art.relevance_model.metrics import Metrics
from state_of_the_art.relevance_model.neuralnet import NeuralNetwork
import torch.nn as nn
from mlflow.models import infer_signature
import mlflow
from state_of_the_art.config import config
import numpy as np


class Pipeline:
    DEFAULT_EPOCHS = 200
    def __init__(self):
        self.EPOCHS = self.DEFAULT_EPOCHS
        self.train_data : List[Tuple[torch.Tensor, torch.Tensor]] = None
        self.test_data : List[Tuple[torch.Tensor, torch.Tensor]] = None
        self.train_split = None
        self.test_split = None
        self.current_epoch_loss = None
        self.average_loss_train_epochs = []
        self.average_loss_test_epochs = []
        self.metrics = Metrics()


    def run(self, epochs: int = None):
        if epochs is None:
            self.EPOCHS = self.DEFAULT_EPOCHS
        else:
            self.EPOCHS = epochs
        print("Running with ", self.EPOCHS, " epochs")
        self.train_data, self.test_data = Dataset().get_train_test_split()

        self.metrics.set_data(self.train_data, self.test_data)
        return self._run_train()
    
    def _run_train(self):
        mlflow.set_tracking_uri(config.MLFLOW_TRACKING_URI)
        mlflow.set_experiment("relevance_model")
        
        print("Tracking uri: ", mlflow.get_tracking_uri())

        self.model = NeuralNetwork()

        with mlflow.start_run():
            print("Training mode for ", self.EPOCHS, " epochs")
            for t in range(self.EPOCHS):
                print(f"Epoch {t+1}\n-------------------------------")
                self.train_epoch()

            print("Done training!")
            input_data_sample = torch.from_numpy(self.test_data[4][0])
            print("Example model call: ", self.model(input_data_sample))
            signature = infer_signature(input_data_sample.numpy(), self.model(input_data_sample).detach().numpy())
            mlflow.pytorch.log_model(self.model, "model", signature=signature)

            mlflow.log_metrics({'epochs': self.EPOCHS})
        
        return self.model

    def train_epoch(self):
        size = len(self.train_data)
        loss_fn = nn.CrossEntropyLoss()
        optimizer = torch.optim.SGD(self.model.parameters(), lr=1e-3)

        self.model.train()
        for batch, (X, y) in enumerate(self.train_data):
            X = torch.from_numpy(X)
            y = torch.from_numpy(np.array(y)).unsqueeze(0)

            # Compute prediction error
            pred = self.model(X)
            loss_object = loss_fn(pred, y)

            # Backpropagation
            loss_object.backward()
            optimizer.step()
            optimizer.zero_grad()

            if batch % 100 == 0:
                loss, current = loss_object.item(), (batch + 1) * len(X)
                print(f"loss: {loss:>7f}  [{current:>5d}/{size:>5d}]")
        
        self.metrics.calculate_train_and_test_metrics_for_epoch(self.model, loss_fn)

    
    def save_model(self, model):
        from state_of_the_art.config  import config
        torch.save(model.state_dict(), config.TEXT_PREDICTOR_PATH_LOCALLY)
        print("Model saved to ", config.TEXT_PREDICTOR_PATH_LOCALLY)





if __name__ == "__main__":
    import fire
    fire.Fire(Pipeline)
