from django.contrib import admin
from .models import Servicos, ServicosFotos
from clientes.models import Clientes

# Register your models here.

class ServicosFotosInline(admin.TabularInline):
    model = ServicosFotos
    extra = 1
@admin.register(Servicos)
class ServicosAdmin(admin.ModelAdmin):
    list_display = ('nome_projeto', 'valor', 'data_entrada', 'status', 'data_prazo', 'cliente')
    list_display_links = ('nome_projeto',)
    search_fields = ('nome_projeto', 'cliente__nome',)
    list_filter = ('data_entrada','status',)
    list_per_page = 20
    ordering = ('status',)
    inlines = [ServicosFotosInline]
    autocomplete_fields = ['cliente']