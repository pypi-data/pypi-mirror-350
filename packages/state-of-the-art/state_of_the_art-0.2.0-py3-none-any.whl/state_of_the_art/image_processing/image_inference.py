from state_of_the_art.image_processing.image_model import ImageModel, load_and_transform_image_for_model
from state_of_the_art.relevance_model.neuralnet import NeuralNetwork
import torch
from typing import List
from sentence_transformers import SentenceTransformer
from state_of_the_art.config import config
import os

class ImageInference:
    instance = None

    @staticmethod
    def get_instance():
        if not ImageInference.instance:
            ImageInference.instance = ImageInference()
        return ImageInference.instance

    def __init__(self) -> None:
        self.model = self.load_trained_model()

    def predict_image(self, image_path: str) -> int:
        """
        return the number of the class of the image
        """
        image = load_and_transform_image_for_model(image_path)
        with torch.no_grad():
            result = self.model(image)
        print(result)
        indices = torch.argmax(result, dim=1).tolist()[0]
        return indices


    def load_trained_model(self):
        model = ImageModel(num_classes=3)
        model.load_state_dict(torch.load(config.IMAGE_PREDICTOR_PATH_LOCALLY))
        return model

if __name__ == "__main__":
    import fire

    fire.Fire()
