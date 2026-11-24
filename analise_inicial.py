
# ==================================================
# PROJETO: DASHBOARD DE VENDAS BI
# ETAPA 1: LEITURA INICIAL DA BASE COM PANDAS
# ==================================================

# Importa a biblioteca Pandas
from pathlib import Path
import pandas as pd

# Define o caminho da base de dados
arquivo = "dados/Vendas_Base_Consolidada_2.csv"

# Lê o arquivo CSV
# sep=";" indica que as colunas são separadas por ponto e vírgula
# dtype=str preserva os valores originais nesta inspeção
df = pd.read_csv(arquivo, sep=";", encoding="utf-8-sig", dtype=str)

# Exibe a quantidade de linhas e colunas
print("Quantidade de linhas:", df.shape[0])
print("Quantidade de colunas:", df.shape[1])

# Exibe os nomes das colunas
print("\nColunas disponíveis:")
print(df.columns.tolist())

# Exibe as primeiras 5 linhas
print("\nPrimeiros registros:")
print(df.head())


# ==================================================
# ETAPA 2: VERIFICAÇÃO DA QUALIDADE DOS DADOS
# ==================================================

# Identifica valores ausentes em cada coluna
print("\n=== VALORES AUSENTES ===")

valores_ausentes = df.isna().sum()

# Exibe somente colunas com valores ausentes
print(valores_ausentes[valores_ausentes > 0])

# Identifica registros integralmente duplicados
print("\n=== REGISTROS DUPLICADOS ===")

duplicados = df.duplicated().sum()

print("Quantidade de registros duplicados:", duplicados)


# ==================================================
# ETAPA 3: INVESTIGAÇÃO DOS DADOS DE PROMOÇÃO
# ==================================================

# Seleciona vendas sem nome de promoção
vendas_sem_promocao = df[
    df["Nome da promoção"].isna()
]

# Verifica quais IDs de promoção aparecem nessas vendas
print("\n=== IDs DAS VENDAS SEM PROMOÇÃO ===")

print(
    vendas_sem_promocao["ID da promoção"].value_counts(
        dropna=False
    )
)

# ==================================================
# ETAPA 4: INVESTIGAÇÃO DOS REGISTROS DUPLICADOS
# ==================================================

# Seleciona todas as ocorrências de linhas repetidas
# keep=False exibe tanto a original quanto suas cópias
duplicados_detalhados = df[
    df.duplicated(keep=False)
]

# Seleciona as principais informações para investigação
colunas_analise = [
    "Data da venda",
    "ID do cliente",
    "ID do produto",
    "ID da promoção",
    "Unidades vendidas",
    "Vendas líquidas (USD)"
]

# Exibe os registros suspeitos
print("\n=== DETALHAMENTO DOS DUPLICADOS ===")

print(
    duplicados_detalhados[colunas_analise].to_string()
)

# ==================================================
# ETAPA 5: VALIDAÇÃO DOS VALORES FINANCEIROS
# ==================================================

# Converte vendas líquidas de texto para número
# Substitui a vírgula decimal por ponto
vendas_usd = pd.to_numeric(
    df["Vendas líquidas (USD)"].str.replace(
        ",", ".", regex=False
    ),
    errors="coerce"
)

# Verifica possíveis falhas na conversão
print("\n=== VALIDAÇÃO FINANCEIRA ===")
print("Valores não convertidos:", vendas_usd.isna().sum())

# Calcula o faturamento líquido total
print(f"Total de vendas líquidas: US$ {vendas_usd.sum():,.2f}")


# ==================================================
# ETAPA 6: VALIDAÇÃO DOS INDICADORES DO DASHBOARD
# ==================================================

# Converte a coluna de lucro para número decimal
lucro_usd = pd.to_numeric(
    df["Lucro (USD)"].str.replace(",", ".", regex=False),
    errors="coerce"
)

# Converte a quantidade de unidades vendidas
unidades = pd.to_numeric(
    df["Unidades vendidas"].str.replace(",", ".", regex=False),
    errors="coerce"
)

# Calcula os indicadores
lucro_total = lucro_usd.sum()
unidades_total = unidades.sum()

# Calcula a margem sobre as vendas líquidas
margem_lucro = (
    lucro_total / vendas_usd.sum()
) * 100

# Exibe os resultados
print("\n=== VALIDAÇÃO DOS KPIs ===")
print(f"Lucro total: US$ {lucro_total:,.2f}")
print(f"Margem de lucro: {margem_lucro:.2f}%")
print(f"Unidades vendidas: {unidades_total:,.0f}")

# Verifica falhas de conversão
print("Lucros não convertidos:", lucro_usd.isna().sum())
print("Unidades não convertidas:", unidades.isna().sum())


# ==================================================
# ETAPA 7: ANÁLISE DO PERÍODO DAS VENDAS
# ==================================================

# Converte a coluna de datas para o formato datetime
datas = pd.to_datetime(
    df["Data da venda"],
    format="%Y-%m-%d",
    errors="coerce"
)

# Identifica o período completo da base
print("\n=== PERÍODO DAS VENDAS ===")
print("Primeira venda:", datas.min())
print("Última venda:", datas.max())

# Identifica possíveis datas inválidas
print("Datas inválidas:", datas.isna().sum())

# Conta quantos registros existem em cada ano
print("\n=== REGISTROS POR ANO ===")
print(datas.dt.year.value_counts().sort_index())


# ==================================================
# ETAPA 8: DEFINIÇÃO DO PERÍODO DE ANÁLISE
# ==================================================

# Mantém somente os registros entre 2020 e 2023
df_tratado = df.loc[
    datas.dt.year.between(2020, 2023)
].copy()

# Verifica a quantidade de registros após o filtro
print("\n=== BASE DE TRABALHO ===")
print("Registros originais:", len(df))
print("Registros após o filtro:", len(df_tratado))
print("Registros excluídos:", len(df) - len(df_tratado))

# Salva uma nova base sem alterar o arquivo original
df_tratado.to_csv(
    "dados/Vendas_2020_2023.csv",
    sep=";",
    index=False,
    encoding="utf-8-sig"
)

print("Nova base salva com sucesso!")


# ==================================================
# ETAPA 9: KPIs DA BASE TRATADA (2020-2023)
# ==================================================

# Converte as vendas líquidas para valores numéricos
vendas_tratadas = pd.to_numeric(
    df_tratado["Vendas líquidas (USD)"].str.replace(
        ",", ".", regex=False
    ),
    errors="coerce"
)

# Converte o lucro para valores numéricos
lucro_tratado = pd.to_numeric(
    df_tratado["Lucro (USD)"].str.replace(
        ",", ".", regex=False
    ),
    errors="coerce"
)

# Converte as unidades vendidas
unidades_tratadas = pd.to_numeric(
    df_tratado["Unidades vendidas"].str.replace(
        ",", ".", regex=False
    ),
    errors="coerce"
)

# Calcula os indicadores da nova base
total_vendas = vendas_tratadas.sum()
total_lucro = lucro_tratado.sum()
total_unidades = unidades_tratadas.sum()

margem_tratada = (
    total_lucro / total_vendas * 100
    if total_vendas != 0 else 0
)

# Exibe os KPIs atualizados
print("\n=== KPIs DA BASE TRATADA ===")
print(f"Vendas líquidas: US$ {total_vendas:,.2f}")
print(f"Lucro total: US$ {total_lucro:,.2f}")
print(f"Margem de lucro: {margem_tratada:.2f}%")
print(f"Unidades vendidas: {total_unidades:,.0f}")

# Verifica eventuais falhas de conversão
print(
    "Falhas de conversão:",
    vendas_tratadas.isna().sum()
    + lucro_tratado.isna().sum()
    + unidades_tratadas.isna().sum()
)

# ==================================================
# ETAPA 10: VERIFICAÇÃO DA COBERTURA MENSAL
# ==================================================

# Converte as datas da base filtrada
datas_tratadas = pd.to_datetime(
    df_tratado["Data da venda"],
    format="%Y-%m-%d",
    errors="coerce"
)

# Organiza ano, mês e data para análise
periodos = pd.DataFrame({
    "Ano": datas_tratadas.dt.year,
    "Mes": datas_tratadas.dt.month,
    "Data": datas_tratadas
})

# Resume a cobertura de cada ano
cobertura = periodos.groupby("Ano").agg(
    Primeira_venda=("Data", "min"),
    Ultima_venda=("Data", "max"),
    Meses_com_vendas=("Mes", "nunique")
)

print("\n=== COBERTURA ANUAL ===")
print(cobertura.to_string())


# ==================================================
# ETAPA 11: VALIDAÇÃO DA DIMENSÃO DE PRODUTOS
# ==================================================

# Conta quantos nomes e categorias diferentes
# aparecem associados a cada ID de produto.
validacao_produtos = df_tratado.groupby(
    "ID do produto"
).agg(
    Nomes_distintos=("Nome do produto", "nunique"),
    Categorias_distintas=("Categoria do produto", "nunique")
)

# Identifica IDs com informações inconsistentes.
inconsistencias = validacao_produtos[
    (validacao_produtos["Nomes_distintos"] > 1)
    | (validacao_produtos["Categorias_distintas"] > 1)
]

print("\n=== VALIDAÇÃO DOS PRODUTOS ===")
print("IDs de produtos:", len(validacao_produtos))
print("IDs com inconsistências:", len(inconsistencias))
print(inconsistencias.to_string())


# ==================================================
# ETAPA 12: CRIAÇÃO DA DIMENSÃO DE PRODUTOS
# ==================================================


# Define os atributos da dimensão
colunas_produtos = [
    "ID do produto",
    "Nome do produto",
    "Categoria do produto"
]

# Seleciona as colunas e remove linhas repetidas
dim_produtos = (
    df_tratado[colunas_produtos]
    .drop_duplicates()
    .sort_values("ID do produto")
    .reset_index(drop=True)
)

# Valida a integridade da chave de produto
assert dim_produtos["ID do produto"].notna().all(), \
    "Existem IDs de produtos nulos."

assert dim_produtos["ID do produto"].is_unique, \
    "Existem IDs de produtos duplicados na dimensão."

# Cria a pasta que armazenará as tabelas do modelo
Path("dados/modelo").mkdir(parents=True, exist_ok=True)

# Exporta a dimensão para um novo CSV
dim_produtos.to_csv(
    "dados/modelo/Dim_Produtos.csv",
    sep=";",
    index=False,
    encoding="utf-8-sig"
)

# Exibe o resultado da criação
print("\n=== DIMENSÃO DE PRODUTOS ===")
print("Total de produtos:", len(dim_produtos))
print(dim_produtos.head().to_string(index=False))
print("Dimensão exportada com sucesso!")


# ==================================================
# ETAPA 13: VALIDAÇÃO DA DIMENSÃO DE CLIENTES
# ==================================================

# Define os atributos que serão analisados
colunas_clientes = [
    "Nome do cliente",
    "Cidade do cliente",
    "Estado do cliente"
]

# Verifica quantos valores distintos existem
# para cada atributo associado ao ID do cliente
validacao_clientes = df_tratado.groupby(
    "ID do cliente",
    dropna=False
)[colunas_clientes].nunique(dropna=False)

# Identifica clientes com informações divergentes
clientes_inconsistentes = validacao_clientes[
    (validacao_clientes > 1).any(axis=1)
]

# Verifica se existem IDs ausentes
ids_ausentes = df_tratado["ID do cliente"].isna().sum()

# Apresenta o diagnóstico
print("\n=== VALIDAÇÃO DOS CLIENTES ===")

print(
    "Clientes distintos:",
    df_tratado["ID do cliente"].nunique()
)

print("Registros sem ID:", ids_ausentes)

print(
    "IDs com inconsistências:",
    len(clientes_inconsistentes)
)

print(clientes_inconsistentes.to_string())


# ==================================================
# ETAPA 14: CRIAÇÃO DA DIMENSÃO DE CLIENTES
# ==================================================

# Define as colunas que farão parte da dimensão
colunas_dim_clientes = [
    "ID do cliente",
    "Nome do cliente",
    "Cidade do cliente",
    "Estado do cliente"
]

# Seleciona as colunas e elimina repetições
dim_clientes = (
    df_tratado[colunas_dim_clientes]
    .drop_duplicates()
    .sort_values("ID do cliente")
    .reset_index(drop=True)
)

# Garante que cada cliente tenha um ID único
assert dim_clientes["ID do cliente"].is_unique, \
    "Erro: existem IDs duplicados na dimensão."

# Garante que não existam IDs nulos
assert dim_clientes["ID do cliente"].notna().all(), \
    "Erro: existem clientes sem ID."

# Exporta a tabela dimensão
dim_clientes.to_csv(
    "dados/modelo/Dim_Clientes.csv",
    sep=";",
    index=False,
    encoding="utf-8-sig"
)

# Exibe os resultados
print("\n=== DIMENSÃO DE CLIENTES ===")
print("Total de clientes:", len(dim_clientes))
print(dim_clientes.head().to_string(index=False))
print("Dimensão exportada com sucesso!")


# ==================================================
# ETAPA 15: VALIDAÇÃO DA DIMENSÃO DE PROMOÇÕES
# ==================================================

# Define os atributos da promoção
colunas_promocoes = [
    "Nome da promoção",
    "Tipo de anúncio",
    "Código do cupom",
    "Tipo de desconto",
    "Percentual da promoção"
]

# Verifica se cada ID possui atributos consistentes
validacao_promocoes = df_tratado.groupby(
    "ID da promoção",
    dropna=False
)[colunas_promocoes].nunique(dropna=False)

# Identifica IDs associados a valores diferentes
promocoes_inconsistentes = validacao_promocoes[
    (validacao_promocoes > 1).any(axis=1)
]

# Exibe o diagnóstico
print("\n=== VALIDAÇÃO DAS PROMOÇÕES ===")

print(
    "IDs distintos:",
    df_tratado["ID da promoção"].nunique()
)

print(
    "IDs com inconsistências:",
    len(promocoes_inconsistentes)
)

print(promocoes_inconsistentes.to_string())


# ==================================================
# ETAPA 16: CRIAÇÃO DA DIMENSÃO DE PROMOÇÕES
# ==================================================

# Define os campos da dimensão
colunas_dim_promocoes = [
    "ID da promoção",
    "Nome da promoção",
    "Tipo de anúncio",
    "Código do cupom",
    "Tipo de desconto",
    "Percentual da promoção"
]

# Seleciona os dados e elimina registros repetidos
dim_promocoes = (
    df_tratado[colunas_dim_promocoes]
    .drop_duplicates()
    .sort_values("ID da promoção")
    .reset_index(drop=True)
)

# Identifica as vendas sem promoção cadastrada
sem_promocao = dim_promocoes["ID da promoção"] == "0"

# Define um nome descritivo para o ID 0
dim_promocoes.loc[
    sem_promocao, "Nome da promoção"
] = "Sem promoção"

# Verifica a integridade dos identificadores
assert dim_promocoes["ID da promoção"].is_unique, \
    "Existem IDs duplicados na dimensão."

assert dim_promocoes["ID da promoção"].notna().all(), \
    "Existem IDs de promoção nulos."

# Exporta a dimensão para a pasta do modelo
dim_promocoes.to_csv(
    "dados/modelo/Dim_Promocoes.csv",
    sep=";",
    index=False,
    encoding="utf-8-sig"
)

# Exibe o resultado
print("\n=== DIMENSÃO DE PROMOÇÕES ===")
print("Total de promoções:", len(dim_promocoes))

print(
    dim_promocoes[
        ["ID da promoção", "Nome da promoção"]
    ].to_string(index=False)
)

print("Dimensão exportada com sucesso!")


# ==================================================
# ETAPA 17: CRIAÇÃO DA DIMENSÃO DE DATAS
# ==================================================

# Converte as datas da base tratada
datas_vendas = pd.to_datetime(
    df_tratado["Data da venda"],
    format="%Y-%m-%d",
    errors="coerce"
)

# Impede a criação da dimensão se houver datas inválidas
assert datas_vendas.notna().all(), \
    "Existem datas inválidas na base de vendas."

# Cria um calendário contínuo entre a primeira e a última venda
dim_datas = pd.DataFrame({
    "Data": pd.date_range(
        start=datas_vendas.min(),
        end=datas_vendas.max(),
        freq="D"
    )
})

# Cria os atributos de análise temporal
dim_datas["Ano"] = dim_datas["Data"].dt.year
dim_datas["Trimestre"] = "T" + dim_datas["Data"].dt.quarter.astype(str)
dim_datas["MesNumero"] = dim_datas["Data"].dt.month
dim_datas["Dia"] = dim_datas["Data"].dt.day

# Define os nomes dos meses em português
meses = {
    1: "Janeiro", 2: "Fevereiro", 3: "Março",
    4: "Abril", 5: "Maio", 6: "Junho",
    7: "Julho", 8: "Agosto", 9: "Setembro",
    10: "Outubro", 11: "Novembro", 12: "Dezembro"
}

dim_datas["MesNome"] = dim_datas["MesNumero"].map(meses)

# Cria o identificador de ano e mês
dim_datas["AnoMes"] = dim_datas["Data"].dt.strftime("%Y-%m")

# Exporta a dimensão calendário
dim_datas.to_csv(
    "dados/modelo/Dim_Datas.csv",
    sep=";",
    index=False,
    encoding="utf-8-sig",
    date_format="%Y-%m-%d"
)

# Apresenta o resultado
print("\n=== DIMENSÃO DE DATAS ===")
print("Total de datas:", len(dim_datas))
print("Primeira data:", dim_datas["Data"].min())
print("Última data:", dim_datas["Data"].max())
print("Dimensão exportada com sucesso!")


# ==================================================
# ETAPA 18: CRIAÇÃO DA TABELA FATO DE VENDAS
# ==================================================

# Define as colunas da tabela fato
colunas_fato = [
    "Data da venda",
    "ID do cliente",
    "ID da promoção",
    "ID do produto",
    "Unidades vendidas",
    "Preço unitário (moeda local)",
    "Preço unitário (USD)",
    "Vendas brutas (moeda local)",
    "Vendas brutas (USD)",
    "Percentual aplicado à venda",
    "Valor do desconto (moeda local)",
    "Valor do desconto (USD)",
    "Vendas líquidas (USD)",
    "Lucro (USD)"
]

# Cria a tabela fato a partir da base tratada
fato_vendas = df_tratado[colunas_fato].copy()

# Define as colunas numéricas
colunas_numericas = [
    "Unidades vendidas",
    "Preço unitário (moeda local)",
    "Preço unitário (USD)",
    "Vendas brutas (moeda local)",
    "Vendas brutas (USD)",
    "Percentual aplicado à venda",
    "Valor do desconto (moeda local)",
    "Valor do desconto (USD)",
    "Vendas líquidas (USD)",
    "Lucro (USD)"
]

# Converte as colunas numéricas
# considerando a vírgula decimal da base original
for coluna in colunas_numericas:
    fato_vendas[coluna] = pd.to_numeric(
        fato_vendas[coluna].str.replace(
            ",", ".", regex=False
        ),
        errors="coerce"
    )

# Impede exportação se houver falhas na conversão
assert fato_vendas[colunas_numericas].notna().all().all(), \
    "Existem valores numéricos inválidos na tabela fato."

# Verifica a integridade das chaves das dimensões
for coluna, dimensao, chave in [
    ("ID do cliente", dim_clientes, "ID do cliente"),
    ("ID do produto", dim_produtos, "ID do produto"),
    ("ID da promoção", dim_promocoes, "ID da promoção")
]:
    assert fato_vendas[coluna].isin(dimensao[chave]).all(), \
        f"Existem chaves sem correspondência: {coluna}"

# Exporta a tabela fato
# decimal="," mantém o padrão decimal brasileiro
fato_vendas.to_csv(
    "dados/modelo/Fato_Vendas.csv",
    sep=";",
    decimal=",",
    index=False,
    encoding="utf-8-sig"
)

# Apresenta os resultados
print("\n=== TABELA FATO DE VENDAS ===")

print("Total de registros:", len(fato_vendas))
print("Total de colunas:", len(fato_vendas.columns))

print(
    "Vendas líquidas: US$",
    round(fato_vendas["Vendas líquidas (USD)"].sum(), 2)
)

print(
    "Lucro total: US$",
    round(fato_vendas["Lucro (USD)"].sum(), 2)
)

print(
    "Unidades vendidas:",
    fato_vendas["Unidades vendidas"].sum()
)

print("Tabela fato exportada com sucesso!")


# ==================================================
# ETAPA 19: TRADUÇÃO DE PRODUTOS E CATEGORIAS
# ==================================================

# Dicionário de tradução dos 30 produtos
# Os IDs originais serão preservados.

produtos_pt = {
    "P001": "Apple iPhone 14",
    "P002": "Samsung Galaxy S21",
    "P003": "TV Sony Bravia 55 Polegadas",
    "P004": "Notebook HP Pavilion",
    "P005": "MacBook Air Apple",
    "P006": "Tênis de Corrida Nike",
    "P007": "Tênis Casual Adidas",
    "P008": "Tênis Esportivo Puma",
    "P009": "Calça Jeans Levi's",
    "P010": "Camisa Casual Zara",
    "P011": "Camiseta H&M",
    "P012": "Túnica Kurta FabIndia",
    "P013": "Terno Raymond",
    "P014": "Mixer e Moedor Bajaj",
    "P015": "Fritadeira Elétrica Philips",
    "P016": "Máquina de Lavar LG",
    "P017": "Micro-ondas IFB",
    "P018": "Panela de Pressão Prestige",
    "P019": "Relógio de Pulso Titan",
    "P020": "Relógio Inteligente Fossil",
    "P021": "Marmita Tupperware",
    "P022": "Jogo de Copos Borosil",
    "P023": "Garrafa Térmica Milton",
    "P024": "Mochila Puma",
    "P025": "Mala de Viagem American Tourister",
    "P026": "Mochila de Trilha Wildcraft",
    "P027": "Shampoo L'Oréal",
    "P028": "Kit de Sabonetes Dove",
    "P029": "Creme Dental Colgate",
    "P030": "Loção Corporal Nivea"
}

# Dicionário de tradução das 8 categorias

categorias_pt = {
    "Electronics": "Eletrônicos",
    "Footwear": "Calçados",
    "Clothing": "Vestuário",
    "Home Appliances": "Eletrodomésticos",
    "Accessories": "Acessórios",
    "Kitchenware": "Utensílios de Cozinha",
    "Bags": "Bolsas e Mochilas",
    "Personal Care": "Cuidados Pessoais"
}

# Valida se todos os produtos possuem tradução
assert set(dim_produtos["ID do produto"]) == set(produtos_pt), \
    "A lista de traduções não corresponde aos produtos."

# Valida se todas as categorias possuem tradução
assert set(dim_produtos["Categoria do produto"]) <= set(categorias_pt), \
    "Existem categorias sem tradução."

# Aplica as traduções mantendo as colunas originais
dim_produtos["Nome do produto"] = (
    dim_produtos["ID do produto"].map(produtos_pt)
)

dim_produtos["Categoria do produto"] = (
    dim_produtos["Categoria do produto"].map(categorias_pt)
)

# Atualiza somente o CSV da dimensão de produtos
dim_produtos.to_csv(
    "dados/modelo/Dim_Produtos.csv",
    sep=";",
    index=False,
    encoding="utf-8-sig"
)

# Confere o resultado final
print("\n=== TRADUÇÃO CONCLUÍDA ===")
print("Produtos traduzidos:", len(dim_produtos))
print(
    "Categorias:",
    dim_produtos["Categoria do produto"].nunique()
)
print(dim_produtos.to_string(index=False))
