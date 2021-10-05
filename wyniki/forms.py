from django import forms
from . import models
from zawody.models import Zawody
from account.models import Account
from wyniki.models import Wyniki
from django.core.exceptions import ValidationError

class DodajZawodnika(forms.ModelForm):
    # zawody=forms.ModelChoiceField(queryset=Zawody.objects.all())
    # zawodnik=forms.ModelChoiceField(queryset=Account.objects.all())
    # class Meta:
    #     model=models.Wyniki
    #     fields = ['zawodnik', 'zawody']
    # def save(self, commit=True):
    #     instance = super().cabe(commit=False)
    #     zaw = self.cleaned_data['zawodnik']
    #     instance.zawodnik = zaw[0]
    #     instance.save(commit)
    #     return instance
    class Meta:
        model = models.Wyniki
        # fields = ['zawody']
        # fields = ['zawodnik', 'zawody']
        fields = [ 'zawody', 'zawodnik']
        # exclude =['zawodnik']

    def __init__(self, *args, **kwargs):
        super(DodajZawodnika, self).__init__(*args, **kwargs)
        self.fields['zawodnik'] = forms.ModelChoiceField(queryset=Account.objects.all())
        self.fields['zawody'] = forms.ModelChoiceField(queryset=Zawody.objects.all())

    def clean(self):
        cleaned_data = super().clean()
        # zaw = cleaned_data.get('zawodnik')
        # zaw = str(cleaned_data.get('zawody'))
        zaw = request.POST['zawody']
        # zaw = self.fields['zawody']
        print(f'zaw wynosi {zaw}')
        # id_zawodow=Zawody.objects.filter(nazwa=zaw)
        wybrane_zawody = Wyniki.objects.filter(zawody__nazwa=zaw).values_list('zawodnik', flat=True).distinct()
        list = []
        # wybrane_zawody2 = wybrane_zawody.get('zawodnik')
        for i in wybrane_zawody:
            # print(f' wybrane zawody {i}')
            list.append(i)
        # zaw = self.fields['zawodnik']
        # print(f' wybrane zawody {list}')
        # lista = 'admin@admin.com'
        # print(f'zawodniczek to {zaw} typ {type(zaw)} {lista} typ {type(lista)}')
        # if zaw == lista:
        #     print('powinno wywalic')
        #     raise ValidationError("juz jest")

