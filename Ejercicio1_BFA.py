# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import pandas as pd
import string
from matplotlib.ticker import AutoMinorLocator

"""""
  Datos discretos Fuencaliente - Ejercicio 1

  Author: Blanca Fernández Álvarez
"""

# Cargar los datos desde el archivo txt
df = pd.read_csv('../ExeclDatosFuenca.csv', delimiter=';')

df["Estacion"] = df["Estacion"].astype(str)

df = df.replace('---', float('nan'))

# Convertir la columna "mmol/kgSW O2" a tipo numérico
df["mmol/kgSW O2"] = pd.to_numeric(df["mmol/kgSW O2"], errors="coerce")

# Filtrar los datos por estaciones y marea
estaciones_lon = df[df["Estacion"].isin(["4", "1", "2", "3"])]
estaciones_lat = df[df["Estacion"].isin(["1", "5", "6"])]

# Calcular la media por estación y marea para cada variable
medias = ["CT (micromol/kgSW)", "mmol/kgSW O2"]
for media in medias:
    # Calcular la media y restablecer el índice para que sea un DataFrame
    media_por_estacion_marea = df.groupby(["Estacion", "Tide"])[media].mean().reset_index()
    
    # Fusionar los DataFrames con los datos de la media calculada
    estaciones_lon = pd.merge(estaciones_lon, media_por_estacion_marea, on=["Estacion", "Tide"], how="left", suffixes=('', '_media'))
    estaciones_lat = pd.merge(estaciones_lat, media_por_estacion_marea, on=["Estacion", "Tide"], how="left", suffixes=('', '_media'))

# Eliminar filas donde la salinidad sea nan
estaciones_lon = estaciones_lon.dropna(subset=["Salinidad"])
estaciones_lat = estaciones_lat.dropna(subset=["Salinidad"])

# Cambiar el orden de las estaciones
estaciones_lon["Orden"] = estaciones_lon["Estacion"].map({"4": 0, "1": 1, "2": 2, "3": 3})
estaciones_lon = estaciones_lon.sort_values(by="Orden")
estaciones_lon = estaciones_lon.drop("Orden", axis=1)

# Crear subplots para cada conjunto de estaciones y marea
fig, axs = plt.subplots(2, 3, figsize=(16, 10))

# Configurar títulos de las columnas
letras = string.ascii_uppercase
letras_A_F = letras[:6]
enumeracion_A_F = [f"{letra}" for letra in letras_A_F]

# Configuración de las etiquetas del eje y
ylabel = ['AT (µmol/kgSW)', 'O$_2$ (mmol/kgSW)', 'pH']
minor_locator_y = AutoMinorLocator(2)

# Configuración de etiquetas de ejes y estilo de la cuadrícula
for ax_row in axs:
    for ax in ax_row:
        ax.set_xlabel('Estación')
        ax.grid(which='both', linestyle='--', linewidth=0.5)
        ax.yaxis.set_minor_locator(minor_locator_y)  # Configurar minor ticks en el eje y
        
# Estaciones 4, 1, 2 y 3
for tide, data in estaciones_lon.groupby("Tide"):
    for i, media in enumerate(["CT (micromol/kgSW)_media", "mmol/kgSW O2_media", "pH"]):
        ax = axs[0, i]
        ax.scatter(data["Estacion"], data[media], label=f"{tide}")
        ax.set_title(f'{enumeracion_A_F[i]}', loc='left')
        ax.set_ylabel(f'{ylabel[i]}')
        ax.legend()
        axs[0, 2].legend(loc = 'lower right')


# Estaciones 1, 5 y 6
for tide, data in estaciones_lat.groupby("Tide"):
    for i, media in enumerate(["CT (micromol/kgSW)_media", "mmol/kgSW O2_media", "pH"]):
        ax = axs[1, i]
        ax.scatter(data["Estacion"], data[media], label=f"{tide}")
        ax.set_title(f'{enumeracion_A_F[i+3]}', loc='left')
        ax.set_ylabel(f'{ylabel[i]}')
        ax.legend()
        

plt.tight_layout()
plt.show()
plt.savefig('./Desktop/Estaciones.png', dpi = 300)


