from django.core.exceptions import ValidationError
from django.db import models
from account.models import Account
from zawody.models import Zawody
class Wyniki(models.Model):
	# zawody = models.CharField(max_length=30)
	slug 		= models.SlugField(default=0)
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
	def save(self, *args, **kwargs):
		self.wynik = self.X*10 + self.Xx*10 + self.dziewiec*9 + self.osiem*8 + self.siedem*7 + self.szesc*6+ self.piec*5+ self.cztery*4+ self.trzy*3+ self.dwa*2+ self.jeden*1
		# self.slug = (self.zawodnik.username + str(self.zawody.id))
		liczba_strzalow = self.X*10 + self.Xx*10 + self.dziewiec+ self.osiem + self.siedem + self.szesc+ self.piec+ self.cztery+ self.trzy+ self.dwa+ self.jeden
		# if liczba_strzalow < 10:
		# 	self.komunikat = ""
		super(Wyniki, self).save(*args, **kwargs)

	def clean(self):
		# print(f'liczba strzalow {self.zawody.liczba_strzalow}')
		liczba_strzalow = self.zawody.liczba_strzalow
		mozliwe_wyniki = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
		if (self.X not in mozliwe_wyniki):
			raise ValidationError({'X': "Uzupełnij  pole wartością od 0 do 10"})
		elif (self.Xx not in mozliwe_wyniki):
			raise ValidationError({'Xx': "Uzupełnij pole wartością od 0 do 10"})
		elif (self.dziewiec not in mozliwe_wyniki):
			raise ValidationError({'dziewiec': "Uzupełnij pole wartością od 0 do 10"})
		elif (self.osiem not in mozliwe_wyniki):
			raise ValidationError({'osiem': "Uzupełnij pole wartością od 0 do 10"})
		elif (self.siedem not in mozliwe_wyniki):
			raise ValidationError({'siedem': "Uzupełnij pole wartością od 0 do 10"})
		elif (self.szesc not in mozliwe_wyniki):
			raise ValidationError({'szesc': "Uzupełnij pole wartością od 0 do 10"})
		elif (self.piec not in mozliwe_wyniki):
			raise ValidationError({'piec': "Uzupełnij pole wartością od 0 do 10"})
		elif (self.cztery not in mozliwe_wyniki):
			raise ValidationError({'cztery': "Uzupełnij pole wartością od 0 do 10"})
		elif (self.trzy not in mozliwe_wyniki):
			raise ValidationError({'trzy': "Uzupełnij pole wartością od 0 do 10"})
		elif (self.dwa not in mozliwe_wyniki):
			raise ValidationError({'dwa': "Uzupełnij pole wartością od 0 do 10"})
		elif (self.jeden not in mozliwe_wyniki):
			raise ValidationError({'jeden': "Uzupełnij pole wartością od 0 do 10"})
		elif self.X+self.Xx+self.dziewiec+self.osiem+self.siedem+self.szesc+self.piec+self.cztery+self.trzy+self.dwa+self.jeden > liczba_strzalow:
			raise ValidationError({'X': f'Maksymalna liczba strzałów w tej konkurencji to {liczba_strzalow}'})


class Ustawienia(models.Model):
	nazwa = models.TextField()
	ustawienie = models.BooleanField(verbose_name='On/Off')

	class Meta:
		verbose_name_plural = "Ustawienia"