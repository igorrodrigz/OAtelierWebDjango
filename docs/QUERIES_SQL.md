# Guia de Consultas SQL - OAtelierWebDjango

## Visão Geral

Este documento contém exemplos práticos de consultas SQL para análise de dados do sistema OAtelierWebDjango. As consultas estão organizadas por módulo e funcionalidade.

## Clientes

### Consultas Básicas

#### 1. Listar todos os clientes
```sql
SELECT * FROM clientes_clientes;
```

#### 2. Clientes cadastrados em um período específico
```sql
SELECT 
    nome,
    email,
    telefone,
    data_cadastro,
    status
FROM clientes_clientes 
WHERE data_cadastro BETWEEN '2025-01-01' AND '2025-12-31'
ORDER BY data_cadastro DESC;
```

#### 3. Clientes por status
```sql
SELECT 
    status,
    COUNT(*) as total_clientes
FROM clientes_clientes 
GROUP BY status;
```

#### 4. Buscar clientes por nome, email ou telefone
```sql
SELECT * FROM clientes_clientes 
WHERE nome LIKE '%João%' 
   OR email LIKE '%@gmail.com%' 
   OR telefone LIKE '%9999%';
```

#### 5. Clientes com mais serviços
```sql
SELECT 
    c.nome,
    c.email,
    COUNT(s.id) as total_servicos
FROM clientes_clientes c
LEFT JOIN servicos_servicos s ON c.id = s.cliente_id
GROUP BY c.id, c.nome, c.email
ORDER BY total_servicos DESC;
```

### Análises Avançadas

#### 6. Clientes ativos vs inativos
```sql
SELECT 
    CASE 
        WHEN status = 'em aberto' THEN 'Ativo'
        WHEN status = 'Finalizado' THEN 'Inativo'
        ELSE 'Outro'
    END as status_cliente,
    COUNT(*) as quantidade
FROM clientes_clientes 
GROUP BY status;
```

#### 7. Clientes por mês de cadastro
```sql
SELECT 
    strftime('%Y-%m', data_cadastro) as mes_cadastro,
    COUNT(*) as novos_clientes
FROM clientes_clientes 
GROUP BY mes_cadastro
ORDER BY mes_cadastro DESC;
```

## Serviços

### Consultas Básicas

#### 1. Listar todos os serviços
```sql
SELECT * FROM servicos_servicos;
```

#### 2. Serviços por status
```sql
SELECT 
    status,
    COUNT(*) as total_servicos,
    AVG(valor) as valor_medio
FROM servicos_servicos 
GROUP BY status;
```

#### 3. Serviços de um cliente específico
```sql
SELECT 
    s.nome_projeto,
    s.data_entrada,
    s.data_prazo,
    s.status,
    s.valor,
    c.nome as cliente
FROM servicos_servicos s
JOIN clientes_clientes c ON s.cliente_id = c.id
WHERE c.id = 1
ORDER BY s.data_entrada DESC;
```

#### 4. Serviços em andamento
```sql
SELECT 
    s.nome_projeto,
    c.nome as cliente,
    s.data_entrada,
    s.data_prazo,
    s.valor,
    s.prioridade
FROM servicos_servicos s
JOIN clientes_clientes c ON s.cliente_id = c.id
WHERE s.status = 'em andamento'
ORDER BY s.prioridade DESC, s.data_prazo ASC;
```

### Análises de Performance

#### 5. Serviços por período de entrada
```sql
SELECT 
    strftime('%Y-%m', data_entrada) as mes_entrada,
    COUNT(*) as total_servicos,
    SUM(valor) as valor_total,
    AVG(valor) as valor_medio
FROM servicos_servicos 
GROUP BY mes_entrada
ORDER BY mes_entrada DESC;
```

#### 6. Serviços atrasados
```sql
SELECT 
    s.nome_projeto,
    c.nome as cliente,
    s.data_prazo,
    s.status,
    s.valor,
    julianday('now') - julianday(s.data_prazo) as dias_atraso
FROM servicos_servicos s
JOIN clientes_clientes c ON s.cliente_id = c.id
WHERE s.data_prazo < date('now') 
  AND s.status NOT IN ('finalizado', 'entregue')
ORDER BY dias_atraso DESC;
```

#### 7. Serviços por prioridade
```sql
SELECT 
    prioridade,
    COUNT(*) as total_servicos,
    AVG(valor) as valor_medio,
    SUM(valor) as valor_total
FROM servicos_servicos 
GROUP BY prioridade
ORDER BY 
    CASE prioridade
        WHEN 'alta' THEN 1
        WHEN 'media' THEN 2
        WHEN 'baixa' THEN 3
    END;
```

### Análises Financeiras

#### 8. Valor total de serviços por mês
```sql
SELECT 
    strftime('%Y-%m', data_entrada) as mes,
    COUNT(*) as total_servicos,
    SUM(valor) as valor_total,
    AVG(valor) as valor_medio
FROM servicos_servicos 
GROUP BY mes
ORDER BY mes DESC;
```

#### 9. Serviços aprovados vs não aprovados
```sql
SELECT 
    aprovacao,
    COUNT(*) as total_servicos,
    SUM(valor) as valor_total,
    AVG(valor) as valor_medio
FROM servicos_servicos 
GROUP BY aprovacao;
```

## Financeiro

### Entradas (Receitas)

#### 1. Total de entradas por mês
```sql
SELECT 
    strftime('%Y-%m', data) as mes,
    COUNT(*) as total_entradas,
    SUM(valor) as valor_total,
    AVG(valor) as valor_medio
FROM financeiro_entrada 
GROUP BY mes
ORDER BY mes DESC;
```

#### 2. Entradas por categoria
```sql
SELECT 
    categoria,
    COUNT(*) as total_entradas,
    SUM(valor) as valor_total,
    AVG(valor) as valor_medio
FROM financeiro_entrada 
GROUP BY categoria
ORDER BY valor_total DESC;
```

#### 3. Entradas em um período específico
```sql
SELECT 
    descricao,
    valor,
    data,
    categoria,
    recebido_por
FROM financeiro_entrada 
WHERE data BETWEEN '2025-01-01' AND '2025-12-31'
ORDER BY data DESC;
```

### Saídas (Despesas)

#### 4. Total de saídas por mês
```sql
SELECT 
    strftime('%Y-%m', data) as mes,
    COUNT(*) as total_saidas,
    SUM(valor) as valor_total,
    AVG(valor) as valor_medio
FROM financeiro_saida 
GROUP BY mes
ORDER BY mes DESC;
```

#### 5. Saídas por categoria
```sql
SELECT 
    categoria,
    COUNT(*) as total_saidas,
    SUM(valor) as valor_total,
    AVG(valor) as valor_medio
FROM financeiro_saida 
GROUP BY categoria
ORDER BY valor_total DESC;
```

### Contas a Pagar

#### 6. Contas a pagar pendentes
```sql
SELECT 
    descricao,
    documento,
    valor,
    data_vencimento,
    categoria,
    julianday(data_vencimento) - julianday('now') as dias_vencimento
FROM financeiro_contapagar 
WHERE pago = 0
ORDER BY data_vencimento ASC;
```

#### 7. Contas a pagar vencendo em 30 dias
```sql
SELECT 
    descricao,
    valor,
    data_vencimento,
    categoria
FROM financeiro_contapagar 
WHERE pago = 0 
  AND data_vencimento BETWEEN date('now') AND date('now', '+30 days')
ORDER BY data_vencimento ASC;
```

#### 8. Total de contas pagas vs pendentes
```sql
SELECT 
    CASE 
        WHEN pago = 1 THEN 'Pago'
        ELSE 'Pendente'
    END as status,
    COUNT(*) as total_contas,
    SUM(valor) as valor_total
FROM financeiro_contapagar 
GROUP BY pago;
```

### Contas a Receber

#### 9. Contas a receber pendentes
```sql
SELECT 
    descricao,
    documento,
    valor,
    data_vencimento,
    categoria,
    julianday(data_vencimento) - julianday('now') as dias_vencimento
FROM financeiro_contareceber 
WHERE recebido = 0
ORDER BY data_vencimento ASC;
```

#### 10. Contas a receber vencendo em 30 dias
```sql
SELECT 
    descricao,
    valor,
    data_vencimento,
    categoria
FROM financeiro_contareceber 
WHERE recebido = 0 
  AND data_vencimento BETWEEN date('now') AND date('now', '+30 days')
ORDER BY data_vencimento ASC;
```

## Relatórios Integrados

### Dashboard Financeiro

#### 1. Resumo financeiro mensal
```sql
SELECT 
    strftime('%Y-%m', data) as mes,
    SUM(CASE WHEN tipo = 'entrada' THEN valor ELSE 0 END) as receitas,
    SUM(CASE WHEN tipo = 'saida' THEN valor ELSE 0 END) as despesas,
    SUM(CASE WHEN tipo = 'entrada' THEN valor ELSE -valor END) as saldo
FROM (
    SELECT data, valor, 'entrada' as tipo FROM financeiro_entrada
    UNION ALL
    SELECT data, valor, 'saida' as tipo FROM financeiro_saida
) as movimentacoes
GROUP BY mes
ORDER BY mes DESC;
```

#### 2. Fluxo de caixa projetado
```sql
SELECT 
    'Contas a Receber' as tipo,
    SUM(valor) as valor_total,
    COUNT(*) as quantidade
FROM financeiro_contareceber 
WHERE recebido = 0
UNION ALL
SELECT 
    'Contas a Pagar' as tipo,
    SUM(valor) as valor_total,
    COUNT(*) as quantidade
FROM financeiro_contapagar 
WHERE pago = 0;
```

### Análise de Clientes

#### 3. Top 10 clientes por valor de serviços
```sql
SELECT 
    c.nome,
    c.email,
    COUNT(s.id) as total_servicos,
    SUM(s.valor) as valor_total_servicos,
    AVG(s.valor) as valor_medio_servicos
FROM clientes_clientes c
LEFT JOIN servicos_servicos s ON c.id = s.cliente_id
GROUP BY c.id, c.nome, c.email
ORDER BY valor_total_servicos DESC
LIMIT 10;
```

#### 4. Clientes sem serviços
```sql
SELECT 
    c.nome,
    c.email,
    c.data_cadastro
FROM clientes_clientes c
LEFT JOIN servicos_servicos s ON c.id = s.cliente_id
WHERE s.id IS NULL
ORDER BY c.data_cadastro DESC;
```

### Análise de Performance

#### 5. Tempo médio de conclusão de serviços
```sql
SELECT 
    status,
    COUNT(*) as total_servicos,
    AVG(julianday(data_entrega) - julianday(data_entrada)) as dias_medio_conclusao
FROM servicos_servicos 
WHERE data_entrega IS NOT NULL
GROUP BY status;
```

#### 6. Serviços por prioridade e status
```sql
SELECT 
    prioridade,
    status,
    COUNT(*) as total_servicos,
    AVG(valor) as valor_medio
FROM servicos_servicos 
GROUP BY prioridade, status
ORDER BY prioridade, status;
```

## Consultas de Manutenção

### Limpeza de Dados

#### 1. Identificar registros duplicados
```sql
SELECT 
    email,
    COUNT(*) as total_duplicados
FROM clientes_clientes 
GROUP BY email
HAVING COUNT(*) > 1;
```

#### 2. Serviços sem cliente
```sql
SELECT 
    s.id,
    s.nome_projeto,
    s.data_entrada
FROM servicos_servicos s
LEFT JOIN clientes_clientes c ON s.cliente_id = c.id
WHERE c.id IS NULL;
```

#### 3. Fotos sem serviço
```sql
SELECT 
    sf.id,
    sf.data_upload
FROM servicos_servicosfotos sf
LEFT JOIN servicos_servicos s ON sf.servico_id = s.id
WHERE s.id IS NULL;
```

### Backup e Restauração

#### 4. Backup de dados essenciais
```sql
-- Backup de clientes
SELECT * FROM clientes_clientes;

-- Backup de serviços
SELECT * FROM servicos_servicos;

-- Backup de entradas financeiras
SELECT * FROM financeiro_entrada;

-- Backup de saídas financeiras
SELECT * FROM financeiro_saida;
```

## Dicas de Performance

### 1. Índices Recomendados
```sql
-- Índices para melhorar performance
CREATE INDEX idx_clientes_email ON clientes_clientes(email);
CREATE INDEX idx_clientes_status ON clientes_clientes(status);
CREATE INDEX idx_servicos_cliente ON servicos_servicos(cliente_id);
CREATE INDEX idx_servicos_status ON servicos_servicos(status);
CREATE INDEX idx_servicos_data_entrada ON servicos_servicos(data_entrada);
CREATE INDEX idx_financeiro_data ON financeiro_entrada(data);
CREATE INDEX idx_financeiro_data_saida ON financeiro_saida(data);
```

### 2. Consultas Otimizadas
```sql
-- Use LIMIT para grandes conjuntos de dados
SELECT * FROM clientes_clientes LIMIT 1000;

-- Use índices em WHERE clauses
SELECT * FROM servicos_servicos WHERE status = 'em_andamento' AND cliente_id = 1;

-- Evite SELECT * quando possível
SELECT id, nome, email FROM clientes_clientes WHERE status = 'em_aberto';
```

## Exemplos de Uso no Django

### 1. Usando ORM do Django
```python
from django.db.models import Count, Sum, Avg
from clientes.models import Clientes
from servicos.models import Servicos

# Clientes com mais serviços
clientes_ativos = Clientes.objects.annotate(
    total_servicos=Count('servicos')
).filter(
    status='em_aberto'
).order_by('-total_servicos')

# Valor total de serviços por mês
from django.db.models.functions import TruncMonth

servicos_mensais = Servicos.objects.annotate(
    mes=TruncMonth('data_entrada')
).values('mes').annotate(
    total=Count('id'),
    valor_total=Sum('valor'),
    valor_medio=Avg('valor')
).order_by('-mes')
```

### 2. Raw SQL no Django
```python
from django.db import connection

def executar_consulta_raw():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 
                c.nome,
                COUNT(s.id) as total_servicos,
                SUM(s.valor) as valor_total
            FROM clientes_clientes c
            LEFT JOIN servicos_servicos s ON c.id = s.cliente_id
            GROUP BY c.id, c.nome
            ORDER BY valor_total DESC
        """)
        return cursor.fetchall()
```

---

**Nota**: Estas consultas são exemplos e podem precisar de ajustes dependendo da versão específica do banco de dados e das necessidades do projeto. Sempre teste as consultas em um ambiente de desenvolvimento antes de usar em produção.

