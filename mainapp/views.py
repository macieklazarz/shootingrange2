from django.shortcuts import render
from account.models import Account
from zawody.models import Sedzia, Turniej
from account.views import sedziowie_lista

# Create your views here.
def home_screen_view(request, pk):
	context = {}
	accounts = Account.objects.all()
	context['accounts'] = accounts
	# print(request.user.username)
	sedziowie = Sedzia.objects.all().values_list('sedzia', flat=True).distinct()
	sedziowie_lista = []
	for i in sedziowie:
		sedziowie_lista.append(i)
	context['sedziowie_lista'] = sedziowie_lista
	context['pk'] = pk
	context['nazwa_turnieju'] = nazwa_turnieju(pk)
	# context['rts_lista'] = rts_lista()
	# print(f'powioazne zawody to {sedziowie_lista}')
	# print(f'pk to {pk}')
	return render(request, "mainapp/home.html", context)


def nazwa_turnieju(arg):
	nazwa = Turniej.objects.filter(id=arg).values_list('nazwa')
	nazwa_flat = []
	for i in nazwa:
		nazwa_flat.append(i)

	return nazwa_flat