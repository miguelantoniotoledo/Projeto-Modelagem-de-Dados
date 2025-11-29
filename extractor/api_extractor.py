import pyodbc
import pandas as pd
import requests

def extrair_dados_banco():

    # --- DADOS DE CONEXÃO ---
    server = input('Digite o local do seu banco (localhost eh permitido)')
    database = input('Digite o nome do seu database')
    username = input('Digite o nome do seu usuário do banco de dados')
    password = input('Digite a senha do banco de dados')
    versaodriver = input('Digite a versao do driver SQL Server') 
    driver = '{ODBC Driver ' & versaodriver & ' for SQL Server}' # driver padrao da minha maquina, trocar caso necessario

    # String de conexão
    conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password};TrustServerCertificate=yes'

    # 1. Definir a consulta SQL (Top 10 Clientes por Valor Total)
    sql_query = """
    SELECT 
        pr.pk_produto,
        pr.nm_produto
    FROM dim_produtos pr;
    """

    try:
        # 2. Conectar e executar a consulta
        conn = pyodbc.connect(conn_str)
        print("Conexão com o SQL Server estabelecida com sucesso!")
        
        df_produtos = pd.read_sql_query(sql_query, conn)

        # 3. Exibir os resultados
        print("\n## 📈 Dados extraidos")
        print(df_produtos)


    except pyodbc.Error as e:
        # Tratar erros de conexão ou driver
        sqlstate = e.args[0]
        print(f"\n❌ ERRO DE CONEXÃO ou EXECUÇÃO SQL:")
        print(f"SQLSTATE: {sqlstate}")
        print(f"Detalhes do erro: {e}")
        print("\nVerifique se:")
        print("* O SQL Server está ativo em 'localhost'.")
        print("* O banco 'dw_northwind' existe.")
        print("* O usuário 'sa' e a senha estão corretos.")
        print(f"* O driver '{driver}' está instalado no seu sistema.")

    finally:
        if 'conn' in locals() and conn:
            conn.close()
            print("\nConexão com o banco de dados fechada.")

def buscar_produto(nome_produto, site_id='MLB'):
    # buscar produto aqui, colocar a funcao
    return None # colocar o retorno correto

def inserir_dw():
    return None