"""Configurações gerais do Data Warehouse"""

engine_connection_string = r'postgresql://postgres:lise890@localhost:5432/iddrs' # String de conexão com o banco de dados

path_asset_figures = r'assets/fig/'
path_asset_dataframes = r'assets/df/'
path_asset_templates = r'assets/tpl/'

colors = {
    'primary': '#00477e',
    'secondary': '#b2beb5',
    'positive': '#004d33',
    'negative': '#a6001a'
}

figsize=(10, 5)