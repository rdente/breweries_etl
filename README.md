# breweries_etl

Uma solução ETL automatizada utilizando a API [Open Brewery DB API](https://www.openbrewerydb.org/)

## Preparação do ambiente

breweries_etl foi construído utilizando Ubuntu, uma distribuição do Linux
  

   - Caso utilize o WSL e tenha problemas para executar alguma distro do Linux, alguns requisitos são necessários para instalar e executar uma distro do WSL, recomendo ler o [WSL_GUIDE.md](https://github.com/rdente/breweries_etl/blob/main/WSL_GUIDE.MD) para mais informações


   - Para instalar o Python no ambiente Ubuntu, leia o documento [PYTHON_GUIDE.md ](https://github.com/rdente/breweries_etl/blob/main/PYTHON_GUIDE.md)


   - Configure seu Apache Airflow acompanhando o documento [AIRFLOW_GUIDE.md](https://github.com/rdente/breweries_etl/blob/main/AIRFLOW_GUIDE.md)

O código em Python foi construído localmente utilizando a IDE do Jupyter por ser mais amigável e ter uma interface gráfica

#
## DAG do Airflow (`breweries_dag.py`)

### Descrição

A DAG do Airflow orquestra uma pipeline de dados que busca, transforma e carrega dados de cervejarias (ETL) a partir da API OpenBreweryDB. A DAG é composta por três tarefas principais, orientadas pela medallion architecture:

### Tarefas

1. **`buscar_dados_cervejaria()`**
- **Descrição**: Chama a API OpenBreweryDB para obter dados das cervejarias
- **Saída**: Retorna uma lista de dados das cervejarias

2. **`transformar_dados()`**
- **Descrição**:  
    Transforma os dados brutos para dados estruturados:
  - Cria uma coluna de localização
  - Agrupa os dados por tipo de cervejaria e localização, contando o número de cervejarias em cada grupo
- **Saídas**: Salva os dados em arquivos Parquet nas camadas bronze, prata e ouro

3. **`carregar_dados_para_camada_ouro()`**
- **Descrição**: Carrega os dados transformados em um banco de dados local SQLite, criando uma tabela chamada `breweries_table`


### Configuração do Banco de Dados

A DAG cria um banco de dados SQLite (`/home/user/breweries.db`) e uma tabela `breweries_table` para armazenar os dados das cervejarias.
No caso, estou utilizando o path para a execução em container (`database = '/usr/local/airflow/breweries.db'`)
#

## **Container - Docker**

Para utilizar executar em uma instancia de um container, leia o [CONTAINER_GUIDE.md ](https://github.com/rdente/breweries_etl/blob/main/CONTAINER_GUIDE.md)
#


## Testes unitários (`test_breweries.py`)

### Descrição

Os testes unitários são responsáveis por verificar se as funções da DAG estão funcionando corretamente
Eles são executados usando o módulo `unittest` do Python

### Testes Implementados

1. **`test_buscar_dados_cervejaria`**
- **Descrição**: Verifica se a função `buscar_dados_cervejaria()` retorna uma lista não vazia de dados das cervejarias
- **O que faz**: Usa o `patch` do `unittest.mock` para simular a resposta da API, evitando uma chamada real durante o teste

2. **`test_transformar_dados`**
- **Descrição**: Verifica se o tratamento dos dados está funcionando corretamente, incluindo a adição da coluna de localização e a agregação dos dados
- **O que faz**: Cria um DataFrame de dados de exemplo e simula a transformação, verificando se os resultados esperados são obtidos

3. **`test_carregar_dados_para_camada_ouro`**
- **Descrição**: Verifica se os dados são carregados corretamente no banco de dados SQLite.
- **O que faz**: Cria um DataFrame de dados de exemplo, salvando em um arquivo Parquet (simulando a função original) e verifica se os dados são inseridos corretamente na tabela `breweries_table`

### Execução dos Testes

Para executar os testes unitários, use este comando no terminal:

```bash
python3 -m unittest /home/user/airflow/dags/test_breweries.py
```

## Monitoramento
Configurar alertas por e-mail para falhas de tarefas no arquivo de configuração do Airflow pode ser uma ferramenta aliado ao uso de uma ferramenta em cloud, por exemplo envio de notificações por chat (Teams ou Slack por exemplo) sobre o status das *runs* das pipelines

## Uso de cloud 
 - Usar serviços em nuvem como *AWS S3* ou *Azure Blob* para armazenar os dados. Houve uma tentativa de implementar via Amazon RDS em PostgreSQL, mas a dificuldades de implementação direcionaram para uma ferramenta mais simplificada.
 - Um orquestrador friendly-user na nuvem como o *Data Factory* com seus recursos do ambiente Azure ou o *AWS Glue* da Amazon fica como uma sugestão.
