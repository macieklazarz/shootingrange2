from django.db import models
from django.core.exceptions import ValidationError
from account.models import Account
from zawody.models import Zawody, ZawodyDynamic, Turniej
from wyniki.models import Wyniki
from account.models import Account
# Create your models here.


class Order(models.Model):
	turniej = models.ForeignKey(Turniej, on_delete=models.SET_NULL, null=True, blank=True)
	zawodnik = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True)
	is_paid = models.BooleanField(default=False, verbose_name='Opłacono')

	def __str__(self):
		return (self.turniej.nazwa)


class OrderItem(models.Model):
	order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
	wynik = models.ForeignKey(Wyniki, on_delete=models.CASCADE, null=True, blank=True)
	is_paid = models.BooleanField(default=False, verbose_name='Opłacono')
	to_pay = models.FloatField(default=0)

