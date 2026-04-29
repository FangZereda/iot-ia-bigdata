-- Média de temperatura por local (sala)
CREATE OR REPLACE VIEW avg_temp_por_local AS
SELECT room_id, AVG(temperature) as avg_temp
FROM temperature_logs
GROUP BY room_id;

-- Contagem de leituras por hora do dia
CREATE OR REPLACE VIEW leituras_por_hora AS
SELECT EXTRACT(HOUR FROM TO_TIMESTAMP(noted_date, 'DD-MM-YYYY HH24:MI')) as hora, COUNT(*) as contagem
FROM temperature_logs
GROUP BY EXTRACT(HOUR FROM TO_TIMESTAMP(noted_date, 'DD-MM-YYYY HH24:MI'))
ORDER BY hora;

-- Temperaturas máximas e mínimas por dia
CREATE OR REPLACE VIEW temp_max_min_por_dia AS
SELECT TO_DATE(SUBSTRING(noted_date FROM 7 FOR 4) || '-' || SUBSTRING(noted_date FROM 4 FOR 2) || '-' || SUBSTRING(noted_date FROM 1 FOR 2), 'YYYY-MM-DD') as data, 
       MAX(temperature) as temp_max, 
       MIN(temperature) as temp_min
FROM temperature_logs
GROUP BY TO_DATE(SUBSTRING(noted_date FROM 7 FOR 4) || '-' || SUBSTRING(noted_date FROM 4 FOR 2) || '-' || SUBSTRING(noted_date FROM 1 FOR 2), 'YYYY-MM-DD')
ORDER BY data;

-- Estatísticas por localização (In/Out)
CREATE OR REPLACE VIEW temp_por_localizacao AS
SELECT location_type, 
       AVG(temperature) as avg_temp,
       MAX(temperature) as temp_max,
       MIN(temperature) as temp_min,
       COUNT(*) as total_leituras
FROM temperature_logs
GROUP BY location_type;

-- Temperatura média por dia
CREATE OR REPLACE VIEW temp_media_por_dia AS
SELECT TO_DATE(SUBSTRING(noted_date FROM 7 FOR 4) || '-' || SUBSTRING(noted_date FROM 4 FOR 2) || '-' || SUBSTRING(noted_date FROM 1 FOR 2), 'YYYY-MM-DD') as data, 
       AVG(temperature) as temp_media
FROM temperature_logs
GROUP BY TO_DATE(SUBSTRING(noted_date FROM 7 FOR 4) || '-' || SUBSTRING(noted_date FROM 4 FOR 2) || '-' || SUBSTRING(noted_date FROM 1 FOR 2), 'YYYY-MM-DD')
ORDER BY data;

-- Contagem por sala e localização
CREATE OR REPLACE VIEW contagem_por_localizacao AS
SELECT room_id, location_type, COUNT(*) as total
FROM temperature_logs
GROUP BY room_id, location_type;