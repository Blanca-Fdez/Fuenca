# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import cartopy.crs as ccrs



"""""
  Datos Fuencaliente - Ejercicio 2

  Author: Blanca Fernández Álvarez
"""
# Cargar los datos desde el archivo txt
df = pd.read_csv('C:/Users/blanc/OneDrive/Desktop/ExeclDatosFuenca.csv', delimiter=';')

df["Estacion"] = df["Estacion"].astype(str)

df = df.replace('---', float('nan'))

# Convertir la columna "mmol/kgSW O2" a tipo numérico
df["mmol/kgSW O2"] = pd.to_numeric(df["mmol/kgSW O2"], errors="coerce")

# Calcular la media por estación y marea para cada variable
medias = ["CT (micromol/kgSW)", "mmol/kgSW O2"]
for media in medias:
    # Calcular la media y restablecer el índice para que sea un DataFrame
    media_por_estacion_marea = df.groupby(["Estacion", "Tide"])[media].mean().reset_index()
    
df = pd.merge(df, media_por_estacion_marea, on=["Estacion", "Tide"], how="left", suffixes=('', '_media'))
df = df.dropna(subset=["Salinidad"])

# Cambiar el nombre a la columna mal nombrada
df["AT"] = df["CT (micromol/kgSW)"]

# Normalizar la alcalinidad a la media de salinidad
df['NAT'] = df["AT"]/df["Salinidad"]*df["Salinidad"].mean()

# Graficar NAT frente a Salinidad
plt.figure(figsize=(10, 6))
plt.scatter(df['Salinidad'], df['NAT'], color='#5E31A8')

# Ajustar una línea de tendencia (polinomio de grado 1)
p = np.polyfit(df['Salinidad'], df['NAT'], 1)
plt.plot(df['Salinidad'], np.polyval(p, df['Salinidad']), color='#5E31A8', linestyle='dashed',
         label=f'Línea de tendencia: Y = {p[0]:.2f}X + {p[1]:.2f}')

pendiente = p[0]
ordenada_origen = p[1]

plt.title('Alcalinidad total normalizada vs. Salinidad')
plt.xlabel('Salinidad (PSS)')
plt.ylabel('Alcalinidad Total (µmol/kgSW)')
plt.legend()
plt.grid(True)
plt.show()

# plt.savefig('C:/Users/blanc/OneDrive/Desktop/Master/CO2 y Adificación/Tendencia.png', dpi = 300)

# cargar el txt de los datos en continuo
AAQ = pd.read_csv('C:/Users/blanc/OneDrive/Desktop/Master/CO2 y Adificación/CO2_david/GPS_AAQ_pCO2_20240206.txt', delimiter=';')

#CAlcular la alcalinidad mediante la gráfica de tendencia anterior
AAQ['Alcalinidad_sal'] = AAQ['Salinity']*pendiente+ordenada_origen


# Normalizar la alcalinidad (NAT) - a la media de las salinidades de los datos
AAQ['NATs'] = AAQ["Alcalinidad_sal"]/AAQ["Salinity"]*AAQ["Salinity"].mean()

# Cargar la alcalinidad obtenida mediante el Co2Sys
Alcalinidad_CO2sys = pd.read_csv('C:/Users/blanc/OneDrive/Desktop/Master/CO2 y Adificación/CO2_david/Alco2.csv', delimiter=';')

AAQ['Alcalinidad_CO2sys'] = Alcalinidad_CO2sys
AAQ['NATco2'] = AAQ["Alcalinidad_CO2sys"]/AAQ["Salinity"]*AAQ["Salinity"].mean()

#Incluimos los datos calculados con el CO2sys: pH, pH25, fCo2, Wca, War y CT
Co2sys = pd.read_csv('C:/Users/blanc/OneDrive/Desktop/Master/CO2 y Adificación/CO2_david/sys.csv', delimiter=';')

#Unimos ambas df
AAQ = pd.merge(AAQ, Co2sys)

######## PLOT

# Extraer las variables de latitud, longitud y las que deseas visualizar en el mapa
latitudes = AAQ['Latitude']
longitudes = AAQ['Longitude']
variable_a_visualizar = AAQ['WAr in'] 
 

# Crear una figura y un eje con proyección Mercator
plt.figure(figsize=(10, 8))
ax = plt.axes(projection=ccrs.Mercator())

# Agregar los datos al mapa como puntos
scatter = ax.scatter(longitudes, latitudes, c=variable_a_visualizar, cmap='BuPu', transform=ccrs.PlateCarree(), s=10)

# Add gridlines
gl = ax.gridlines(draw_labels=True)

gl.xlabels_top = False
gl.ylabels_right = False

# Añadir una barra de color para la variable visualizada
cbar = plt.colorbar(scatter, ax=ax, orientation='vertical', fraction=0.05, extend="max")
cbar.set_label('$\omega_Ar$')

# Añadir título y etiquetas de los ejes
plt.title("$\omega$ Aragonita", loc="left")
plt.xlabel('Longitud')
plt.ylabel('Latitud')

# Mostrar el mapa
plt.show()
