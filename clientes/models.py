from django.db import models

# Create your models here.
class Clientes(models.Model):
    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
    nome = models.CharField(max_length=100)
    endereco = models.CharField(max_length=255, null=True, blank=True)
    cep = models.CharField(max_length=10, null=True, blank=True)
    cpf_cnpj = models.CharField(max_length=14, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    telefone = models.CharField(max_length=15, null=True, blank=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=12, choices=[('ativo', 'ativo'), ('inativo', 'inativo')], default='ativo')
    data_atualizacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome