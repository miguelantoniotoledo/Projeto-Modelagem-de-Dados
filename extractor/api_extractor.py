import pyodbc
import pandas as pd
import requests
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
import time

def extrair_dados_banco():

    # --- DADOS DE CONEXÃO ---
    # Inicializa DataFrames para garantir retorno mesmo em caso de erro
    df_clientes = pd.DataFrame()
    df_fornecedores = pd.DataFrame()

    server = input('Digite o local do seu banco (localhost eh permitido): ')
    database = input('Digite o nome do seu database: ')
    username = input('Digite o nome do seu usuário do banco de dados: ')
    password = input('Digite a senha do banco de dados: ')
    versaodriver = input('Digite a versao do driver SQL Server: ') 
    driver = f"{{ODBC Driver {versaodriver} for SQL Server}}" # driver padrao da minha maquina, trocar caso necessario
    
    # String de conexão
    conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password};TrustServerCertificate=yes'

    # 1. Definir a consulta SQL 

    sql_query_clientes = """
       SELECT 
        pr.pk_cliente,
        pr.nm_cidade,
        pr.nm_pais
        FROM dim_clientes pr;
       """
    sql_query_fornecedores = """
       SELECT 
        pr.pk_fornecedor,
        pr.nm_cidade,
        pr.nm_pais
        FROM dim_fornecedores pr;
        """
    
    try:
        # 2. Conectar e executar a consulta
        conn = pyodbc.connect(conn_str)
        print("Conexão com o SQL Server estabelecida com sucesso!")
        
        df_clientes = pd.read_sql_query(sql_query_clientes, conn)
        df_fornecedores = pd.read_sql_query(sql_query_fornecedores, conn)

        # 3. Exibir os resultados
        print("\n## 📈 Dados extraidos")
        print(df_clientes)
        print(df_fornecedores)

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

    return df_clientes, df_fornecedores

GEOLOCATOR = Nominatim(user_agent="geocodificador_corporativo_v1")

def geocodificar_dataframe(df1: pd.DataFrame, df2: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Recebe dois DataFrames contendo colunas `nm_cidade` e `nm_pais`,
    adiciona colunas `latitude` e `longitude` em ambos e retorna os dois DataFrames geocodificados.
    """
    def _processar_df(df: pd.DataFrame, label: str) -> pd.DataFrame:
        if df is None or df.empty:
            print(f"⚠️ {label}: DataFrame vazio ou None. Pulando.")
            return df

        df = df.copy()
        df['latitude'] = None
        df['longitude'] = None

        print(f"⏳ [{label}] Iniciando geocodificação para {len(df)} registros...")

        for index, row in df.iterrows():
            cidade = row.get('nm_cidade')
            pais = row.get('nm_pais')
            endereco_completo = f"{cidade}, {pais}"

            try:
                location = GEOLOCATOR.geocode(endereco_completo, timeout=10)

                if location:
                    df.loc[index, 'latitude'] = location.latitude
                    df.loc[index, 'longitude'] = location.longitude

            except (GeocoderTimedOut, GeocoderServiceError) as e:
                print(f"❌ Erro/Timeout na requisição para: {endereco_completo}. Detalhe: {e}")
                if isinstance(e, GeocoderServiceError):
                    print("Interrompendo o processo devido a um erro de serviço.")
                    break

            time.sleep(1)

        print(f"✔️ [{label}] Geocodificação concluída.")
        return df

    df1_geo = _processar_df(df1, 'CLIENTES')
    df2_geo = _processar_df(df2, 'FORNECEDORES')

    return df1_geo, df2_geo

def pipeline_geocodificacao_dados(df_clientes_bruto: pd.DataFrame, df_fornecedores_bruto: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]: 
    print("\n--- 🗺️ Processo de Geocodificação Iniciado ---")
    
    # Processar o DataFrame de Clientes
    print("\n[CLIENTES]")
    # Agora a função recebe ambos os DataFrames e retorna ambos geocodificados
    df_clientes_coordenadas, df_fornecedores_coordenadas = geocodificar_dataframe(
        df_clientes_bruto.copy(), df_fornecedores_bruto.copy()
    )
    
    print("\n--- ✅ Pipeline Concluído ---")
    return df_clientes_coordenadas, df_fornecedores_coordenadas

def inserir_dw(df_clientes_geo=None, df_fornecedores_geo=None):

    def _obter_conexao():
        server = input('Digite o local do seu banco (localhost eh permitido): ')
        database = input('Digite o nome do seu database: ')
        username = input('Digite o nome do seu usuário do banco de dados: ')
        password = input('Digite a senha do banco de dados: ')
        versaodriver = input('Digite a versao do driver SQL Server (ex: 18): ')
        driver = f'{{ODBC Driver {versaodriver} for SQL Server}}'
        conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password};TrustServerCertificate=yes'
        return pyodbc.connect(conn_str)

    # If not provided, extract and geocode
    if df_clientes_geo is None or df_fornecedores_geo is None:
        print('\nNão foram fornecidos DataFrames. Irei extrair e geocodificar automaticamente.')
        df_clientes, df_fornecedores = extrair_dados_banco()
        df_clientes_geo, df_fornecedores_geo = pipeline_geocodificacao_dados(df_clientes, df_fornecedores)
    else:
        df_clientes_geo = df_clientes_geo.copy()
        df_fornecedores_geo = df_fornecedores_geo.copy()

    # Validar se existem colunas necessárias
    if df_clientes_geo is None or df_clientes_geo.empty:
        print('⚠️ DataFrame de clientes vazio. Nada a inserir/atualizar para clientes.')
    if df_fornecedores_geo is None or df_fornecedores_geo.empty:
        print('⚠️ DataFrame de fornecedores vazio. Nada a inserir/atualizar para fornecedores.')

    try:
        conn = _obter_conexao()
        cursor = conn.cursor()

        # Atualizar clientes
        if df_clientes_geo is not None and not df_clientes_geo.empty:
            # Preparar tuplas (latitude, longitude, pk_cliente)
            if 'pk_cliente' not in df_clientes_geo.columns:
                raise KeyError("Coluna 'pk_cliente' não encontrada no DataFrame de clientes.")

            clientes_params = []
            for _, row in df_clientes_geo.iterrows():
                pk = row.get('pk_cliente')
                lat = row.get('latitude') if 'latitude' in row.index else None
                lon = row.get('longitude') if 'longitude' in row.index else None
                clientes_params.append((lat, lon, pk))

            update_clientes_sql = "UPDATE dim_clientes SET latitude = ?, longitude = ? WHERE pk_cliente = ?;"
            cursor.executemany(update_clientes_sql, clientes_params)
            conn.commit()
            print(f"✔️ Atualizados {len(clientes_params)} registros em 'dim_clientes'.")

        # Atualizar fornecedores
        if df_fornecedores_geo is not None and not df_fornecedores_geo.empty:
            if 'pk_fornecedor' not in df_fornecedores_geo.columns:
                raise KeyError("Coluna 'pk_fornecedor' não encontrada no DataFrame de fornecedores.")

            fornecedores_params = []
            for _, row in df_fornecedores_geo.iterrows():
                pk = row.get('pk_fornecedor')
                lat = row.get('latitude') if 'latitude' in row.index else None
                lon = row.get('longitude') if 'longitude' in row.index else None
                fornecedores_params.append((lat, lon, pk))

            update_fornecedores_sql = "UPDATE dim_fornecedores SET latitude = ?, longitude = ? WHERE pk_fornecedor = ?;"
            cursor.executemany(update_fornecedores_sql, fornecedores_params)
            conn.commit()
            print(f"✔️ Atualizados {len(fornecedores_params)} registros em 'dim_fornecedores'.")

    except pyodbc.Error as e:
        print('\n❌ Erro ao conectar/atualizar o banco de dados:')
        print(e)
    except Exception as e:
        print('\n❌ Erro inesperado:')
        print(e)
    finally:
        try:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals() and conn:
                conn.close()
                print('\nConexão com o banco de dados encerrada.')
        except Exception:
            pass