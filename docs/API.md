# Documentação da API - OAtelierWebDjango

## Visão Geral

O OAtelierWebDjango utiliza o Django Admin como interface principal para gerenciamento de dados. Esta documentação descreve as funcionalidades disponíveis através da interface administrativa e possíveis extensões para APIs REST.

## Interface Administrativa (Django Admin)

### Acesso
- **URL**: `/admin/`
- **Autenticação**: Requer superusuário ou usuário com permissões administrativas

### Módulos Disponíveis

#### 1. Clientes

**Modelo**: `clientes.Clientes`

**Funcionalidades**:
- Listagem de todos os clientes
- Criação de novos clientes
- Edição de dados existentes
- Exclusão de clientes
- Filtros por status, data de cadastro
- Busca por nome, email, telefone
- Exportação de dados (CSV, XLSX)

**Campos**:
- `nome`: Nome completo do cliente
- `endereco`: Endereço completo
- `cep`: CEP
- `cpf`: CPF (formato: XXX.XXX.XXX-XX)
- `email`: Email (único)
- `telefone`: Telefone
- `data_cadastro`: Data de cadastro (automático)
- `status`: Status do cliente (Em Aberto/Finalizado)
- `data_atualizacao`: Data de atualização (automático)

#### 2. Serviços

**Modelos**: `servicos.Servicos`, `servicos.ServicosFotos`

**Funcionalidades**:
- Gestão completa de serviços
- Upload de fotos do progresso
- Controle de status e prioridades
- Relacionamento com clientes
- Acompanhamento de prazos

**Campos do Serviço**:
- `nome_projeto`: Nome do projeto
- `cliente`: Relacionamento com cliente
- `data_entrada`: Data de entrada
- `data_prazo`: Prazo de entrega
- `status`: Status do serviço
- `prioridade`: Prioridade (Baixa/Média/Alta)
- `descricao`: Descrição detalhada
- `material_adicional`: Materiais adicionais
- `valor`: Valor do serviço
- `quem_recebeu`: Responsável pelo recebimento
- `aprovacao`: Aprovação do cliente
- `data_entrega`: Data de entrega
- `quem_retirou`: Quem retirou o serviço

**Campos das Fotos**:
- `servico`: Relacionamento com serviço
- `foto`: Upload de imagem
- `data_upload`: Data do upload (automático)

#### 3. Financeiro

**Modelos**: `financeiro.Entrada`, `financeiro.Saida`, `financeiro.ContaPagar`, `financeiro.ContaReceber`

**Funcionalidades**:
- Controle de fluxo de caixa
- Gestão de contas a pagar e receber
- Categorização de movimentações
- Relatórios financeiros

**Entradas**:
- `descricao`: Descrição da entrada
- `valor`: Valor recebido
- `data`: Data da entrada
- `categoria`: Categoria da receita
- `recebido_por`: Quem recebeu

**Saídas**:
- `descricao`: Descrição da saída
- `valor`: Valor pago
- `data`: Data da saída
- `categoria`: Categoria da despesa
- `pago_por`: Quem pagou

**Contas a Pagar**:
- `descricao`: Descrição da conta
- `documento`: Número do documento
- `valor`: Valor a pagar
- `data_vencimento`: Data de vencimento
- `categoria`: Categoria
- `pago`: Status de pagamento

**Contas a Receber**:
- `descricao`: Descrição da conta
- `documento`: Número do documento
- `valor`: Valor a receber
- `data_vencimento`: Data de vencimento
- `categoria`: Categoria
- `recebido`: Status de recebimento

#### 4. Estoque e Ferramentas

**Modelos**: `estoque.*`, `ferramentas.*`

**Funcionalidades**:
- Controle de materiais
- Gestão de ferramentas
- Inventário
- Status de disponibilidade

## Extensões para API REST

### Estrutura Proposta

Para implementar uma API REST completa, considere a seguinte estrutura:

#### 1. Instalação de Dependências

```bash
pip install djangorestframework
pip install django-cors-headers
```

#### 2. Configuração no settings.py

```python
INSTALLED_APPS = [
    # ... apps existentes
    'rest_framework',
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    # ... outros middlewares
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}
```

#### 3. Serializers

**clientes/serializers.py**:
```python
from rest_framework import serializers
from .models import Clientes

class ClientesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clientes
        fields = '__all__'
        read_only_fields = ('data_cadastro', 'data_atualizacao')
```

**servicos/serializers.py**:
```python
from rest_framework import serializers
from .models import Servicos, ServicosFotos

class ServicosFotosSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServicosFotos
        fields = '__all__'

class ServicosSerializer(serializers.ModelSerializer):
    fotos = ServicosFotosSerializer(many=True, read_only=True)
    cliente_nome = serializers.CharField(source='cliente.nome', read_only=True)
    
    class Meta:
        model = Servicos
        fields = '__all__'
```

#### 4. ViewSets

**clientes/views.py**:
```python
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Clientes
from .serializers import ClientesSerializer

class ClientesViewSet(viewsets.ModelViewSet):
    queryset = Clientes.objects.all()
    serializer_class = ClientesSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status']
    search_fields = ['nome', 'email', 'telefone']
    ordering_fields = ['nome', 'data_cadastro']
    ordering = ['-data_cadastro']
```

#### 5. URLs da API

**oatelier_django/urls.py**:
```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from clientes.views import ClientesViewSet
from servicos.views import ServicosViewSet

router = DefaultRouter()
router.register(r'clientes', ClientesViewSet)
router.register(r'servicos', ServicosViewSet)

urlpatterns = [
    # ... URLs existentes
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]
```

### Endpoints da API

#### Clientes

- `GET /api/clientes/` - Listar clientes
- `POST /api/clientes/` - Criar cliente
- `GET /api/clientes/{id}/` - Detalhes do cliente
- `PUT /api/clientes/{id}/` - Atualizar cliente
- `DELETE /api/clientes/{id}/` - Excluir cliente

**Filtros**:
- `?status=em_aberto` - Filtrar por status
- `?search=joão` - Buscar por nome, email ou telefone
- `?ordering=nome` - Ordenar por campo

#### Serviços

- `GET /api/servicos/` - Listar serviços
- `POST /api/servicos/` - Criar serviço
- `GET /api/servicos/{id}/` - Detalhes do serviço
- `PUT /api/servicos/{id}/` - Atualizar serviço
- `DELETE /api/servicos/{id}/` - Excluir serviço

**Filtros**:
- `?cliente={id}` - Filtrar por cliente
- `?status=em_andamento` - Filtrar por status
- `?data_entrada__gte=2025-01-01` - Filtrar por data

#### Financeiro

- `GET /api/entradas/` - Listar entradas
- `GET /api/saidas/` - Listar saídas
- `GET /api/contas-pagar/` - Listar contas a pagar
- `GET /api/contas-receber/` - Listar contas a receber

### Autenticação

#### Token Authentication

```python
# settings.py
INSTALLED_APPS = [
    # ...
    'rest_framework.authtoken',
]

# Comando para criar tokens
python manage.py shell
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
user = User.objects.get(username='admin')
token = Token.objects.create(user=user)
print(token.key)
```

#### Uso do Token

```bash
curl -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b" \
     http://localhost:8000/api/clientes/
```

### Documentação Automática

#### drf-yasg (Swagger)

```bash
pip install drf-yasg
```

**settings.py**:
```python
INSTALLED_APPS = [
    # ...
    'drf_yasg',
]
```

**urls.py**:
```python
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="OAtelier API",
        default_version='v1',
        description="API para sistema de gestão de ateliê",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    # ... outras URLs
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0)),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0)),
]
```

## Exemplos de Uso

### JavaScript (Fetch API)

```javascript
// Listar clientes
fetch('/api/clientes/', {
    headers: {
        'Authorization': 'Token seu-token-aqui',
        'Content-Type': 'application/json',
    }
})
.then(response => response.json())
.then(data => console.log(data));

// Criar cliente
fetch('/api/clientes/', {
    method: 'POST',
    headers: {
        'Authorization': 'Token seu-token-aqui',
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        nome: 'João Silva',
        email: 'joao@email.com',
        telefone: '(11) 99999-9999',
        status: 'em_aberto'
    })
})
.then(response => response.json())
.then(data => console.log(data));
```

### Python (requests)

```python
import requests

# Configuração
base_url = 'http://localhost:8000/api'
headers = {
    'Authorization': 'Token seu-token-aqui',
    'Content-Type': 'application/json'
}

# Listar clientes
response = requests.get(f'{base_url}/clientes/', headers=headers)
clientes = response.json()

# Criar serviço
novo_servico = {
    'nome_projeto': 'Mesa de Jantar',
    'cliente': 1,
    'data_entrada': '2025-01-15',
    'data_prazo': '2025-02-15',
    'status': 'em_andamento',
    'valor': '1500.00'
}

response = requests.post(f'{base_url}/servicos/', 
                        json=novo_servico, 
                        headers=headers)
```

## Considerações de Segurança

1. **Autenticação**: Sempre use autenticação para APIs
2. **Permissões**: Configure permissões adequadas
3. **Validação**: Valide todos os dados de entrada
4. **Rate Limiting**: Implemente limitação de taxa
5. **HTTPS**: Use HTTPS em produção
6. **CORS**: Configure CORS adequadamente

## Monitoramento e Logs

```python
# settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'api.log',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
```

Esta documentação fornece uma base sólida para implementar e utilizar APIs no sistema OAtelierWebDjango, seguindo as melhores práticas do Django REST Framework.

