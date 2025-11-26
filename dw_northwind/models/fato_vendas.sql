{{ config(
  enabled= true,
  materialized='table'
) }}

WITH detalhes as (
SELECT
det.OrderID as pk_venda,
det.ProductID as sk_produto,
det.UnitPrice as flt_valor_unit,
det.Quantity as flt_quantidade,
(det.Quantity * det.UnitPrice) as flt_valor_sem_desconto,
(det.Quantity * det.UnitPrice) - (det.Discount * det.UnitPrice) as flt_valor_final
FROM {{
    source('northwind','Order Details')
}} as det
),

vendas as (
SELECT
ven.OrderID as pk_venda,
ven.CustomerID as sk_cliente,
ven.EmployeeID as sk_funcionario,
ven.Freight as flt_frete,
CAST(ven.OrderDate AS DATE) dt_venda,
ven.ShipCountry as nm_pais_venda
FROM {{
    source('northwind','Orders')
}} as ven
) 

SELECT
vend.pk_venda,
vend.sk_cliente,
vend.sk_funcionario,
FORMAT(vend.dt_venda, 'yyyyMMdd') sk_dt_venda,
COALESCE(vend.nm_pais_venda,'Sem Informacao') as nm_pais_venda,
SUM(det.flt_quantidade) as flt_qnt_produtos,
SUM(det.flt_valor_sem_desconto) as flt_vlr_sem_desconto,
SUM(det.flt_valor_final) AS flt_vlr_sem_frete,
SUM(det.flt_valor_final) + MIN(vend.flt_frete) AS flt_vlr_com_frete
FROM vendas vend
LEFT JOIN detalhes det 
ON vend.pk_venda = det.pk_venda
GROUP BY vend.pk_venda, vend.sk_cliente, vend.sk_funcionario, vend.dt_venda, nm_pais_venda