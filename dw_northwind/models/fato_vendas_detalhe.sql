{{ config(
  enabled= true,
  materialized='table'
) }}

SELECT
CONCAT(det.OrderId, '-', det.ProductID) as pk_detalhe, 
det.OrderID as sk_venda,
det.ProductID as sk_produto,
vend.EmployeeID as sk_funcionario,
vend.CustomerID as sk_cliente,
det.UnitPrice as flt_valor_unit,
det.Quantity as flt_quantidade,
(det.Quantity * det.UnitPrice) as flt_valor_sem_desconto,
(det.Quantity * det.UnitPrice) - (det.Discount * det.UnitPrice) as flt_valor_final
FROM 
{{
    source('northwind','Order Details')
}} as det
LEFT JOIN {{
    source('northwind','Orders')
}} as vend
ON det.OrderID = vend.OrderID