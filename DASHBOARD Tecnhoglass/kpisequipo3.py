import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from analisis_publicidad import cargar_datos, ordenar_periodos, calcular_porcentaje_aumento, graficar_barras
def dashboard_objetivo_3():

    # Usar las funciones individualmente
    archivo_csv = 'files/Datos_Agrupados_Por_Periodo.csv'
    df = pd.read_csv(archivo_csv)
    orden_periodos = ['Pre-Publicidad', 'Durante Publicidad', 'Post-Publicidad']

    # Llamar funciones específicas
    datos = cargar_datos(archivo_csv)
    datos_ordenados = ordenar_periodos(datos, orden_periodos)
    comparacion = calcular_porcentaje_aumento(datos_ordenados)

    # Dividir en columnas con mayor separación
    col1, col2, col3= st.columns([3,3,3])  # Ajustar los anchos de las columnas

    # Primera columna: gráfica de barras
    with col1:
        st.write("**KPI 1:  Porcentaje de Incremento en el alcance durante el pago de publicidad.**")
        st.write("***Fórmulas utilizadas:***")
        st.write("1. Diferencia de Alcance= Alcance con Publicidad−Alcance Sin Publicidad", "\n", "2. Porcentaje de Incremento= (diferencia de alcance / alcance sin publicidad) x 100")
        graficar_barras(datos_ordenados, comparacion, orden_periodos)  # Mostrar la gráfica
        st.write("***Las variables utilizadas fueron:***")
        st.table(pd.DataFrame({
            "Variable": ["Periodo", "Red de alcance", "Cantidad"],
            "Descripción": [
                "Clasifica las fechas en los periodos Pre-Publicidad (09/09/2024 - 21/10/2024), Durante Publicidad (22/10/2024 - 27/10/2024) y Post-Publicidad (28/10/2024 - 15/11/2024).",
                "Muestra a qué red social pertenece el alcance.",
                "Muestra la cantidad de alcance alcance por día independientemente de la publicación."
            ]
        }))
        st.write("***Interpretaciones:***")
        st.write("La gráfica muestra que el alcance incrementó un 683% en Facebook y 338% en Instagram respecto al promedio del periodo orgánico. "
                 "***El periodo de publicidad pagada superó el 20% esperado en un 663% en Facebook y 318% en instagram.***",
                 "Cabe mencionar que la cantidad de datos en cada periodo difiere significativamente, ya que solo se pagaron 5 días de publicidad, lo cual puede afectar la exactitud de los resultados.", "\n")

    with col2:

        # Cargar los datos
        data = pd.read_csv("files/KPIS_PUBLICIDAD - ventas x mayoreo.csv")

        # Convertir la columna de fecha a formato datetime
        data['Fecha de venta'] = pd.to_datetime(data['Fecha de venta'], format='%d/%m/%Y')

        # Crear una columna que indique si la venta tiene publicidad pagada
        data['Publicidad'] = data['Publicidad'].apply(lambda x: 'Pagada' if x == 'Pagada' else 'No pagada')

        fecha_inicio = pd.to_datetime('2024-10-22')
        fecha_fin = pd.to_datetime('2024-10-27')

        # Filtrar ventas antes y después de la publicidad
        ventas_previas = data[data['Fecha de venta'] < fecha_inicio]
        ventas_posteriores = data[data['Fecha de venta'] >= fecha_inicio]

        # Calcular el total de ventas con y sin publicidad
        ventas_previas_sin_publicidad = ventas_previas[ventas_previas['Publicidad'] == 'No pagada']['Precio'].sum()
        ventas_previas_con_publicidad = ventas_previas[ventas_previas['Publicidad'] == 'Pagada']['Precio'].sum()

        ventas_posteriores_sin_publicidad = ventas_posteriores[ventas_posteriores['Publicidad'] == 'No pagada'][
            'Precio'].sum()
        ventas_posteriores_con_publicidad = ventas_posteriores[ventas_posteriores['Publicidad'] == 'Pagada']['Precio'].sum()

        # Calcular el KPI de cambio porcentual
        if ventas_previas_sin_publicidad != 0:  # Evitar división por cero
            porcentaje_cambio = (
                                        ventas_posteriores_con_publicidad - ventas_previas_con_publicidad) / ventas_previas_sin_publicidad * 100
        else:
            porcentaje_cambio = 0

        # Mostrar resultados en Streamlit
        st.write(
            "***KPI 2: Comparación de ventas previas y posteriores a la implementación de publicidad pagada, total de ventas con y sin publicidad pagada.***")
        st.write("***Fórmula utilizada:***")
        st.write(
            "1. (Ventas posteriores con publicidad - Ventas previas a la publicidad) / Ventas previas sin publicidad * 100")

        tabla_resultados = pd.DataFrame({
            "Tipo de Venta": ["Previas con Publicidad", "Previas sin Publicidad", "Posteriores con Publicidad",
                              "Posteriores sin Publicidad"],
            "Total de Ventas ($)": [ventas_previas_con_publicidad, ventas_previas_sin_publicidad,
                                    ventas_posteriores_con_publicidad, ventas_posteriores_sin_publicidad],
            "Porcentaje (%)": [
                (ventas_previas_con_publicidad / (ventas_previas_con_publicidad + ventas_previas_sin_publicidad)) * 100 if (
                                                                                                                                       ventas_previas_con_publicidad + ventas_previas_sin_publicidad) != 0 else 0,
                (ventas_previas_sin_publicidad / (ventas_previas_con_publicidad + ventas_previas_sin_publicidad)) * 100 if (
                                                                                                                                       ventas_previas_con_publicidad + ventas_previas_sin_publicidad) != 0 else 0,
                (ventas_posteriores_con_publicidad / (
                            ventas_posteriores_con_publicidad + ventas_posteriores_sin_publicidad)) * 100 if (
                                                                                                                         ventas_posteriores_con_publicidad + ventas_posteriores_sin_publicidad) != 0 else 0,
                (ventas_posteriores_sin_publicidad / (
                            ventas_posteriores_con_publicidad + ventas_posteriores_sin_publicidad)) * 100 if (
                                                                                                                         ventas_posteriores_con_publicidad + ventas_posteriores_sin_publicidad) != 0 else 0,
            ]
        })

        # Crear el menú desplegable
        opcion = st.selectbox("Selecciona el KPI que deseas visualizar:", ["KPI 2.1", "KPI 2.2"])

        if opcion == "KPI 2.1":
            # Filtrar ventas antes y después de la publicidad
            fecha_inicio = pd.to_datetime('2024-10-22')
            fecha_fin = pd.to_datetime('2024-10-27')

            ventas_previas = data[data['Fecha de venta'] < fecha_inicio]
            ventas_posteriores = data[data['Fecha de venta'] >= fecha_inicio]

            # Calcular el total de ventas con y sin publicidad
            ventas_previas_sin_publicidad = ventas_previas[ventas_previas['Publicidad'] == 'No pagada']['Precio'].sum()
            ventas_previas_con_publicidad = ventas_previas[ventas_previas['Publicidad'] == 'Pagada']['Precio'].sum()
            ventas_posteriores_sin_publicidad = ventas_posteriores[ventas_posteriores['Publicidad'] == 'No pagada'][
                'Precio'].sum()
            ventas_posteriores_con_publicidad = ventas_posteriores[ventas_posteriores['Publicidad'] == 'Pagada'][
                'Precio'].sum()

            # Graficar
            fig, ax = plt.subplots()
            ax.bar(['Previas', 'Posteriores'], [ventas_previas_con_publicidad, ventas_posteriores_con_publicidad],
                   color='orange', label='Ventas con publicidad')
            ax.bar(['Previas', 'Posteriores'], [ventas_previas_sin_publicidad, ventas_posteriores_sin_publicidad],
                   color='blue',
                   label='Ventas sin publicidad', alpha=0.7)

            ax.set_ylabel('Ventas ($)')
            ax.set_title('Comparación de Ventas: Sin publicidad aplicada vs Con publicidad aplicada')
            ax.legend()

            # Mostrar la gráfica en Streamlit
            st.pyplot(fig)

            st.write("***Las variables utilizadas fueron:***")
            st.table(pd.DataFrame({
                "Variables": ["Ventas previas sin publicidad", "Ventas posteriores con publicidad", "Ventas posteriores sin publicidad"],
                "Descripción": [
                    "Ventas realizadas antes de implementar publicidad pagada.",
                    "Ventas realizadas despúes de implementar publicidad pagada.",
                    "Ventas realizadas despues de terminar el periodo de publicidad pagada."

                ]
            }))

            st.write("Distribución de Ventas: Comparación con y sin Publicidad")
            st.table(tabla_resultados)

            st.write("***Interpretación:***")
            st.write(
                "La gráfica compara las ventas previas y posteriores a la publicidad, diferenciando entre ventas con y sin publicidad.")

        elif opcion == "KPI 2.2":
            # Calcular el total de ventas con y sin publicidad
            total_con_publicidad = data[data['Publicidad'] == 'Pagada']['Precio'].sum()
            total_sin_publicidad = data[data['Publicidad'] == 'No pagada']['Precio'].sum()

            # Calcular el total general de ventas
            total_ventas = data['Precio'].sum()

            # Calcular los porcentajes de ventas con y sin publicidad
            porcentaje_con_publicidad = (total_con_publicidad / total_ventas) * 100 if total_ventas != 0 else 0
            porcentaje_sin_publicidad = (total_sin_publicidad / total_ventas) * 100 if total_ventas != 0 else 0

            # Crear la gráfica de barras
            fig, ax = plt.subplots()
            ax.bar(['Con Publicidad', 'Sin Publicidad'], [total_con_publicidad, total_sin_publicidad],
                   color=["blue", "orange"])

            # Etiquetas y título
            ax.set_ylabel("Total de Ventas ($)")
            ax.set_title("Total de Ventas: Con y Sin Publicidad")
            ax.bar_label(ax.containers[0])  # Agregar etiquetas a las barras

            # Mostrar la gráfica en Streamlit
            st.pyplot(fig)

            st.write("***Las variables utilizadas fueron:***")
            st.table(pd.DataFrame({
                "Variables": ["Ventas con publicidad", "Ventas sin publicidad"],
                "Descripción": [
                    " Ventas realizadas relacionadas con la publicidad pagada",
                    "Ventas realizadas que no esten relacionadas con la publicidad pagada, ya sea previa o posteriormente",
                ]
            }))

            st.write("***Interpretación:***")
            st.write(
                "La gráfica muestra la distribución total de ventas con y sin publicidad pagada. El porcentaje asociado a ventas con publicidad es relevante para evaluar la efectividad de las campañas.")

    # Tercera columna: espacio para Jaz
    with col3:
        st.write("**KPI 3: Costo por Conversión (CPC) por venta generada, tanto sin publicidad como con publicidad a través de redes sociales.**")
        st.write("***Fórmulas utilizadas:***")
        st.write("1. Con publicidad: CPC = Costo total de la publicidad (campaña) / Número total de conversiones.", "\n",
                 "2. Sin publicidad: Costo sin publicidad = Costo unitario × Cantidad de productos vendidos / Total de unidades vendidas sin publicidad")

        # Columnas para el dataframe
        columnas = ['Ventas', 'Modelo', 'Vidrio', 'Precio', 'Vendedores', 'Fecha de venta', 'Publicidad', 'Costo de compra']
        datosjaz = pd.read_csv("files/jazkpis.csv", sep=',', header=0, names=columnas)
        datosjaz['Fecha de venta'] = pd.to_datetime(datosjaz['Fecha de venta'], format='%d/%m/%Y').dt.date

        # Filtrar las ventas con publicidad
        publicidad_pagada = datosjaz[datosjaz['Publicidad'] == 'Pagada']

        # Calcular métricas
        costo_unitario = datosjaz['Costo de compra'].median()  # Costo sin publicidad
        ventas_con_publicidad = len(publicidad_pagada)  # Número de conversiones
        costo_conversion = 200 / ventas_con_publicidad if ventas_con_publicidad > 0 else 0  # Costo por conversión con publicidad

        # Crear un resumen de costos en un dataframe
        resumen_costos = pd.DataFrame({
            'Tipo de Costo': ['Con Publicidad', 'Sin Publicidad'],
            'Costo': [costo_conversion, costo_unitario]
        })

        # Graficar las barras
        fig, ax = plt.subplots(figsize=(10, 6))

        sns.barplot(x='Tipo de Costo', y='Costo', data=resumen_costos, palette=['pink', 'lightblue'], ax=ax)

        # Añadir etiquetas sobre las barras
        for i, row in resumen_costos.iterrows():
            ax.text(i, row['Costo'] + 0.2, f"{row['Costo']:.2f}", ha='center', va='bottom', color='green')

        # Configurar el gráfico
        ax.set_title('Costo por Conversión con y sin Publicidad', fontsize=15)
        ax.set_xlabel('Tipo de Costo', fontsize=12)
        ax.set_ylabel('Costo ($)', fontsize=12)

        # Mostrar la gráfica en Streamlit
        st.pyplot(fig)

        st.write("***Las variables utilizadas fueron:***", "\n")
        st.table(pd.DataFrame({
            "Variables": [
                "Costo Total de Publicidad",
                "Cantidad de Conversiones",
                "Períodos con y sin Publicidad"
            ],
            "Descripción": [
                "El gasto total realizado en la campaña durante el periodo de publicidad pagada.",
                "Las conversiones que se generaron gracias a la campaña, es decir, la cantidad de compras.",
                "Los períodos donde fue pagada la publicidad (en este caso, 5 días) y los días que no había publicidad."
            ]
        }))

        st.write("***Interpretaciones:***")
        st.write(
            "La gráfica nos muestra un CPC alto durante la publicidad, es significa que la empresa está gastando 50 unidades monetarias en promedio, lo que indica que la campaña no fue tan efectiva. En contraste, el CPC sin invertir en publicidad es considerablemente más bajo con 15 unidades monetarias. Esto sugiere que la campaña de publicidad está siendo costosa en términos de retorno por cada conversión obtenida.")

