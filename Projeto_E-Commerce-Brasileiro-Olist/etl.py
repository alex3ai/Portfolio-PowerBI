import pandas as pd
from sqlalchemy import create_engine
#(import glob) apenas quando precisar enontrar diversos arquivos_ 
#_idênticos que não precisam de mapeamento de nome".

# Crie a "engine" de conexão com o seu banco PostgreSQL
# Formato: 'postgresql://usuario:senha@localhost:porta/nome_do_banco'
# (O usuário padrão é 'postgres' e a porta padrão é 5432)
engine = create_engine('postgresql://postgres:admin@localhost:5432/ecommerce_db')
print("Script executado com sucesso!")
print("Bibliotecas importadas e engine criada.")

arquivos_para_tabelas = {
    'olist_customers_dataset': 'customers',
    'olist_orders_dataset': 'orders',
    'olist_order_items_dataset': 'order_items',
    'olist_geolocation_dataset': 'geolocation',
    'olist_order_payments_dataset': 'order_payments',
    'olist_order_reviews_dataset': 'order_reviews',
    'olist_products_dataset': 'products',
    'olist_sellers_dataset': 'sellers',
    'product_category_name_translation': 'product_category_name_translation'
    # Adicione os outros (products, sellers, etc.)
}

caminho_dados = r'C:\Users\alex_\Desktop\PE33\Projetos PE33\Projeto 2\data' # Pasta onde estão os CSVs
print('Sucesso!!!')

print("Iniciando processo de ETL...")

for nome_arquivo, nome_tabela in arquivos_para_tabelas.items():
    print(f"Processando {nome_arquivo} -> {nome_tabela}...")

    # --- EXTRACT ---
    df = pd.read_csv(f"{caminho_dados}/{nome_arquivo}.csv")

    # --- TRANSFORM ---
    # 1. Simples: Apenas para garantir, removemos colunas "Unnamed" se existirem
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

    # 2. Crucial: Converter colunas de data/hora (que são texto no CSV)
    # Identificamos colunas que terminam com '_timestamp' ou '_date'
    colunas_data = [col for col in df.columns if 'timestamp' in col or '_date' in col]
    for col in colunas_data:
        df[col] = pd.to_datetime(df[col], errors='coerce') # 'coerce' transforma erros em Nulo (NaT)

    # --- LOAD ---
    # Usamos df.to_sql para carregar o DataFrame na tabela SQL
    df.to_sql(
        nome_tabela,
        engine,
        if_exists='replace', # 'append' adiciona os dados. (Use 'replace' se você não criou as tabelas no Passo 2)
        index=False        # Não queremos o índice do Pandas no SQL
    )

print("Processo de ETL concluído com sucesso!")