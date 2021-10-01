from django.db import models
from account.models import Account
class Zawody(models.Model):
	nazwa = models.CharField(max_length=30)

	def __str__(self):
		return self.nazwa
# Create your models here.
