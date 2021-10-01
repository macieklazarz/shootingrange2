from django.shortcuts import render
from wyniki.models import Wyniki
# Create your views here.
def wyniki(request):
	wyniki1 = Wyniki.objects.filter(zawody = 1)
	print(wyniki1)
	return render(request, 'wyniki/wyniki.html', {'wyniki': wyniki1})