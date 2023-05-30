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
        self.plot_evolucao_asps()
        self.df_asps()

    def plot_evolucao_asps(self):
        df = self._df[['data_base', 'indice', 'minimo']].copy()
        # df = utils.completa_data_base(df, self._data_base_final.year, list(df.columns), 'data_base')
        # df.fillna(0, inplace=True)
        df['data_base'] = pd.to_datetime(df['data_base'], format='%Y-%m-%d')
        fig, ax = plt.subplot_mosaic("""A
                                                B""", figsize=config.figsize, sharex=False, sharey=False)
        ax['A'].set_title('Aplicação de receita decorrente de impostos em ASPS')
        ax['A'].xaxis.set_major_formatter(mdates.DateFormatter('%m/%y'))
        ax['A'].xaxis.set_ticks(df['data_base'])
        ax['A'].set_ylim(0, 0.5)
        ax['A'].yaxis.set_ticks([])
        ax['A'].plot(df['data_base'], df['minimo'], color=config.colors['secondary'])
        ax['A'].bar(df['data_base'], df['indice'], edgecolor=config.colors['primary'], hatch='////', color='white',
                    width=20)
        for x, y in zip(df['data_base'], df['indice']):
            ax['A'].text(x, y, '{:.2%}'.format(y).replace('.', ','), ha='center', va='bottom', fontsize=16)
        ax['A'].legend([]).remove()

        df = self._df[['data_base', 'receita_bc', 'despesa_bc']].copy()
        df['minimo'] = round(df['receita_bc'] * 0.15, 2)
        # df = utils.completa_data_base(df, self._data_base_final.year, list(df.columns), 'data_base')
        # df.fillna(0, inplace=True)
        df['data_base'] = pd.to_datetime(df['data_base'], format='%Y-%m-%d')
        ax['B'].set_title('Evolução da base de cálculo do ASPS')
        ax['B'].xaxis.set_major_formatter(mdates.DateFormatter('%m/%y'))
        ax['B'].xaxis.set_ticks(df['data_base'])
        ax['B'].plot(df['data_base'], df['despesa_bc'], marker='s', color=config.colors['negative'],
                     label='Despesa ASPS')
        ax['B'].plot(df['data_base'], df['minimo'], marker='^', color=config.colors['positive'],
                     label='Mínimo a aplicar', linestyle='--')
        ax['B'].legend(loc='upper left')
        ax['B'].yaxis.set_major_formatter(
            FuncFormatter(lambda x, pos: f'{x:,.0f}'.replace(',', '_').replace('.', ',').replace('_', '.')))

        plt.tight_layout()
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
        # df = utils.completa_data_base(df, self._data_base_final.year, list(df.columns), 'data_base')
        # df.fillna(0, inplace=True)
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
