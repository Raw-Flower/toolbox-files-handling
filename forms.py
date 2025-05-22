from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, ProhibitNullCharactersValidator, FileExtensionValidator
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from .models import Status, SampleRecord

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
        raise ValidationError(
            message=_('Your attached file is too big to upload(Maximum %(size_limit)s KB).'),
            code='file_too_large',
            params={
                'size_limit':settings.TOTAL_FILE_SIZE
            }
        )
    return image

def FileImagesChecking(files):
    #Check total images attach to the request
    if len(files) > settings.MAXINUM_MULTI_FILE:
        raise ValidationError(
            message= _('The maximum files to upload simultaneously is %(multi_file_allow)s.'),
            code='max_file_count_exceeded',
            params={
                'multi_file_allow':settings.MAXINUM_MULTI_FILE
            }
        )
    
    #Check totalSize from the fileinput
    inputSize = sum(round(i.size/1024,2) for i in files)#generator comprehension
    if inputSize > settings.TOTAL_MULTI_FILE_SIZE:
        raise ValidationError(
            message= _('Your attached files are too big to upload(Maximum %(multi_file_size_limit)s KB)'),
            code='total_file_size_exceeded',
            params={
                'multi_file_size_limit':settings.TOTAL_MULTI_FILE_SIZE
            }
        )
    return files

class SampleRecordForm(forms.Form):
    title = forms.CharField(
        label = 'Title',
        help_text = 'Identifier in DB',
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
            FileExtensionValidator(allowed_extensions=settings.CUSTOM_FILE_EXTENSIONS,message=f'Invalid file extension, valid file extensions are {settings.CUSTOM_FILE_EXTENSIONS}'),
            imagesTotalSize_validator,
        ]
    )
    
    image_multiple = MultipleFileField(
        required = False,
        validators = [
            FileExtensionValidator(allowed_extensions=settings.CUSTOM_FILE_EXTENSIONS, message=f'Invalid file extension, valid file extensions are {settings.CUSTOM_FILE_EXTENSIONS}'),
        ]
    )
    
    def clean_image_multiple(self):
        image_multiple = self.cleaned_data.get('image_multiple')
        FileImagesChecking(image_multiple)
        return image_multiple
    

class RecordFilterForm(forms.Form):
    id = forms.CharField(
        help_text='filter_option',
        required=False,
        max_length = 250,
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'placeholder':'ID',
            }
        ),
        validators = [
            RegexValidator(regex='^[0-9]+$',message='This field contains unvalid characters.'),
        ]
    )
    
    title = forms.CharField(
        help_text='filter_option',
        required=False,
        max_length = 250,
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'placeholder':'Title',
            }
        ),
        validators = [
            RegexValidator(regex='^[a-zA-Z0-9 ]+$',message='This field contains unvalid characters.'),
        ]
    )
    
    status = forms.ChoiceField(
        help_text='filter_option',
        required=False,
        choices=Status.choices,
        widget = forms.Select(
            attrs={
                'class':'form-control'
            }
        ),
         validators=[
            RegexValidator(regex='^[0-9]+$',message='This field contains unvalid characters.')
        ]
    )
    
class SampleRecordModelForm(forms.ModelForm):
    image = forms.ImageField(
        required=False,        
        validators=[
            FileExtensionValidator(allowed_extensions=settings.CUSTOM_FILE_EXTENSIONS,message=f'Invalid file extension, valid file extensions are {settings.CUSTOM_FILE_EXTENSIONS}'),
            imagesTotalSize_validator,
        ]
    )
    image.widget.template_name = 'image_mngt/widgets/customFileInput.html'
    image.widget.clear_checkbox_label = 'Remove'
 
    class Meta:
        model = SampleRecord
        fields = ['title','image']
        
    def clean(self):
        clean_data = super().clean()
        post_data = self.data
        clean_data['remove'] = post_data.get('remove','off') #Manually add the remove field
        return clean_data
