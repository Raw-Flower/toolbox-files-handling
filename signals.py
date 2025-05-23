from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import SampleRecord, ImageRecord
from .utils import remove_folder, remove_image

@receiver(post_delete, sender=SampleRecord)
def handle_folder_delete(sender, instance, using, origin, **kwargs):
    '''
    sender=Model
    instance=model instance
    using=database alias -> default
    origin=queryset or model instance
    '''
    if instance.status == 0:
        remove_folder(instance.foldername)
        
@receiver(post_delete, sender=ImageRecord)
def handle_file_delete(sender, instance, using, origin, **kwargs):
    remove_image(instance.image)