from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import Account, VerificationTokens, ForgotPasswordPin


class AccountAdmin(UserAdmin):
    list_display = ('pk', 'email', 'username', 'date_joined', 'last_login')
    search_fields = ('pk', 'email', 'username',)
    readonly_fields = ('pk', 'date_joined', 'last_login','is_admin', 'is_staff')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Account, AccountAdmin)
admin.site.register(VerificationTokens)
admin.site.register(ForgotPasswordPin)

