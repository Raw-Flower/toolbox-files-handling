from django.views.generic import TemplateView, FormView
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import SampleRecordForm
from .models import SampleRecord, ImageRecord
from .model_utils import saveRecord, SaveMultiImages

# Create your views here.
class IndexView(TemplateView):
    template_name = 'image_mngt/core/index.html'
    
class ImageRecorCreationView(FormView):
    template_name = 'image_mngt/core/record_add.html'
    form_class = SampleRecordForm
    success_url = reverse_lazy('image_mngt:image_creation')
    
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            instance = saveRecord(form.cleaned_data)
            if len(form.cleaned_data['image_multiple']) > 0:
                SaveMultiImages(form.cleaned_data['image_multiple'],instance)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
    
    def form_valid(self, form):
        messages.success(request=self.request, message='Sample record has been created succesfully.')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(request=self.request, message='Your data submitted has some errors. please check and try again.')
        return super().form_invalid(form)