# %%

import pandas as pd

import plotly.express as px

import warnings

warnings.filterwarnings("ignore")

# %%

nomes = ["Vendedor", 
         "Pais", 
         "Produto", 
         "Data", 
         "Valor", 
         "Caixas Enviadas"]

schema = {"Vendedor": str, 
        "Pais": "category", 
        "Produto": "category", 
        "Data": str, 
        "Valor": str, 
        "Caixas Enviadas" : int}

ds = pd.read_csv("../data/chocolate_sales.csv", header = 0, names = nomes, dtype = schema)

print("Resumo do dataset:")

print(ds.info())

print("\nEstatísticas gerais:")

print(ds.describe())

print("\nValores ausentes:")

print(ds.isnull().sum())

# %%

ds.head()

# %%

ds["Valor"] = ds["Valor"].str.strip()

ds[["Unit", "Valor($)"]] = ds["Valor"].str.split("$", expand = True)

ds["Valor($)"] = ds["Valor($)"].str.replace(",", "").astype("int")

ds.drop(["Unit", "Valor"], axis = 1, inplace = True)

# %%

ds["Data"] = pd.to_datetime(ds["Data"])

ds.info()

# %%

ds["Ano"] = ds["Data"].dt.year

ds["Mes"] = ds["Data"].dt.month_name()

# %%

def vlr_total(dados):

    valor_total = dados["Valor($)"].sum()

    valor_total = f"${valor_total:,.2f}"

    return valor_total

# %%

def ticket_medio(dados):

    vnds_totais = len(list(dados.index))

    tck_medio = round(((dados["Valor($)"].sum())/ vnds_totais), 2)

    tck_medio = f"${tck_medio:,.2f}"

    return tck_medio

# %%

def caixas_totais(dados):

    cx_totais = dados["Caixas Enviadas"].sum()

    cx_totais = f"{cx_totais:,}".replace(",", ".")

    return cx_totais

# %%

vnd_pais = ds.groupby("Pais", as_index = False)["Valor($)"].sum().sort_values(by = "Valor($)",ascending = False)

vnd_pais["Valor($)"] = round((vnd_pais["Valor($)"]/1000000), 2)

grfc_pais = px.bar(
    data_frame = vnd_pais,
    x = "Valor($)",
    y = "Pais",
    color = "Pais",
    color_discrete_sequence = px.colors.qualitative.Pastel)

grfc_pais.update_layout(
    title = "Vendas por Países em Milhões ($)",
    template = "plotly",
    margin = dict(l = 50, r = 50, b = 50, t = 50),
    xaxis_title = "Valor das Vendas ($)",
    yaxis_title = "",
    showlegend = False)

grfc_pais.show()

# %%
