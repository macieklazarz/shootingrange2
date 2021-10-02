from django.shortcuts import render
from account.models import Account

# Create your views here.
def home_screen_view(request):
	context = {}
	accounts = Account.objects.all()
	context['accounts'] = accounts
	print(request.user.username)
	return render(request, "mainapp/home.html", context)
