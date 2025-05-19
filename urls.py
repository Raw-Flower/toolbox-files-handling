from django.urls import path
from . import views

app_name = 'image_mngt'
urlpatterns = [
    path(route='index',view=views.IndexView.as_view(),name='index'),
    path(route='add',view=views.SampleCreationView.as_view(),name='add'),
    path(route='list',view=views.SampleListView.as_view(),name='list'),
]
