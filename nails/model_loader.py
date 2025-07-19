# classifier/model_loader.py
from pathlib import Path

import torch
import torchvision.models as models
from torch import nn


def load_vgg16_model():
    try:
        model = models.vgg16()
        model.classifier[6] = nn.Linear(in_features=4096, out_features=10)
        model_path = Path(__file__).parent / "models/vgg_16_epoch_15.pth"
        model.load_state_dict(torch.load(model_path, map_location=torch.device("cpu")))
        model.eval()

        return model

    except Exception as e:
        print(f"Model loading failed: {e}")
        return None


def load_efficientnet_model():
    try:
        model = models.efficientnet_v2_s(
            weights=models.EfficientNet_V2_S_Weights.DEFAULT
        )
        model.classifier[1] = nn.Linear(model.classifier[1].in_features, 10)
        model_path = Path(__file__).parent / "models/efficientnetv2s_epoch5.pth"
        model.load_state_dict(torch.load(model_path, map_location="cpu"))
        model.eval()
        return model

    except Exception as e:
        print(f"Model loading failed: {e}")
        return None
