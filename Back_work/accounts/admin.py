from django.contrib import admin
from .models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'nickname', 'username', 'image',)

admin.site.register(User, UserAdmin)