import pandas as pd
import numpy as np
import os

def calcular_iae(df, iso_pais_origen, year=None):
    """
    Calcula el IAE (Índice de Afinidad Económica) y devuelve los 3 destinos
    más baratos para tu economia.
    
    Args:
        df (pd.DataFrame): DataFrame con los datos de PIB per cápita.
        iso_pais_origen (str): El código ISO3 del país de origen.
        year (int, optional): El año para el cálculo. Por defecto, usa el más reciente.

    Returns:
        list: Una lista de códigos ISO3 de los 3 mejores destinos.
        
    Raises:
        ValueError: Si el país de origen no se encuentra o no hay datos de PIB.
    """
    # 1. Limpiar los datos
    df_limpio = df.dropna(subset=["PIB per capital"]).copy()

    # 2. Validar el país de origen
    df_origen = df_limpio[df_limpio["ISO3"] == iso_pais_origen]
    if df_origen.empty:
        raise ValueError(f"❌ El país con código ISO3 '{iso_pais_origen}' no existe en el dataset.")

    # 3. Determinar el año a utilizar
    if year is None or year not in df_origen["Year"].unique():
        year = df_origen["Year"].max()
        print(f"⚠️ Usando el último año disponible para {iso_pais_origen}: {year}")

    # 4. Obtener el PIB per cápita del país de origen
    pib_origen_valor = df_origen[df_origen["Year"] == year]["PIB per capital"].values
    if not pib_origen_valor:
        raise ValueError(f"❌ No se encontró el PIB per cápita para {iso_pais_origen} en el año {year}.")
    pib_origen = pib_origen_valor[0]

    # 5. Filtrar el DataFrame para el año de interés
    df_year = df_limpio[df_limpio["Year"] == year].copy()

    # 6. Calcular el IAE
    df_year["IAE"] = pib_origen / df_year["PIB per capital"]

    # 7. Excluir el país de origen
    df_year = df_year[df_year["ISO3"] != iso_pais_origen]

    # 8. Ordenar y seleccionar los 3 mejores
    mejores_destinos = df_year.sort_values("IAE", ascending=False).head(3)
    
    # 9. Rellenar la lista si no hay 3 destinos
    top_destinos_list = mejores_destinos["ISO3"].tolist()
    while len(top_destinos_list) < 3:
        top_destinos_list.append(None)
    
    return top_destinos_list[:3]

def analizar_destinos_favorables(iso_pais_origen):
    """
    Realiza el análisis de IAE y muestra los 3 destinos más favorables para un país dado.

    Args:
        iso_pais_origen (str): El código ISO3 del país de origen para el análisis.
    """
    # Define la ruta al archivo
    file_path = "resultados.csv"

    # Verificar si el archivo combinado existe
    if not os.path.exists(file_path):
        print(f"Error: El archivo '{file_path}' no se encontró.")
        print("Por favor, asegúrate de que el archivo CSV combinado se haya generado y esté en la ruta correcta.")
        return

    try:
        # Cargar los datos desde el archivo CSV
        df = pd.read_csv(file_path)
        
        # Obtener los 3 destinos más favorables para el país de origen
        destinos = calcular_iae(df, iso_pais_origen)
        print(f"Top 3 destinos más baratos para un viajero de {iso_pais_origen}:")
        print(destinos)
        
    except Exception as e:
        print(f"Ocurrió un error al procesar los datos: {e}")

def get_top_3_months_with_holidays(codigo_pais):
    """
    Función que devuelve el top 3 de meses con IOI y UNA fecha festiva por mes
    """
    try:
        # Cargar el archivo con los datos de IOI
        df_ioi = pd.read_csv('IOI.csv')
        
        # Cargar el archivo de días festivos globales
        df_holidays = pd.read_csv('datos/global_holidays.csv')
        df_holidays['Date'] = pd.to_datetime(df_holidays['Date'])
        
        # Filtrar por el código del país en IOI
        df_pais_ioi = df_ioi[df_ioi['ISO3'] == codigo_pais].copy()
        
        if df_pais_ioi.empty:
            return f"No se encontraron datos de IOI para el país: {codigo_pais}"
        
        # Filtrar días festivos para el país (solo públicos)
        df_pais_holidays = df_holidays[
            (df_holidays['ISO3'] == codigo_pais) & 
            (df_holidays['Type'] == 'Public holiday')
        ].copy()
        
        if df_pais_holidays.empty:
            return f"No se encontraron días festivos para el país: {codigo_pais}"
        
        # Extraer día y mes de las fechas festivas
        df_pais_holidays['Day'] = df_pais_holidays['Date'].dt.day
        df_pais_holidays['Month'] = df_pais_holidays['Date'].dt.month
        
        # Ordenar por IOI descendente y tomar los top 3 meses
        top_3_meses = df_pais_ioi.nlargest(3, 'IOI')
        
        # Formatear los resultados
        resultado = f"Top 3 meses para {codigo_pais}:\n"
        resultado += "=" * 50 + "\n"
        
        for i, (_, row) in enumerate(top_3_meses.iterrows(), 1):
            mes = row['Month']
            mes_nombre = row['Month_Name']
            
            # Filtrar días festivos para este mes y tomar solo UNO
            festivos_mes = df_pais_holidays[df_pais_holidays['Month'] == mes]
            
            resultado += f"{i}. {mes_nombre}:\n"
            resultado += f"   • IOI: {row['IOI']:.2f}\n"
            resultado += f"   • Score Oportunidad: {row['Score_Oportunidad']:.2f}\n"
            resultado += f"   • Score Disponibilidad: {row['Avg_Score_Disponibilidad']:.2f}\n"
            
            if not festivos_mes.empty:
                # Tomar solo el primer festivo del mes
                festivo = festivos_mes.iloc[0]
                resultado += f"   • Festivo: {festivo['Name']} (Día {festivo['Day']})\n"
            else:
                resultado += f"   • Festivo: No hay días festivos registrados\n"
            
            resultado += "\n"
        
        return resultado
        
    except FileNotFoundError as e:
        return f"Error: No se encontró el archivo - {str(e)}"
    except Exception as e:
        return f"Error: {str(e)}"

def mostrar_paises_disponibles():
    """
    Función que muestra todos los países disponibles
    """
    try:
        df_ioi = pd.read_csv('IOI.csv')
        paises = sorted(df_ioi['ISO3'].unique())
        
        print("Países disponibles en el archivo IOI:")
        print("-" * 40)
        for i, pais in enumerate(paises, 1):
            print(f"{i}. {pais}")
        
        return paises
        
    except FileNotFoundError:
        print("Error: No se encontró el archivo IOI_paises_filtrados.csv")
        return []
    except Exception as e:
        print(f"Error: {str(e)}")
        return []

def calcular_iae(df, iso_pais_origen, year=None):
    """
    Calcula el IAE (Índice de Afinidad Económica) y devuelve los 3 destinos
    más favorables.
    
    Args:
        df (pd.DataFrame): DataFrame con los datos de PIB per cápita.
        iso_pais_origen (str): El código ISO3 del país de origen.
        year (int, optional): El año para el cálculo. Por defecto, usa el más reciente.

    Returns:
        list: Una lista de códigos ISO3 de los 3 mejores destinos.
        
    Raises:
        ValueError: Si el país de origen no se encuentra o no hay datos de PIB.
    """
    # 1. Limpiar los datos
    df_limpio = df.dropna(subset=["PIB per capital"]).copy()

    # 2. Validar el país de origen
    df_origen = df_limpio[df_limpio["ISO3"] == iso_pais_origen]
    if df_origen.empty:
        raise ValueError(f"❌ El país con código ISO3 '{iso_pais_origen}' no existe en el dataset.")

    # 3. Determinar el año a utilizar
    if year is None or year not in df_origen["Year"].unique():
        year = df_origen["Year"].max()
        print(f"⚠️ Usando el último año disponible para {iso_pais_origen}: {year}")

    # 4. Obtener el PIB per cápita del país de origen
    pib_origen_valor = df_origen[df_origen["Year"] == year]["PIB per capital"].values
    if not pib_origen_valor:
        raise ValueError(f"❌ No se encontró el PIB per cápita para {iso_pais_origen} en el año {year}.")
    pib_origen = pib_origen_valor[0]

    # 5. Filtrar el DataFrame para el año de interés
    df_year = df_limpio[df_limpio["Year"] == year].copy()

    # 6. Calcular el IAE
    df_year["IAE"] = pib_origen / df_year["PIB per capital"]

    # 7. Excluir el país de origen
    df_year = df_year[df_year["ISO3"] != iso_pais_origen]

    # 8. Ordenar y seleccionar los 3 mejores
    mejores_destinos = df_year.sort_values("IAE", ascending=False).head(3)
    
    # 9. Rellenar la lista si no hay 3 destinos
    top_destinos_list = mejores_destinos["ISO3"].tolist()
    while len(top_destinos_list) < 3:
        top_destinos_list.append(None)
    
    return top_destinos_list[:3]

def obtener_nombre_pais(iso_code):
    """
    Obtiene el nombre del país a partir de su código ISO3.

    Args:
        iso_code (str): Código ISO3 del país (ej. 'AUS', 'USA', etc.)

    Returns:
        str: Nombre del país o None si no se encuentra
    """
    file_path = "datos/resultados.csv"  
    
    # Verificar si el archivo existe
    if not os.path.exists(file_path):
        print(f"Error: El archivo '{file_path}' no se encontró.")
        return None
    
    try:
        # Leer el archivo CSV
        df = pd.read_csv(file_path)
        
        # Buscar el código ISO3 en la columna 'IS03'
        pais = df[df['ISO3'] == iso_code]
        
        if not pais.empty:
            # Obtener el primer nombre de país encontrado
            nombre_pais = pais['System'].iloc[0]
            return nombre_pais
        else:
            print(f"No se encontró el país con código ISO3: {iso_code}")
            return None
            
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        return None
    
def analizar_destinos_favorables(iso_pais_origen):
    """
    Realiza el análisis de IAE y muestra los 3 destinos más favorables para un país dado.

    Args:
        iso_pais_origen (str): El código ISO3 del país de origen para el análisis.
    """
    # Define la ruta al archivo
    file_path = "datos/resultados.csv"

    # Verificar si el archivo combinado existe
    if not os.path.exists(file_path):
        print(f"Error: El archivo '{file_path}' no se encontró.")
        print("Por favor, asegúrate de que el archivo CSV combinado se haya generado y esté en la ruta correcta.")
        return

    try:
        # Cargar los datos desde el archivo CSV
        df = pd.read_csv(file_path)
        
        # Obtener los 3 destinos más favorables para el país de origen
        destinos = calcular_iae(df, iso_pais_origen)
        print(f"Top 3 destinos más favorables para un viajero de {iso_pais_origen}:")
        for codigo in destinos:
            nombre_pais = obtener_nombre_pais(codigo)
            print(nombre_pais)
        
    except Exception as e:
        print(f"Ocurrió un error al procesar los datos: {e}")

# PROGRAMA PRINCIPAL
if __name__ == "__main__":
    print("=== TOP 3 MESES CON UN DÍA FESTIVO POR PAÍS ===")
    print()
    
    # Mostrar países disponibles
    paises_disponibles = mostrar_paises_disponibles()
    
    if not paises_disponibles:
        exit()
    
    print()
    
    while True:
        print("\nOpciones:")
        print("1. Buscar top 3 meses con un festivo para un país específico")
        print("2. Salir")
        
        opcion = input("\nSelecciona una opción (1-2): ").strip()
        
        if opcion == '1':
            # Pedir código del país
            codigo_pais = input("\nIngresa el código del país: ").strip()
            
            # Obtener y mostrar resultados
            resultado = get_top_3_months_with_holidays(codigo_pais)
            print("\n" + resultado)
            
            analizar_destinos_favorables(codigo_pais)
            
        elif opcion == '2':
            print("¡Hasta luego!")
            break
            
        else:
            print("Opción no válida. Por favor, selecciona 1, 2 o 3.")