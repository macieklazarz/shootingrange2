from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField
from .models import Zawody, Sedzia


class ZawodyModelForm(forms.ModelForm):
	class Meta:
		model = Zawody
		fields = (
			'nazwa',
			'liczba_strzalow',
			'turniej',
			)
	def __init__(self, *args, **kwargs):
		super(ZawodyModelForm, self).__init__(*args, **kwargs)
		self.fields['liczba_strzalow'].label = 'Liczba strzałów'

#formularz przypisywania sędziego do konkurencji
class SedziaModelForm(forms.ModelForm):
	class Meta:
		model = Sedzia
		fields = (
			'zawody',
			'sedzia',
			)
	def __init__(self, *args, **kwargs):
		super(SedziaModelForm, self).__init__(*args, **kwargs)
		#w propertce sedzia możemy wybrać tylko takiego usera, który jest sędzią
		self.fields['sedzia'].queryset = self.fields['sedzia'].queryset.filter(is_sedzia=1)
		self.fields['sedzia'].label = 'Sędzia'