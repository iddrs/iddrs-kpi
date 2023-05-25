from iddrs import config
from jinja2 import Environment, FileSystemLoader, select_autoescape
import os
import pandas as pd

class KPIBase():

    def save_fig(self, fig, obj_name):
        fig.savefig(f'{config.path_asset_figures}{obj_name}.png')

    def save_df(self, df, obj_name):
        df.to_excel(f'{config.path_asset_dataframes}{obj_name}.xlsx', sheet_name='data')


def generate_report(app_name):
    def format_datetime(value, format='%d/%m/%Y'):
        return value.strftime(format)

    def format_money(value, decimals=2):
        number = f'{value:,.{decimals}f}'.replace(',', '_').replace('.', ',').replace('_', '.')
        if value == 0.0 or value == 0:
            number = '-'
        if value < 0.0:
            number = f'({number})'
        return number

    def format_percent(value, decimals=2):
        return f'{value:,.{decimals}%}'.replace(',', '_').replace('.', ',').replace('_', '.')

    env = Environment(
        loader=FileSystemLoader(config.path_asset_templates, encoding='utf-8'),
        autoescape=select_autoescape()
    )
    env.filters['format_datetime'] = format_datetime
    env.filters['format_money'] = format_money
    env.filters['format_percent'] = format_percent
    template = env.get_template('mun.html')
    html = template.render(
        meta={
            'escopo': 'Município de Independência / RS',
            'competencia': 'abril de 2023'
        },
        figlist=load_figs(config.path_asset_figures),
        dflist=load_dfs(config.path_asset_dataframes)
    )
    with open(f'reports/{app_name}.html', 'w', encoding='utf-8') as f:
        f.write(html)

def load_figs(dir_fig):
    files_dict = {}
    for file in os.listdir(dir_fig):
        file_path = os.path.join(dir_fig, file)
        if os.path.isfile(file_path):
            file_name, file_ext = os.path.splitext(file)
            files_dict[file_name] = file_path
    return files_dict


def load_dfs(dir_df):
    df_dict = {}
    for file in os.listdir(dir_df):
        file_path = os.path.join(dir_df, file)
        if os.path.isfile(file_path):
            file_name, file_ext = os.path.splitext(file)
            df_dict[file_name] = pd.read_excel(file_path, sheet_name='data')
    return df_dict
