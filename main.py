from extractor.api_extractor import (
    extrair_dados_banco,
    pipeline_geocodificacao_dados,
    inserir_dw,
)

def main():
    """
    Função principal que orquestra a extração de dados do banco e 
    a geocodificação usando o pipeline do Geopy.
    """
    print("\n=======================================================")
    print("        INÍCIO DO SCRIPT DE GEOCODIFICAÇÃO DE DADOS")
    print("=======================================================")

    # 1. Chamar a função de extração do banco (Pergunta credenciais ao usuário e retorna DataFrames brutos)
    print("\n--- 🔍 PASSO 1: EXTRAÇÃO DO BANCO DE DADOS ---")
    df_clientes_bruto, df_fornecedores_bruto = extrair_dados_banco()

    # Verifica se os DataFrames foram preenchidos
    if df_clientes_bruto.empty and df_fornecedores_bruto.empty:
        print("\n🚫 Não há dados para processar. Finalizando o script.")
    else:
        # 2. Chamar a função principal de geocodificação (Recebe 2 DataFrames, Devolve 2 DataFrames)
        print("\n--- 🗺️ PASSO 2: GEOCODIFICAÇÃO COM GEOPY ---")
        df_clientes_final, df_fornecedores_final = pipeline_geocodificacao_dados(
            df_clientes_bruto, 
            df_fornecedores_bruto
        )

        # 3. Exibir os resultados finais
        print("\n\n--- 📊 RESULTADOS FINAIS COM COORDENADAS ---")
        
        print("\n## CLIENTES GEOCODIFICADOS (Amostra)")
        if not df_clientes_final.empty:
            print(df_clientes_final.head())
        else:
            print("Nenhum cliente processado.")
            
        print("\n## FORNECEDORES GEOCODIFICADOS (Amostra)")
        if not df_fornecedores_final.empty:
            print(df_fornecedores_final.head())
        else:
            print("Nenhum fornecedor processado.")
        # 4. Gravar/atualizar as coordenadas no banco de dados
        print("\n--- 💾 PASSO 3: GRAVANDO COORDENADAS NO BANCO ---")
        if (df_clientes_final is not None and not df_clientes_final.empty) or (
            df_fornecedores_final is not None and not df_fornecedores_final.empty
        ):
            try:
                inserir_dw(df_clientes_geo=df_clientes_final, df_fornecedores_geo=df_fornecedores_final)
            except Exception as e:
                print(f"❌ Falha ao gravar dados no banco: {e}")
        else:
            print("⚠️ Nenhum dado geocodificado para gravar no banco.")
    print("\n=======================================================")
    print("            SCRIPT FINALIZADO")
    print("=======================================================")

if __name__ == "__main__":
    main()
