import pandas as pd

import iddrs.kpi
from iddrs import db, utils, config
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter

class ASPS(iddrs.kpi.KPIBase):

    def __init__(self, ano, mes):
        self._data_base_final = utils.get_database(ano, mes)
        self._data_base_inicial = utils.get_primeiro_dia_ano(ano)
        self._df = db.exec_sql(f'SELECT * FROM indicadores."ASPS" WHERE data_base BETWEEN \'{self._data_base_inicial}\' AND \'{self._data_base_final}\' ORDER BY data_base ASC')

    def run(self):
        self.plot_evolucao_indice_asps()
        self.df_asps()

    def plot_evolucao_indice_asps(self):
        df = self._df[['data_base', 'indice', 'minimo']].copy()
        df['data_base'] = pd.to_datetime(df['data_base'], format='%Y-%m-%d')
        fig, ax = plt.subplots(figsize=config.figsize)
        ax.text(0, 1.1, 'Aplicação de receita decorrente de impostos em ASPS', fontsize=14, fontweight='bold',
                transform=ax.transAxes)
        ax.text(0, 1.05, 'valores acumulados', fontsize=12, transform=ax.transAxes)
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%y'))
        ax.xaxis.set_ticks(df['data_base'])
        ax.set_ylim(0, 0.5)
        ax.yaxis.set_ticks([])
        ax.plot(df['data_base'], df['minimo'], color=config.colors['secondary'])
        ax.bar(df['data_base'], df['indice'], edgecolor=config.colors['primary'], hatch='////', color='white', width=20)
        for x, y in zip(df['data_base'], df['indice']):
            ax.text(x, y, '{:.2%}'.format(y).replace('.', ','), ha='center', va='bottom', fontsize=16)
        ax.legend([]).remove()
        # plt.show()
        self.save_fig(fig, 'evolucao_indice_asps')

    def df_asps(self):
        df = self._df[['data_base', 'indice', 'receita_bc', 'despesa_bc']].copy()
        df['diferenca'] = round(df['despesa_bc'] - (df['receita_bc'] * 0.15), 2)
        self.save_df(df, 'asps')


class Saude(iddrs.kpi.KPIBase):

    def __init__(self, ano, mes):
        self._data_base_final = utils.get_database(ano, mes)
        self._data_base_inicial = utils.get_primeiro_dia_ano(ano)

    def run(self):
        self.plot_evolucao_receita_despesa()
        self.df_receita_despesa()

    def plot_evolucao_receita_despesa(self):
        df = db.exec_sql(f'SELECT data_base, arrecadado, empenhado, liquidado FROM indicadores."RECEITA_DESPESA_SAUDE" WHERE data_base BETWEEN \'{self._data_base_inicial}\' AND \'{self._data_base_final}\' ORDER BY data_base ASC')
        df['data_base'] = pd.to_datetime(df['data_base'], format='%Y-%m-%d')
        fig, ax = plt.subplots(figsize=config.figsize)
        ax.text(0, 1.1, 'Evolução da receita e despesa da saúde', fontsize=14, fontweight='bold',
                transform=ax.transAxes)
        ax.text(0, 1.05, 'valores acumulados | receita arrecadada | despesa empenhada e liquidada', fontsize=12, transform=ax.transAxes)
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%y'))
        ax.xaxis.set_ticks(df['data_base'])
        ax.yaxis.set_major_formatter(FuncFormatter(lambda x, pos: f'{x:,.0f}'.replace(',', '_').replace('.', ',').replace('_', '.')))
        ax.plot(df['data_base'], df['arrecadado'], color=config.colors['positive'], label='Arrecadado', marker='o')
        ax.plot(df['data_base'], df['empenhado'], color=config.colors['negative'], label='Empenhado', marker='s')
        ax.plot(df['data_base'], df['liquidado'], color=config.colors['negative'], label='Liquidado', marker='^', alpha=0.7)
        ax.legend()
        self.save_fig(fig, 'evolucao_receita_despesa_saude')

    def df_receita_despesa(self):
        df = db.exec_sql(f'SELECT data_base, arrecadado, empenhado, liquidado, pago FROM indicadores."RECEITA_DESPESA_SAUDE" WHERE data_base BETWEEN \'{self._data_base_inicial}\' AND \'{self._data_base_final}\' ORDER BY data_base ASC')
        self.save_df(df, 'receita_despesa_saude')
