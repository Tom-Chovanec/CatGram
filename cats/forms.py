from django import forms
from .models import CatImage


class CatImageForm(forms.ModelForm):
    class Meta:
        model = CatImage
        fields = ['image', 'title']
