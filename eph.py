#importar las librerias
import streamlit as st
import os
import pandas as pd
import numpy as np
import pickle
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
#disabling the warnings
import warnings
warnings.filterwarnings("ignore")

def main():
   st.set_page_config(
   page_title="Observatorio del Hábitat Urbano",
   page_icon="🌎",
   layout="centered",
   initial_sidebar_state="expanded",
   menu_items=None)

    
   # Header
   st.header('Observatorio del Hábitat Urbano')

   # Text

   tab1, tab2, tab3 , tab4, tab5 = st.tabs(["Presentación", "Metodología", "Resultados", "Visualizaciones", "Conclusiones"])

   with tab1:
      st.subheader('Presentación')
      st.markdown('El __Observatorio del Hábitat Urbano__ tiene como objetivo...\n\nInvestigadorxs: Guadalupe __Atienza Rela__ | Santiago __Federico__')
   
   with tab2:
      st.subheader('Metodología')
      st.markdown('Existen diversas metodologías para calcular déficit habitacional. En este caso, utilizaremos la metodología seguida por el Gobierno de la Ciudad de Buenos Aires, que toma la propuesta desarrollada por la CEPAL en el documento “América Latina: información y herramientas socio-demográficas para analizar y atender el déficit habitacional”, la cual permite obtener estimaciones compatibles (y por tanto comparables) con los datos disponibles a nivel nacional y de otros países de la región de América Latina.')
      st.markdown('Esta metodología distingue entre dos formas de déficit: cuantitativo, que refiere al excedente de hogares en relación a la cantidad de viviendas no precarias o mejorables (o, dicho de otro modo, a la cantidad de viviendas que faltan en relación a la cantidad de hogares existentes); y cualitativo, que refiere a la cantidad de hogares que viven en viviendas en otro tipo de condiciones deficitarias.')
      st.markdown('La base de datos de EPH proporciona todas las variables necesarias para realizar este cálculo. Para poder realizarlo primero deben tenerse en cuenta las siguientes definiciones.')   
      st.markdown('__- Viviendas precarias irrecuperables:__ son aquellas que por la calidad de los materiales con que han sido construidas o por su naturaleza no pueden ser mejoradas en sus condiciones de habitabilidad. Las categorías que corresponden a esta definición son: Local no construido para habitación, Otros (incluye casillas, ranchos y otro tipo de construcciones semejantes).')
      st.markdown('__- Viviendas precarias recuperables:__ son aquellas que mediante obras de refacción pueden mejorar sus condiciones de habitabilidad. Las categorías que corresponden a esta definición son: Pieza en Inquilinatos, hoteles o pensiones y Casas Tipo B (todas las que cumplen por lo menos con una de las siguientes condiciones: tienen piso de tierra o ladrillo suelto u otro material y/o no tienen provisión de agua por cañería dentro de la vivienda y/o no disponen de inodoro con descarga de agua).')
      st.markdown('__- Viviendas no precarias:__ son aquellas de condiciones materiales satisfactorias. Las categorías que corresponden a esta definición son: Departamentos y Casas Tipo A.')
      st.markdown('__- Hacinamiento crítico:__ hogares que presentan tres o más personas por habitación utilizada para dormir.')
      st.markdown('Para establecer la condición de déficit habitacional como atributo de cada uno de los hogares, se procederá entonces a crear variables que registren para cada observación si se trata de hogares que habitan en viviendas precarias irrecuperables o recuperables, o presentan hacinamiento crítico.')
      st.markdown('Una vez definidas estas variables podemos calcular la condición de los hogares en relación al déficit habitacional. Contemplaremos como hemos dicho ambos tipos de déficit (cuanti y cualitativo):')
      st.markdown('__- Hogares con déficit habitacional cuantitativo:__ hogares que comparten su vivienda o viven en viviendas precarias irrecuperables.')
      st.markdown('__- Hogares con déficit habitacional cualitativo de tipo I:__ hogares que viven en viviendas precarias recuperables.')
      st.markdown('__- Hogares con déficit habitacional cualitativo de tipo II:__ hogares que viven en viviendas no precarias en condición de hacinamiento crítico.')
   
   with tab3:
      st.subheader('Resultados')
      with open('tabla_pivot_porcentaje.pkl', 'rb') as t_1:
         tabla_pivot_porcentaje = pickle.load(t_1)
         st.table(tabla_pivot_porcentaje)

   with tab4:
      st.subheader('Visualizaciones')
      with open('grafico_gba.pkl', 'rb') as g_1:
         grafico_gba = pickle.load(g_1)
      st.plotly_chart(grafico_gba, use_container_width=True)
   
   with tab5:
      st.subheader('Conclusiones')

if __name__ == '__main__':
    main()