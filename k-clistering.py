import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os

try:
    df_original = pd.read_csv('datos/average_annual_passengers.csv')
except FileNotFoundError:
    print("Error: El archivo 'average_annual_passengers.csv' no se encuentra.")
    print("Asegúrate de que el archivo está en la misma carpeta que el script.")
    exit()

# Crear un DataFrame para los datos incompletos
df_indefinido = df_original[df_original.isnull().any(axis=1)].copy()
df_indefinido['Categoria'] = 'Indefinido'

# Crear un DataFrame para los datos completos
df_completo = df_original.dropna().copy()

print("Datos completos encontrados:", df_completo.shape[0])
print("Datos indefinidos encontrados:", df_indefinido.shape[0])

# Paso 2: Estandarizar los datos completos
X_completo = df_completo[['Promedio_Pasajeros_Internacionales', 'Promedio_Pasajeros_Nacionales']]
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_completo)

# Método del codo para determinar k óptimo
print("\nCalculando método del codo para determinar k óptimo...")
inertia = []
k_range = range(1, 11)

for k in k_range:
    kmeans = KMeans(n_clusters=k, init='k-means++', max_iter=300, n_init=10, random_state=42)
    kmeans.fit(X_scaled)
    inertia.append(kmeans.inertia_)

# Crear directorio para gráficas si no existe
if not os.path.exists('graficas_clustering'):
    os.makedirs('graficas_clustering')

# Gráfica del método del codo
plt.figure(figsize=(10, 6))
plt.plot(k_range, inertia, 'bo-')
plt.xlabel('Número de clusters (k)')
plt.ylabel('Inercia')
plt.title('Método del Codo para Determinar k Óptimo')
plt.xticks(k_range)
plt.grid(True, alpha=0.3)
plt.savefig('graficas_clustering/metodo_codo.png', dpi=300, bbox_inches='tight')
plt.close()
print("Gráfica del método del codo guardada en 'graficas_clustering/metodo_codo.png'")

# Paso 3: Aplicar K-Means con k=3 y categorizar
kmeans = KMeans(n_clusters=3, init='k-means++', max_iter=300, n_init=10, random_state=42)
df_completo['Categoria'] = kmeans.fit_predict(X_scaled)

# Asignar nombres a las categorías basados en los centroides
centroids_original = scaler.inverse_transform(kmeans.cluster_centers_)

hogareno_cluster = np.argmax(centroids_original[:, 0])
internacional_cluster = np.argmax(centroids_original[:, 1])
mixto_cluster = [i for i in range(3) if i not in [internacional_cluster, hogareno_cluster]][0]

df_completo['Categoria'] = df_completo['Categoria'].map({
    internacional_cluster: 'Internacional',
    hogareno_cluster: 'Hogareño',
    mixto_cluster: 'Mixto'
})

# Gráfica de los clusters
plt.figure(figsize=(10, 8))
colors = {'Internacional': 'red', 'Hogareño': 'blue', 'Mixto': 'green'}
scatter = plt.scatter(df_completo['Promedio_Pasajeros_Internacionales'], 
                     df_completo['Promedio_Pasajeros_Nacionales'], 
                     c=df_completo['Categoria'].map(colors), 
                     alpha=0.6, s=50)

# Plot centroides
centroids_df = pd.DataFrame(centroids_original, 
                           columns=['Promedio_Pasajeros_Internacionales', 'Promedio_Pasajeros_Nacionales'])
centroids_df['Categoria'] = ['Internacional', 'Hogareño', 'Mixto']
plt.scatter(centroids_df['Promedio_Pasajeros_Internacionales'], 
           centroids_df['Promedio_Pasajeros_Nacionales'], 
           c=centroids_df['Categoria'].map(colors), 
           s=200, marker='X', edgecolors='black', linewidth=2)

plt.xlabel('Promedio Pasajeros Internacionales')
plt.ylabel('Promedio Pasajeros Nacionales')
plt.title('Clustering de Países por Patrón de Viajeros\n(k=3 clusters)')
plt.legend(handles=[plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color, 
                              markersize=10, label=cat) 
                   for cat, color in colors.items()])
plt.grid(True, alpha=0.3)
plt.savefig('graficas_clustering/clusters_k3.png', dpi=300, bbox_inches='tight')
plt.close()
print("Gráfica de clusters guardada en 'graficas_clustering/clusters_k3.png'")

# Paso 4: Unir los datos completos e indefinidos
df_final = pd.concat([df_completo, df_indefinido], ignore_index=True)
df_final['Categoria'] = df_final['Categoria'].fillna('Indefinido')

# Paso 5: Seleccionar las columnas finales y exportar a CSV
df_final_resultado = df_final[['ISO3', 'Year', 'Categoria']]

print("\nVista previa del resultado final:")
print(df_final_resultado.head(10))
print("\nConteo de categorías:")
print(df_final_resultado['Categoria'].value_counts())

# Exportar a CSV
df_final_resultado.to_csv('resultado_categorizacion_iso.csv', index=False)
print("\n¡Proceso completado! El archivo 'resultado_categorizacion_iso.csv' ha sido creado.")
