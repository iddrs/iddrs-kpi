from iddrs.kpi.topics import educacao
from iddrs.kpi import generate_report

ano = 2023
mes = 4

educacao.MDE(ano, mes).run()
educacao.Fundeb(ano, mes).run()
educacao.Educacao(ano, mes).run()

generate_report(f'mun_{ano}-{mes}')