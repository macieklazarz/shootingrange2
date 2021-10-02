from django.contrib import admin
from account.models import Account
from wyniki.models import Wyniki

# Register your models here.
@admin.register(Wyniki)
class WynikiAdmin(admin.ModelAdmin):
	list_display = ('zawody', 'zawodnik', 'X', 'Xx', 'dziewiec', 'osiem', 'siedem', 'szesc', 'piec', 'cztery', 'trzy', 'dwa', 'jeden', 'wynik', 'komunikat')
	search_fields = ('zawody', 'zawodnik')

# admin.site.register(Account, WynikiAdmin)