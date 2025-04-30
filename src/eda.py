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

def formata_dataset(dados):

    dados["Valor"] = dados["Valor"].str.strip()

    dados[["Unit", "Valor($)"]] = dados["Valor"].str.split("$", expand = True)

    dados["Valor($)"] = dados["Valor($)"].str.replace(",", "").astype("int")

    dados.drop(["Unit", "Valor"], axis = 1, inplace = True)

    ds["Data"] = pd.to_datetime(ds["Data"])

    ds["Ano"] = ds["Data"].dt.year()

    ds["Mes"] = ds["Data"].dt.month_name()

    ordem_meses = ["January", 
                "February", 
                "March", 
                "April", 
                "May", 
                "June",
                "July", 
                "August"]

    ds["Mes"] = pd.Categorical(
                    ds["Mes"], 
                    categories = ordem_meses, 
                    ordered = True)

    return dados

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

def grafico_pais(dados):

    vnd_pais = dados.groupby("Pais", as_index = False)["Valor($)"].sum().sort_values(by = "Valor($)",ascending = False)

    vnd_pais["Valor($)"] = round((vnd_pais["Valor($)"]/1000000), 2)

    grfc_pais = px.bar(
        data_frame = vnd_pais,
        x = "Valor($)",
        y = "Pais",
        text = "Valor($)",
        color = "Pais",
        color_discrete_sequence = px.colors.qualitative.Pastel)

    grfc_pais.update_traces(
        textposition = "outside",
        texttemplate = "$ %{x:.2f}M") 

    grfc_pais.update_layout(
        title = "Faturamento por Países em Milhões ($)",
        template = "plotly",
        margin = dict(l = 50, r = 50, b = 50, t = 50),
        xaxis_title = "",
        yaxis_title = "",
        showlegend = False,
        xaxis_tickformat = ".1f",
        xaxis_ticksuffix = "M",
        xaxis = dict(range = [0, (vnd_pais["Valor($)"].max() * 1.5)]))

    return grfc_pais

# %%

def grafico_mes(dados):

    vnds_mes = dados.groupby("Mes", as_index = False)["Valor($)"].sum()

    vnds_mes["Valor($)"] = vnds_mes["Valor($)"] / 1000

    grfc_mes = px.bar(
        data_frame = vnds_mes,
        x = "Valor($)",
        y = "Mes",
        text = "Valor($)",
        color = "Mes",
        color_discrete_sequence = px.colors.qualitative.Pastel)

    grfc_mes.update_traces(
        textposition = "outside",
        texttemplate = "$ %{x:.0f}k",
        cliponaxis = False) 

    grfc_mes.update_layout(
        title = "Faturamento por Mensal ($)",
        template = "plotly",
        margin = dict(l = 50, r = 50, b = 50, t = 50),
        xaxis_title = "",
        yaxis_title = "",
        showlegend = False,
        xaxis_tickformat = "0.f",
        xaxis_ticksuffix = "k",
        xaxis = dict(range = [0, 1000],
                    dtick = 200))

    return grfc_mes


# %%
