from django.contrib import admin
from .models import Client

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'created_at')
    exclude = ('token_auth', 'user_integration', 'password_integration')
    pass