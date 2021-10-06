from django.shortcuts import render, redirect
from wyniki.models import Wyniki, Ustawienia
from zawody.models import Sedzia, Zawody
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from . import forms
from django.db.models import Count
from django.contrib.auth.decorators import login_required
# from django.utils import simplejson
# Create your views here.

@csrf_exempt
@login_required(login_url="/login/")
def wyniki_edycja(request):
	# print(f'req user {request.user.id}')
	user_id = request.user.id 																				#sprawdzamy użytkownika ktory jest zalogowany
	powiazane_zawody = Sedzia.objects.filter(sedzia__id = user_id).values_list('zawody', flat=True)			#sprawdzamy do jakich zawodow jest przyporzadkowany sedzua
	powiazane_zawody_lista = []																				#robimy liste powiazanych zawodow
	for i in powiazane_zawody:
		powiazane_zawody_lista.append(i)
	# print(f'powiazane_zawody TO {powiazane_zawody_lista}')

	# if (request.user.username == 'admin'):
	# 	wyniki1 = Wyniki.objects.filter(zawody = 1)
	# else:
	# 	wyniki1 = Wyniki.objects.filter(zawody = 2)

	wyniki = []	
	zawody_nazwa = []																							#robimy liste ktorej elementami beda wyniki poszczegolnych zawodow
	for i in powiazane_zawody_lista:
		wyniki.append(Wyniki.objects.filter(zawody = i))
		# zawody_nazwa.append(Zawody.objects.filter(id = i).values_list('nazwa', flat=True))
	nazwy_zawodow = Zawody.objects.filter(id__in=powiazane_zawody_lista).values_list('nazwa', flat=True)
	for i in nazwy_zawodow:
		zawody_nazwa.append(i)
	# print(f'wyniki to {wyniki[0]}')
	# wyniki1 = Wyniki.objects.all()
	# print(wyniki1)
	# for i in wyniki1:
	# 	print(i.zawodnik)
	# print(f'wyniki moje to {wyniki[1]}')
	# print(f'wyniki cale to {wyniki}')
	print(f'zawody nazwa to {zawody_nazwa}')
	# print(f'wyniki1 to {wyniki1}')
	return render(request, 'wyniki/edytuj_wyniki.html', {'wyniki': wyniki, 'zawody_nazwa': zawody_nazwa})

@login_required(login_url="/login/")
def wyniki(request):
	zawody = Zawody.objects.all().values_list('id', flat=True).order_by('id')
	zawody_lista = []
	for i in zawody:
		zawody_lista.append(i)
	zawody_nazwa_queryset = Zawody.objects.all().values_list('nazwa', flat=True).order_by('id')
	zawody_nazwa = []
	for i in zawody_nazwa_queryset:
		zawody_nazwa.append(i)
	# print(f'zawody to {zawody_lista}')
	# print(f'zawody nazwa to {zawody_nazwa}')
	wyniki = []																								#robimy liste ktorej elementami beda wyniki poszczegolnych zawodow
	for i in zawody_lista:
		wyniki.append(Wyniki.objects.filter(zawody = i).order_by('-wynik', '-X', '-Xx', '-dziewiec', '-osiem', '-siedem'))
	# wyniki1 = Wyniki.objects.filter(zawody = 1).order_by('-wynik', '-X', '-Xx')
	# wyniki2 = Wyniki.objects.filter(zawody = 2)
	# wyniki1 = Wyniki.objects.all()
	# print(wyniki1)
	# for i in wyniki1:
	# 	print(i.zawodnik)

	# klasyfikacja_generalna = Wyniki.objects.all().order_by('-wynik', '-X', '-Xx', '-dziewiec', '-osiem', '-siedem')
	klasyfikacja_generalna = Wyniki.objects.raw('select id, zawodnik_id, sum(X) as X, sum(Xx) as Xx,sum(dziewiec) as dziewiec, sum(osiem) as osiem,sum(siedem) as siedem , sum(szesc) as szesc, sum(piec) as piec, sum(cztery) as cztery, sum(trzy) as trzy, sum(dwa) as dwa, sum(jeden) as jeden, sum(wynik) as wynik from wyniki_wyniki group by zawodnik_id order by wynik desc, X desc, Xx desc, dziewiec desc, osiem desc, siedem DESC')
	# print(klasyfikacja_generalna.values_list())
	# query = Wyniki.objects.all().query
	# query.group_by = ['zawodnik']
	# klasyfikacja_generalna = QuerySet(query=query, model=Wyniki)
	return render(request, 'wyniki/wyniki.html', {'wyniki': wyniki, 'zawody_nazwa':zawody_nazwa, 'klasyfikacja_generalna': klasyfikacja_generalna})

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
	# print(f"wynik wynosi {result}")
	student.wynik=result
	student.save()
	# wyniki1 = Wyniki.objects.filter(zawody = 1)
	return JsonResponse({"success":"Updated"})
	# return render(request, 'wyniki/wyniki.html', {'wyniki': wyniki1})


# @login_required(login_url="/accounts/login/")
@login_required(login_url="/login/")
def rejestracja_na_zawody(request):
	if request.method == 'POST':
		# wybrane_zawody = request.POST.getlist('zawody')[0]
		wybrane_zawody = request.POST['zawody']
		# wybrane_zawody = request.POST
		# print("dupa")
		# request.POST.getlist('zawody')=wybrane_zawody
		# print(f'selected {wybrane_zawody}')
		form = forms.DodajZawodnika(request.POST)
		# form2 = forms.DodajZawodnika2(request.POST, request.FILES)
		# zaw = request.POST.get('zawodnik')
		# form.fields['zawodnik'].choices = [(zaw, zaw)]
		if form.is_valid():
			# print("dupa1")
			instance1 = form.save()
			return redirect('home')
	else:
		user = request.user.id
		# print(f'user to {user}')
		def_data = {
		'zawodnik' : user
		}
		# form = forms.DodajZawodnika(initial=def_data)
		# form = forms.DodajZawodnika()
		print(user)
		form = forms.DodajZawodnika(initial={'zawodnik': user})
	dodawanie_zawodnika = Ustawienia.objects.filter(nazwa='Rejestracja').values_list("ustawienie")
	for i in dodawanie_zawodnika:
		opcja = i[0]
	# # form = forms.DodajZawodnika()
	# dodawanie_zawodnika = Ustawienia.objects.filter(nazwa='Rejestracja').values_list("ustawienie")
	# # dodawanie_zawodnika = Ustawienia.objects.values_list()
	# # print(dodawanie_zawodnika)
	# for i in dodawanie_zawodnika:
	# 	opcja = i[0]
	# # qry = "select ustawienie from mainapp_ustawienia where nazwa = 'Rejestracja';"
	# # # cursor=connection.cursor()
	# # # wynik = cursor.execute(qry)
	# # wynik = Ustawienia.objects.raw(qry)
	# # for wyn in wynik:
	# # 	wynik = wyn.ustawienie
	# print(request.user)


	return render(request, 'wyniki/rejestracja_na_zawody.html', {'form':form, 'dodawanie_zawodnika':opcja})