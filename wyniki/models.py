from django.db import models
from account.models import Account
from zawody.models import Zawody
class Wyniki(models.Model):
	# zawody = models.CharField(max_length=30)
	zawody 		= models.ForeignKey(Zawody, on_delete=models.CASCADE)
	zawodnik 	= models.ForeignKey(Account, on_delete=models.CASCADE)
	X			=models.IntegerField(blank=True, null=False, default=0)
	Xx			=models.IntegerField(blank=True, null=False, default=0, verbose_name='/')
	dziewiec	=models.IntegerField(blank=True, null=False, default=0, verbose_name='9')
	osiem		=models.IntegerField(blank=True, null=False, default=0, verbose_name='8')
	siedem		=models.IntegerField(blank=True, null=False, default=0, verbose_name='7')
	szesc		=models.IntegerField(blank=True, null=False, default=0, verbose_name='6')
	piec		=models.IntegerField(blank=True, null=False, default=0, verbose_name='5')
	cztery		=models.IntegerField(blank=True, null=False, default=0, verbose_name='4')
	trzy		=models.IntegerField(blank=True, null=False, default=0, verbose_name='3')
	dwa			=models.IntegerField(blank=True, null=False, default=0, verbose_name='2')
	jeden		=models.IntegerField(blank=True, null=False, default=0, verbose_name='1')
	wynik 		=models.IntegerField(blank=True, default=0)
	komunikat	=models.CharField(blank=True, max_length=100)

	class Meta:
		verbose_name_plural = "Wyniki"
# Create your models here.


class Ustawienia(models.Model):
	nazwa = models.TextField()
	ustawienie = models.BooleanField(verbose_name='On/Off')

	class Meta:
		verbose_name_plural = "Ustawienia"