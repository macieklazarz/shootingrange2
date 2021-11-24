from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login, authenticate, logout
from account.forms import RegistrationForm, AccountAuthenticationForm, AccountModelForm, RtsModelForm
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Account, Rts
from zawody.models import Sedzia
# from wyniki.views import sedziowie_lista


def sedziowie_lista():
	sedziowie = Sedzia.objects.all().values_list('sedzia', flat=True).distinct()
	sedziowie_lista = []
	for i in sedziowie:
		sedziowie_lista.append(i)
	return sedziowie_lista

def rts_lista():
	rts = Rts.objects.all().values_list('user', flat=True).distinct()
	rts_lista = []
	for i in rts:
		rts_lista.append(i)
	return rts_lista

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

class AccountUpdateView(UpdateView):
	template_name = "account/account_update.html"
	form_class = AccountModelForm
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['sedziowie_lista'] = sedziowie_lista()
		context['rts_lista'] = rts_lista()
		return context

	def get_queryset(self):
		return Account.objects.all()

	def get_success_url(self):
		return reverse("users")
		
	def form_valid(self, form):
		return super(AccountUpdateView,self).form_valid(form)

class AccountListView(ListView):
	template_name = "account/account_list.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['sedziowie_lista'] = sedziowie_lista()
		context['rts_lista'] = rts_lista()
		return context

	def get_queryset(self):
		return Account.objects.all()

	def dispatch(self, request, *args, **kwargs):
		if request.user.is_admin:
			return super(AccountListView, self).dispatch(request, *args, **kwargs)
		else:
			return redirect('not_authorized')

	# def dispatch(self, request, *args, **kwargs):
	# 	wynik_pk = self.kwargs.get('pk')
	# 	zawody_pk = Wyniki.objects.filter(id = wynik_pk).values_list('zawody__id', flat=True)
	# 	zawody_pk_lista = []
	# 	for i in zawody_pk:
	# 		zawody_pk_lista.append(i)
	# 	zawody_pk_lista = zawody_pk_lista[0]
	# 	sedzia_pk = Sedzia.objects.filter(zawody__id = zawody_pk_lista).values_list('sedzia__id', flat=True)
	# 	sedzia_pk_lista = []
	# 	for i in sedzia_pk:
	# 		sedzia_pk_lista.append(i)
	# 	print(f'zawody: {zawody_pk_lista}')
	# 	print(f'sedzia_id: {sedzia_pk_lista}')
	# 	user_id=self.request.user.id
	# 	print(f'user_id: {user_id}')
	# 	if user_id in sedzia_pk_lista:
	# 		print('sedzia jest')
	# 		return super(WynikUpdateView, self).dispatch(request, *args, **kwargs)
	# 	else:
	# 		print('sedzia nie ma')
	# 		return redirect('not_authorized')


class AccountDeleteView(DeleteView):
	template_name = "account/account_delete.html"
	context_object_name = 'zawodnik'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['sedziowie_lista'] = sedziowie_lista()
		context['rts_lista'] = rts_lista()
		return context

	def get_queryset(self):
		return Account.objects.all()

	def get_success_url(self):
		return reverse("users")

	def dispatch(self, request, *args, **kwargs):
		if request.user.is_admin:
			return super(AccountDeleteView, self).dispatch(request, *args, **kwargs)
		else:
			return redirect('not_authorized')


class RtsListView(ListView):
	template_name = "account/rts_list.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['sedziowie_lista'] = sedziowie_lista()
		context['rts_lista'] = rts_lista()
		return context

	def get_queryset(self):
		return Rts.objects.all()

	def dispatch(self, request, *args, **kwargs):
		if request.user.is_admin:
			return super(RtsListView, self).dispatch(request, *args, **kwargs)
		else:
			return redirect('not_authorized')




class RtsDeleteView(DeleteView):
	template_name = "account/rts_delete.html"
	context_object_name = 'rts'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['sedziowie_lista'] = sedziowie_lista()
		context['rts_lista'] = rts_lista()
		return context

	def get_queryset(self):
		return Rts.objects.all()

	def get_success_url(self):
		return reverse("users_rts")

	def dispatch(self, request, *args, **kwargs):
		if request.user.is_admin:
			return super(RtsDeleteView, self).dispatch(request, *args, **kwargs)
		else:
			return redirect('not_authorized')

class RtsCreateView(CreateView):
	template_name = "account/rts_add.html"
	form_class = RtsModelForm

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['sedziowie_lista'] = sedziowie_lista()
		context['rts_lista'] = rts_lista()
		return context

	def get_success_url(self):
		return reverse("users_rts")
		return super(RtsCreateView, self).form_valid(form)

	def dispatch(self, request, *args, **kwargs):
		if request.user.is_admin:
			return super(RtsCreateView, self).dispatch(request, *args, **kwargs)
		else:
			return redirect('not_authorized')