from django.views.generic import TemplateView, FormView, ListView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from .forms import SampleRecordForm, RecordFilterForm, SampleRecordModelForm, ChildRecordModelForm
from .models import SampleRecord, ImageRecord
from .model_utils import saveRecord, SaveMultiImages
from .utils import checkFilesReplace

# Create your views here.
class IndexView(TemplateView):
    template_name = 'image_mngt/core/index.html'
    
class SampleCreationView(FormView):
    template_name = 'image_mngt/core/record_add.html'
    form_class = SampleRecordForm
    success_url = reverse_lazy('image_mngt:add')
    
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
    
class SampleListView(ListView):
    template_name = 'image_mngt/core/record_list.html'
    model = SampleRecord
    paginate_by = 5
    context_object_name = 'records'
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['filter_form'] = RecordFilterForm(self.request.GET)
        return context
    
    def get_queryset(self):
        if self.request.GET:
            filter_form = RecordFilterForm(self.request.GET)
            if filter_form.is_valid():
                query_filters = Q(id__exact = filter_form.cleaned_data['id']) if filter_form.cleaned_data['id']!='' else Q()
                query_filters &= Q(title__icontains = filter_form.cleaned_data['title']) if filter_form.cleaned_data['title']!='' else Q()
                query_filters &= Q(status__exact = filter_form.cleaned_data['status']) if filter_form.cleaned_data['status']!='' else Q(status=1)
                queryset = SampleRecord.objects.filter(query_filters).order_by('-createtime')
                return queryset
            else:
                messages.error(request=self.request,message='Your filters have some issues, please check.')
        queryset = SampleRecord.objects.all().order_by('-createtime')
        return queryset
    
class SampleStatusChangeView(TemplateView):
    template_name = 'image_mngt/core/record_disable.html'
    success_url = reverse_lazy("image_mngt:list")
        
    def get(self, request, pk, *args, **kwargs):
        kwargs['pk'] = pk #Assign PK to kwargs
        kwargs['instance'] = get_object_or_404(SampleRecord, id=pk) #Assing instance value
        return super().get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        instance = get_object_or_404(SampleRecord, id=kwargs.get('pk')) #Assing instance value
        instance.status = 1 if instance.status == 0 else 0
        instance.save()
        messages.success(request=self.request, message='Sample record status has been updated succesfully.')
        return redirect(self.success_url)
    
class SampleDeleteView(DeleteView):
    template_name = 'image_mngt/core/record_delete.html'
    success_url = reverse_lazy("image_mngt:list")
    model = SampleRecord
    queryset = SampleRecord.objects.filter(status=0)
    
    def form_valid(self, form):
        messages.success(request=self.request, message='Sample record has been deleted succesfully.')
        return super().form_valid(form)
    
class SampleUpdateView(UpdateView):
    template_name = 'image_mngt/core/record_update.html'
    model = SampleRecord
    queryset = SampleRecord.objects.filter(status=1)
    form_class = SampleRecordModelForm
    
    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['images_related'] = ImageRecord.objects.filter(parent_record=self.get_object().id)
        return context
    
    def get_success_url(self):
        success_url = reverse_lazy("image_mngt:update", kwargs={"pk":self.get_object()})
        return str(success_url)
        
    def form_valid(self, form):
        instance = self.get_object()     
        form = checkFilesReplace(instance,form)
        messages.success(request=self.request, message='Sample record has been updated successfully.')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(request=self.request,message='Your data have some issues, please check and try again.')
        return response
        
class ChildUpdateView(UpdateView):
    template_name = 'image_mngt/core/record_child_update.html'
    model = ImageRecord
    queryset = ImageRecord.objects.filter(status=1)
    form_class = ChildRecordModelForm
    
    def get_success_url(self):
        success_url = reverse_lazy("image_mngt:update_child", kwargs={"pk":self.get_object().id})
        return str(success_url)
    
    def form_valid(self, form):
        instance = self.get_object()     
        form = checkFilesReplace(instance,form)
        messages.success(request=self.request, message='Child record has been updated successfully.')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(request=self.request,message='Your data have some issues, please check and try again.')
        return response
    
class ChildDeleteView(DeleteView):
    template_name = 'image_mngt/core/record_child_delete.html'
    model = ImageRecord
    
    def get_success_url(self):
        success_url = reverse_lazy("image_mngt:update", kwargs={"pk":self.get_object().parent_record})
        return str(success_url)
    
    def form_valid(self, form):
        messages.success(request=self.request, message='Child record has been deleted succesfully.')
        return super().form_valid(form)