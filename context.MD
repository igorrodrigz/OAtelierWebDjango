# Contexto do Projeto OAtelierWebDjango - Melhores Práticas para Cursor

## Visão Geral do Projeto

O **OAtelierWebDjango** é um sistema completo de gestão para ateliês e oficinas de marcenaria, desenvolvido em Django 5.2. O projeto segue as melhores práticas do Django e implementa uma arquitetura modular e escalável.

### Estrutura do Projeto
```
OAtelierWebDjango/
├── oatelier_django/          # Configurações principais do projeto
├── clientes/                 # Módulo de gestão de clientes
├── servicos/                 # Módulo de controle de serviços
├── financeiro/               # Módulo financeiro (entradas, saídas, contas)
├── estoque/                  # Módulo de controle de estoque
├── ferramentas/              # Módulo de gestão de ferramentas
├── usuarios/                 # Módulo de usuários
├── templates/                # Templates HTML
├── static/                   # Arquivos estáticos
├── media/                    # Upload de arquivos
├── docs/                     # Documentação completa
└── context.MD               # Este arquivo
```

## Tecnologias e Dependências

### Stack Principal
- **Django 5.2**: Framework web principal
- **Python 3.12+**: Linguagem de programação
- **SQLite/MySQL**: Banco de dados
- **Pillow**: Processamento de imagens
- **WhiteNoise**: Servir arquivos estáticos
- **Gunicorn**: Servidor WSGI para produção
- **django-import-export**: Exportação de dados

### Dependências (requirements.txt)
```
asgiref==3.8.1
Brotli==1.1.0
Django==5.2
Faker==37.1.0
gunicorn==23.0.0
mysqlclient==2.2.7
packaging==25.0
pillow==11.2.1
python-decouple==3.8
sqlparse==0.5.3
tzdata==2025.2
whitenoise==6.9.0
django-import-export==3.0.0
```

## Arquitetura e Padrões

### Padrão MTV (Django)
- **Models**: Definição da estrutura do banco e lógica de negócio
- **Views**: Processamento de requisições HTTP
- **Templates**: Renderização de HTML

### Princípios de Design
- **DRY (Don't Repeat Yourself)**: Evitar duplicação de código
- **Separation of Concerns**: Separação de responsabilidades
- **Single Responsibility**: Cada classe tem uma responsabilidade
- **Modularidade**: Apps independentes e reutilizáveis

## Módulos do Sistema

### 1. Clientes (`clientes/`)
**Modelo Principal**: `Clientes`
- Dados pessoais completos (nome, endereço, CPF, email, telefone)
- Status de atendimento (em aberto/finalizado)
- Histórico de cadastro e atualizações
- Relacionamento 1:N com serviços

**Funcionalidades**:
- CRUD completo via Django Admin
- Busca e filtros avançados
- Exportação de dados (CSV, XLSX)
- Validação de dados únicos (email)

### 2. Serviços (`servicos/`)
**Modelos**: `Servicos`, `ServicosFotos`
- Registro completo de projetos
- Controle de status (aguardando, em andamento, finalizado, etc.)
- Upload de fotos do progresso
- Controle de prazos e prioridades
- Relacionamento com clientes

**Funcionalidades**:
- Gestão completa de serviços
- Upload de imagens com organização por cliente
- Acompanhamento de status e prazos
- Sistema de aprovação

### 3. Financeiro (`financeiro/`)
**Modelos**: `Entrada`, `Saida`, `ContaPagar`, `ContaReceber`
- Controle de fluxo de caixa
- Gestão de contas a pagar e receber
- Categorização de movimentações
- Relatórios financeiros

### 4. Módulos de Suporte
- **Estoque**: Controle de materiais e inventário
- **Ferramentas**: Gestão de ferramentas e manutenção
- **Usuários**: Sistema de usuários e permissões

## Configurações Importantes

### Settings (`oatelier_django/settings.py`)
- **DEBUG**: Configurado via variável de ambiente
- **SECRET_KEY**: Gerenciada via python-decouple
- **ALLOWED_HOSTS**: Configurado para múltiplos ambientes
- **DATABASES**: Suporte a SQLite (dev) e MySQL (prod)
- **STATIC/MEDIA**: Configuração para arquivos estáticos e uploads
- **MIDDLEWARE**: WhiteNoise para servir arquivos estáticos

### URLs (`oatelier_django/urls.py`)
- **Admin**: `/admin/` - Interface administrativa
- **Dashboard**: `/dashboard/` - Painel principal
- **Index**: `/` - Página inicial
- **Status**: `/status/` - Página de status
- **Gerador**: `/gerador/` - Ferramentas de geração

## Banco de Dados

### Estrutura Principal
```sql
-- Clientes
clientes_clientes (id, nome, endereco, cep, cpf, email, telefone, data_cadastro, status, data_atualizacao)

-- Serviços
servicos_servicos (id, nome_projeto, cliente_id, data_entrada, data_prazo, status, prioridade, descricao, valor, aprovacao, data_entrega, quem_retirou)

-- Fotos dos Serviços
servicos_servicosfotos (id, servico_id, foto, data_upload)

-- Financeiro
financeiro_entrada (id, descricao, valor, data, categoria, recebido_por)
financeiro_saida (id, descricao, valor, data, categoria, pago_por)
financeiro_contapagar (id, descricao, documento, valor, data_vencimento, categoria, pago)
financeiro_contareceber (id, descricao, documento, valor, data_vencimento, categoria, recebido)
```

### Relacionamentos
- `Clientes (1) ←→ (N) Servicos`
- `Servicos (1) ←→ (N) ServicosFotos`

## Melhores Práticas para Desenvolvimento

### 1. Estrutura de Código
```python
# Sempre use docstrings
def minha_funcao(parametro):
    """
    Descrição da função.
    
    Args:
        parametro: Descrição do parâmetro
        
    Returns:
        Descrição do retorno
    """
    pass

# Use type hints quando possível
from typing import List, Optional

def processar_clientes(clientes: List[Clientes]) -> Optional[dict]:
    pass
```

### 2. Models
```python
class MeuModelo(models.Model):
    # Sempre defina verbose_name para campos
    nome = models.CharField(max_length=100, verbose_name="Nome")
    
    # Use choices para campos com opções limitadas
    status = models.CharField(
        max_length=20,
        choices=[
            ('ativo', 'Ativo'),
            ('inativo', 'Inativo'),
        ],
        default='ativo'
    )
    
    # Sempre defina __str__
    def __str__(self):
        return self.nome
    
    # Use Meta para configurações adicionais
    class Meta:
        verbose_name = "Meu Modelo"
        verbose_name_plural = "Meus Modelos"
        ordering = ['nome']
```

### 3. Views
```python
# Prefira Class-Based Views para operações CRUD
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

class ClienteListView(ListView):
    model = Clientes
    template_name = 'clientes/cliente_list.html'
    context_object_name = 'clientes'
    paginate_by = 20
    
    def get_queryset(self):
        return Clientes.objects.filter(status='ativo')

# Use function-based views para lógica simples
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    context = {
        'total_clientes': Clientes.objects.count(),
        'servicos_ativos': Servicos.objects.filter(status='em_andamento').count(),
    }
    return render(request, 'dashboard.html', context)
```

### 4. Templates
```html
<!-- Use extends para herança -->
{% extends 'base.html' %}

<!-- Use blocks para conteúdo dinâmico -->
{% block content %}
    <!-- Sempre use csrf_token em formulários -->
    <form method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit">Salvar</button>
    </form>
{% endblock %}

<!-- Use include para componentes reutilizáveis -->
{% include 'includes/navbar.html' %}
```

### 5. Forms
```python
from django import forms
from .models import Clientes

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Clientes
        fields = ['nome', 'email', 'telefone']
        
    def clean_email(self):
        email = self.cleaned_data['email']
        if Clientes.objects.filter(email=email).exists():
            raise forms.ValidationError("Este email já está cadastrado.")
        return email
```

## Comandos Úteis

### Desenvolvimento
```bash
# Executar servidor
python manage.py runserver

# Criar migrações
python manage.py makemigrations

# Aplicar migrações
python manage.py migrate

# Shell do Django
python manage.py shell

# Criar superusuário
python manage.py createsuperuser

# Coletar arquivos estáticos
python manage.py collectstatic

# Testes
python manage.py test
```

### Produção
```bash
# Verificar configurações
python manage.py check --deploy

# Backup do banco
python manage.py dumpdata > backup.json

# Restaurar backup
python manage.py loaddata backup.json
```

## Padrões de Nomenclatura

### Arquivos e Diretórios
- **Apps**: Nome no plural, minúsculas (`clientes`, `servicos`)
- **Models**: Nome no singular, PascalCase (`Cliente`, `Servico`)
- **Views**: Nome descritivo, snake_case (`cliente_list`, `servico_detail`)
- **Templates**: Nome descritivo, snake_case (`cliente_list.html`)
- **URLs**: Nome descritivo, kebab-case (`cliente-list`, `servico-detail`)

### Variáveis e Funções
- **Variáveis**: snake_case (`nome_cliente`, `data_cadastro`)
- **Funções**: snake_case (`processar_cliente`, `validar_email`)
- **Classes**: PascalCase (`ClienteListView`, `ServicoForm`)
- **Constantes**: UPPER_CASE (`MAX_LENGTH`, `DEFAULT_STATUS`)

## Segurança

### Configurações Importantes
```python
# settings.py
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
```

### Validação de Dados
- Sempre valide dados de entrada
- Use forms do Django para validação
- Sanitize dados antes de salvar
- Use prepared statements (ORM do Django)

## Performance

### Otimizações de Query
```python
# Use select_related para ForeignKey
clientes = Clientes.objects.select_related('cidade').all()

# Use prefetch_related para ManyToMany
servicos = Servicos.objects.prefetch_related('fotos').all()

# Use only() para campos específicos
clientes = Clientes.objects.only('nome', 'email').all()

# Use defer() para excluir campos
servicos = Servicos.objects.defer('descricao').all()
```

### Cache
```python
from django.core.cache import cache

# Cache simples
cache.set('chave', valor, timeout=3600)
valor = cache.get('chave')

# Cache de template
{% load cache %}
{% cache 500 'nome_cache' %}
    <!-- Conteúdo cacheado -->
{% endcache %}
```

## Testes

### Estrutura de Testes
```python
from django.test import TestCase
from django.urls import reverse
from .models import Clientes

class ClienteModelTest(TestCase):
    def setUp(self):
        self.cliente = Clientes.objects.create(
            nome="João Silva",
            email="joao@email.com"
        )
    
    def test_cliente_creation(self):
        self.assertEqual(self.cliente.nome, "João Silva")
        self.assertEqual(self.cliente.email, "joao@email.com")
    
    def test_cliente_str(self):
        self.assertEqual(str(self.cliente), "João Silva")

class ClienteViewTest(TestCase):
    def test_cliente_list_view(self):
        response = self.client.get(reverse('cliente-list'))
        self.assertEqual(response.status_code, 200)
```

## Deploy e Produção

### Configurações de Produção
- **DEBUG = False**
- **ALLOWED_HOSTS** configurado
- **SECRET_KEY** segura
- **DATABASE** MySQL ou PostgreSQL
- **STATIC_ROOT** configurado
- **MEDIA_ROOT** configurado

### Servidores
- **Gunicorn**: Servidor WSGI
- **Nginx**: Proxy reverso
- **MySQL/PostgreSQL**: Banco de dados
- **Redis**: Cache (opcional)

## Extensões Futuras

### APIs REST
- Django REST Framework
- Serializers para modelos
- ViewSets para CRUD
- Autenticação via tokens

### Funcionalidades Adicionais
- Sistema de notificações
- Relatórios avançados
- Dashboard interativo
- Integração com sistemas externos
- App mobile

## Recursos de Aprendizagem

### Documentação Oficial
- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Django Admin](https://docs.djangoproject.com/en/stable/ref/contrib/admin/)

### Comunidade
- [Django Forum](https://forum.djangoproject.com/)
- [Stack Overflow - Django](https://stackoverflow.com/questions/tagged/django)
- [Reddit - Django](https://www.reddit.com/r/django/)

### Ferramentas Recomendadas
- **Django Debug Toolbar**: Para desenvolvimento
- **Django Extensions**: Utilitários úteis
- **Django Crispy Forms**: Formulários bonitos
- **Django Filter**: Filtros avançados

---

**Nota**: Este arquivo serve como contexto para o Cursor AI, fornecendo informações essenciais sobre o projeto para auxiliar no desenvolvimento e manutenção do código. Mantenha este arquivo atualizado conforme o projeto evolui.
