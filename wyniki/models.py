from django.db import models
from account.models import Account
from zawody.models import Zawody
class Wyniki(models.Model):
	# zawody = models.CharField(max_length=30)
	zawody = models.ForeignKey(Zawody, on_delete=models.CASCADE)
	zawodnik = models.ForeignKey(Account, on_delete=models.CASCADE)
	wynik1 = models.IntegerField(blank=True, null=False, default=0)
# Create your models here.
