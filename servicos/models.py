from django.db import models
from django.contrib import admin
from clientes.models import Clientes
# Create your models here.




def upload_to(instance, filename):
    return f'servicos_fotos/{instance.servico.cliente.id}/{filename}'

class Servicos(models.Model):
    nome_projeto = models.CharField(max_length=100)
    cliente = models.ForeignKey(Clientes, on_delete=models.CASCADE, related_name='servicos', verbose_name='Cliente')
    data_entrada = models.DateField()
    data_prazo = models.DateField()
    status = models.CharField(max_length=20, choices=[('aguardando servico', 'Aguardando Serviço'), ('em andamento', 'Em Andamento'),
                                                    ('secagem', 'Secagem'), ('polimento', 'Polimento'),('vistoria', 'Vistoria'), ('finalizado', 'Finalizado'), ('entregue', 'Entregue')])
    prioridade = models.CharField(max_length=20, choices=[('baixa', 'Baixa'), ('media', 'Média'), ('alta', 'Alta')])
    descricao = models.TextField()
    material_adicional = models.TextField(blank=True, null=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    quem_recebeu = models.CharField(max_length=100)
    aprovacao = models.BooleanField(default=False)
    data_entrega = models.DateField(blank=True, null=True)
    quem_retirou = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = "Serviço"
        verbose_name_plural = "Serviços"

    def __str__(self):
        return f'Serviço {self.id} - {self.cliente.nome}'
    
class ServicosFotos(models.Model):
    servico = models.ForeignKey(Servicos, on_delete=models.CASCADE, related_name='fotos')
    foto = models.ImageField(upload_to=upload_to)
    data_upload = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Foto do Serviço {self.servico.id} - {self.servico.cliente.nome}'