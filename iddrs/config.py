"""Configurações gerais do Data Warehouse"""

engine_connection_string = r'postgresql+psycopg2://postgres:lise890@localhost:5432/iddrs' # String de conexão com o banco de dados

path_asset_figures = r'assets/fig/'
path_asset_dataframes = r'assets/df/'
path_asset_templates = r'assets/tpl/'

colors = {
    'primary': '#2980b9',
    'secondary': '#7f8c8d',
    'positive': '#16a085',
    'negative': '#c0392b'
}

figsize=(10, 5)

path_output = r'docs'