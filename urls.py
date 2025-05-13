from django.urls import path
from . import views

app_name = 'image_mngt'
urlpatterns = [
    path(route='index',view=views.IndexView.as_view(),name='index'),
    path(route='creation',view=views.ImageRecorCreationView.as_view(),name='image_creation'),
]
