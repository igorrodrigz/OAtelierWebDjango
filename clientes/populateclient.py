import os
import sys
import django

# Adiciona o diretório raiz do projeto ao PYTHONPATH
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configura o ambiente do Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'oatelier_django.settings')
django.setup()

from clientes.models import Clientes
from random import randint, choice
from faker import Faker

fake = Faker()

for _ in range(20):
    Clientes.objects.create(
        nome=fake.name(),
        endereco=fake.address(),
        cep=fake.postcode(),
        cpf=fake.cpf(),
        email=fake.email(),
        telefone=fake.phone_number()
    )
print("Clientes criados!")