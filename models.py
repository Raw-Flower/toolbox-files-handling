from django.db import models
from django.utils.translation import gettext_lazy as _
from .utils import get_file_path

# Create your models here.
class Status(models.IntegerChoices):
    enable = (1,'Active')
    disable = (0,'Inactive')

class SampleRecord(models.Model):
    title = models.CharField(_("Title"), max_length=50)
    foldername = models.CharField(_("foldername"), max_length=50, default='')
    image = models.ImageField(_("Image"), upload_to=get_file_path, blank=True)
    createtime = models.DateTimeField(_('createtime'), auto_now_add=True)
    updatetime = models.DateTimeField(_("updatetime"), auto_now=True)
    status = models.IntegerField(_("Status"), choices=Status, default=Status.enable)
    
    class Meta:
        verbose_name = _("Sample record")
        verbose_name_plural = _("Sample records")

    def __str__(self):
        return str(self.id)
    
class ImageRecord(models.Model):
    parent_record = models.ForeignKey(to=SampleRecord, verbose_name=_("Parent record"), on_delete=models.CASCADE)
    image = models.ImageField(_("Image"), upload_to=get_file_path)
    createtime = models.DateTimeField(_('createtime'), auto_now_add=True)
    updatetime = models.DateTimeField(_("updatetime"), auto_now=True)
    status = models.IntegerField(_("Status"), choices=Status, default=Status.enable)

    class Meta:
        verbose_name = _("Image record")
        verbose_name_plural = _("Image records")

    def __str__(self):
        return str(self.id)