from django.contrib import admin
from .models import Entrada, Saida, ContaPagar, ContaReceber
from import_export.admin import ImportExportModelAdmin
from import_export import resources

# Resources
class EntradaResource(resources.ModelResource):
    class Meta:
        model = Entrada

class SaidaResource(resources.ModelResource):
    class Meta:
        model = Saida

class ContaPagarResource(resources.ModelResource):
    class Meta:
        model = ContaPagar
        fields = ('id', 'descricao', 'valor', 'data_vencimento', 'categoria', 'pago', 'criado_em', 'atualizado_em')

class ContaReceberResource(resources.ModelResource):
    class Meta:
        model = ContaReceber

# Admins
@admin.register(Entrada)
class EntradaAdmin(ImportExportModelAdmin):
    resource_class = EntradaResource
    list_display = ('descricao', 'valor', 'data', 'categoria', 'recebido_por', 'criado_em', 'atualizado_em')
    search_fields = ('descricao', 'categoria')
    list_filter = ('data', 'categoria')

@admin.register(Saida)
class SaidaAdmin(ImportExportModelAdmin):
    resource_class = SaidaResource
    list_display = ('descricao', 'valor', 'data', 'categoria', 'pago_por', 'criado_em', 'atualizado_em')
    search_fields = ('descricao', 'categoria')
    list_filter = ('data', 'categoria')

@admin.register(ContaPagar)
class ContaPagarAdmin(ImportExportModelAdmin):
    resource_class = ContaPagarResource
    list_display = ('descricao', 'valor', 'data_vencimento', 'categoria', 'pago', 'criado_em', 'atualizado_em')
    search_fields = ('descricao', 'categoria')
    list_filter = ('data_vencimento', 'categoria', 'pago')

@admin.register(ContaReceber)
class ContaReceberAdmin(ImportExportModelAdmin):
    resource_class = ContaReceberResource
    list_display = ('descricao', 'valor', 'data_vencimento', 'categoria', 'recebido', 'criado_em', 'atualizado_em')
    search_fields = ('descricao', 'categoria')
    list_filter = ('data_vencimento', 'categoria', 'recebido')
