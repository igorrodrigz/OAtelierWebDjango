from financeiro.models import Entrada, Saida, ContaPagar, ContaReceber
from random import randint, choice
from datetime import date, timedelta

#Entrada
for i in range(20):
    Entrada.objects.create(
        descricao=f"Entrada {i+1}",
        valor=randint(100, 1000),
        data=date.today() - timedelta(days=randint(1, 30)),
        categoria=choice(['Salário', 'Venda', 'Serviço']),
        pago=choice(['Sim', 'Não']),
    )

#Saida
for i in range(20):
    Saida.objects.create(
        descricao=f"Saída {i+1}",
        valor=randint(100, 1000),
        data=date.today() - timedelta(days=randint(1, 30)),
        categoria=choice(['Aluguel', 'Conta', 'Compra']),
        pago_por=choice(['Cartão', 'Dinheiro']),
    )

#ContaPagar
for i in range(20):
    ContaPagar.objects.create(
        descricao=f"Conta a Pagar {i+1}",
        valor=randint(100, 1000),
        data_vencimento=date.today() + timedelta(days=randint(1, 30)),
        categoria=choice(['Aluguel', 'Conta', 'Compra']),
        pago=choice([True, False]),
    )

#ContaReceber
for i in range(20):
    ContaReceber.objects.create(
        descricao=f"Conta a Receber {i+1}",
        valor=randint(100, 1000),
        data_vencimento=date.today() + timedelta(days=randint(1, 30)),
        categoria=choice(['Salário', 'Venda', 'Serviço']),
        recebido=choice([True, False]),
    )
print("Dados populados com sucesso!")