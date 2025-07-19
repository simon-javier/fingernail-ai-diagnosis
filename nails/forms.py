from django import forms

from .models import Nail


class NailForm(forms.ModelForm):
    class Meta:
        model = Nail
        fields = ["nail_image"]
