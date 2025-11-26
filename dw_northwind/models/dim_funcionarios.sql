{{ config(
  enabled= true,
  materialized='table'
) }}

SELECT
DISTINCT
fun.EmployeeID as pk_funcionario,
CONCAT(fun.FirstName,' ',fun.LastName) as nm_funcionario,
DATEDIFF(YEAR,fun.BirthDate,CAST('1998-01-01' AS DATE)) as int_idade, 
DATEDIFF(MONTH,fun.HireDate,CAST('1998-01-01' AS DATE)) as int_meses_tempo_casa,
fun.Title as ds_cargo,
reg.RegionDescription as ds_regiao
FROM {{
    source('northwind','Employees')
}}
as fun
LEFT JOIN {{
    source('northwind','EmployeeTerritories')
}} as fterr
ON fun.EmployeeID = fterr.EmployeeID
LEFT JOIN {{
    source('northwind','Territories')
}} as terr
ON fterr.TerritoryID = terr.TerritoryID
LEFT JOIN {{
    source('northwind','Region')
}} as reg
ON terr.RegionID = reg.RegionID