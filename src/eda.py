# %%

import pandas as pd

import seaborn as sns

import matplotlib.pyplot as plt

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

ds.info()

# %%

ds.head()

# %%

ds["Valor"] = ds["Valor"].str.strip()

ds[["Unit", "Valor($)"]] = ds["Valor"].str.split("$", expand = True)

ds["Valor($)"] = ds["Valor($)"].str.replace(",", "").astype("float")

ds.drop(["Unit", "Valor"], axis = 1, inplace = True)

# %%

ds["Data"] = pd.to_datetime(ds["Data"])

ds.info()

# %%
