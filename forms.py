from django import forms
from .models import ImageRecord

class ImageRecordForm(forms.ModelForm):
    class Meta():
        model = ImageRecord
        fields = ['title','image_single','image_multiple']