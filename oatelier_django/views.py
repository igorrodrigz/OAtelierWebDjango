from django.shortcuts import render, redirect
from django.forms import modelformset_factory
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, Q
from datetime import datetime, timedelta
from financeiro.forms import EntradaForm, SaidaForm, ContaPagarForm, ContaReceberForm
from financeiro.models import Entrada, Saida, ContaPagar, ContaReceber
from servicos.models import Servicos


@login_required
def inserir_lote_financeiro(request):
    formsets_info = [
        ('entrada', Entrada, EntradaForm),
        ('saida', Saida, SaidaForm),
        ('contapagar', ContaPagar, ContaPagarForm),
        ('contareceber', ContaReceber, ContaReceberForm),
    ]
    context = {}
    if request.method == 'POST':
        for prefix, model, form_class in formsets_info:
            FormSet = modelformset_factory(model, form=form_class, extra=10, max_num=10, can_delete=False)
            formset = FormSet(request.POST, prefix=prefix)
            context[f'{prefix}_formset'] = formset
            if formset.is_valid():
                objs = [f.save(commit=False) for f in formset if f.cleaned_data]
                if objs:
                    model.objects.bulk_create(objs)
        return redirect('dashboard')
    else:
        for prefix, model, form_class in formsets_info:
            FormSet = modelformset_factory(model, form=form_class, extra=10, max_num=10, can_delete=False)
            context[f'{prefix}_formset'] = FormSet(queryset=model.objects.none(), prefix=prefix)
    return render(request, 'financeiro/inserir_lote.html', context)



@login_required
def dashboard(request):
    # Filtros de mês/ano

    # Sempre usar mês/ano atual como padrão, exceto se GET explicito
    mes_raw = request.GET.get('mes')
    ano_raw = request.GET.get('ano')
    now = datetime.now()
    try:
        mes = int(mes_raw) if mes_raw is not None and mes_raw != '' else now.month
    except (ValueError, TypeError):
        mes = now.month
    try:
        ano = int(ano_raw) if ano_raw is not None and ano_raw != '' else now.year
    except (ValueError, TypeError):
        ano = now.year
    mes_str = f'{mes:02}'

    # Entradas e Saídas do mês/ano selecionado
    entradas_mes = Entrada.objects.filter(data__month=mes, data__year=ano)
    saidas_mes = Saida.objects.filter(data__month=mes, data__year=ano)

    # Categorias de Entradas
    entrada_categorias = entradas_mes.values('categoria').annotate(total=Sum('valor')).order_by('-total')
    entrada_categorias_labels = [c['categoria'] for c in entrada_categorias]
    entrada_categorias_data = [float(c['total']) for c in entrada_categorias]

    # Categorias de Saídas
    saida_categorias = saidas_mes.values('categoria').annotate(total=Sum('valor')).order_by('-total')
    saida_categorias_labels = [c['categoria'] for c in saida_categorias]
    saida_categorias_data = [float(c['total']) for c in saida_categorias]

    total_entradas = entradas_mes.aggregate(total=Sum('valor'))['total'] or 0
    total_saidas = saidas_mes.aggregate(total=Sum('valor'))['total'] or 0
    saldo_mes = total_entradas - total_saidas

    # Ticket médio
    ticket_medio = entradas_mes.aggregate(avg=Sum('valor')/Count('id'))['avg'] if entradas_mes.count() > 0 else 0
    if not ticket_medio or ticket_medio == float('inf'):
        ticket_medio = 0

    # Quantidade de serviços
    servicos_qtd = Servicos.objects.filter(data_entrada__month=mes, data_entrada__year=ano).count()

    # Listas principais
    principais_entradas = entradas_mes.order_by('-valor')[:5]
    principais_saidas = saidas_mes.order_by('-valor')[:5]


    # Gráfico de entradas/saídas do mês
    entrada_labels = [e.data.strftime('%d/%m') for e in entradas_mes]
    entrada_data = [float(e.valor) for e in entradas_mes]
    saida_data = [float(s.valor) for s in saidas_mes]

    # Gráfico Contas a Receber x Contas a Pagar (pagos)
    # Agrupar por dia do mês
    from collections import defaultdict
    cr_pagos = ContaReceber.objects.filter(data_vencimento__month=mes, data_vencimento__year=ano, recebido=True)
    cp_pagos = ContaPagar.objects.filter(data_vencimento__month=mes, data_vencimento__year=ano, pago=True)
    dias = sorted(set(list(cr_pagos.values_list('data_vencimento', flat=True)) + list(cp_pagos.values_list('data_vencimento', flat=True))))
    dias_labels = [d.strftime('%d/%m') for d in dias]
    cr_por_dia = defaultdict(float)
    cp_por_dia = defaultdict(float)
    for c in cr_pagos:
        cr_por_dia[c.data_vencimento.strftime('%d/%m')] += float(c.valor)
    for c in cp_pagos:
        cp_por_dia[c.data_vencimento.strftime('%d/%m')] += float(c.valor)
    cr_pagos_data = [cr_por_dia[d] for d in dias_labels]
    cp_pagos_data = [cp_por_dia[d] for d in dias_labels]

    # Contas a pagar
    contas_pagar = ContaPagar.objects.filter(data_vencimento__year=ano)
    total_pagar_pendentes = contas_pagar.filter(pago=False).aggregate(total=Sum('valor'))['total'] or 0
    total_pagar_pagas = contas_pagar.filter(pago=True).aggregate(total=Sum('valor'))['total'] or 0
    proximas_pagar = contas_pagar.filter(pago=False, data_vencimento__gte=datetime.now()).order_by('data_vencimento')[:5]
    # Agrupar por categoria: quantidade e soma dos valores não pagos
    pagar_por_categoria = contas_pagar.filter(pago=False).values('categoria').annotate(
        qtd=Count('id'),
        total=Sum('valor')
    )

    # Contas a receber
    contas_receber = ContaReceber.objects.filter(data_vencimento__year=ano)
    total_receber_pendentes = contas_receber.filter(recebido=False).aggregate(total=Sum('valor'))['total'] or 0
    total_receber_recebidas = contas_receber.filter(recebido=True).aggregate(total=Sum('valor'))['total'] or 0
    proximas_receber = contas_receber.filter(recebido=False, data_vencimento__gte=datetime.now()).order_by('data_vencimento')[:5]
    # Agrupar por categoria: quantidade e soma dos valores não recebidos
    receber_por_categoria = contas_receber.filter(recebido=False).values('categoria').annotate(
        qtd=Count('id'),
        total=Sum('valor')
    )

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
        'entrada_categorias_labels': entrada_categorias_labels,
        'entrada_categorias_data': entrada_categorias_data,
        'saida_categorias_labels': saida_categorias_labels,
        'saida_categorias_data': saida_categorias_data,
        'cr_pagos_labels': dias_labels,
        'cr_pagos_data': cr_pagos_data,
        'cp_pagos_data': cp_pagos_data,
        'pagar_por_categoria': list(pagar_por_categoria),
        'receber_por_categoria': list(receber_por_categoria),
    })

