# iddrs-kpi

Sistema gerador de relatório de indicadores do Município de Independência/RS.


## Objetivo geral

Produzir relatório com indicadores da Prefeitura, Câmara de Vereadores e FAPS.


## Requisitos dos relatórios

- Relatórios de periodocidade mensal para cada uma das seguintes entidades:
  -  Prefeitura;
  -  Câmara de Vereadores;
  -  FAPS.
-  Geração em PDF;
-  Considerar a necessidade de impressão dos relatórios em escala de cinza;
-  Geração a partir dos dados existentes no data warehouse.


## Conteúdo dos relatórios

Cada relatórios deve conter indicadores relativos à limites e restrições constitucionais e legais e relativos à questões orçamentárias e financeiras.

Para isso, deve fazer uso de visualizações, tabelas e textos.

Visualizações são gráficos utilizados para demonstrar tendências gerais, comportamentos e valores em determinado perído ou entre períodos.

Tabelas contém os dados utilizados nas visualizações.

Textos são elementos elucidativos, explicativos e complementares às visualizações e tabelas.

Numa escala de prioridade, temos as visualizações, as tabelas e, por último os textos, visto que o foco dos relatórios são os dados.


## Estrutura e organização dos relatórios

Cada relatório deve ser estruturado em três níveis hierárquicos:
- Temática: apresenta uma área temática dos indicadores;
- Assunto: é um detalhamento de determinada temática e agrupa indicadores interrelacionados;
- Indicador: apresenta os dados através das visualizações bem como os textos relacionados.

A ordem ideal de apresentação em cada indicador é a seguinte:
- Título do indicador;
- Explanação do objetivo do indicador;
- Visualização;
- Explicação dos dados que compõem a visualização;
- Tabela de dados;
- Explicação dos dados que compõe a tabela;
- Análise do desempenho do indicador.

