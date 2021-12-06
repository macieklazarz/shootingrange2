from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404, reverse
from wyniki.models import Wyniki, Ustawienia
from zawody.models import Sedzia, Zawody
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from . import forms
from django.db.models import Count, Value as V, CharField, F, TextField
from django.contrib.auth.decorators import login_required
import datetime
import xlwt
from django.db.models.functions import Concat
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import WynikiModelForm, RejestracjaModelForm, UstawieniaModelForm
from zawody.models import Sedzia
from account.views import sedziowie_lista
# from django.contrib.auth.mixins import LoginRequiredMixin
# from agents.mixins import OrganisorAndLoginRequiredMixin
# from django.utils import simplejson
# Create your views here.



@csrf_exempt
@login_required(login_url="/login/")
def wyniki_edycja(request):
	context = {}
	context['sedziowie_lista'] = sedziowie_lista()
	# context['rts_lista'] = rts_lista()
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
		wyniki.append(Wyniki.objects.filter(zawody = i).order_by('zawodnik'))
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
	context['wyniki'] = wyniki
	context['zawody_nazwa'] = zawody_nazwa
	return render(request, 'wyniki/edytuj_wyniki.html', context)

@login_required(login_url="/login/")
def wyniki(request):
	context = {}
	context['sedziowie_lista'] = sedziowie_lista()
	# context['rts_lista'] = rts_lista()
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
	wyniki = []		
	sedziowie_queryset = []																						#robimy liste ktorej elementami beda wyniki poszczegolnych zawodow
	sedziowie = []
	for i in zawody_lista:
		# wyniki.append(Wyniki.objects.filter(zawody = i).order_by('-wynik', '-X', '-Xx', '-dziewiec', '-osiem', '-siedem'))
		wyniki.append(Wyniki.objects.filter(zawody = i).order_by('-wynik', '-X', '-Xx', '-dziewiec', '-osiem', '-siedem'))
		# sedziowie_queryset.append(Sedzia.objects.filter(zawody = i).values_list(Concat('sedzia__imie', V(' '), 'sedzia__nazwisko'), output_field=CharField(), Flat = True))
		# sedziowie_queryset.append(Sedzia.objects.filter(zawody = i).values_list('sedzia__imie', flat = True))
		sedziowie_queryset.append(Sedzia.objects.filter(zawody = i).values_list('sedzia__imie', 'sedzia__nazwisko'))
		# sedziowie_queryset.append(Sedzia.objects.filter(zawody = i).values_list('sedzia__imie', 'sedzia__nazwisko'))
		# sedziowie_queryset.append(Sedzia.objects.annotate(text=Concat("sedzia__imie", V("xxx_"), "sedzia__nazwisko"), output_field=CharField()).filter(zawody = i))
	for i in sedziowie_queryset:
		sedziowie.append(i)
	context['sedziowie'] = sedziowie
	# print(f'sedziowie TO {sedziowie}')
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
	context['wyniki'] = wyniki
	context['zawody_nazwa'] = zawody_nazwa
	context['klasyfikacja_generalna'] = klasyfikacja_generalna

	# return render(request, 'wyniki/wyniki.html', {'wyniki': wyniki, 'zawody_nazwa':zawody_nazwa, 'sedziowie':sedziowie, 'klasyfikacja_generalna': klasyfikacja_generalna})
	return render(request, 'wyniki/wyniki.html', context)


# @login_required(login_url="/accounts/login/")
@login_required(login_url="/login/")
def rejestracja_na_zawody(request):
	context = {}
	if request.method == 'POST':
		wybrane_zawody = request.POST['zawody']
		form = forms.DodajZawodnika(request.POST)
		if form.is_valid():
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
		context['form'] = form
	context['sedziowie_lista'] = sedziowie_lista()
	# context['rts_lista'] = rts_lista()
	dodawanie_zawodnika = Ustawienia.objects.filter(nazwa='Rejestracja').values_list("ustawienie")
	for i in dodawanie_zawodnika:
		opcja = i[0]
	context['dodawanie_zawodnika'] = opcja
	return render(request, 'wyniki/rejestracja_na_zawody.html', context)


class RejestracjaNaZawodyView(LoginRequiredMixin, CreateView):
	login_url = '/login/'
	template_name = "wyniki/rejestracja.html"
	form_class = RejestracjaModelForm
	# user_id = request.user.id

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['sedziowie_lista'] = sedziowie_lista()
		dodawanie_zawodnika = Ustawienia.objects.filter(nazwa='Rejestracja').values_list("ustawienie")
		for i in dodawanie_zawodnika:
			opcja = i[0]
		context['dodawanie_zawodnika'] = opcja
		return context

	def get_success_url(self):
		return reverse("rejestracja_na_zawody")
		return super(RejestracjaNaZawodyView, self).form_valid(form)

	def get_form_kwargs(self):
		kwargs = super(RejestracjaNaZawodyView, self).get_form_kwargs()
		kwargs.update({'user': self.request.user.rts})
		# kwargs.update({'user': request.user.id})
		return kwargs

	def get_initial(self, *args, **kwargs):
		initial = super(RejestracjaNaZawodyView, self).get_initial()
		initial = initial.copy()
		initial['zawodnik'] = self.request.user
		return initial


# @login_required(login_url="/login/")
# def wyniki_edit(request, slug, nr_zawodow):
# 	user_id = request.user.id 																				#sprawdzamy użytkownika ktory jest zalogowany
# 	powiazane_zawody = Sedzia.objects.filter(sedzia__id = user_id).values_list('zawody', flat=True)			#sprawdzamy do jakich zawodow jest przyporzadkowany sedzua
# 	powiazane_zawody_lista = []																				#robimy liste powiazanych zawodow
# 	for i in powiazane_zawody:
# 		powiazane_zawody_lista.append(i)
# 	# print(f'powiozane zawody: {powiazane_zawody_lista} typ: {type(powiazane_zawody_lista)}')
# 	# print(f'nr zawodow to {nr_zawodow} typ: {type(nr_zawodow)}')
# 	if int(nr_zawodow) in powiazane_zawody_lista:
# 		print('Success!')
# 		post = get_object_or_404(Wyniki, slug=slug)
# 		print(f'post  = {post}')
# 		if request.method == 'POST':
# 			form = forms.Wyniki_edit(request.POST, instance=post)
# 			if form.is_valid():
# 				post = form.save(commit=False)
# 				post.save()
# 				print('zapisano')
# 				return redirect('wyniki_edycja')
# 		else:
# 			form = forms.Wyniki_edit(instance=post)
# 			print('niezapisano')
# 		template = 'wyniki/wyniki_edit.html'
# 		context = {'form': form, 'i': post}
# 		return render(request, template, context)
# 	else:
# 		return redirect('home')


class WynikUpdateView(LoginRequiredMixin, UpdateView):
	login_url = '/login/'
	template_name = "wyniki/wyniki_edit.html"
	form_class = WynikiModelForm
	context_object_name = 'cont'
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		# context['rts_lista'] = rts_lista()
		context['sedziowie_lista'] = sedziowie_lista()
		return context

	def get_queryset(self):
		return Wyniki.objects.all()

	def get_success_url(self):
		return reverse("wyniki_edycja")
		
	def form_valid(self, form):
		return super(WynikUpdateView,self).form_valid(form)

	def dispatch(self, request, *args, **kwargs):
		wynik_pk = self.kwargs.get('pk')
		zawody_pk = Wyniki.objects.filter(id = wynik_pk).values_list('zawody__id', flat=True)
		zawody_pk_lista = []
		for i in zawody_pk:
			zawody_pk_lista.append(i)
		zawody_pk_lista = zawody_pk_lista[0]
		sedzia_pk = Sedzia.objects.filter(zawody__id = zawody_pk_lista).values_list('sedzia__id', flat=True)
		sedzia_pk_lista = []
		for i in sedzia_pk:
			sedzia_pk_lista.append(i)
		print(f'zawody: {zawody_pk_lista}')
		print(f'sedzia_id: {sedzia_pk_lista}')
		user_id=self.request.user.id
		print(f'user_id: {user_id}')
		if user_id in sedzia_pk_lista:
			print('sedzia jest')
			return super(WynikUpdateView, self).dispatch(request, *args, **kwargs)
		else:
			print('sedzia nie ma')
			return redirect('not_authorized')


def not_authorized(request):
	return render(request, 'wyniki/not_authorized.html')

@login_required(login_url="/login/")
def exportexcel(request):
	if request.user.username == 'admin':
		response=HttpResponse(content_type='application/ms-excel')
		response['Content-Disposition'] = 'attachment; filename=Wyniki_' + str(datetime.datetime.now())+'.xls'
		wb = xlwt.Workbook(encoding='utf-8')

		zawody = Zawody.objects.all().values_list('nazwa', flat=True).order_by('id')
		ws = []
		for i in zawody:
			ws.append(wb.add_sheet(i))

		# ws1=wb.add_sheet('Zawody wójta gminy Nieporęt')
		# ws2=wb.add_sheet('Zawody wójta gminy Serock')
		# ws3=wb.add_sheet('Wyniki_klasyfikacja_generalna')
		row_num = 0
		font_style = xlwt.XFStyle()
		font_style.font.bold=True

		columns = ['Imię', 'Nazwisko', 'Email', 'X', '/', '9', '8', '7','6','5','4','3','2','1', 'Wynik']

		for col_num in range(len(columns)):
			for i in ws:
				i.write(row_num, col_num, columns[col_num], font_style)
			# ws1.write(row_num, col_num, columns[col_num], font_style)
			# ws2.write(row_num, col_num, columns[col_num], font_style)
			# ws3.write(row_num, col_num, columns[col_num], font_style)

		font_style = xlwt.XFStyle()
		zawody_id = Zawody.objects.all().values_list('id', flat=True).order_by('id')
		zawody_id_lista = []
		for i in zawody_id:
			zawody_id_lista.append(i)

		# print(f'zawody;ista to {zawody_id_lista}')
		rows = []
		for i in zawody_id_lista:
			rows.append(Wyniki.objects.filter(zawody__id = i).values_list('zawodnik__imie','zawodnik__nazwisko', 'zawodnik__email', 'X', 'Xx', 'dziewiec', 'osiem', 'siedem', 'szesc', 'piec', 'cztery', 'trzy', 'dwa', 'jeden', 'wynik').order_by('-wynik', '-X', '-Xx', '-dziewiec', '-osiem', '-siedem', '-szesc', '-piec', '-cztery', '-trzy', '-dwa', '-jeden'))
		# print(f'rows1 to {rows[3]}')

		for x,y in enumerate(ws):
			row_num = 0
			for row in rows[x]:
				row_num +=1
				for col_num in range(len(row)):
					y.write(row_num, col_num, str(row[col_num]), font_style)

		wb.save(response)

		return(response)

	else:
		return redirect('home')


class KonkurencjaDeleteView(LoginRequiredMixin, DeleteView):
	login_url = '/login/'
	template_name = "wyniki/konkurencja_delete.html"
	context_object_name = 'zawodnik'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['sedziowie_lista'] = sedziowie_lista()
		# context['rts_lista'] = rts_lista()
		return context

	def get_queryset(self):
		return Wyniki.objects.all()

	def get_success_url(self):
		return reverse("wyniki")

	def dispatch(self, request, *args, **kwargs):
		try:
			if request.user.is_admin:
				return super(KonkurencjaDeleteView, self).dispatch(request, *args, **kwargs)
			else:
				return redirect('not_authorized')
		except:
			return redirect('not_authorized')


class UstawieniaListView(LoginRequiredMixin, ListView):
	login_url = '/login/'
	template_name = "wyniki/ustawienia_list.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['sedziowie_lista'] = sedziowie_lista()
		# context['rts_lista'] = rts_lista()
		return context

	def get_queryset(self):
		return Ustawienia.objects.all()

	def dispatch(self, request, *args, **kwargs):
		try:
			if request.user.is_admin:
				return super(UstawieniaListView, self).dispatch(request, *args, **kwargs)
			else:
				return redirect('not_authorized')
		except:
			return redirect('not_authorized')
	
class UstawieniaUpdateView(LoginRequiredMixin,UpdateView):
	login_url = '/login/'
	template_name = "wyniki/ustawienia_edit.html"
	form_class = UstawieniaModelForm
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['sedziowie_lista'] = sedziowie_lista()
		# context['rts_lista'] = rts_lista()
		return context

	def get_queryset(self):
		return Ustawienia.objects.all()

	def get_success_url(self):
		return reverse("home")
		
	def dispatch(self, request, *args, **kwargs):
		try:
			if request.user.is_admin:
				return super(UstawieniaUpdateView, self).dispatch(request, *args, **kwargs)
			else:
				return redirect('not_authorized')
		except:
			return redirect('not_authorized')

