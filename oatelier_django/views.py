from django.shortcuts import render
from datetime import datetime
from servicos.models import Servicos
from financeiro.models import ContaPagar, ContaReceber
from django.db import models

def dashboard(request):
    # Dados para o Dashboard
    entrada_labels = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
    entrada_data = [
        ContaReceber.objects.filter(data_vencimento__month=i).aggregate(total=models.Sum('valor'))['total'] or 0]
    saida_data = [
        ContaPagar.objects.filter(data_vencimento__month=i).aggregate(total=models.Sum('valor'))['total'] or 0]
    # Calculo do total de contas a pagar e receber
    total_contas_pagar = ContaPagar.objects.aggregate(total=models.Sum('valor'))['total'] or 0
    total_contas_receber = ContaReceber.objects.aggregate(total=models.Sum('valor'))['total'] or 0
    # Calculo do saldo
    saldo = total_contas_receber - total_contas_pagar
    
    
    # Calculo do total de serviços
    total_servicos = Servicos.objects.aggregate(total=models.Sum('valor'))['total'] or 0
    # Calculo do total de serviços por mês
    servicos_por_mes = Servicos.objects.filter(data__month=datetime.now().month).aggregate(total=models.Sum('valor'))['total'] or 0
    # Calculo do total de serviços por ano
    servicos_por_ano = Servicos.objects.filter(data__year=datetime.now().year).aggregate(total=models.Sum('valor'))['total'] or 0

    #dados para os filtros
    meses = [
        {'mes': 'Janeiro', 'valor': 1},
        {'mes': 'Fevereiro', 'valor': 2},
        {'mes': 'Março', 'valor': 3},
        {'mes': 'Abril', 'valor': 4},
        {'mes': 'Maio', 'valor': 5},
        {'mes': 'Junho', 'valor': 6},
        {'mes': 'Julho', 'valor': 7},
        {'mes': 'Agosto', 'valor': 8},
        {'mes': 'Setembro', 'valor': 9},
        {'mes': 'Outubro', 'valor': 10},
        {'mes': 'Novembro', 'valor': 11},
        {'mes': 'Dezembro', 'valor': 12}
    ]
    anos = list(range(2020, datetime.now().year + 1))
    mes_atual = datetime.now().month
    ano_atual = datetime.now().year
    # Renderiza o template com os dados do dashboard
    return render(request, 'dashboard.html', {
        'entrada_labels': entrada_labels,
        'entrada_data': entrada_data,
        'saida_data': saida_data,
        'total_contas_pagar': total_contas_pagar,
        'total_contas_receber': total_contas_receber,
        'saldo': saldo,
        'total_servicos': total_servicos,
        'servicos_por_mes': servicos_por_mes,
        'servicos_por_ano': servicos_por_ano,
        'meses': meses,
        'anos': anos,
        'mes_atual': mes_atual,
        'ano_atual': ano_atual
    })

