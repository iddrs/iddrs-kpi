import pandas as pd

import iddrs.kpi
from iddrs import db, utils, config
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

class MDE(iddrs.kpi.KPIBase):

    def __init__(self, ano, mes):
        self._data_base_final = utils.get_database(ano, mes)
        self._data_base_inicial = utils.get_primeiro_dia_ano(ano)
        self._df = db.exec_sql(f'SELECT * FROM indicadores."MDE" WHERE data_base BETWEEN \'{self._data_base_inicial}\' AND \'{self._data_base_final}\' ORDER BY data_base ASC')

    def run(self):
        self.plot_evolucao_indice_mde()
        # self.df_mde()

    def plot_evolucao_indice_mde(self):
        df = self._df[['data_base', 'indice', 'minimo']].copy()
        df['data_base'] = pd.to_datetime(df['data_base'], format='%Y-%m-%d')
        fig, ax = plt.subplots(figsize=config.figsize)
        ax.text(0, 1.1, 'Aplicação de receita decorrente de impostos em MDE', fontsize=14, fontweight='bold',
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
        self.save_fig(fig, 'evolucao_indice_mde')

    def df_mde(self):
        df = self._df[['data_base', 'indice', 'receita_bc', 'despesa_bc']].copy()
        df['diferenca'] = round(df['despesa_bc'] - (df['receita_bc'] * 0.25), 2)
        self.save_df(df, 'mde')
