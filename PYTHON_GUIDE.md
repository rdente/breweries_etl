PYTHON GUIDE

Este documento é uma preparação do Python no Ubuntu: Utilize `sudo apt-get install python3.9` para instalar o Python.
Após a instalação, instale as bibliotecas:
pyarrow, requests, pandas e fastparquet

Utilize `pip install pyarrow`, `pip install requests`, `pip install pandas` e `pip install fastparquet` no terminal

Para o Airflow, utilize este comando no terminal:

`AIRFLOW_VERSION=2.10.1
PYTHON_VERSION="$(python -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')"
CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"
pip install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"`