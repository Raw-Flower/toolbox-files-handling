from .models import SampleRecord, ImageRecord
from .utils import get_folder_name

def saveRecord(cleaned_data):
    instance = SampleRecord(
        title = cleaned_data['title'],
        foldername = get_folder_name(),
        image = cleaned_data['image_single']
    )
    instance.save()
    return instance
    
def SaveMultiImages(images_list,parent_obj):
    for image in images_list:
        instance = ImageRecord(
            parent_record = parent_obj,
            image = image
        )
        instance.save()