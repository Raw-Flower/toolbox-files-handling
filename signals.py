from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import SampleRecord
from .utils import remove_folder

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