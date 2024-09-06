from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import sqlite3
import requests
import pandas as pd
import os

###########################################################################


# Garantir que os diretórios existam
os.makedirs('camada_bronze', exist_ok=True)
os.makedirs('camada_prata', exist_ok=True)
os.makedirs('camada_ouro', exist_ok=True)

argumentos_padrao = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Criar banco de dados SQLite
database = '/home/dente/breweries.db'
conn = sqlite3.connect(database)

# Criar a tabela breweries_table
with conn:
    conn.execute('''
        CREATE TABLE IF NOT EXISTS breweries_table (
            brewery_type TEXT,
            location TEXT,
            count INTEGER
        )
    ''')

def buscar_dados_cervejaria(**kwargs):
    url = 'https://api.openbrewerydb.org/breweries'
    try:
        resposta = requests.get(url)
        resposta.raise_for_status()
        dados = resposta.json()
        return dados
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Erro ao buscar dados: {e}")

def transformar_dados(**kwargs):
    ti = kwargs['ti']
    dados = ti.xcom_pull(task_ids='buscar_dados_cervejaria')
    df = pd.DataFrame(dados)
    df.to_parquet('camada_bronze/dados_parquet.parquet', index=False)
    df['localizacao'] = df['city'] + ', ' + df['state']
    df.to_parquet('camada_prata/dados_parquet_por_localizacao.parquet', index=False)
    df_agregado = df.groupby(['brewery_type', 'localizacao']).size().reset_index(name='contagem')
    df_agregado.to_parquet('camada_ouro/cervejarias_agregadas.parquet', index=False)

def carregar_dados_para_camada_ouro(**kwargs):
    conn = sqlite3.connect(database)
    df = pd.read_parquet('camada_ouro/cervejarias_agregadas.parquet')
    
    # Inserir dados no SQLite
    df.to_sql('breweries_table', conn, if_exists='replace', index=False)
    conn.close()

with DAG(
    'pipeline_open_brewery_db',
    default_args=argumentos_padrao,
    description='Um DAG para buscar, transformar e carregar dados de cervejarias',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2023, 9, 1),
    catchup=False,
) as dag:

    tarefa_busca = PythonOperator(
        task_id='buscar_dados_cervejaria',
        python_callable=buscar_dados_cervejaria,
    )

    tarefa_transformacao = PythonOperator(
        task_id='transformar_dados',
        python_callable=transformar_dados,
    )

    tarefa_carregamento = PythonOperator(
        task_id='carregar_dados_para_camada_ouro',
        python_callable=carregar_dados_para_camada_ouro,
    )

    tarefa_busca >> tarefa_transformacao >> tarefa_carregamento