from state_of_the_art.relevance_model.neuralnet import NeuralNetwork
import torch
from typing import List
from sentence_transformers import SentenceTransformer
from state_of_the_art.config import config
import os

class PersonalPreferenceInference:
    instance = None

    @staticmethod
    def get_instance():
        if not PersonalPreferenceInference.instance:
            PersonalPreferenceInference.instance = PersonalPreferenceInference()
        return PersonalPreferenceInference.instance

    def __init__(self) -> None:
        self.model = load_trained_model()
        self.sentence_transformer = SentenceTransformer("all-mpnet-base-v2")

    def predict_batch(self, texts: List[str]) -> List[int]:
        if not texts:
            raise ValueError("No texts provided for batch prediction")
        data = torch.from_numpy(self.create_embeddings(texts))
        indices = torch.argmax(self.model(data), dim=1).tolist()
        return indices

    def predict(self, text: str) -> int:
        return self.predict_batch([text])[0]


    def create_embeddings(self, texts: List[str]):
        return self.sentence_transformer.encode(texts)


def load_trained_model():
    model = NeuralNetwork()
    model.load_state_dict(torch.load(config.TEXT_PREDICTOR_PATH_LOCALLY))
    return model

if __name__ == "__main__":
    import fire

    fire.Fire()
