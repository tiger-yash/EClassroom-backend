
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from authentication.models import Account,GoogleAuth



class AccountAdmin(UserAdmin):
	list_display = ('email','username', 'is_teacher', 'is_student')
	search_fields = ('email','username',)
	readonly_fields=('id',)

	filter_horizontal = ()
	list_filter = ()
	fieldsets = ()


admin.site.register(Account, AccountAdmin)
admin.site.register(GoogleAuth)