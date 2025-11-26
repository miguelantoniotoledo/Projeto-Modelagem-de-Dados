{{ config(
  enabled= true,
  materialized='table'
) }}

SELECT
sup.SupplierID as pk_fornecedor,
sup.CompanyName as nm_fornecedor,
sup.Country as nm_pais,
sup.City as nm_cidade,
COALESCE(sup.Region, 'Sem Regiao') as nm_regiao
FROM {{
    source('northwind','Suppliers')
}} as sup