# classifier/utils.py
import io

from PIL import Image
from torchvision import transforms


def transform_image(image_bytes):
    transform = transforms.Compose(
        [
            transforms.Resize(size=(224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ]
    )

    # Open the image from bytes
    image = Image.open(io.BytesIO(image_bytes))

    # Apply the transforms and add a batch dimension
    return transform(image).unsqueeze(0)
