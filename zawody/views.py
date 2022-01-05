from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views import generic
from django.shortcuts import render, reverse
from .forms import ZawodyModelForm, SedziaModelForm
from .models import Sedzia, Zawody
from wyniki.views import sedziowie_lista
from django.shortcuts import redirect
from account.views import sedziowie_lista
from mainapp.views import nazwa_turnieju

# Create your views here.

class ZawodyListView(LoginRequiredMixin, ListView):
	login_url = '/login/'
	template_name = "zawody/zawody_lista.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['sedziowie_lista'] = sedziowie_lista()
		# context['rts_lista'] = rts_lista()
		context['pk'] = self.kwargs['pk']
		context['nazwa_turnieju'] = nazwa_turnieju(self.kwargs['pk'])
		return context

	def get_queryset(self):
		return Zawody.objects.all()

	def dispatch(self, request, *args, **kwargs):
		try:
			if request.user.is_admin:
				return super(ZawodyListView, self).dispatch(request, *args, **kwargs)
			else:
				return redirect('not_authorized')
		except:
			return redirect('not_authorized')

class ZawodyCreateView(LoginRequiredMixin, CreateView):
	login_url = '/login/'
	template_name = "zawody/zawody_create.html"
	form_class = ZawodyModelForm

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['sedziowie_lista'] = sedziowie_lista()
		context['pk'] = self.kwargs['pk']
		context['nazwa_turnieju'] = nazwa_turnieju(self.kwargs['pk'])
		# context['rts_lista'] = rts_lista()
		return context

	def get_success_url(self):
		return reverse("zawody_lista", kwargs={'pk':self.kwargs['pk']})
		return super(ZawodyCreateView, self).form_valid(form)
	def dispatch(self, request, *args, **kwargs):
		try:
			if request.user.is_admin:
				print('proba')
				return super(ZawodyCreateView, self).dispatch(request, *args, **kwargs)
			else:
				print('try')
				return redirect('not_authorized')
		except:
			# print('exc')
			# return redirect("not_authorized")
			# return reverse("zawody_lista pk=self.kwargs['pk']")
			pass
			

class ZawodyDeleteView(LoginRequiredMixin, DeleteView):
	login_url = '/login/'
	template_name = "zawody/zawody_delete.html"
	context_object_name = 'zawody'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['sedziowie_lista'] = sedziowie_lista()
		context['pk'] = self.kwargs['pk']
		context['nazwa_turnieju'] = nazwa_turnieju(self.kwargs['pk_turniej'])
		# context['rts_lista'] = rts_lista()
		return context

	def get_queryset(self):
		return Zawody.objects.all()

	def get_success_url(self):
		return reverse("zawody_lista", kwargs={'pk': self.kwargs['pk_turniej']})

	def dispatch(self, request, *args, **kwargs):
		try:
			if request.user.is_admin:
				return super(ZawodyDeleteView, self).dispatch(request, *args, **kwargs)
			else:
				return redirect('not_authorized')
		except:
			# return redirect('not_authorized')
			# return redirect('not_authorized')
			pass




class SedziaCreateView(LoginRequiredMixin, CreateView):
	login_url = '/login/'
	template_name = "zawody/sedzia_create.html"
	form_class = SedziaModelForm

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['sedziowie_lista'] = sedziowie_lista()
		context['pk'] = self.kwargs['pk']
		context['nazwa_turnieju'] = nazwa_turnieju(self.kwargs['pk'])
		# context['rts_lista'] = rts_lista()
		return context

	def get_success_url(self):
		return reverse("sedzia_lista", kwargs={'pk': self.kwargs['pk']})
		return super(SedziaCreateView, self).form_valid(form)

	def dispatch(self, request, *args, **kwargs):
		if request.user.is_admin:
			return super(SedziaCreateView, self).dispatch(request, *args, **kwargs)
		else:
			return redirect('not_authorized')

class SedziaListView(LoginRequiredMixin, ListView):
	login_url = '/login/'
	template_name = "zawody/sedzia_lista.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['sedziowie_lista'] = sedziowie_lista()
		context['pk'] = self.kwargs['pk']
		context['nazwa_turnieju'] = nazwa_turnieju(self.kwargs['pk'])
		# context['rts_lista'] = rts_lista()
		return context

	def get_queryset(self):
		return Sedzia.objects.all().order_by('zawody')

	def dispatch(self, request, *args, **kwargs):
		try:
			if request.user.is_admin:
				print(request.user.id)
				return super(SedziaListView, self).dispatch(request, *args, **kwargs)
			else:
				return redirect('not_authorized')
		except:
			return redirect('not_authorized')


class SedziaDeleteView(LoginRequiredMixin, DeleteView):
	login_url = '/login/'
	template_name = "zawody/sedzia_delete.html"
	context_object_name = 'sedzia'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['sedziowie_lista'] = sedziowie_lista()
		context['pk'] = self.kwargs['pk_turniej']
		context['nazwa_turnieju'] = nazwa_turnieju(self.kwargs['pk_turniej'])
		# context['rts_lista'] = rts_lista()
		return context

	def get_queryset(self):
		return Sedzia.objects.all()

	def get_success_url(self):
		return reverse("sedzia_lista", kwargs={'pk': self.kwargs['pk_turniej']})

	def dispatch(self, request, *args, **kwargs):
		try:
			if request.user.is_admin:
				return super(SedziaDeleteView, self).dispatch(request, *args, **kwargs)
			else:
				return redirect('not_authorized')
		except:
			return redirect('not_authorized')


