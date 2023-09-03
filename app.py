import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Variables iniciales
capital_inicial = 0
inversion_anual = 20000
anos = 17
rendimiento_promedio = 0.04
desviacion_estandar = 0.10
num_simulaciones = 1000

# Función para simular un único intento de 17 años de inversión
def simular_inversion(anos, capital_inicial, inversion_anual, rendimiento_promedio, desviacion_estandar):
    capital = capital_inicial
    rendimientos = []
    for i in range(anos):
        rendimiento = np.random.normal(rendimiento_promedio, desviacion_estandar)
        capital = capital * (1 + rendimiento) + inversion_anual
        rendimientos.append(capital)
    return rendimientos

# Función para realizar la simulación de Montecarlo
def montecarlo_simulacion(anos, capital_inicial, inversion_anual, rendimiento_promedio, desviacion_estandar, num_simulaciones):
    resultados = []
    for i in range(num_simulaciones):
        rendimientos = simular_inversion(anos, capital_inicial, inversion_anual, rendimiento_promedio, desviacion_estandar)
        resultados.append(rendimientos)
    return resultados

# Crear la interfaz de la aplicación Streamlit
st.title('Simulación de Montecarlo para Estrategia de Inversión')
st.write('Esta aplicación realiza una simulación de Montecarlo para una estrategia de inversión de 17 años.')

# Entradas del usuario
capital_inicial = st.number_input('Capital Inicial', value=0)
inversion_anual = st.number_input('Inversión Anual', value=20000)
anos = st.number_input('Años', value=17)
rendimiento_promedio = st.number_input('Rendimiento Promedio', value=0.04)
desviacion_estandar = st.number_input('Desviación Estándar', value=0.10)
num_simulaciones = st.number_input('Número de Simulaciones', value=1000)

# Realizar la simulación
if st.button('Realizar Simulación'):
    resultados = montecarlo_simulacion(anos, capital_inicial, inversion_anual, rendimiento_promedio, desviacion_estandar, num_simulaciones)
    rendimiento_promedio_total = np.mean([resultado[-1] for resultado in resultados])
    monto_promedio_acumulado = np.mean([resultado[-1] for resultado in resultados])
    escenario_pesimista = np.percentile([resultado[-1] for resultado in resultados], 5)
    escenario_optimista = np.percentile([resultado[-1] for resultado in resultados], 95)
    
    st.write('Rendimiento Promedio Total:', rendimiento_promedio_total)
    st.write('Monto Promedio Acumulado:', monto_promedio_acumulado)
    st.write('Escenario Pesimista:', escenario_pesimista)
    st.write('Escenario Optimista:', escenario_optimista)

# Mostrar gráficos
if st.button('Mostrar Gráficos'):
    # Crear y mostrar gráficos
    plt.hist([resultado[-1] for resultado in resultados], bins=50)
    plt.axvline(x=rendimiento_promedio_total, color='r', linestyle='dashed', linewidth=2)
    plt.axvline(x=escenario_pesimista, color='g', linestyle='dashed', linewidth=2)
    plt.axvline(x=escenario_optimista, color='y', linestyle='dashed', linewidth=2)
    plt.title('Distribución de Montos Finales de las Simulaciones')
    plt.xlabel('Monto Final')
    plt.ylabel('Frecuencia')
    st.pyplot(plt)
    plt.clf()

    # Graficar monto ahorrado por cada año
    plt.plot(range(anos), np.mean(resultados, axis=0))
    plt.title('Monto Ahorrado Promedio por Año')
    plt.xlabel('Año')
    plt.ylabel('Monto Ahorrado')
    st.pyplot(plt)
    plt.clf()

    # Graficar monto acumulado por cada año
    plt.plot(range(anos), np.mean(np.cumsum(resultados, axis=1), axis=0))
    plt.title('Monto Acumulado Promedio por Año')
    plt.xlabel('Año')
    plt.ylabel('Monto Acumulado')
    st.pyplot(plt)
