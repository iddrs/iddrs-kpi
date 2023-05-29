from iddrs.kpi.topics import educacao, saude
from iddrs.kpi import generate_dash, generate_landingpage

ano = 2023
mes = 4

educacao.MDE(ano, mes).run()
educacao.Fundeb(ano, mes).run()
educacao.Educacao(ano, mes).run()
saude.ASPS(ano, mes).run()
saude.Saude(ano, mes).run()

generate_dash(ano, mes)
generate_landingpage(ano, mes)