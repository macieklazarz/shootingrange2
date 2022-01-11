from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login, authenticate, logout
from account.forms import RegistrationForm, RegistrationFormSedzia, AccountAuthenticationForm, AccountModelForm, SedziaModelForm
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Account
from zawody.models import Sedzia, Turniej
# from wyniki.views import sedziowie_lista
# from rest_auth.views import PasswordResetView, PasswordResetConfirmView, PasswordResetDoneView, PasswordResetCompleteView
from django.contrib.auth import views as auth_views
# from mainapp.views import nazwa_turnieju
from shootingrange import settings
import urllib
import json


def nazwa_turnieju(arg):
	nazwa = Turniej.objects.filter(id=arg).values_list('nazwa')
	nazwa_flat = []
	for i in nazwa:
		nazwa_flat.append(i)

	return nazwa_flat

def sedziowie_lista():
	sedziowie = Sedzia.objects.all().values_list('sedzia', flat=True).distinct()
	sedziowie_lista = []
	for i in sedziowie:
		sedziowie_lista.append(i)
	return sedziowie_lista

# def rts_lista():
# 	rts = Rts.objects.all().values_list('user', flat=True).distinct()
# 	rts_lista = []
# 	for i in rts:
# 		rts_lista.append(i)
# 	return rts_lista

def registration_form(request, pk):
	context={}
	context['pk'] = pk
	context['nazwa_turnieju'] = nazwa_turnieju(pk)
	if request.POST:
		form=RegistrationForm(request.POST)
		if form.is_valid():
			print('jest is valid')
			recaptcha_response = request.POST.get('g-recaptcha-response')
			url = 'https://www.google.com/recaptcha/api/siteverify'
			values = {'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,'response': recaptcha_response}
			data = urllib.parse.urlencode(values).encode()
			req =  urllib.request.Request(url, data=data)
			response = urllib.request.urlopen(req)
			result = json.loads(response.read().decode())
			if result['success']:
				print('jest success')
				form.save()
				messages.success(request, 'New comment added with success!')
				email = form.cleaned_data.get('email')
				raw_password = form.cleaned_data.get('password1')
				account = authenticate(email=email, password=raw_password)
				login(request, account)
				return redirect('home', pk)
			else:
				print(' nie ma success')
				messages.error(request, 'Invalid reCAPTCHA. Please try again.')
		else:
			context['registration_form'] = form
	else:
		form = RegistrationForm()
		context['registration_form'] = form
	return render(request, 'account/register.html', context)

def registration_form_sedzia(request, pk):
	context={}
	context['pk'] = pk
	context['nazwa_turnieju'] = nazwa_turnieju(pk)
	if request.POST:
		form=RegistrationFormSedzia(request.POST)
		if form.is_valid():
			print('jest is valid')
			recaptcha_response = request.POST.get('g-recaptcha-response')
			url = 'https://www.google.com/recaptcha/api/siteverify'
			values = {'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,'response': recaptcha_response}
			data = urllib.parse.urlencode(values).encode()
			req =  urllib.request.Request(url, data=data)
			response = urllib.request.urlopen(req)
			result = json.loads(response.read().decode())
			if result['success']:
				# print('jest success')
				form.save()
				messages.success(request, 'New comment added with success!')
				email = form.cleaned_data.get('email')
				raw_password = form.cleaned_data.get('password1')
				account = authenticate(email=email, password=raw_password)
				login(request, account)
				return redirect('home', pk)
			else:
				# print(' nie ma success')
				messages.error(request, 'Invalid reCAPTCHA. Please try again.')
		else:
			context['registration_form'] = form
	else:
		form = RegistrationFormSedzia()
		context['registration_form'] = form
	return render(request, 'account/register_sedzia.html', context)
@login_required(login_url="/start/")
def registration_form_no_login(request,pk):
	context={}
	context['pk'] = pk
	context['nazwa_turnieju'] = nazwa_turnieju(pk)
	if request.POST:
		form=RegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			email = form.cleaned_data.get('email')
			# email = form.cleaned_data.get('inputemail')
			raw_password = form.cleaned_data.get('password1')
			# raw_password = form.cleaned_data.get('inputPassword1')
			account = authenticate(email=email, password=raw_password)
			# login(request, account)
			return redirect('users', pk)
		else:
			context['registration_form'] = form
	else:
		form = RegistrationForm()
		context['registration_form'] = form
	return render(request, 'account/register.html', context)

def logout_view(request, pk):
	logout(request)
	return redirect('home', pk)

def login_view(request, pk):
	context = {}
	context['nazwa_turnieju'] = nazwa_turnieju(pk)
	user = request.user
	if user.is_authenticated:
		return redirect("home")
	if request.POST:
		form = AccountAuthenticationForm(request.POST)
		if form.is_valid():
			email = request.POST['email']
			password = request.POST['password']
			user = authenticate(email=email, password=password)

			if user:
				login(request, user)
				return redirect("home", pk)
	else:
		form = AccountAuthenticationForm()

	context['login_form'] = form
	context['pk'] = pk
	return render(request, 'account/login.html', context)

def login_info(request, pk):
	return redirect('not_authorized')


class AccountUpdateView(LoginRequiredMixin, UpdateView):
	login_url = 'start'
	template_name = "account/account_update.html"
	form_class = AccountModelForm
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['sedziowie_lista'] = sedziowie_lista()
		context['pk'] = self.kwargs['pk_turniej']
		context['nazwa_turnieju'] = nazwa_turnieju(self.kwargs['pk'])
		# context['rts_lista'] = rts_lista()
		return context

	def get_queryset(self):
		return Account.objects.all()

	def get_success_url(self):
		return reverse("users", kwargs={'pk': self.kwargs['pk_turniej']})
		
	def form_valid(self, form):
		return super(AccountUpdateView,self).form_valid(form)

	def dispatch(self, request, *args, **kwargs):
		try:
			if request.user.rts:
				return super(AccountUpdateView, self).dispatch(request, *args, **kwargs)
			else:
				return redirect('not_authorized')
		except:
			return redirect('not_authorized')

class SedziaUpdateView(LoginRequiredMixin, UpdateView):
	login_url = 'start'
	template_name = "account/account_update.html"
	form_class = SedziaModelForm
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['sedziowie_lista'] = sedziowie_lista()
		context['pk'] = self.kwargs['pk_turniej']
		context['nazwa_turnieju'] = nazwa_turnieju(self.kwargs['pk'])
		# context['rts_lista'] = rts_lista()
		return context

	def get_queryset(self):
		return Account.objects.all()

	def get_success_url(self):
		return reverse("sedzia_lista", kwargs={'pk': self.kwargs['pk_turniej']})
		
	def form_valid(self, form):
		return super(SedziaUpdateView,self).form_valid(form)

	def dispatch(self, request, *args, **kwargs):
		try:
			if request.user.rts:
				return super(SedziaUpdateView, self).dispatch(request, *args, **kwargs)
			else:
				return redirect('not_authorized')
		except:
			return redirect('not_authorized')

class AccountListView(LoginRequiredMixin, ListView):
	login_url = 'start'
	template_name = "account/account_list.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['sedziowie_lista'] = sedziowie_lista()
		# context['rts_lista'] = rts_lista()
		context['pk'] = self.kwargs['pk']
		context['nazwa_turnieju'] = nazwa_turnieju(self.kwargs['pk'])
		return context

	def get_queryset(self):
		return Account.objects.all()

	def dispatch(self, request, *args, **kwargs):
		try:
			if request.user.rts:
				return super(AccountListView, self).dispatch(request, *args, **kwargs)
			else:
				return redirect('not_authorized')
		except:
			return redirect('not_authorized')



class AccountDeleteView(LoginRequiredMixin, DeleteView):
	login_url = 'start'
	template_name = "account/account_delete.html"
	context_object_name = 'zawodnik'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['sedziowie_lista'] = sedziowie_lista()
		context['pk'] = self.kwargs['pk_turniej']
		context['nazwa_turnieju'] = nazwa_turnieju(self.kwargs['pk_turniej'])
		# context['rts_lista'] = rts_lista()
		return context

	def get_queryset(self):
		return Account.objects.all()

	def get_success_url(self):
		return reverse("users", kwargs={'pk': self.kwargs['pk_turniej']})

	def dispatch(self, request, *args, **kwargs):
		try:
			if request.user.rts:
				return super(AccountDeleteView, self).dispatch(request, *args, **kwargs)
			else:
				return redirect('not_authorized')
		except:
			return redirect('not_authorized')
			# pass


class PasswordResetViewNew(auth_views.PasswordResetView):
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['sedziowie_lista'] = sedziowie_lista()
		context['pk'] = self.kwargs['pk']
		context['nazwa_turnieju'] = nazwa_turnieju(self.kwargs['pk'])
		# context['rts_lista'] = rts_lista()
		return context
	def get_success_url(self):
		return reverse("password_reset_done", kwargs={'pk': self.kwargs['pk']})


class PasswordResetDoneViewNew(auth_views.PasswordResetDoneView):
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['sedziowie_lista'] = sedziowie_lista()
		context['pk'] = self.kwargs['pk']
		context['nazwa_turnieju'] = nazwa_turnieju(self.kwargs['pk'])
		# context['rts_lista'] = rts_lista()
		return context

class PasswordResetConfirmViewNew(auth_views.PasswordResetConfirmView):
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		# context['sedziowie_lista'] = sedziowie_lista()
		# context['pki'] = self.kwargs['pk']
		# context['nazwa_turnieju'] = nazwa_turnieju(self.kwargs['pk'])
		# context['rts_lista'] = rts_lista()
		return context

class PasswordResetCompleteViewNew(auth_views.PasswordResetCompleteView):
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		# context['sedziowie_lista'] = sedziowie_lista()
		# context['pk'] = self.kwargs['pk']
		# context['nazwa_turnieju'] = nazwa_turnieju(self.kwargs['pk'])
		# context['rts_lista'] = rts_lista()
		return context