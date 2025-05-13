from django.urls import path
from .views import index

app_name = 'image_mngt'
urlpatterns = [
    path(route='home',view=index,name='home')
]
