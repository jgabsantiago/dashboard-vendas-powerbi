Dashboard de Vendas | Projeto Acadêmico de Business Intelligence

Projeto de análise de vendas desenvolvido utilizando Python, Pandas, Power BI e DAX, com foco no tratamento de dados, modelagem dimensional e construção de indicadores para análise de desempenho comercial.

Sobre o Projeto

Este dashboard foi desenvolvido inicialmente como parte de um trabalho de Projeto Integrador (PI) do curso de Análise e Desenvolvimento de Sistemas, do Centro Universitário Senac.

O trabalho utiliza uma base fictícia de vendas, com informações referentes ao período de 2020 a 2023.

A proposta foi aplicar conhecimentos adquiridos durante a graduação, passando por diferentes etapas de um projeto de análise de dados: preparação da base, organização das informações, criação de medidas e desenvolvimento de visualizações.

Após a etapa acadêmica, continuei aprimorando o projeto, realizando ajustes na estrutura dos dados, nos indicadores e na apresentação visual do dashboard.

Minha Trajetória na Área de Dados:

Atualmente, curso Análise e Desenvolvimento de Sistemas e atuo como estagiário na área de Dados.

Estou em um processo de aprendizado e desenvolvimento profissional, buscando ampliar meus conhecimentos em SQL, Python, Power BI e outras ferramentas relacionadas à análise de dados.

O desenvolvimento deste dashboard faz parte dessa trajetória. Além de atender à proposta acadêmica, foi uma oportunidade de trabalhar com ferramentas que estou conhecendo e aprofundando meus conhecimentos.

Ao longo do projeto, pude praticar o tratamento de dados com Python e Pandas, a organização de um modelo dimensional e a construção de medidas e visualizações no Power BI.

Este repositório faz parte do meu portfólio de estudos e projetos, no qual pretendo registrar minha evolução técnica e as experiências adquiridas durante minha formação.

Natureza do projeto: acadêmico, desenvolvido com dados fictícios para fins educacionais e demonstrativos.


## Base de Dados

O projeto utiliza uma base fictícia de vendas, com registros referentes ao período de 2020 a 2023.

Após a preparação dos dados, foram utilizados 3.509 registros de vendas, organizados em um modelo dimensional.

A base contempla:

- 30 produtos, distribuídos em 8 categorias.
- 50 clientes.
- Informações de vendas, descontos e lucro.
- Dados geográficos dos clientes.
- Histórico de datas e promoções.

Os valores financeiros estão representados em dólares americanos (USD).

## Tratamento e Preparação dos Dados

A preparação dos dados foi realizada utilizando Python e a biblioteca Pandas.

Inicialmente, explorei a estrutura da base para compreender as informações disponíveis e identificar os ajustes necessários antes da utilização no Power BI.

Entre as atividades realizadas, destacam-se:

- Leitura e inspeção dos arquivos CSV.
- Verificação dos tipos de dados e padronização de campos.
- Tratamento dos formatos numéricos e de datas.
- Delimitação do período analisado.
- Separação das informações em tabelas de fatos e dimensões.
- Padronização dos nomes dos produtos e categorias para português.
- Exportação das tabelas tratadas para utilização no Power BI.

Essa etapa foi importante para compreender a preparação de dados e sua influência na qualidade das análises.

## Modelagem Dimensional

No Power BI, os dados foram organizados utilizando uma estrutura de modelo estrela (Star Schema), separando os registros de vendas das informações descritivas.

A modelagem foi composta pelas seguintes tabelas:

| Tabela | Finalidade |
|---|---|
| Fato_Vendas | Armazena os registros e valores das vendas |
| Dim_Produtos | Informações dos produtos e suas categorias |
| Dim_Clientes | Dados cadastrais e geográficos dos clientes |
| Dim_Promocoes | Informações relacionadas às promoções |
| Dim_Datas | Calendário utilizado nas análises temporais |

Os relacionamentos foram configurados no padrão um-para-muitos (1:N), conectando as dimensões à tabela fato.

A utilização desse modelo permitiu organizar as informações para a construção de indicadores e a aplicação de filtros nas análises.
