import unittest
import sqlite3
import pandas as pd
from unittest.mock import patch
from breweries_dag import buscar_dados_cervejaria, transformar_dados, carregar_dados_para_camada_ouro  # Substitua 'your_module' pelo nome do seu módulo


class TestBreweryDataPipeline(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Configurações iniciais para os testes
        cls.database = '/home/dente/breweries.db'
        cls.conn = sqlite3.connect(cls.database)
        cls.cursor = cls.conn.cursor()
        cls.cursor.execute('''
            CREATE TABLE IF NOT EXISTS breweries_table (
                brewery_type TEXT,
                location TEXT,
                count INTEGER
            )
        ''')

    @classmethod
    def tearDownClass(cls):
        # Limpar o banco de dados após os testes
        cls.cursor.execute('DROP TABLE IF EXISTS breweries_table')
        cls.conn.close()

    @patch('requests.get')
    def test_buscar_dados_cervejaria(self, mock_get):
        # Simular a resposta da API
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [
            {'brewery_type': 'micro', 'city': 'San Diego', 'state': 'CA'},
            {'brewery_type': 'brewpub', 'city': 'Los Angeles', 'state': 'CA'},
        ]
        
        dados = buscar_dados_cervejaria()
        self.assertIsInstance(dados, list)
        self.assertGreater(len(dados), 0)

    def test_transformar_dados(self):
        # Testar a transformação de dados
        mock_data = [
            {'brewery_type': 'micro', 'city': 'San Diego', 'state': 'CA'},
            {'brewery_type': 'brewpub', 'city': 'Los Angeles', 'state': 'CA'},
        ]
        df = pd.DataFrame(mock_data)

        # Simular a transformação
        df['localizacao'] = df['city'] + ', ' + df['state']
        df_agregado = df.groupby(['brewery_type', 'localizacao']).size().reset_index(name='contagem')

        # Verificar se a transformação foi realizada corretamente
        self.assertIn('localizacao', df.columns)
        self.assertEqual(df_agregado.shape[0], 2)  # Deve haver 2 tipos de cervejarias

    def test_carregar_dados_para_camada_ouro(self):
        # Testar a inserção de dados no SQLite
        mock_data = [
            {'brewery_type': 'micro', 'location': 'San Diego, CA', 'count': 5},
            {'brewery_type': 'brewpub', 'location': 'Los Angeles, CA', 'count': 3},
        ]
        df = pd.DataFrame(mock_data)
        df.to_parquet('camada_ouro/cervejarias_agregadas.parquet', index=False)

        carregar_dados_para_camada_ouro()

        # Verificar se os dados foram inseridos no banco de dados
        self.cursor.execute("SELECT * FROM breweries_table")
        rows = self.cursor.fetchall()
        self.assertEqual(len(rows), 2)  # Deve haver 2 entradas

if __name__ == '__main__':
    unittest.main()
