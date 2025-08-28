from django.db import models

# Create your models here.
class Clientes(models.Model):
    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
    nome = models.CharField(max_length=100)
    endereco = models.CharField(max_length=255)
    cep = models.CharField(max_length=10)
    cpf = models.CharField(max_length=14)
    email = models.EmailField(max_length=100, unique=True)
    telefone = models.CharField(max_length=15)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=12, choices=[('em aberto', 'Em Aberto'), ('Finalizado', 'Finalizado')], default='Em andamento')
    data_atualizacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome