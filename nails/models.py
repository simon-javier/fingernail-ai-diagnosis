import torch
from django.db import models
from django.urls import reverse

from .model_loader import load_efficientnet_model
from .utils import transform_image

# Load the model once when the module is imported
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


class Nail(models.Model):
    nail_classification = models.CharField(max_length=100, blank=True, null=True)
    confidence_level = models.DecimalField(
        max_length=10, max_digits=10, decimal_places=2, blank=True, null=True
    )
    nail_image = models.ImageField(upload_to="nail_img/")

    def get_absolute_url(self):
        return reverse("result_detail", kwargs={"pk": self.pk})

    def save(self, *args, **kwargs):
        # Check if this is a new object or if the image has changed
        old_image = None
        if self.pk:
            try:
                old_image = Nail.objects.get(pk=self.pk).nail_image
            except Nail.DoesNotExist:
                old_image = None

        # Save the object first to ensure the file is available
        super().save(*args, **kwargs)

        # Only classify if we have an image and (it's new or changed or no classification exists)
        if self.nail_image and (
            old_image != self.nail_image or not self.nail_classification
        ):
            try:
                self.classify_image()
            except Exception as e:
                print(f"Classification error: {e}")
                self.nail_classification = "Classification Error"
                # Save again with the error status
                super().save(update_fields=["nail_classification", "confidence_level"])

    def classify_image(self):
        """Classify the nail image and update the nail_classification field"""
        try:
            image_path = self.nail_image.path

            # Read the image bytes
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
            self.nail_classification = predicted_class
            self.confidence_level = max_probability.max().item()

            # Save only the classification field to avoid recursion
            super().save(update_fields=["nail_classification", "confidence_level"])

            print(
                f"Nail {self.pk} classified as: {predicted_class}\nConfidence Level {max_probability.max().item()}"
            )

        except Exception as e:
            raise Exception(f"Error classifying imager {e}")

    def __str__(self):
        return f"Nail {self.pk} - {self.nail_classification or 'Not classified'} - {self.confidence_level or 'Not classified'}"
