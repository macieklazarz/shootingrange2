from django.shortcuts import render
from account.models import Account
from zawody.models import Sedzia

# Create your views here.
def home_screen_view(request):
	context = {}
	accounts = Account.objects.all()
	context['accounts'] = accounts
	# print(request.user.username)
	sedziowie = Sedzia.objects.all().values_list('sedzia', flat=True).distinct()
	sedziowie_lista = []
	for i in sedziowie:
		sedziowie_lista.append(i)
	context['sedziowie_lista'] = sedziowie_lista
	print(f'powioazne zawody to {sedziowie_lista}')
	return render(request, "mainapp/home.html", context)
