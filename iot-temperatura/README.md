# Pipeline de Dados IoT - Temperatura

Projeto de pipeline de dados para processar leituras de temperatura de dispositivos IoT e armazenar em banco de dados PostgreSQL, com dashboard interativo Streamlit.

## Tecnologias Utilizadas

- **Python 3.14**: Linguagem de programação
- **PostgreSQL**: Banco de dados relacional
- **Docker**: Containerização
- **Streamlit**: Framework para dashboards interativos
- **SQLAlchemy**: ORM para conexão com banco de dados
- **Plotly**: Biblioteca de visualização
- **Pandas**: Manipulação de dados

## Estrutura do Projeto

```
trabalho-unifecaf-iot-bigdata/
├── data/
│   └── temperature_readings.csv    # Dataset de temperaturas
├── docs/
│   └── views.sql                  # Views SQL criadas
├── docker/
│   └── Dockerfile.postgres         # Configuração Docker
├── main.py                        # Script principal
├── README.md                      # Este arquivo
└── requirements.txt              # Dependências Python
```

## Pré-requisitos

- Python 3.8 ou superior
- Docker Desktop
- PostgreSQL (ou usar container Docker)

## Instalação

### 1. Clonar o repositório

```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
```

### 2. Criar ambiente virtual

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

Ou instalar individualmente:

```bash
pip install pandas psycopg2-binary sqlalchemy streamlit plotly python-dotenv
```

### 4. Configurar variáveis de ambiente

Crie um arquivo `.env` no diretório raiz:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=iot_db
DB_USER=postgres
DB_PASSWORD=postgres
```

## Configuração do Banco de Dados

### Opção 1: Usar Docker (Recomendado)

```bash
docker run --name postgres-iot -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres
```

### Opção 2: Usar Docker Compose

```bash
docker-compose up -d
```

### 3. Criar banco de dados

Acesse o PostgreSQL e crie o banco:

```bash
docker exec -it postgres-iot psql -U postgres -c "CREATE DATABASE iot_db;"
```

## Execução

### Executar Dashboard Streamlit

```bash
streamlit run main.py
```

O dashboard abrirá em `http://localhost:8501`

## Views SQL Criadas

### 1. avg_temp_por_dispositivo
Calcula a temperatura média por dispositivo IoT.

```sql
SELECT device_id, AVG(temperature) as avg_temp
FROM temperature_logs
GROUP BY device_id;
```

**Propósito**: Identificar qual dispositivo tem a maior/menor temperatura média.

### 2. leituras_por_hora
Conta o número de leituras por hora do dia.

```sql
SELECT EXTRACT(HOUR FROM noted_date::timestamp) as hora, COUNT(*) as contagem
FROM temperature_logs
GROUP BY EXTRACT(HOUR FROM noted_date::timestamp);
```

**Propósito**: Analisar a distribuição de leituras ao longo do dia.

### 3. temp_max_min_por_dia
Mostra temperaturas máximas e mínimas por dia.

```sql
SELECT DATE(noted_date::timestamp) as data, 
       MAX(temperature) as temp_max, 
       MIN(temperature) as temp_min
FROM temperature_logs
GROUP BY DATE(noted_date::timestamp);
```

**Propósito**: Identificar variações diárias de temperatura.

### 4. temp_por_cidade
Estatísticas de temperatura por cidade.

```sql
SELECT city, 
       AVG(temperature) as avg_temp,
       MAX(temperature) as temp_max,
       MIN(temperature) as temp_min,
       COUNT(*) as total_leituras
FROM temperature_logs
GROUP BY city;
```

**Propósito**: Comparar temperaturas entre diferentes localizações.

### 5. leituras_por_dispositivo
Contagem total de leituras por dispositivo.

```sql
SELECT device_id, COUNT(*) as total_leituras
FROM temperature_logs
GROUP BY device_id;
```

**Propósito**: Monitorar atividade de cada dispositivo.

### 6. temp_media_por_dia
Temperatura média por dia.

```sql
SELECT DATE(noted_date::timestamp) as data, 
       AVG(temperature) as temp_media
FROM temperature_logs
GROUP BY DATE(noted_date::timestamp);
```

**Propósito**: Acompanhar tendência de temperatura ao longo do tempo.

## Comandos Git

```bash
# Inicializar repositório
git init

# Adicionar arquivos
git add .

# Criar commit
git commit -m "Projeto inicial: Pipeline de Dados IoT"

# Adicionar remote
git remote add origin https://github.com/usuario/repositorio.git

# Enviar para GitHub
git push -u origin main

# Atualizar repositório local
git pull origin main
```

## Insights dos Dados

1. **Variação térmica diaria**: A temperatura varia significativamente entre dia e noite
2. **Padrão de comportamento**: Dispositivos mostram padrões consistente de temperatura
3. **Monitoramento**: D1 tende a ter temperaturas mais elevadas que D3
4. **Horário de pico**: Maior atividade de leituras em horário comercial

## Deploy

### Render.com

1. Criar conta no Render.com
2. Conectar repositório GitHub
3. Configurar comando: `streamlit run main.py`
4. Definir variáveis de ambiente

## Capturas de Tela

[Adicione capturas de tela do dashboard aqui]

## Licença

MIT License

## Autor

Seu Nome - seu.email@exemplo.com