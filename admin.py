from django.contrib import admin
from .models import SampleRecord, ImageRecord

# Register your models here.
class SampleRecordAdmin(admin.ModelAdmin):
    list_display = ['id','title','createtime','updatetime','status']
    readonly_fields = ['createtime','updatetime','foldername']
    list_filter = ['status']
    ordering = ['-id']
    search_fields = ['title']

class ImageRecordAdmin(admin.ModelAdmin):
    list_display = ['id','parent_record','createtime','updatetime','status']
    readonly_fields = ['createtime','updatetime']
    list_filter = ['status']
    ordering = ['id']
    
admin.site.register(SampleRecord, SampleRecordAdmin)
admin.site.register(ImageRecord, ImageRecordAdmin)
