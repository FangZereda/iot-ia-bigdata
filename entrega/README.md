# Pipeline de Dados IoT - Temperatura

Repositório para entrega do trabalho de IoT e Big Data - UniFECAP.

## Projeto

Pipeline de dados para processar leituras de temperatura de dispositivos IoT, armazenar em PostgreSQL e visualizar via dashboard Streamlit.

## Tecnologias

- Python 3.x
- PostgreSQL (Docker)
- Docker
- Streamlit
- SQLAlchemy
- Plotly
- Pandas

## Estrutura

```
entrega/
├── src/
│   └── dashboard.py      # Script Python (processamento + dashboard)
├── data/
│   └── IOT-temp.csv   # Base de dados de temperaturas IoT
├── docs/
│   └── views.sql      # Views SQL para consulta
├── docker/
│   └── Dockerfile.postgres  # Configuração Docker PostgreSQL
├── README.md
└── requirements.txt
```

## Pré-requisitos

- Python 3.8+
- Docker Desktop

## Instalação

```bash
# Criar ambiente virtual
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Instalar dependências
pip install -r requirements.txt
```

## Banco de Dados (Docker)

```bash
# Criar container PostgreSQL
docker run --name postgres-iot -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres

# Criar banco de dados
docker exec -it postgres-iot psql -U postgres -c "CREATE DATABASE iot_db;"
```

## Execução

```bash
streamlit run src/dashboard.py
```

Dashboard disponível em: http://localhost:8501

## Base de Dados

**Fonte**: Smart Room Temperature Dataset

**Link Kaggle**: https://www.kaggle.com/datasets/ranikay/smart-room-temperature

**Descrição**: Dados de temperatura coletados de salas com sensores IoT, contendo:
- room_id: Identificação da sala
- noted_date: Data e hora da leitura
- temp: Temperatura em graus Celsius
- out/in: Localização (Inside/Outside)

## Views SQL

### 1. avg_temp_por_local
Temperatura média por sala (room_id)
```sql
SELECT room_id, AVG(temperature) as avg_temp
FROM temperature_logs
GROUP BY room_id;
```

### 2. leituras_por_hora
Contagem de leituras por hora do dia
```sql
SELECT EXTRACT(HOUR FROM TO_TIMESTAMP(noted_date, 'DD-MM-YYYY HH24:MI')) as hora, 
       COUNT(*) as contagem
FROM temperature_logs
GROUP BY hora;
```

### 3. temp_max_min_por_dia
Temperaturas máximas e mínimas por dia
```sql
SELECT TO_DATE(...) as data, 
       MAX(temperature) as temp_max, 
       MIN(temperature) as temp_min
FROM temperature_logs
GROUP BY data;
```

## Capturas de Tela do Dashboard

### Visualização 1: Média de Temperatura por Local
![ Média por Sala](docs/captura1.png)

### Visualização 2: Leituras por Hora
![ Leituras por Hora](docs/captura2.png)

### Visualização 3: Temperaturas Máximas e Mínimas por Dia
![ Temp Max Min](docs/captura3.png)

## Comandos Git

```bash
# Inicializar repositório
git init

# Adicionar arquivos
git add .

# Criar commit
git commit -m "Projeto Pipeline IoT"

# Adicionar remote
git remote add origin https://github.com/FangZereda/iot-ia-bigdata.git

# Enviar para GitHub
git push -u origin master

# Atualizar repositório local
git pull origin master
```

##Insights dos Dados

1. Temperatura média na Sala Admin: ~35°C
2. Horários com maior atividade: 5h, 6h e 9h
3. Variação térmica diária: 27°C a 35°C

## Licença

MIT