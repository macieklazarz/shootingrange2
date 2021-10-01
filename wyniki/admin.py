from django.contrib import admin
from account.models import Account
from wyniki.models import Wyniki

# Register your models here.
@admin.register(Wyniki)
class WynikiAdmin(admin.ModelAdmin):
	list_display = ('zawody', 'zawodnik', 'wynik1')
	search_fields = ('zawody', 'zawodnik')

# admin.site.register(Account, WynikiAdmin)