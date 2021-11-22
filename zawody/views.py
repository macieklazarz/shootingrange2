from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views import generic
from django.shortcuts import render, reverse
from .forms import ZawodyModelForm, SedziaModelForm
from .models import Sedzia, Zawody

# Create your views here.

class ZawodyListView(ListView):
	template_name = "zawody/zawody_lista.html"
	# context_object_name = 'sedzia'

	def get_queryset(self):
		return Zawody.objects.all()

class ZawodyCreateView(CreateView):
	template_name = "zawody/zawody_create.html"
	form_class = ZawodyModelForm

	def get_success_url(self):
		return reverse("zawody_lista")
		return super(ZawodyCreateView, self).form_valid(form)

class ZawodyDeleteView(DeleteView):
	template_name = "zawody/zawody_delete.html"
	context_object_name = 'zawody'

	def get_queryset(self):
		return Zawody.objects.all()

	def get_success_url(self):
		return reverse("zawody_lista")

	def sedzia_delete(request, pk):
		zawody = Zawody.objects.get(id=pk)
		zawody.delete()
		return redirect("zawody_lista")



class SedziaCreateView(CreateView):
	template_name = "zawody/sedzia_create.html"
	form_class = SedziaModelForm

	def get_success_url(self):
		return reverse("sedzia_lista")
		return super(SedziaCreateView, self).form_valid(form)


class SedziaListView(ListView):
	template_name = "zawody/sedzia_lista.html"
	# context_object_name = 'sedzia'

	def get_queryset(self):
		return Sedzia.objects.all().order_by('zawody')

class SedziaDeleteView(DeleteView):
	template_name = "zawody/sedzia_delete.html"
	context_object_name = 'sedzia'

	def get_queryset(self):
		return Sedzia.objects.all()

	def get_success_url(self):
		return reverse("sedzia_lista")

	def sedzia_delete(request, pk):
		sedzia = Sedzia.objects.get(id=pk)
		sedzia.delete()
		return redirect("sedzia_lista")