{{ config(
  enabled= true,
  materialized='table'
) }}

SELECT 
pr.ProductID as pk_produto,
pr.ProductName as nm_produto,
COALESCE(pr.SupplierID, 9999) as sk_fornecedor,
COALESCE(sp.CompanyName, 'Fornecedor Não Cadastrado') as nm_fornecedor,
COALESCE(sp.Region, 'Sem Regiao') as nm_regiao_fornecedor,
COALESCE(cat.CategoryName,'Sem Categoria') as nm_categoria,
COALESCE(pr.UnitPrice,0) as flt_valor,
COALESCE(pr.UnitsInStock,0) as int_estoque
FROM {{
    source('northwind','Products')
    }} as pr
LEFT JOIN {{
    source('northwind','Categories')
    }} as cat 
ON pr.CategoryID = cat.CategoryID
LEFT JOIN {{
    source('northwind','Suppliers')
    }} as sp
ON pr.SupplierID = sp.SupplierID
