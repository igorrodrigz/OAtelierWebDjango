from django.shortcuts import render
from django.db.models import Sum, Count, Q
from datetime import datetime, timedelta
from servicos.models import Servicos
from financeiro.models import Entrada, Saida, ContaPagar, ContaReceber
import json

def dashboard(request):
    # Filtros de mês/ano
    mes = int(request.GET.get('mes', datetime.now().month))
    ano = int(request.GET.get('ano', datetime.now().year))

    # Entradas e Saídas do mês/ano selecionado
    entradas_mes = Entrada.objects.filter(data__month=mes, data__year=ano)
    saidas_mes = Saida.objects.filter(data__month=mes, data__year=ano)
    total_entradas = entradas_mes.aggregate(total=Sum('valor'))['total'] or 0
    total_saidas = saidas_mes.aggregate(total=Sum('valor'))['total'] or 0
    saldo_mes = total_entradas - total_saidas

    # Listas principais
    principais_entradas = entradas_mes.order_by('-valor')[:5]
    principais_saidas = saidas_mes.order_by('-valor')[:5]

    # Evolução anual
    entrada_labels = []
    entrada_data = []
    saida_data = []
    for m in range(1, 13):
        entrada_labels.append(f"{m:02d}/{ano}")
        entrada_data.append(float(Entrada.objects.filter(data__month=m, data__year=ano).aggregate(total=Sum('valor'))['total'] or 0))
        saida_data.append(float(Saida.objects.filter(data__month=m, data__year=ano).aggregate(total=Sum('valor'))['total'] or 0))

    # Contas a pagar
    contas_pagar = ContaPagar.objects.filter(data_vencimento__year=ano)
    total_pagar_pendentes = contas_pagar.filter(pago=False).aggregate(total=Sum('valor'))['total'] or 0
    total_pagar_pagas = contas_pagar.filter(pago=True).aggregate(total=Sum('valor'))['total'] or 0
    proximas_pagar = contas_pagar.filter(pago=False, data_vencimento__gte=datetime.now()).order_by('data_vencimento')[:5]
    # Gráfico por categoria/status
    pagar_por_categoria = contas_pagar.values('categoria').annotate(qtd=Count('id'))

    # Contas a receber
    contas_receber = ContaReceber.objects.filter(data_vencimento__year=ano)
    total_receber_pendentes = contas_receber.filter(recebido=False).aggregate(total=Sum('valor'))['total'] or 0
    total_receber_recebidas = contas_receber.filter(recebido=True).aggregate(total=Sum('valor'))['total'] or 0
    proximas_receber = contas_receber.filter(recebido=False, data_vencimento__gte=datetime.now()).order_by('data_vencimento')[:5]
    receber_por_categoria = contas_receber.values('categoria').annotate(qtd=Count('id'))

    # Percentuais
    pct_pagas = (total_pagar_pagas / (total_pagar_pendentes + total_pagar_pagas) * 100) if (total_pagar_pendentes + total_pagar_pagas) > 0 else 0
    pct_recebidas = (total_receber_recebidas / (total_receber_pendentes + total_receber_recebidas) * 100) if (total_receber_pendentes + total_receber_recebidas) > 0 else 0

    # Alertas de contas vencendo em breve (próximos 7 dias)
    hoje = datetime.now().date()
    vencendo_pagar = contas_pagar.filter(pago=False, data_vencimento__range=[hoje, hoje+timedelta(days=7)])
    vencendo_receber = contas_receber.filter(recebido=False, data_vencimento__range=[hoje, hoje+timedelta(days=7)])

    # Serviços - preparar listas para gráficos
    servicos_status = Servicos.objects.values('status').annotate(qtd=Count('id'))
    servicos_labels = [s['status'] for s in servicos_status]
    servicos_data = [s['qtd'] for s in servicos_status]

    # Filtros para selects
    meses = [
        {'nome': 'Janeiro', 'valor': 1},
        {'nome': 'Fevereiro', 'valor': 2},
        {'nome': 'Março', 'valor': 3},
        {'nome': 'Abril', 'valor': 4},
        {'nome': 'Maio', 'valor': 5},
        {'nome': 'Junho', 'valor': 6},
        {'nome': 'Julho', 'valor': 7},
        {'nome': 'Agosto', 'valor': 8},
        {'nome': 'Setembro', 'valor': 9},
        {'nome': 'Outubro', 'valor': 10},
        {'nome': 'Novembro', 'valor': 11},
        {'nome': 'Dezembro', 'valor': 12}
    ]
    anos = list(range(2020, datetime.now().year + 1))

    return render(request, 'dashboard.html', {
        'meses': meses,
        'anos': anos,
        'mes_atual': mes,
        'ano_atual': ano,
        'entrada_labels': json.dumps(entrada_labels),
        'entrada_data': json.dumps(entrada_data),
        'saida_data': json.dumps(saida_data),
        'total_entradas': total_entradas,
        'total_saidas': total_saidas,
        'saldo_mes': saldo_mes,
        'principais_entradas': principais_entradas,
        'principais_saidas': principais_saidas,
        'total_pagar_pendentes': total_pagar_pendentes,
        'total_pagar_pagas': total_pagar_pagas,
        'proximas_pagar': proximas_pagar,
        'pagar_por_categoria': list(pagar_por_categoria),
        'total_receber_pendentes': total_receber_pendentes,
        'total_receber_recebidas': total_receber_recebidas,
        'proximas_receber': proximas_receber,
        'receber_por_categoria': list(receber_por_categoria),
        'pct_pagas': pct_pagas,
        'pct_recebidas': pct_recebidas,
        'vencendo_pagar': vencendo_pagar,
        'vencendo_receber': vencendo_receber,
        'servicos': list(servicos_status),
        'servicos_labels': json.dumps(servicos_labels),
        'servicos_data': json.dumps(servicos_data),
    })

