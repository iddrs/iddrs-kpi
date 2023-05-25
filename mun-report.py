from iddrs.kpi.topics import educacao
from iddrs.kpi import generate_report

ano = 2023
mes = 4

mde = educacao.MDE(ano, mes)
mde.run()

generate_report(f'mun_{ano}-{mes}')