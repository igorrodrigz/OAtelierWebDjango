from django import forms
from financeiro.models import Entrada, Saida, ContaPagar, ContaReceber

class EntradaForm(forms.ModelForm):
    parcelas = forms.ChoiceField(
        choices=[(str(i), f"{i}x") for i in range(1, 13)],
        label="Parcelas",
        initial="1",
        required=False
    )

    class Meta:
        model = Entrada
        fields = ['descricao', 'valor', 'data', 'categoria', 'recebido_por']

class SaidaForm(forms.ModelForm):
    parcelas = forms.ChoiceField(
        choices=[(str(i), f"{i}x") for i in range(1, 13)],
        label="Parcela(s)",
        initial="1",
        required=False
    )

    class Meta:
        model = Saida
        fields = ['descricao', 'valor', 'data', 'categoria', 'pago_por']

class ContaPagarForm(forms.ModelForm):
    parcelas = forms.ChoiceField(
        choices=[(str(i), f"{i}x") for i in range(1, 13)],
        label="Parcelas",
        initial="1",
        required=False
    )

    class Meta:
        model = ContaPagar
        fields = ['descricao', 'documento', 'valor', 'data_vencimento', 'categoria', 'pago']

class ContaReceberForm(forms.ModelForm):
    parcelas = forms.ChoiceField(
        choices=[(str(i), f"{i}x") for i in range(1, 13)],
        label="Parcelas",
        initial="1",
        required=False
    )

    class Meta:
        model = ContaReceber
        fields = ['descricao', 'documento', 'valor', 'data_vencimento', 'categoria', 'recebido']
