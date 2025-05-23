from datetime import datetime
import uuid
import shutil
import os
from django.conf import settings
from django.db.models import FileField, ImageField

def get_folder_name():
    currentDate = datetime.now()
    timestamp = currentDate.strftime("%Y%m%d%H%M%S%f")
    return timestamp

def get_file_path(instance,filename):
    foldername = instance.foldername if getattr(instance,'foldername',None)!=None else instance.parent_record.foldername
    unique_id = uuid.uuid4().hex
    fileExt = filename[filename.index('.'):]
    newFileName = f'{unique_id}{fileExt}'
    path = f'images_mngt/{foldername}/{newFileName}'
    return path

def remove_folder(foldername):
    folder_path = f'{settings.BASE_DIR}/media/images_mngt/{foldername}'
    try:
        shutil.rmtree(folder_path)
    except FileNotFoundError:
        print(f'ERROR: Folder not found ({foldername}).')  
    except Exception as e:
        print(f'ERROR({type(e).__name__}): {e}')
        
def remove_image(filename):
    image_path = f'{settings.BASE_DIR}/media/{filename}'
    try:
        os.remove(image_path)
    except FileNotFoundError:
        print(f'ERROR: Image not found in ({image_path}).')  
    except Exception as e:
        print(f'ERROR({type(e).__name__}): {e}')

def checkFilesReplace(instance,form):
    model = instance.__class__
    for field in model._meta.get_fields():
        if isinstance(field,(FileField,ImageField)):
            field_name = field.name
            has_file = True if hasattr(instance,field_name) else False # Flag to define if instance already have a related any value in field_name
            
            #Check if new file was send from form or remove field was checked
            if (getattr(instance,field_name) != form.cleaned_data[field_name] and has_file) or (form.cleaned_data['remove'] == 'on'):
                remove_image(getattr(instance,field_name)) # Remove image from resource
                #If remove field was checked
                if form.cleaned_data['remove'] == 'on':
                    setattr(form.instance,field_name,None) # Break relation between file value and model
                    del(form.cleaned_data['remove']) # Delete remove value to avoid saving issues
    return form