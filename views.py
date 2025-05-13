from django.views.generic import TemplateView, CreateView
from .forms import ImageRecordForm
from .models import ImageRecord

# Create your views here.
class IndexView(TemplateView):
    template_name = 'image_mngt/core/index.html'
    
class ImageRecorCreationView(CreateView):
    template_name = 'image_mngt/core/record_add.html'
    form_class = ImageRecordForm