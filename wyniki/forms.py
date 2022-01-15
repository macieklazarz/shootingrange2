from django import forms
from . import models
from zawody.models import Zawody, Turniej
from account.models import Account
from wyniki.models import Wyniki, Ustawienia
from django.core.exceptions import ValidationError
from django.forms.widgets import CheckboxSelectMultiple
from django.forms.models import ModelMultipleChoiceField
from django.forms.models import inlineformset_factory



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
        #sprawdzam czy zawodnik nie jest już przypisany do danej konkurencji
        wybrane_zawody = cleaned_data.get('zawody').id                                                                                                          
        wybrany_zawodnik = cleaned_data.get('zawodnik').id                                                                                                       
        zawodnik_juz_zarejestrowany = Wyniki.objects.filter(zawody=wybrane_zawody, zawodnik=wybrany_zawodnik)
        if zawodnik_juz_zarejestrowany:                                                                               
            raise ValidationError("Jesteś już zarejestrowany na te zawody")
            #formularz jest czyszczony więc ustawiam wartość początkową w polu zawodnik na tego zawodnika, który próbuje się zarejestrować
            self.fields['zawodnik'] =wybrany_zawodnik



    def __init__(self, *args, **kwargs):
        from django.forms.widgets import HiddenInput
        #kwargs podwawane są z views.py
        user = kwargs.pop('user', None)
        pk = kwargs.pop('pk', None)
        super(RejestracjaModelForm, self).__init__(*args, **kwargs)
        self.fields['zawody'].queryset = Zawody.objects.filter(turniej__id=pk)
        self.fields['zawodnik'].queryset = Account.objects.all().order_by('nazwisko')

        #w zmiennej user podawana jest 1 jeśli user wywołujący formularz to rts (patrz plik views.py). Wtedy taki user może wybrać zawodnika, którego chce zarejestrować
        if not user:
            self.fields['zawodnik'].widget = HiddenInput()


class TurniejModelForm(forms.ModelForm):
    class Meta:
        model = Turniej
        fields = (
            'nazwa',
            'rejestracja',
            )

ModuleFormSet = inlineformset_factory(Account,
                                      Wyniki,
                                      fields=['oplata',],
                                      extra=0,
                                      can_delete=False,
                                      labels = {'oplata': 'Opłata',}
                                      )

