# Deploy no Render - Documentação

## 📋 Pré-requisitos

1. Conta no [Render.com](https://render.com)
2. Repositório no GitHub com as alterações

## 🚀 Passos para Deploy

### 1. Criar Web Service no Render

1. Acesse o painel do Render
2. Clique em "New +" → "Web Service"
3. Conecte seu repositório do GitHub
4. Configure os seguintes campos:

**Configurações Básicas:**
- **Name**: `oatelier-web-django` (ou nome de sua preferência)
- **Region**: `Oregon` (ou região mais próxima)
- **Branch**: `main` (ou branch desejada)
- **Runtime**: `Python 3`

**Configurações de Build:**
- **Build Command**: `./build.sh`
- **Start Command**: `gunicorn oatelier_django.wsgi`

### 2. Configurar Variáveis de Ambiente

No painel do Render, adicione as seguintes variáveis de ambiente:

**Obrigatórias:**
```
SECRET_KEY=sua-secret-key-super-secreta-aqui
DEBUG=False
```

**Banco de Dados (PostgreSQL):**
O Render fornece automaticamente a variável `DATABASE_URL` quando você adiciona um banco PostgreSQL.

### 3. Adicionar Banco de Dados PostgreSQL

1. No painel do Render, clique em "New +" → "PostgreSQL"
2. Configure:
   - **Name**: `oatelier-db`
   - **Database**: `oatelier`
   - **User**: `oatelier_user`
3. Após criar, conecte o banco ao seu Web Service

### 4. Deploy

1. Clique em "Create Web Service"
2. O Render irá automaticamente:
   - Executar o build script (`build.sh`)
   - Instalar dependências
   - Coletar arquivos estáticos
   - Executar migrações
   - Iniciar a aplicação

## 🔧 Configurações de Desenvolvimento Local

### Usando SQLite (Recomendado para desenvolvimento)
```bash
# Copie o arquivo de exemplo
cp .env.example .env

# Edite o .env com suas configurações:
SECRET_KEY=sua-secret-key-local
DEBUG=True
DB_ENGINE=sqlite
```

### Usando MySQL (Se necessário)
```bash
# No arquivo .env:
SECRET_KEY=sua-secret-key-local
DEBUG=True
DB_ENGINE=mysql
DB_NAME=nome_do_banco
DB_USER=usuario
DB_PASSWORD=senha
DB_HOST=localhost
DB_PORT=3306
```

## 📝 Comandos Úteis

### Desenvolvimento Local
```bash
# Instalar dependências
pip install -r requirements.txt

# Executar migrações
python manage.py migrate

# Coletar arquivos estáticos
python manage.py collectstatic

# Executar servidor de desenvolvimento
python manage.py runserver
```

### Produção
```bash
# Build (executa automaticamente no Render)
./build.sh

# Iniciar com Gunicorn (executa automaticamente no Render)
gunicorn oatelier_django.wsgi
```

## 🔍 Monitoramento

- **Health Check**: `https://seu-app.onrender.com/health/`
- **Admin**: `https://seu-app.onrender.com/admin/`
- **Dashboard**: `https://seu-app.onrender.com/`

## 🛠️ Solução de Problemas

### Erro de Static Files
Se houver problemas com arquivos estáticos, verifique:
1. `STATIC_ROOT` está configurado
2. WhiteNoise está no MIDDLEWARE
3. `collectstatic` foi executado

### Erro de Database
1. Verifique se o PostgreSQL está conectado
2. Confirme se as migrações foram executadas
3. Verifique a variável `DATABASE_URL`

### Erro 500
1. Verifique os logs no painel do Render
2. Confirme se `DEBUG=False` em produção
3. Verifique as variáveis de ambiente

## 📱 URLs de Exemplo

Após o deploy, seu app estará disponível em URLs como:
- `https://oatelier-web-django.onrender.com/`
- `https://oatelier-web-django.onrender.com/admin/`
- `https://oatelier-web-django.onrender.com/health/`

## 🔐 Segurança

✅ **Implementado:**
- Variáveis de ambiente para dados sensíveis
- DEBUG=False em produção
- HTTPS automático no Render
- Headers de segurança configurados
- WhiteNoise para arquivos estáticos

⚠️ **Importante:**
- Nunca commite arquivos `.env` 
- Use SECRET_KEY forte em produção
- Mantenha dependências atualizadas