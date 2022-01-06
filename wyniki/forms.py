from django import forms
from . import models
from zawody.models import Zawody, Turniej
from account.models import Account
from wyniki.models import Wyniki, Ustawienia
from django.core.exceptions import ValidationError
from django.forms.widgets import CheckboxSelectMultiple
from django.forms.models import ModelMultipleChoiceField

class Wyniki_edit(forms.ModelForm):
    class Meta:
        model = models.Wyniki
        fields = ['zawodnik', 'X', 'Xx', 'dziewiec', 'osiem', 'siedem', 'szesc', 'piec', 'cztery', 'trzy', 'dwa', 'jeden']

    def __init__(self, *args, **kwargs):
        super(Wyniki_edit, self).__init__(*args, **kwargs)
        self.fields['zawodnik'].disabled = True

class DodajZawodnika(forms.ModelForm):

    class Meta:
        model = models.Wyniki

        fields = [ 'zawody', 'zawodnik']


    def __init__(self, *args, **kwargs):
        from django.forms.widgets import HiddenInput
        super(DodajZawodnika, self).__init__(*args, **kwargs)
        # self.fields['zawodnik'] = forms.ModelChoiceField(queryset=Account.objects.all())
        self.fields['zawodnik'].widget = HiddenInput()
        # self.fields['zawody'] = forms.ModelChoiceField(queryset=Zawody.objects.all())
        # self.fields['zawody'] = 'admin@admin.com'

    def clean(self):
        cleaned_data = super().clean()
        wybrane_zawody = cleaned_data.get('zawody')                                                                                                                 #sprawdzam jakie wybrano zawody
        wybrany_zawodnik = str(cleaned_data.get('zawodnik'))                                                                                                        #sprawdzam jakiego wybrano zawodnika (tu zostanie przypisany mail)
        # zaw = str(cleaned_data.get('zawody'))
        # zaw = request.POST['zawody']
        # zaw = self.fields['zawody']
        print(f'zawody to {wybrane_zawody}')
        print(f'zawodnik to {wybrany_zawodnik}')
        # id_zawodow=Zawody.objects.filter(nazwa=zaw)
        zawodnicy_przypisani_do_zawodow = Wyniki.objects.filter(zawody__nazwa=wybrane_zawody).values_list('zawodnik', flat=True).distinct()                          #wybieram wszystkich zawodników którzy są przypisani do wybranych zawodów (zmienna wybrane_zawody)
        zawodnicy_przypisani_do_zawodow_lista = []
        # wybrane_zawody2 = wybrane_zawody.get('zawodnik')
        for i in zawodnicy_przypisani_do_zawodow:
            # print(f' wybrane zawody {i}')
            zawodnicy_przypisani_do_zawodow_lista.append(i)                                                                                                          #robię listę z wsyztskich zawodników przypisanych do danych zawodow
        # print(f'zawodnicy przypisani do zawodow to {zawodnicy_przypisani_do_zawodow_lista}')
        zawodnicy_przypisani_do_zawodow_email = Account.objects.filter(pk__in=zawodnicy_przypisani_do_zawodow_lista).values_list('email', flat=True).distinct()      #sprawdzam mail zawodnikow wybranych do zawodow
        zawodnicy_przypisani_do_zawodow_email_lista = []
        for i in zawodnicy_przypisani_do_zawodow_email:
            zawodnicy_przypisani_do_zawodow_email_lista.append(i)                                                                                                      #robie liste z mailami uczestnikow wybranych zawodow
        print(f'zawodnicy email {zawodnicy_przypisani_do_zawodow_email_lista}')
        if (wybrany_zawodnik in zawodnicy_przypisani_do_zawodow_email_lista):                                                                               #sprawdzam czy wybrany zawodnik jest na liscie z mailami uczestnikow wybranych zawodow
            # print('powinno wywalic')
            raise ValidationError("Jesteś już zarejestrowany na te zawody")
            # self.fields['zawodnik'] =

class WynikiModelForm(forms.ModelForm):
    CHOICE= [
        ('0', '0'),
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
        ('9', '9'),
        ('10', '10')
    ]
    X = forms.CharField(widget=forms.Select(choices=CHOICE))
    Xx = forms.CharField(widget=forms.Select(choices=CHOICE), label='10')
    dziewiec = forms.CharField(widget=forms.Select(choices=CHOICE))
    osiem = forms.CharField(widget=forms.Select(choices=CHOICE))
    siedem = forms.CharField(widget=forms.Select(choices=CHOICE))
    szesc = forms.CharField(widget=forms.Select(choices=CHOICE))
    piec = forms.CharField(widget=forms.Select(choices=CHOICE))
    cztery = forms.CharField(widget=forms.Select(choices=CHOICE))
    trzy = forms.CharField(widget=forms.Select(choices=CHOICE))
    dwa = forms.CharField(widget=forms.Select(choices=CHOICE))
    jeden = forms.CharField(widget=forms.Select(choices=CHOICE))
    class Meta:
        model = Wyniki
        fields = ['X', 'Xx', 'dziewiec', 'osiem', 'siedem', 'szesc', 'piec', 'cztery', 'trzy', 'dwa', 'jeden','kara']

class RejestracjaModelForm(forms.ModelForm):
    class Meta:
        model = Wyniki
        fields = (
            'zawody',
            'zawodnik',
            )




    def clean(self):
        cleaned_data = super().clean()
        wybrane_zawody = cleaned_data.get('zawody').id                                                                                                           #sprawdzam jakie wybrano zawody
        wybrany_zawodnik = cleaned_data.get('zawodnik').id                                                                                                       #sprawdzam jakiego wybrano zawodnika (tu zostanie przypisany mail)

        print(f'zawody to {wybrane_zawody}')
        # print(f'zawodnik to {wybrany_zawodnik}')

        zawodnicy_przypisani_do_zawodow = Wyniki.objects.filter(zawody__id=wybrane_zawody).values_list('zawodnik', flat=True).distinct()                          #wybieram wszystkich zawodników którzy są przypisani do wybranych zawodów (zmienna wybrane_zawody)
        zawodnicy_przypisani_do_zawodow_lista = []
        for i in zawodnicy_przypisani_do_zawodow:
            # print(f' wybrane zawody {i}')
            zawodnicy_przypisani_do_zawodow_lista.append(i)                                                                                                          #robię listę z wsyztskich zawodników przypisanych do danych zawodow
        print(f'zawodnicy przypisani do zawodow to {zawodnicy_przypisani_do_zawodow_lista}')
        if (wybrany_zawodnik in zawodnicy_przypisani_do_zawodow_lista):                                                                               #sprawdzam czy wybrany zawodnik jest na liscie z mailami uczestnikow wybranych zawodow
            raise ValidationError("Jesteś już zarejestrowany na te zawody")
            self.fields['zawodnik'] =wybrany_zawodnik

    def __init__(self, *args, **kwargs):
        from django.forms.widgets import HiddenInput
        user = kwargs.pop('user', None)
        pk = kwargs.pop('pk', None)
        super(RejestracjaModelForm, self).__init__(*args, **kwargs)
        print(f'user admin to {user}')
        self.fields['zawody'].queryset = Zawody.objects.filter(turniej__id=pk)
        # self.fields['zawodnik'] = forms.ModelChoiceField(queryset=Account.objects.all())
        if not user:
            self.fields['zawodnik'].widget = HiddenInput()


class TurniejModelForm(forms.ModelForm):
    class Meta:
        model = Turniej
        fields = (
            'nazwa',
            'rejestracja',
            )


class UstawieniaModelForm(forms.ModelForm):
    class Meta:
        model = Ustawienia
        fields = (
            'nazwa',
            'ustawienie',
            )

    def __init__(self, *args, **kwargs):
        from django.forms.widgets import HiddenInput
        super(UstawieniaModelForm, self).__init__(*args, **kwargs)
        self.fields['nazwa'].widget = HiddenInput()


class OplataModelForm(forms.ModelForm):
    class Meta:
        model = Wyniki
        fields = (
            'oplata',
            )

    # def clean(self):
    #     cleaned_data = super().clean()
    #     nazwisko = cleaned_data.get('nazwisko') 
    #     nazwisko = nazwisko.upper() 
    #     self.cleaned_data['nazwisko'] = nazwisko