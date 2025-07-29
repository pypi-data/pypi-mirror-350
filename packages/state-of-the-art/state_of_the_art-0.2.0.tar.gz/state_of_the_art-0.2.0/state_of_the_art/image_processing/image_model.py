import torch.nn as nn
from PIL import Image
from torchvision import transforms
class ImageModel(nn.Module):
    def __init__(self, num_classes):
        super().__init__()
        self.net = nn.Sequential(
            nn.Conv2d(3, 16, 3, padding=1),  # assuming RGB
            nn.ReLU(),
            nn.MaxPool2d(2, 2),
            nn.Conv2d(16, 32, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),
            nn.Flatten(),
            nn.Linear(32 * 16 * 16, num_classes)  # 64x64 input -> downsampled to 16x16
        )

    def forward(self, x):
        return self.net(x)


def load_and_transform_image_for_model(image_path: str):
    """
    where image_path is a path to an image
    """
    image = Image.open(image_path).convert('RGB')
    result = transform_image(image)
    result = result.unsqueeze(0)
    return result

def get_transform():
    return transforms.Compose([
        transforms.Resize((64, 64)),  # adjust as needed
        transforms.ToTensor(),
        transforms.Normalize((0.5,), (0.5,))  # adjust if RGB
    ])

def transform_image(image):
    """
    where image is a PIL image
    """
    return get_transform()(image)
