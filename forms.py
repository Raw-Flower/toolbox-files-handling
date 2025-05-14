from django import forms
from .models import SampleRecord, ImageRecord
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, ProhibitNullCharactersValidator, FileExtensionValidator
from django.conf import settings

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True
    
class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)
        
    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result
        
def imagesTotalSize_validator(image):
    imageSize = round(image.size/1024,2)
    if imageSize > settings.TOTAL_FILE_SIZE:
        raise ValidationError('Your attached file is too big to upload(Maximum 200 KB).')
    return image

def FileImagesChecking(files):
    #Check total images attach to the request
    if len(files) > settings.MAXINUM_MULTI_FILE:
        raise ValidationError('The maximum files to upload simultaneously is 3.')
    
    #Check totalSize from the fileinput
    inputSize = sum(round(i.size/1024,2) for i in files)#generator comprehension
    if inputSize > settings.TOTAL_MULTI_FILE_SIZE:
        raise ValidationError('Your attached files are too big to upload(Maximum 600 KB).')
    
    return files

class SampleRecordForm(forms.Form):
    title = forms.CharField(
        label = 'Title',
        help_text = '',
        max_length = 250,
        min_length = 5,
        validators = [
            RegexValidator(regex='^[a-zA-Z0-9 ]+$',message='This fields contains unvalid characters.'),
            ProhibitNullCharactersValidator,
        ]
    )
    
    image_single = forms.ImageField(
        required = False,
        validators = [
            FileExtensionValidator(allowed_extensions=settings.CUSTOM_FILE_EXTENSIONS,message='Invalid file extension, valid file extensions are .jpeg .jpg .pgn'),
            imagesTotalSize_validator,
            FileImagesChecking,
        ]
    )
    
    image_multiple = MultipleFileField(
        required = False,
        validators = [
            FileExtensionValidator(allowed_extensions=settings.CUSTOM_FILE_EXTENSIONS, message='Invalid file extension, valid file extensions are .jpeg .jpg .pgn'),
            imagesTotalSize_validator,
        ]
    )