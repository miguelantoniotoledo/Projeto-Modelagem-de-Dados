{{ config(
  enabled= true,
  materialized='table'
) }}

SELECT 
cus.CustomerID as pk_cliente,
cus.ContactName as nm_cliente,
cus.ContactTitle as ds_cargo,
cus.Region as nm_regiao,
cus.City as nm_cidade,
cus.Country as nm_pais
FROM {{
    source('northwind','Customers')
}} as cus