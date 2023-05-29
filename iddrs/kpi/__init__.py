from iddrs import config
from jinja2 import Environment, FileSystemLoader, select_autoescape
import os
import shutil
import pandas as pd
from datetime import datetime, timedelta
import locale


locale.setlocale(locale.LC_ALL, 'pt_BR.utf8')


class KPIBase():

    def save_fig(self, fig, obj_name):
        fig.savefig(f'{config.path_asset_figures}{obj_name}.png')

    def save_df(self, df, obj_name):
        df.to_excel(f'{config.path_asset_dataframes}{obj_name}.xlsx', sheet_name='data')

def load_figs(dir_fig):
    files_dict = {}
    for file in os.listdir(dir_fig):
        file_path = os.path.join(dir_fig, file)
        if os.path.isfile(file_path):
            file_name, file_ext = os.path.splitext(file)
            # files_dict[file_name] = file_path
            files_dict[file_name] = file
    return files_dict


def load_dfs(dir_df):
    df_dict = {}
    for file in os.listdir(dir_df):
        file_path = os.path.join(dir_df, file)
        if os.path.isfile(file_path):
            file_name, file_ext = os.path.splitext(file)
            df_dict[file_name] = pd.read_excel(file_path, sheet_name='data')
    return df_dict


def generate_dash(ano, mes):
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
    data_base = datetime(ano, mes, 1)
    competencia_anterior = (data_base - timedelta(days=1)).strftime('%Y-%m')
    competencia_posterior = (data_base + timedelta(days=31)).strftime('%Y-%m')
    competencia_texto = data_base.strftime('%B/%Y')
    context={
        'uf': 'RS',
        'ente': 'Município de Independência',
        'ano': ano,
        'mes': mes,
        'competencia': f'{ano}-{str(mes).zfill(2)}',
        'competencia_texto': competencia_texto,
        'competencia_anterior': competencia_anterior,
        'competencia_posterior': competencia_posterior,
        'tema': 'index'
    }
    base_dir_output = os.path.join(config.path_output, f'{ano}-{str(mes).zfill(2)}')
    save_tpl(base_dir_output, 'index.html', env, context)
    context['tema'] = 'educacao'
    save_tpl(base_dir_output, 'educacao.html', env, context)
    copy_figs(base_dir_output)

def save_tpl(basedir, tpl, env, context, output=None):
    if output is None:
        output = tpl
    template = env.get_template(f'{tpl}.jinja')
    html = template.render(
        figlist=load_figs(config.path_asset_figures),
        dflist=load_dfs(config.path_asset_dataframes),
        **context
    )
    if not os.path.exists(basedir):
        os.makedirs(basedir)
    with open(os.path.join(basedir, output), 'w', encoding='utf-8') as f:
        f.write(html)


def copy_figs(basedir):
    diretorio_origem = config.path_asset_figures
    diretorio_destino = basedir
    if not os.path.exists(diretorio_destino):
        os.makedirs(diretorio_destino)
    for arquivo in os.listdir(diretorio_origem):
        caminho_arquivo = os.path.join(diretorio_origem, arquivo)
        if os.path.isfile(caminho_arquivo):
            shutil.copy2(caminho_arquivo, diretorio_destino)


def generate_landingpage(ano, mes):
    env = Environment(
        loader=FileSystemLoader(config.path_asset_templates, encoding='utf-8'),
        autoescape=select_autoescape()
    )
    context={
        'uf': 'RS',
        'ente': 'Município de Independência',
        'site': 'https://www.independencia.rs.gov.br',
        'transparencia': 'https://transparencia.abase.com.br/home/UYRTIeXh9qU=',
        'contas_publicas': 'https://www.independencia.rs.gov.br/site/contaspublicas',
        'orcamentos': 'https://www.independencia.rs.gov.br/site/planosmetas',
        'ano': ano,
        'mes': mes,
        'competencia': f'{ano}-{str(mes).zfill(2)}'
    }
    base_dir_output = config.path_output
    save_tpl(base_dir_output, 'landingpage.html', env, context, output='index.html')

    