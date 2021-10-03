from django import forms
from . import models

class DodajZawodnika(forms.ModelForm):
    class Meta:
        model = models.Wyniki
        fields = ['zawodnik', 'zawody']

