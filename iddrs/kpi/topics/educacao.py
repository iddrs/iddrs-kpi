import pandas as pd

import iddrs.kpi
from iddrs import db, utils, config
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter

class MDE(iddrs.kpi.KPIBase):

    def __init__(self, ano, mes):
        self._data_base_final = utils.get_database(ano, mes)
        self._data_base_inicial = utils.get_primeiro_dia_ano(ano)
        self._df = db.exec_sql(f'SELECT * FROM indicadores."MDE" WHERE data_base BETWEEN \'{self._data_base_inicial}\' AND \'{self._data_base_final}\' ORDER BY data_base ASC')

    def run(self):
        self.plot_evolucao_mde()
        self.df_mde()

    def plot_evolucao_mde(self):
        df = self._df[['data_base', 'indice', 'minimo']].copy()
        # df = utils.completa_data_base(df, self._data_base_final.year, list(df.columns), 'data_base')
        # df.fillna(0, inplace=True)
        # df['minimo'] = 0.25
        df['data_base'] = pd.to_datetime(df['data_base'], format='%Y-%m-%d')
        fig, ax = plt.subplot_mosaic("""A
                                        B""", figsize=config.figsize, sharex=False, sharey=False)
        ax['A'].set_title('Aplicação de receita decorrente de impostos em MDE')
        ax['A'].xaxis.set_major_formatter(mdates.DateFormatter('%m/%y'))
        ax['A'].xaxis.set_ticks(df['data_base'])
        ax['A'].set_ylim(0, 0.5)
        ax['A'].yaxis.set_ticks([])
        ax['A'].plot(df['data_base'], df['minimo'], color=config.colors['secondary'])
        ax['A'].bar(df['data_base'], df['indice'], edgecolor=config.colors['primary'], hatch='////', color='white', width=20)
        for x, y in zip(df['data_base'], df['indice']):
            ax['A'].text(x, y, '{:.2%}'.format(y).replace('.', ','), ha='center', va='bottom', fontsize=12)
        ax['A'].legend([]).remove()

        df = self._df[['data_base', 'receita_bc', 'despesa_bc']].copy()
        df['minimo'] = round(df['receita_bc'] * 0.25, 2)
        # df = utils.completa_data_base(df, self._data_base_final.year, list(df.columns), 'data_base')
        # df.fillna(0, inplace=True)
        df['data_base'] = pd.to_datetime(df['data_base'], format='%Y-%m-%d')
        ax['B'].set_title('Evolução da base de cálculo do MDE')
        ax['B'].xaxis.set_major_formatter(mdates.DateFormatter('%m/%y'))
        ax['B'].xaxis.set_ticks(df['data_base'])
        ax['B'].plot(df['data_base'], df['despesa_bc'], marker='s', color=config.colors['negative'], label='Despesa MDE')
        ax['B'].plot(df['data_base'], df['minimo'], marker='^', color=config.colors['positive'], label='Mínimo a aplicar', linestyle='--')
        ax['B'].legend(loc='upper left')
        ax['B'].yaxis.set_major_formatter(FuncFormatter(lambda x, pos: f'{x:,.0f}'.replace(',', '_').replace('.', ',').replace('_', '.')))

        plt.tight_layout()
        self.save_fig(fig, 'evolucao_indice_mde')



    def df_mde(self):
        df = self._df[['data_base', 'indice', 'receita_bc', 'despesa_bc']].copy()
        df['diferenca'] = round(df['despesa_bc'] - (df['receita_bc'] * 0.25), 2)
        self.save_df(df, 'mde')


class Fundeb(iddrs.kpi.KPIBase):

    def __init__(self, ano, mes):
        self._data_base_final = utils.get_database(ano, mes)
        self._data_base_inicial = utils.get_primeiro_dia_ano(ano)
        self._df = db.exec_sql(f'SELECT * FROM indicadores."FUNDEB" WHERE data_base BETWEEN \'{self._data_base_inicial}\' AND \'{self._data_base_final}\' ORDER BY data_base ASC')

    def run(self):
        self.plot_evolucao_remuneracao_fundeb()
        self.df_remun_fundeb()

    def plot_evolucao_remuneracao_fundeb(self):
        df = self._df[['data_base', 'indice_remun', 'minimo_remun']].copy()
        # df = utils.completa_data_base(df, self._data_base_final.year, list(df.columns), 'data_base')
        # df.fillna(0, inplace=True)
        # df['minimo_remun'] = 0.7
        df['data_base'] = pd.to_datetime(df['data_base'], format='%Y-%m-%d')
        fig, ax = plt.subplot_mosaic("""A
                                                B""", figsize=config.figsize, sharex=False, sharey=False)
        ax['A'].set_title('Aplicação da receita do Fundeb em remuneração')
        ax['A'].xaxis.set_major_formatter(mdates.DateFormatter('%m/%y'))
        ax['A'].xaxis.set_ticks(df['data_base'])
        ax['A'].set_ylim(0, 1.2)
        ax['A'].yaxis.set_ticks([])
        ax['A'].plot(df['data_base'], df['minimo_remun'], color=config.colors['secondary'])
        ax['A'].bar(df['data_base'], df['indice_remun'], edgecolor=config.colors['primary'], hatch='////', color='white',
                    width=20)
        for x, y in zip(df['data_base'], df['indice_remun']):
            ax['A'].text(x, y, '{:.2%}'.format(y).replace('.', ','), ha='center', va='bottom', fontsize=12)
        ax['A'].legend([]).remove()

        df = self._df[['data_base', 'receita_bc_remun', 'despesa_bc_remun']].copy()
        df['minimo_remun'] = round(df['receita_bc_remun'] * 0.7, 2)
        # df = utils.completa_data_base(df, self._data_base_final.year, list(df.columns), 'data_base')
        # df.fillna(0, inplace=True)
        df['data_base'] = pd.to_datetime(df['data_base'], format='%Y-%m-%d')
        ax['B'].set_title('Evolução da base de cálculo da Remuneração/Fundeb')
        ax['B'].xaxis.set_major_formatter(mdates.DateFormatter('%m/%y'))
        ax['B'].xaxis.set_ticks(df['data_base'])
        ax['B'].plot(df['data_base'], df['despesa_bc_remun'], marker='s', color=config.colors['negative'], label='Despesa Remuneração/Fundeb')
        ax['B'].plot(df['data_base'], df['minimo_remun'], marker='^', color=config.colors['positive'],
                     label='Mínimo a aplicar', linestyle='--')
        ax['B'].legend(loc='upper left')
        ax['B'].yaxis.set_major_formatter(
            FuncFormatter(lambda x, pos: f'{x:,.0f}'.replace(',', '_').replace('.', ',').replace('_', '.')))

        plt.tight_layout()
        self.save_fig(fig, 'evolucao_indice_remun_fundeb')

    def df_remun_fundeb(self):
        df = self._df[['data_base', 'indice_remun', 'receita_bc_remun', 'despesa_bc_remun']].copy()
        df['diferenca_remun'] = round(df['despesa_bc_remun'] - (df['receita_bc_remun'] * 0.7), 2)
        self.save_df(df, 'fundeb_remun')


class Educacao(iddrs.kpi.KPIBase):

    def __init__(self, ano, mes):
        self._data_base_final = utils.get_database(ano, mes)
        self._data_base_inicial = utils.get_primeiro_dia_ano(ano)

    def run(self):
        self.plot_evolucao_receita_despesa()
        self.df_receita_despesa()

    def plot_evolucao_receita_despesa(self):
        df = db.exec_sql(f'SELECT data_base, arrecadado, empenhado, liquidado FROM indicadores."RECEITA_DESPESA_EDUCACAO" WHERE data_base BETWEEN \'{self._data_base_inicial}\' AND \'{self._data_base_final}\' ORDER BY data_base ASC')
        # df = utils.completa_data_base(df, self._data_base_final.year, list(df.columns), 'data_base')
        # df.fillna(0, inplace=True)
        df['data_base'] = pd.to_datetime(df['data_base'], format='%Y-%m-%d')
        fig, ax = plt.subplots(figsize=config.figsize)
        ax.text(0, 1.1, 'Evolução da receita e despesa da educação', fontsize=14, fontweight='bold',
                transform=ax.transAxes)
        ax.text(0, 1.05, 'valores acumulados | receita arrecadada | despesa empenhada e liquidada', fontsize=12, transform=ax.transAxes)
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%y'))
        ax.xaxis.set_ticks(df['data_base'])
        ax.yaxis.set_major_formatter(FuncFormatter(lambda x, pos: f'{x:,.0f}'.replace(',', '_').replace('.', ',').replace('_', '.')))
        ax.plot(df['data_base'], df['arrecadado'], color=config.colors['positive'], label='Arrecadado', marker='o')
        ax.plot(df['data_base'], df['empenhado'], color=config.colors['negative'], label='Empenhado', marker='s')
        ax.plot(df['data_base'], df['liquidado'], color=config.colors['negative'], label='Liquidado', marker='^', alpha=0.7)
        ax.legend()
        self.save_fig(fig, 'evolucao_receita_despesa_educacao')

    def df_receita_despesa(self):
        df = db.exec_sql(f'SELECT data_base, arrecadado, empenhado, liquidado, pago FROM indicadores."RECEITA_DESPESA_EDUCACAO" WHERE data_base BETWEEN \'{self._data_base_inicial}\' AND \'{self._data_base_final}\' ORDER BY data_base ASC')
        self.save_df(df, 'receita_despesa_educacao')
