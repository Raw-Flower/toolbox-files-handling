from datetime import datetime
import uuid
import shutil
from django.conf import settings

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
    print(folder_path)
    try:
        shutil.rmtree(folder_path)
    except FileNotFoundError:
        print(f'ERROR: Folder not found ({foldername}).')  
    except Exception as e:
        print(f'ERROR({type(e).__name__}): {e}')