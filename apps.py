from django.apps import AppConfig

class ImageMngtConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'image_mngt'
    
    def ready(self):
        from .signals import handle_folder_delete
