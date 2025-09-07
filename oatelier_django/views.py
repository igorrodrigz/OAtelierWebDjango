from django.shortcuts import render
from django.db.models import Sum, Count, Q
from datetime import datetime, timedelta
from servicos.models import Servicos
from financeiro.models import Entrada, Saida, ContaPagar, ContaReceber
import json

def dashboard(request):
    # Filtros de mês/ano
    mes = request.GET.get('mes')
    if mes is None:
        mes = f'{datetime.now().month:02}'
    else:
        mes = f'{int(mes):02}'
    ano = int(request.GET.get('ano', datetime.now().year))

    # Entradas e Saídas do mês/ano selecionado
    entradas_mes = Entrada.objects.filter(data__month=int(mes), data__year=ano)
    saidas_mes = Saida.objects.filter(data__month=int(mes), data__year=ano)
    total_entradas = entradas_mes.aggregate(total=Sum('valor'))['total'] or 0
    total_saidas = saidas_mes.aggregate(total=Sum('valor'))['total'] or 0
    saldo_mes = total_entradas - total_saidas

    # Ticket médio
    ticket_medio = entradas_mes.aggregate(avg=Sum('valor')/Count('id'))['avg'] if entradas_mes.count() > 0 else 0
    if not ticket_medio or ticket_medio == float('inf'):
        ticket_medio = 0

    # Quantidade de serviços
    servicos_qtd = Servicos.objects.filter(data_entrada__month=int(mes), data_entrada__year=ano).count()

    # Listas principais
    principais_entradas = entradas_mes.order_by('-valor')[:5]
    principais_saidas = saidas_mes.order_by('-valor')[:5]

    # Gráfico de entradas/saídas do mês
    entrada_labels = [e.data.strftime('%d/%m') for e in entradas_mes]
    entrada_data = [float(e.valor) for e in entradas_mes]
    saida_data = [float(s.valor) for s in saidas_mes]

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
        {'nome': 'Janeiro', 'valor': '01'},
        {'nome': 'Fevereiro', 'valor': '02'},
        {'nome': 'Março', 'valor': '03'},
        {'nome': 'Abril', 'valor': '04'},
        {'nome': 'Maio', 'valor': '05'},
        {'nome': 'Junho', 'valor': '06'},
        {'nome': 'Julho', 'valor': '07'},
        {'nome': 'Agosto', 'valor': '08'},
        {'nome': 'Setembro', 'valor': '09'},
        {'nome': 'Outubro', 'valor': '10'},
        {'nome': 'Novembro', 'valor': '11'},
        {'nome': 'Dezembro', 'valor': '12'}
    ]
    anos = list(range(2020, datetime.now().year + 1))

    return render(request, 'dashboard.html', {
        'meses': meses,
        'anos': anos,
        'mes_atual': mes,
        'ano_atual': ano,
        'entrada_labels': entrada_labels,
        'entrada_data': entrada_data,
        'saida_data': saida_data,
        'total_entradas': total_entradas,
        'total_saidas': total_saidas,
        'saldo_mes': saldo_mes,
        'servicos_qtd': servicos_qtd,
        'ticket_medio': ticket_medio,
        'principais_entradas': principais_entradas,
        'principais_saidas': principais_saidas,
        'servicos_labels': servicos_labels,
        'servicos_data': servicos_data,
    })

