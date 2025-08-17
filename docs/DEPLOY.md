# Guia de Deploy e Produção - OAtelierWebDjango

## Visão Geral

Este documento fornece instruções detalhadas para fazer o deploy do sistema OAtelierWebDjango em ambiente de produção, incluindo configurações de segurança, otimizações de performance e monitoramento.

## Pré-requisitos

### Servidor
- **Sistema Operacional**: Ubuntu 20.04+ ou CentOS 8+
- **RAM**: Mínimo 2GB (recomendado 4GB+)
- **CPU**: 2 cores (recomendado 4+)
- **Armazenamento**: 20GB+ de espaço livre
- **Rede**: Acesso à internet para instalação de dependências

### Software
- **Python**: 3.12+
- **Nginx**: Servidor web
- **Gunicorn**: Servidor WSGI
- **MySQL**: Banco de dados (produção)
- **Redis**: Cache e sessões (opcional)
- **Git**: Controle de versão

## Configuração do Ambiente

### 1. Atualização do Sistema

```bash
# Ubuntu/Debian
sudo apt update && sudo apt upgrade -y

# CentOS/RHEL
sudo yum update -y
```

### 2. Instalação do Python

```bash
# Ubuntu/Debian
sudo apt install python3 python3-pip python3-venv -y

# CentOS/RHEL
sudo yum install python3 python3-pip -y
```

### 3. Instalação do Nginx

```bash
# Ubuntu/Debian
sudo apt install nginx -y

# CentOS/RHEL
sudo yum install nginx -y
```

### 4. Instalação do MySQL

```bash
# Ubuntu/Debian
sudo apt install mysql-server -y

# CentOS/RHEL
sudo yum install mysql-server -y

# Configuração inicial
sudo mysql_secure_installation
```

### 5. Instalação do Redis (Opcional)

```bash
# Ubuntu/Debian
sudo apt install redis-server -y

# CentOS/RHEL
sudo yum install redis -y
```

## Configuração do Projeto

### 1. Clone do Repositório

```bash
# Criar diretório para o projeto
sudo mkdir -p /var/www/oatelier
sudo chown $USER:$USER /var/www/oatelier

# Clonar o repositório
cd /var/www/oatelier
git clone <url-do-repositorio> .
```

### 2. Configuração do Ambiente Virtual

```bash
# Criar ambiente virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
pip install gunicorn
```

### 3. Configuração das Variáveis de Ambiente

```bash
# Criar arquivo .env
nano .env
```

**Conteúdo do .env**:
```env
# Configurações do Django
SECRET_KEY=sua-chave-secreta-muito-segura-aqui
DEBUG=False
ALLOWED_HOSTS=seu-dominio.com,www.seu-dominio.com,IP-DO-SERVIDOR

# Configurações do Banco de Dados
DB_ENGINE=django.db.backends.mysql
DB_NAME=oatelier_prod
DB_USER=oatelier_user
DB_PASSWORD=sua-senha-segura
DB_HOST=localhost
DB_PORT=3306

# Configurações de Email (opcional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=seu-email@gmail.com
EMAIL_HOST_PASSWORD=sua-senha-de-app

# Configurações de Cache (opcional)
REDIS_URL=redis://localhost:6379/0
```

### 4. Configuração do Banco de Dados

```bash
# Acessar MySQL
sudo mysql -u root -p

# Criar banco de dados
CREATE DATABASE oatelier_prod CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# Criar usuário
CREATE USER 'oatelier_user'@'localhost' IDENTIFIED BY 'sua-senha-segura';
GRANT ALL PRIVILEGES ON oatelier_prod.* TO 'oatelier_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### 5. Configuração do Django

**settings.py** (produção):
```python
import os
from decouple import config

# Configurações de Segurança
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS').split(',')

# Configuração do Banco de Dados
DATABASES = {
    'default': {
        'ENGINE': config('DB_ENGINE'),
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
    }
}

# Configurações de Arquivos Estáticos
STATIC_ROOT = '/var/www/oatelier/staticfiles'
MEDIA_ROOT = '/var/www/oatelier/media'

# Configurações de Segurança
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Configurações de Sessão
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True

# Configurações de Log
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/var/log/oatelier/django.log',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
```

### 6. Execução das Migrações

```bash
# Ativar ambiente virtual
source venv/bin/activate

# Executar migrações
python manage.py makemigrations
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser

# Coletar arquivos estáticos
python manage.py collectstatic --noinput
```

## Configuração do Gunicorn

### 1. Arquivo de Configuração

```bash
# Criar arquivo de configuração
nano /var/www/oatelier/gunicorn.conf.py
```

**Conteúdo**:
```python
# Configuração do Gunicorn
bind = "127.0.0.1:8000"
workers = 3
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50
timeout = 30
keepalive = 2
preload_app = True
```

### 2. Arquivo de Serviço Systemd

```bash
# Criar arquivo de serviço
sudo nano /etc/systemd/system/oatelier.service
```

**Conteúdo**:
```ini
[Unit]
Description=OAtelier Django Application
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/oatelier
Environment="PATH=/var/www/oatelier/venv/bin"
ExecStart=/var/www/oatelier/venv/bin/gunicorn --config gunicorn.conf.py oatelier_django.wsgi:application
ExecReload=/bin/kill -s HUP $MAINPID
Restart=always

[Install]
WantedBy=multi-user.target
```

### 3. Ativação do Serviço

```bash
# Recarregar systemd
sudo systemctl daemon-reload

# Habilitar serviço
sudo systemctl enable oatelier

# Iniciar serviço
sudo systemctl start oatelier

# Verificar status
sudo systemctl status oatelier
```

## Configuração do Nginx

### 1. Arquivo de Configuração

```bash
# Criar arquivo de configuração
sudo nano /etc/nginx/sites-available/oatelier
```

**Conteúdo**:
```nginx
server {
    listen 80;
    server_name seu-dominio.com www.seu-dominio.com;

    # Redirecionamento para HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name seu-dominio.com www.seu-dominio.com;

    # Configurações SSL
    ssl_certificate /etc/letsencrypt/live/seu-dominio.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/seu-dominio.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;

    # Configurações de Segurança
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;

    # Logs
    access_log /var/log/nginx/oatelier_access.log;
    error_log /var/log/nginx/oatelier_error.log;

    # Arquivos estáticos
    location /static/ {
        alias /var/www/oatelier/staticfiles/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Arquivos de mídia
    location /media/ {
        alias /var/www/oatelier/media/;
        expires 1y;
        add_header Cache-Control "public";
    }

    # Proxy para Gunicorn
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }
}
```

### 2. Ativação do Site

```bash
# Criar link simbólico
sudo ln -s /etc/nginx/sites-available/oatelier /etc/nginx/sites-enabled/

# Remover site padrão
sudo rm /etc/nginx/sites-enabled/default

# Testar configuração
sudo nginx -t

# Recarregar Nginx
sudo systemctl reload nginx
```

## Configuração SSL com Let's Encrypt

### 1. Instalação do Certbot

```bash
# Ubuntu/Debian
sudo apt install certbot python3-certbot-nginx -y

# CentOS/RHEL
sudo yum install certbot python3-certbot-nginx -y
```

### 2. Obtenção do Certificado

```bash
# Obter certificado
sudo certbot --nginx -d seu-dominio.com -d www.seu-dominio.com

# Renovação automática
sudo crontab -e
# Adicionar linha: 0 12 * * * /usr/bin/certbot renew --quiet
```

## Configuração de Backup

### 1. Script de Backup

```bash
# Criar script de backup
nano /var/www/oatelier/backup.sh
```

**Conteúdo**:
```bash
#!/bin/bash

# Configurações
BACKUP_DIR="/var/backups/oatelier"
DATE=$(date +%Y%m%d_%H%M%S)
DB_NAME="oatelier_prod"
DB_USER="oatelier_user"
DB_PASSWORD="sua-senha-segura"

# Criar diretório de backup
mkdir -p $BACKUP_DIR

# Backup do banco de dados
mysqldump -u $DB_USER -p$DB_PASSWORD $DB_NAME > $BACKUP_DIR/db_backup_$DATE.sql

# Backup dos arquivos de mídia
tar -czf $BACKUP_DIR/media_backup_$DATE.tar.gz /var/www/oatelier/media/

# Manter apenas os últimos 7 backups
find $BACKUP_DIR -name "*.sql" -mtime +7 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete

echo "Backup concluído: $DATE"
```

### 2. Configuração de Cron

```bash
# Tornar script executável
chmod +x /var/www/oatelier/backup.sh

# Adicionar ao cron
crontab -e
# Adicionar linha: 0 2 * * * /var/www/oatelier/backup.sh
```

## Monitoramento e Logs

### 1. Configuração de Logs

```bash
# Criar diretório de logs
sudo mkdir -p /var/log/oatelier
sudo chown www-data:www-data /var/log/oatelier

# Configurar rotação de logs
sudo nano /etc/logrotate.d/oatelier
```

**Conteúdo**:
```
/var/log/oatelier/*.log {
    daily
    missingok
    rotate 52
    compress
    delaycompress
    notifempty
    create 644 www-data www-data
}
```

### 2. Monitoramento com Systemd

```bash
# Verificar status dos serviços
sudo systemctl status nginx
sudo systemctl status oatelier
sudo systemctl status mysql
sudo systemctl status redis

# Verificar logs
sudo journalctl -u oatelier -f
sudo journalctl -u nginx -f
```

## Otimizações de Performance

### 1. Configuração do MySQL

```bash
# Editar configuração do MySQL
sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf
```

**Adicionar**:
```ini
[mysqld]
innodb_buffer_pool_size = 1G
innodb_log_file_size = 256M
innodb_flush_log_at_trx_commit = 2
query_cache_size = 64M
query_cache_type = 1
```

### 2. Configuração do Nginx

```bash
# Editar configuração principal do Nginx
sudo nano /etc/nginx/nginx.conf
```

**Otimizações**:
```nginx
http {
    # Configurações de buffer
    client_body_buffer_size 128k;
    client_max_body_size 10m;
    client_header_buffer_size 1k;
    large_client_header_buffers 4 4k;
    
    # Configurações de timeout
    client_body_timeout 12;
    client_header_timeout 12;
    keepalive_timeout 15;
    send_timeout 10;
    
    # Configurações de gzip
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_types
        text/plain
        text/css
        text/xml
        text/javascript
        application/json
        application/javascript
        application/xml+rss
        application/atom+xml
        image/svg+xml;
}
```

## Segurança

### 1. Configuração do Firewall

```bash
# Instalar UFW
sudo apt install ufw -y

# Configurar regras
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 80
sudo ufw allow 443

# Ativar firewall
sudo ufw enable
```

### 2. Configuração de Usuários

```bash
# Criar usuário específico para o aplicativo
sudo adduser oatelier
sudo usermod -aG www-data oatelier

# Configurar permissões
sudo chown -R oatelier:www-data /var/www/oatelier
sudo chmod -R 755 /var/www/oatelier
```

### 3. Atualizações Automáticas

```bash
# Instalar unattended-upgrades
sudo apt install unattended-upgrades -y

# Configurar
sudo dpkg-reconfigure -plow unattended-upgrades
```

## Troubleshooting

### Problemas Comuns

1. **Erro 502 Bad Gateway**
   - Verificar se o Gunicorn está rodando
   - Verificar logs do Nginx e Gunicorn
   - Verificar configuração do proxy

2. **Erro de Permissão**
   - Verificar permissões dos arquivos
   - Verificar usuário do serviço
   - Verificar SELinux (CentOS)

3. **Erro de Banco de Dados**
   - Verificar conexão com MySQL
   - Verificar credenciais no .env
   - Verificar se o banco existe

### Comandos Úteis

```bash
# Verificar status dos serviços
sudo systemctl status oatelier nginx mysql

# Verificar logs
sudo tail -f /var/log/oatelier/django.log
sudo tail -f /var/log/nginx/oatelier_error.log

# Reiniciar serviços
sudo systemctl restart oatelier
sudo systemctl restart nginx

# Verificar portas em uso
sudo netstat -tlnp | grep :80
sudo netstat -tlnp | grep :443
sudo netstat -tlnp | grep :8000
```

## Conclusão

Este guia fornece uma configuração completa e segura para deploy do OAtelierWebDjango em produção. Lembre-se de:

1. **Sempre fazer backup** antes de alterações
2. **Monitorar logs** regularmente
3. **Manter o sistema atualizado**
4. **Testar em ambiente de staging** antes de produção
5. **Documentar alterações** feitas no servidor

Para suporte adicional, consulte a documentação oficial do Django, Nginx e Gunicorn.

