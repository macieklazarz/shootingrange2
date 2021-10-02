from django.shortcuts import render
from wyniki.models import Wyniki
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
# Create your views here.

@csrf_exempt
def wyniki_edycja(request):
	if (request.user.username == 'admin'):
		wyniki1 = Wyniki.objects.filter(zawody = 1)
	else:
		wyniki1 = Wyniki.objects.filter(zawody = 2)
	# wyniki1 = Wyniki.objects.all()
	print(wyniki1)
	for i in wyniki1:
		print(i.zawodnik)
	return render(request, 'wyniki/edytuj_wyniki.html', {'wyniki': wyniki1})

def wyniki(request):
	wyniki1 = Wyniki.objects.filter(zawody = 1).order_by('-wynik', '-X', '-Xx')
	wyniki2 = Wyniki.objects.filter(zawody = 2)
	# wyniki1 = Wyniki.objects.all()
	# print(wyniki1)
	for i in wyniki1:
		print(i.zawodnik)
	return render(request, 'wyniki/wyniki.html', {'wyniki': wyniki1})

@csrf_exempt
def savestudent(request):
	id=request.POST.get('id', '')
	type=request.POST.get('type','')
	value=request.POST.get('value','')
	student=Wyniki.objects.get(id=id)
	if type=="X":
		student.X=value
	if type=="Xx":
		student.Xx=value
	if type=="dziewiec":
		student.dziewiec=value
	if type=="osiem":
		student.osiem=value
	if type=="siedem":
		student.siedem=value
	if type=="szesc":
		student.szesc=value
	if type=="piec":
		student.piec=value
	if type=="cztery":
		student.cztery=value
	if type=="trzy":
		student.trzy=value
	if type=="dwa":
		student.dwa=value
	if type=="jeden":
		student.jeden=value
		
	# student.wynik=student.Xx+student.X
	result=int(student.X)*10+int(student.Xx)*10+int(student.dziewiec)*9+int(student.osiem)*8+int(student.siedem)*7+int(student.szesc)*6+int(student.piec)*5+int(student.cztery)*4+int(student.trzy)*3+int(student.dwa)*2+int(student.jeden)*1
	print(f"wynik wynosi {result}")
	student.wynik=result
	student.save()
	# wyniki1 = Wyniki.objects.filter(zawody = 1)
	return JsonResponse({"success":"Updated"})
	# return render(request, 'wyniki/wyniki.html', {'wyniki': wyniki1})