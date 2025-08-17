# OAtelierWebDjango - Sistema de Gestão para Ateliê

## Visão Geral

O OAtelierWebDjango é um sistema completo de gestão desenvolvido em Django para ateliês e oficinas de marcenaria. O sistema oferece funcionalidades integradas para gerenciamento de clientes, serviços, controle financeiro, estoque e ferramentas.

## Características Principais

- **Gestão de Clientes**: Cadastro completo com dados pessoais e status de atendimento
- **Controle de Serviços**: Acompanhamento de projetos com fotos, prazos e status
- **Módulo Financeiro**: Controle de entradas, saídas, contas a pagar e receber
- **Gestão de Estoque**: Controle de materiais e ferramentas
- **Interface Administrativa**: Painel Django Admin customizado
- **Upload de Imagens**: Sistema de fotos para acompanhamento de serviços
- **Relatórios**: Exportação de dados via django-import-export

## Tecnologias Utilizadas

- **Django 5.2**: Framework web principal
- **Python 3.12**: Linguagem de programação
- **SQLite/MySQL**: Banco de dados
- **Pillow**: Processamento de imagens
- **WhiteNoise**: Servir arquivos estáticos
- **Gunicorn**: Servidor WSGI para produção
- **django-import-export**: Exportação de dados

## Estrutura do Projeto

```
OAtelierWebDjango/
├── oatelier_django/          # Configurações principais
├── clientes/                 # Módulo de gestão de clientes
├── servicos/                 # Módulo de controle de serviços
├── financeiro/               # Módulo financeiro
├── estoque/                  # Módulo de controle de estoque
├── ferramentas/              # Módulo de gestão de ferramentas
├── usuarios/                 # Módulo de usuários
├── templates/                # Templates HTML
├── static/                   # Arquivos estáticos
├── media/                    # Upload de arquivos
└── docs/                     # Documentação
```

## Instalação e Configuração

### Pré-requisitos

- Python 3.12+
- pip
- Ambiente virtual (recomendado)

### Passos de Instalação

1. **Clone o repositório**
   ```bash
   git clone <url-do-repositorio>
   cd OAtelierWebDjango
   ```

2. **Crie e ative o ambiente virtual**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure as variáveis de ambiente**
   Crie um arquivo `.env` na raiz do projeto:
   ```env
   SECRET_KEY=sua-chave-secreta-aqui
   DEBUG=True
   DATABASE_URL=sqlite:///db.sqlite3
   ```

5. **Execute as migrações**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Crie um superusuário**
   ```bash
   python manage.py createsuperuser
   ```

7. **Execute o servidor de desenvolvimento**
   ```bash
   python manage.py runserver
   ```

## Configuração de Banco de Dados

### SQLite (Desenvolvimento)
O projeto está configurado para usar SQLite por padrão, ideal para desenvolvimento.

### MySQL (Produção)
Para usar MySQL em produção, descomente a configuração no `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT', default='3306'),
    }
}
```

## Módulos do Sistema

### 1. Clientes (`clientes/`)
- Cadastro completo de clientes
- Dados pessoais (nome, endereço, CPF, email, telefone)
- Status de atendimento
- Histórico de cadastro

### 2. Serviços (`servicos/`)
- Registro de projetos e serviços
- Acompanhamento de status (aguardando, em andamento, finalizado, etc.)
- Upload de fotos do progresso
- Controle de prazos e prioridades
- Valores e aprovações

### 3. Financeiro (`financeiro/`)
- **Entradas**: Registro de receitas
- **Saídas**: Controle de despesas
- **Contas a Pagar**: Controle de obrigações
- **Contas a Receber**: Acompanhamento de recebíveis
- Categorização de movimentações

### 4. Estoque (`estoque/`)
- Controle de materiais
- Gestão de inventário
- Alertas de estoque baixo

### 5. Ferramentas (`ferramentas/`)
- Cadastro de ferramentas
- Controle de manutenção
- Status de disponibilidade

## URLs Principais

- **Admin**: `/admin/` - Interface administrativa do Django
- **Dashboard**: `/dashboard/` - Painel principal do sistema
- **Index**: `/` - Página inicial
- **Status**: `/status/` - Página de status do sistema
- **Gerador**: `/gerador/` - Ferramentas de geração de dados

## Comandos Úteis

```bash
# Executar servidor de desenvolvimento
python manage.py runserver

# Criar migrações
python manage.py makemigrations

# Aplicar migrações
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser

# Coletar arquivos estáticos
python manage.py collectstatic

# Shell do Django
python manage.py shell

# Testes
python manage.py test
```

## Deploy em Produção

### Configurações de Produção

1. **Alterar DEBUG para False**
2. **Configurar ALLOWED_HOSTS**
3. **Usar banco de dados MySQL**
4. **Configurar arquivos estáticos**
5. **Usar Gunicorn como servidor WSGI**

### Exemplo de deploy no Render

```yaml
# render.yaml
services:
  - type: web
    name: oatelier-django
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn oatelier_django.wsgi:application
    envVars:
      - key: PYTHON_VERSION
        value: 3.12.0
      - key: SECRET_KEY
        generateValue: true
      - key: DEBUG
        value: false
```

## Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## Suporte

Para suporte e dúvidas, entre em contato através dos canais oficiais do projeto.

---

**Desenvolvido com ❤️ para ateliês e oficinas de marcenaria**

