from datetime import datetime
import locale
import yaml
import calendar

locale.setlocale(locale.LC_ALL, 'pt_BR.utf8')

periodo = None

with open('../../_config.yml', 'r') as f:
    ydata = yaml.safe_load(f)
    periodo = ydata['parse']['myst_substitutions']['data_base']
dt = datetime.strptime(periodo, '%B de %Y')
last_day = calendar.monthrange(dt.year, dt.month)[1]
dt = datetime(dt.year, dt.month, last_day)
data_base = dt.strftime('%Y-%m-%d')


controle_mes = f'{str(dt.year)}{str(dt.month).zfill(2)}'
controle_ano = f'{str(dt.year)}'

controle_mes_ano_anterior = f'{str(dt.year - 1)}12'