import torch
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import NailForm
from .model_loader import load_efficientnet_model
from .models import Nail
from .utils import transform_image

MODEL = load_efficientnet_model()
CLASS_NAMES = [
    "Acral Lentiginous Melanoma",
    "Beaus Line",
    "Blue Finger",
    "Clubbing",
    "Healthy Nail",
    "Koilonychia",
    "Muehrckes Lines",
    "Onychogryphosis",
    "Pitting",
    "Terry-s Nail",
]


class UploadImageView(CreateView):
    model = Nail
    form_class = NailForm

    def form_valid(self, form):
        # Let super() handle the initial save
        response = super().form_valid(form)

        # Now self.object is the saved Nail instance
        try:
            image_path = self.object.nail_image.path

            # Read the image bytes for our transform function
            with open(image_path, "rb") as f:
                image_bytes = f.read()

            # Transform the image and make a prediction
            tensor = transform_image(image_bytes)
            with torch.inference_mode():
                outputs = MODEL(tensor)
                max_probability = torch.softmax(outputs, dim=1).squeeze(0)
                predicted_idx = max_probability.argmax().item()
                predicted_class = CLASS_NAMES[predicted_idx]

            # Update the classification result
            self.object.nail_classification = predicted_class
            self.object.confidence_level = max_probability.max().item()
            self.object.save()

            # Optional: Verify the save worked
            self.object.refresh_from_db()
            print(f"Classification saved: {self.object.nail_classification}")
            print(f"Confidence level saved: {self.object.confidence_level}")

        except (FileNotFoundError, ValueError, IndexError) as e:
            # Handle any errors that might occur during classification
            print(f"Error during classification: {e}")
            # You might want to set a default classification or handle this differently
            self.object.nail_classification = "Classification Error"
            self.object.confidence_level = "Classification Error"
            self.object.save()

        return response

    def get_success_url(self):
        return reverse_lazy("result_detail", kwargs={"pk": self.object.pk})
