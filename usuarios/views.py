from django.shortcuts import render

# Create your views here.
from django.db.models.functions import TruncMonth
from django.db.models import Sum, Count
from datetime import date
from servicos.models import Servico
from financeiro.models import Entrada, Saida, ContaPagar, ContaReceber

def dashboard(request):
    # Entradas e saídas por mês
    entradas = Entrada.objects.annotate(mes=TruncMonth('data')).values('mes').annotate(total=Sum('valor')).order_by('mes')
    saidas = Saida.objects.annotate(mes=TruncMonth('data')).values('mes').annotate(total=Sum('valor')).order_by('mes')

    entrada_labels = [e['mes'].strftime('%b/%Y') for e in entradas]
    entrada_data = [float(e['total']) for e in entradas]
    saida_data = [float(s['total']) for s in saidas]

    # Contas pendentes
    pagar = ContaPagar.objects.filter(pago=False).count()
    receber = ContaReceber.objects.filter(recebido=False).count()

    # Status dos serviços
    servicos = Servico.objects.values('status').annotate(qtd=Count('id'))

    return render(request, 'dashboard.html', {
        "entrada_labels": entrada_labels,
        "entrada_data": entrada_data,
        "saida_data": saida_data,
        "pagar": pagar,
        "receber": receber,
        "servicos": servicos,
    })
