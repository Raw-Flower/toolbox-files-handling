from django.db import models
from django.utils.translation import gettext_lazy as _
from .utils import get_file_path

# Create your models here.
class Status(models.IntegerChoices):
    enable = (1,'Active')
    disable = (0,'Inactive')

class ImageRecord(models.Model):
    title = models.CharField(_("Title"), max_length=50)
    image_single = models.ImageField(_("Single reference"), upload_to=get_file_path)
    image_multiple = models.ImageField(_("Multiple references"), upload_to=get_file_path)
    createtime = models.DateTimeField(_('createtime'), auto_now_add=True)
    updatetime = models.DateTimeField(_("updatetime"), auto_now=False)
    status = models.IntegerField(_("Status"), choices=Status, default=Status.enable)
    
    class Meta:
        verbose_name = _("Image record")
        verbose_name_plural = _("Image records")

    def __str__(self):
        return self.title

