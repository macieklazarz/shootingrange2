from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from account.models import Account, Rts



# Register your models here.

class AccountAdmin(UserAdmin):
	list_display = ('email', 'username','nazwisko', 'imie', 'date_joined', 'last_login', 'is_admin', 'is_staff', 'paid')
	search_fields = ('email', 'username', 'nazwisko')
	readonly_field = ('date_joined', 'last_login')

	filter_horizontal = ()
	list_filter = ()
	fieldsets = ()

admin.site.register(Account, AccountAdmin)
admin.site.register(Rts)
