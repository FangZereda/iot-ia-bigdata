# Pipeline de Dados IoT - Temperatura

Projeto de pipeline de dados para processar leituras de temperatura de dispositivos IoT e armazenar em banco de dados PostgreSQL, com dashboard interativo Streamlit.

## Tecnologias Utilizadas

- Python 3.x
- PostgreSQL
- Docker
- Streamlit
- SQLAlchemy
- Plotly
- Pandas

## Estrutura do Projeto

```
iot-temperatura/
├── data/
│   └── IOT-temp.csv
├── docs/
│   └── views.sql
├── docker/
│   └── Dockerfile.postgres
├── main.py
├── README.md
└── requirements.txt
```

## Pré-requisitos

- Python 3.8+
- Docker Desktop
- PostgreSQL (ou container Docker)

## Instalação

### 1. Clonar o repositório

```bash
git clone https://github.com/FangZereda/iot-ia-bigdata.git
cd iot-temperatura
```

### 2. Criar ambiente virtual

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

### 4. Criar arquivo .env

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=iot_db
DB_USER=postgres
DB_PASSWORD=postgres
```

## Configuração do Banco

```bash
docker run --name postgres-iot -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres
docker exec -it postgres-iot psql -U postgres -c "CREATE DATABASE iot_db;"
```

## Execução

```bash
streamlit run main.py
```

Dashboard disponível em: http://localhost:8501

## Views SQL

### 1. avg_temp_por_local
Temperatura média por sala

### 2. leituras_por_hora
Contagem de leituras por hora

### 3. temp_max_min_por_dia
Temperaturas máximas e mínimas por dia

## Licença

MIT