WITH range_datas AS (
    SELECT
        MIN(orderdate) AS min_data,
        MAX(orderdate) AS max_data
    FROM {{
		source('northwind','Orders')
	}}

),
date_spine AS (
SELECT
    DATEADD(DAY, n.number, rg.min_data) AS date_day 
FROM
    range_datas rg 
CROSS APPLY ( 
    SELECT TOP (DATEDIFF(DAY, rg.min_data, rg.max_data) + 1)
        ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) - 1 AS number
    FROM
        sys.all_columns ac1
    CROSS JOIN
        sys.all_columns ac2
) AS n
)

SELECT
    FORMAT(date_day, 'yyyyMMdd') AS pk_data,
    CAST(date_day AS DATE) AS data_completa,
    YEAR(date_day) AS ano,
    MONTH(date_day) AS mes,
    DAY(date_day) AS dia,
    DATENAME(WEEKDAY, date_day) AS dia_semana,
	DATENAME(MONTH, date_day) AS nome_mes_completo,
	SUBSTRING(DATENAME(MONTH, date_day),0,4) AS nome_mes_abreviado
FROM
    date_spine