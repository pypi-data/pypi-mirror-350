import matplotlib.pyplot as plt
import numpy as np
import torch
import pandas as pd

class Metrics:
    def __init__(self):
        self.epochs_results = []

    def set_data(self, train_data, test_data):
        self.train_data = train_data
        self.test_data = test_data

    def calculate_metrics(self, model):
        results = {}
        train_metrics = self._calculate_metrics_for_data(model, self.train_data)
        results['train'] = train_metrics

        test_metrics = self._calculate_metrics_for_data(model, self.test_data)
        results['test'] = test_metrics

        return results

    def calculate_train_and_test_metrics_for_epoch(self, model, loss_fn):
        print("Calculating metrics for epoch")

        results = {
        }

        train_metrics = self._calculate_metrics_for_data(model, self.train_data, loss_fn)
        results['train'] = train_metrics

        test_metrics = self._calculate_metrics_for_data(model, self.test_data, loss_fn)
        results['test'] = test_metrics
        self.epochs_results.append(results)
        print("Train for Epoch", results['train'])
        print("Test for Epoch", results['test'])

        return results
    
    def _calculate_metrics_for_data(self, model, data, loss_fn = None):
        aux = {
            'recall_class_0_success': 0,
            'recall_class_0_fail': 0,
            'recall_class_1_success': 0,
            'recall_class_1_fail': 0,
            'recall_class_2_success': 0,
            'recall_class_2_fail': 0,
            'recall_class_3_success': 0,
            'recall_class_3_fail': 0,
            'recall_class_4_success': 0,
            'recall_class_4_fail': 0,
        }

        result = {
            'loss': 0,
            'accuracy': 0,
        }
        average_loss = 0
        accuracy = 0

        for i in range(len(data)):
            pred, label, prediction_class = self._run_single_prediction(model, data[i])

            if loss_fn:
                # convert label to tensor
                loss = loss_fn(pred, torch.from_numpy(np.array(label)).unsqueeze(0))
                average_loss += loss.item()

            if prediction_class == label:
                accuracy += 1
                aux['recall_class_' + str(label) + '_success'] += 1
            else:
                aux['recall_class_' + str(label) + '_fail'] += 1

            
        if loss_fn:
            result['loss'] = average_loss / len(data)
        result['accuracy'] = accuracy / len(data)

        result['recall_class_0'] = self._calculate_recall_for_class(aux, 0)
        result['recall_class_1'] = self._calculate_recall_for_class(aux, 1)
        result['recall_class_2'] = self._calculate_recall_for_class(aux, 2)
        result['recall_class_3'] = self._calculate_recall_for_class(aux, 3)
        result['recall_class_4'] = self._calculate_recall_for_class(aux, 4)

        return result
    
    def _calculate_recall_for_class(self, aux, class_number):

        success = aux['recall_class_' + str(class_number) + '_success']
        fail = aux['recall_class_' + str(class_number) + '_fail']
        if success + fail == 0:
            return 100
        return success / (success + fail)
    

    def _run_single_prediction(self, model, row):
        X = torch.from_numpy(row[0])
        label = row[1]
        pred = model(X)
        prediction_class = torch.argmax(pred, dim=1).item()
        return pred, label, prediction_class


    def _calculate_class_totals(self, data):
        class_totals = {
            0: 0,
            1: 0,
            2: 0,
            3: 0,
            4: 0,
        }
        for i in range(len(data)):
            class_totals[data[i][1]] += 1
        print("Class totals: ", class_totals)
        return class_totals

    
    def get_dataframe(self) -> pd.DataFrame: # type: ignore
        result = []
        for epoch, data in enumerate(self.epochs_results):
            epoch = epoch + 1
            result.append({
                'epoch': epoch,
                'train_loss': data['train']['loss'],
                'test_loss': data['test']['loss'],
                'train_accuracy': data['train']['accuracy'],
                'test_accuracy': data['test']['accuracy'],
                'train_recall_class_0': data['train']['recall_class_0'],
                'test_recall_class_0': data['test']['recall_class_0'],
                'train_recall_class_1': data['train']['recall_class_1'],
                'test_recall_class_1': data['test']['recall_class_1'],
                'train_recall_class_2': data['train']['recall_class_2'],
                'test_recall_class_2': data['test']['recall_class_2'],
                'train_recall_class_3': data['train']['recall_class_3'],
                'test_recall_class_3': data['test']['recall_class_3'],
                'train_recall_class_4': data['train']['recall_class_4'],
                'test_recall_class_4': data['test']['recall_class_4'],
            })
        return pd.DataFrame(result)
    
    def plot(self):
        df = self.get_dataframe()
        plt.plot(df['epoch'], df['train_loss'], label='Train Loss')
        plt.plot(df['epoch'], df['test_loss'], label='Test Loss')
        plt.plot(df['epoch'], df['train_accuracy'], label='Train Accuracy')
        plt.plot(df['epoch'], df['test_accuracy'], label='Test Accuracy')
        plt.plot(df['epoch'], df['train_recall_class_0'], label='Train Recall Class 0')
        plt.plot(df['epoch'], df['test_recall_class_0'], label='Test Recall Class 0')
        plt.plot(df['epoch'], df['train_recall_class_1'], label='Train Recall Class 1')
        plt.plot(df['epoch'], df['test_recall_class_1'], label='Test Recall Class 1')
        plt.plot(df['epoch'], df['train_recall_class_2'], label='Train Recall Class 2')
        plt.plot(df['epoch'], df['test_recall_class_2'], label='Test Recall Class 2')
        plt.legend()
        plt.show()
