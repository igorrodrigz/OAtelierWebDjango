from django.contrib import admin
from .models import Clientes

# Register your models here.

@admin.register(Clientes)
class ClienteAdmin(admin.ModelAdmin):
    verbose_name = "Cliente"
    verbose_name_plural = "Clientes"
    list_display = ('nome', 'endereco', 'email','status')
    search_fields = ('nome', 'telefone', 'endereco', 'email',)
    list_filter = ('data_cadastro','status',)
    list_per_page = 10
    ordering = ('status',)

