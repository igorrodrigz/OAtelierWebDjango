from django.contrib import admin
from .models import Clientes

# Register your models here.

@admin.register(Clientes)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'endereco', 'email','status')
    search_fields = ('nome', 'telefone', 'endereco', 'email',)
    list_filter = ('data_cadastro','status',)
    list_per_page = 10
    ordering = ('status',)

