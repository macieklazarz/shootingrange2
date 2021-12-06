from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login, authenticate, logout
from account.forms import RegistrationForm, AccountAuthenticationForm, AccountModelForm
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Account
from zawody.models import Sedzia
# from wyniki.views import sedziowie_lista


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

def registration_form(request):
	context={}
	if request.POST:
		form=RegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			email = form.cleaned_data.get('email')
			# email = form.cleaned_data.get('inputemail')
			raw_password = form.cleaned_data.get('password1')
			# raw_password = form.cleaned_data.get('inputPassword1')
			account = authenticate(email=email, password=raw_password)
			login(request, account)
			return redirect('home')
		else:
			context['registration_form'] = form
	else:
		form = RegistrationForm()
		context['registration_form'] = form
	return render(request, 'account/register.html', context)

def registration_form_no_login(request):
	context={}
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
			return redirect('users')
		else:
			context['registration_form'] = form
	else:
		form = RegistrationForm()
		context['registration_form'] = form
	return render(request, 'account/register.html', context)

def logout_view(request):
	logout(request)
	return redirect('home')

def login_view(request):
	context = {}
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
				return redirect("home")
	else:
		form = AccountAuthenticationForm()

	context['login_form'] = form
	return render(request, 'account/login.html', context)

class AccountUpdateView(LoginRequiredMixin, UpdateView):
	login_url = '/login/'
	template_name = "account/account_update.html"
	form_class = AccountModelForm
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['sedziowie_lista'] = sedziowie_lista()
		# context['rts_lista'] = rts_lista()
		return context

	def get_queryset(self):
		return Account.objects.all()

	def get_success_url(self):
		return reverse("users")
		
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

class AccountListView(LoginRequiredMixin, ListView):
	login_url = '/login/'
	template_name = "account/account_list.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['sedziowie_lista'] = sedziowie_lista()
		# context['rts_lista'] = rts_lista()
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
	login_url = '/login/'
	template_name = "account/account_delete.html"
	context_object_name = 'zawodnik'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['sedziowie_lista'] = sedziowie_lista()
		# context['rts_lista'] = rts_lista()
		return context

	def get_queryset(self):
		return Account.objects.all()

	def get_success_url(self):
		return reverse("users")

	def dispatch(self, request, *args, **kwargs):
		try:
			if request.user.rts:
				return super(AccountDeleteView, self).dispatch(request, *args, **kwargs)
			else:
				return redirect('not_authorized')
		except:
			return redirect('not_authorized')


