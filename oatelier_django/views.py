from django.shortcuts import render
from datetime import datetime

def dashboard(request):
    # Dados fictícios para o dashboard
    entrada_labels = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun']
    entrada_data = [1000, 1500, 2000, 2500, 3000, 3500]
    saida_data = [800, 1200, 1800, 2000, 2500, 3000]

    pagar = 5  # Contas a pagar pendentes
    receber = 8  # Contas a receber pendentes

    servicos = [
        {'status': 'Pendente', 'qtd': 10},
        {'status': 'Em andamento', 'qtd': 5},
        {'status': 'Concluído', 'qtd': 15},
    ]

    # Dados para os filtros
    meses = [
        {'valor': 1, 'nome': 'Janeiro'},
        {'valor': 2, 'nome': 'Fevereiro'},
        {'valor': 3, 'nome': 'Março'},
        {'valor': 4, 'nome': 'Abril'},
        {'valor': 5, 'nome': 'Maio'},
        {'valor': 6, 'nome': 'Junho'},
    ]
    anos = [2023, 2024, 2025]
    mes_atual = datetime.now().month
    ano_atual = datetime.now().year

    context = {
        'entrada_labels': entrada_labels,
        'entrada_data': entrada_data,
        'saida_data': saida_data,
        'pagar': pagar,
        'receber': receber,
        'servicos': servicos,
        'meses': meses,
        'anos': anos,
        'mes_atual': mes_atual,
        'ano_atual': ano_atual,
    }
    return render(request, 'dashboard.html', context)