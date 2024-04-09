from django.contrib import admin

from users.models import Users


class UsersAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'mobile_number', 'last_login')
    list_filter = ('username', 'email')


admin.site.register(Users, UsersAdmin)
