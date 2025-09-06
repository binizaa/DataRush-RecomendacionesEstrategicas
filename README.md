# 🌍 ¿Cómo se relaciona la salud económica con los hábitos de viaje de sus ciudadanos?

Este programa en **Python** permite analizar información económica y de días festivos de distintos países para recomendar:

1. Los **Top 3 destinos más favorables** para un país, basados en el **Índice de Afinidad Económica (IAE)** y que es más probable a consumir (internacionalmente o nacionalmente), basandonos en PIB de cada país.
2. Los **Top 3 meses con mayor oportunidad de viaje**, incluyendo al menos **un día festivo por mes**.

## Video
[link](https://youtu.be/icPNIkfCbuU)
---

## 📂 Archivos requeridos

Para que el programa funcione correctamente, necesitas tener los siguientes archivos en tu proyecto:

* `datos/resultados.csv` → Contiene datos de PIB per cápita por país y año.
* `datos/global_holidays.csv` → Contiene los días festivos públicos de varios países.
* `IOI.csv` → Archivo con el **Índice de Oportunidad de Intercambio (IOI)** por país y mes.

⚠️ **Nota importante**: asegúrate de que las rutas y nombres de archivo coincidan exactamente, ya que el código los busca en las carpetas `datos/` y raíz del proyecto.

---

## ⚙️ Instalación

1. Clona este repositorio o descarga los archivos en tu computadora.
2. Instala las dependencias necesarias (se recomienda usar un entorno virtual):

```bash
pip install pandas numpy
```

---

## ▶️ Cómo ejecutar el programa

1. Abre una terminal en la carpeta donde se encuentra el archivo principal `.py`.
2. Ejecuta el programa con:

```bash
python main.py
```

---

## 🖥️ Uso del programa

Cuando lo ejecutes, verás un menú interactivo:

```
=== TOP 3 MESES CON UN DÍA FESTIVO POR PAÍS ===

Países disponibles en el archivo IOI:
----------------------------------------
1. ARG
2. MEX
3. USA
...

Opciones:
1. Buscar top 3 meses con un festivo para un país específico
2. Salir
```

* **Opción 1:** Ingresa el código ISO3 de un país (ejemplo: `MEX`) para obtener:

  * Top 3 meses con IOI más alto y un día festivo por mes.
  * Top 3 destinos más favorables según el IAE para ese país.

* **Opción 2:** Salir del programa.

---

## 📌 Funcionalidades principales

* `calcular_iae(df, iso_pais_origen, year=None)` → Calcula los 3 destinos más favorables para un país.
* `get_top_3_months_with_holidays(codigo_pais)` → Devuelve los 3 mejores meses con al menos un día festivo.
* `mostrar_paises_disponibles()` → Muestra todos los países disponibles en el dataset IOI.
* `obtener_nombre_pais(iso_code)` → Devuelve el nombre de un país a partir de su código ISO3.

---

## 💡 Recomendaciones

* Mantén los archivos CSV actualizados con los últimos datos de PIB y días festivos.
* Asegúrate de que los nombres de las columnas en los CSV coincidan con los esperados en el código.
* Usa un entorno virtual para evitar conflictos con otras versiones de Python o librerías.

---

## 📄 Licencia

Este proyecto es de uso educativo y libre para análisis de datos y aprendizaje de Python.
