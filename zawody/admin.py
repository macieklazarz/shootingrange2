from zawody.models import Zawody
from django.contrib import admin

# Register your models here.
@admin.register(Zawody)
class ZawodyAdmin(admin.ModelAdmin):
	list_display = ('nazwa',)
	search_fields = ('nazwa',)
