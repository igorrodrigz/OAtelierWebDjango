from django.contrib import admin
from .models import Entrada, Saida, ContaPagar, ContaReceber

# Register your models here.
@admin.register(Entrada)
class EntradaAdmin(admin.ModelAdmin):
    list_display = ('descricao', 'valor', 'data', 'categoria', 'recebido_por', 'criado_em', 'atualizado_em')
    search_fields = ('descricao', 'categoria')
    list_filter = ('data', 'categoria')


@admin.register(Saida)
class SaidaAdmin(admin.ModelAdmin):
    list_display = ('descricao', 'valor', 'data', 'categoria', 'pago_por', 'criado_em', 'atualizado_em')
    search_fields = ('descricao', 'categoria')
    list_filter = ('data', 'categoria')

@admin.register(ContaPagar)
class ContaPagarAdmin(admin.ModelAdmin):
    list_display = ('descricao', 'valor', 'data_vencimento', 'categoria', 'pago', 'criado_em', 'atualizado_em')
    search_fields = ('descricao', 'categoria')
    list_filter = ('data_vencimento', 'categoria', 'pago')

@admin.register(ContaReceber)
class ContaReceberAdmin(admin.ModelAdmin):
    list_display = ('descricao', 'valor', 'data_vencimento', 'categoria', 'recebido', 'criado_em', 'atualizado_em')
    search_fields = ('descricao', 'categoria')
    list_filter = ('data_vencimento', 'categoria', 'recebido')

    
