#importar las librerias
import streamlit as st
import os
import pandas as pd
import numpy as np
import pickle
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import seaborn as sns
#disabling the warnings
import warnings
warnings.filterwarnings("ignore")

def main():
   st.set_page_config(
   page_title="OBSERVATORIO DEL HABITAT URBANO | Deficit Habitacional",
   page_icon="🌎",
   layout="wide",
   initial_sidebar_state="expanded",
   menu_items=None)

    
   # Header
   st.header('__OBSERVATORIO DEL HÁBITAT URBANO__ | Déficit Habitacional')

   # Text

   tab1, tab2, tab3 , tab4 = st.tabs(["Presentación", "Metodología", "Series de Tiempo", "Próximas incorporaciones"])

   with tab1:
      st.subheader('Presentación')
      st.markdown('El __Observatorio del Hábitat Urbano__ tiene como objetivo generar indicadores que permitan __visibilizar problemáticas__ vinculadas al hábitat urbano en la Argentina y __monitorear la efectividad__ de las políticas públicas aplicadas.')  
      st.markdown('Como primer paso, se avanzó en la construcción del primer indicador de __evolución del Déficit Habitacional__ en los aglomerados de la __Argentina__. La sección de _"Metodología"_ detalla cómo se construyen el indicador y los gráficos de la sección _"Visualizaciones"_.')
      st.markdown('Es intención de los y las investigadoras incrementar el número de indicadores a ser representados por lo que cualquier aporte es bienvenido.')
      st.markdown('Investigadorxs: Guadalupe __Atienza Rela__ | Santiago __Federico__')
   
   with tab2:
      st.subheader('Metodología')
      st.markdown('Existen diversas metodologías para calcular __déficit habitacional__. En este caso, se utiliza la metodología seguida por el __Gobierno de la Ciudad de Buenos Aires__, que toma la propuesta desarrollada por la __CEPAL__ en el documento _“América Latina: información y herramientas socio-demográficas para analizar y atender el déficit habitacional”_, la cual permite obtener estimaciones compatibles _(y por tanto comparables)_ con los datos disponibles a nivel nacional y de otros países de la __región de América Latina__.')
      st.markdown('Esta metodología distingue entre dos formas de déficit: __cuantitativo__, que refiere al excedente de hogares en relación a la cantidad de viviendas no precarias o mejorables (o, dicho de otro modo, a la cantidad de viviendas que faltan en relación a la cantidad de hogares existentes); y __cualitativo__, que refiere a la cantidad de hogares que viven en viviendas en otro tipo de condiciones deficitarias.')
      st.markdown('La base de datos de __Encuesta Permanente de Hogares__ proporciona todas las variables necesarias para realizar este cálculo. Para poder realizarlo primero deben tenerse en cuenta las siguientes definiciones.')   
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
      opciones = {'Déficit Habitacional':['Déficit Habitacional Consolidado','Hogares por vivienda','Viviendas irrecuperables','Viviendas recuperables','Hacinamiento en viviendas'],
                  #'Dinámicas del Mercado de Suelos':['1','2']
                  }
      
      seleccion = st.multiselect('Seleccione la __serie de tiempo__ a visualizar:', opciones.keys())
    
      for dataset in seleccion:
         st.header(dataset)
         aglomerado = st.selectbox(
         "Selección del __aglomerado__ a visualizar", 
         ('Gran La Plata','Bahía Blanca ‐ Cerri','Gran Rosario','Gran Santa Fé','Gran Paraná','Posadas', 'Gran Resistencia', 'Cdro. Rivadavia – Rada Tilly', 'Gran Mendoza', 
            'Corrientes', 'Gran Córdoba', 'Concordia', 'Formosa', 'Neuquén – Plottier', 'S.del Estero ‐ La Banda', 'Jujuy ‐ Palpalá', 'Río Gallegos', 'Gran Catamarca', 'Salta', 
            'La Rioja', 'San Luis ‐ El Chorrillo', 'Gran San Juan', 'Gran Tucumán ‐ T. Viejo', 'Santa Rosa ‐ Toay', 'Ushuaia ‐ Río Grande', 'Ciudad de Buenos Aires', 'Partidos del GBA', 
            'Mar del Plata ‐ Batán', 'Río Cuarto', 'San Nicolás – Villa Constitución', 'Rawson – Trelew', 'Viedma – Carmen de Patagones'),key=0)
         
         graficos_seleccionados = st.multiselect(f'Selección de __Series de Tiempo__ para {dataset}:', opciones[dataset])
                  
         if 'Déficit Habitacional Consolidado' in graficos_seleccionados:
            data = pd.read_csv('porcentajes_totales.csv',sep=';')
            data = data.set_index(['DATE'])
            fig=go.Figure()
            fig.add_trace(go.Scatter(x=data.index,y=data[aglomerado],name=f'Déficit Habitacional para el aglomerado de {aglomerado}'))
            fig.add_trace(go.Scatter(x=data.index,y=data['Promedio Nacional'],name=f'Déficit Habitacional, promedio nacional'))
            fig.update_layout(title=f'Porcentaje de Déficit Habitacional consolidado para el aglomerado de {aglomerado}',xaxis_title='Fecha',yaxis_title='Hogares con déficit habitacional(%)', height=600)
            fig.update_layout(hovermode="x unified")
            fig.update_xaxes(
            tickformat="%m-%Y", 
            dtick="M3")
            st.plotly_chart(fig, use_container_width=True)
            st.caption('Fuente: Elaboración propia en base a datos de la EPH (2003-2022)')

         if 'Hogares por vivienda' in graficos_seleccionados:   
            data = pd.read_csv('porcentajes_hogarxviv.csv',sep=';')
            data = data.set_index(['DATE'])
            fig=go.Figure()
            fig.add_trace(go.Scatter(x=data.index,y=data[aglomerado],name=f'Viviendas con más de un hogar para el aglomerado de {aglomerado}'))
            fig.add_trace(go.Scatter(x=data.index,y=data['Promedio Nacional'],name=f'Viviendas con más de un hogar, promedio nacional'))
            fig.update_layout(title=f'Porcentaje de viviendas con más de un hogar para el aglomerado de {aglomerado}',xaxis_title='Fecha',yaxis_title='Viviendas con más de un hogar (%)', height=600)
            fig.update_layout(hovermode="x unified")
            fig.update_xaxes(
            tickformat="%m-%Y", 
            dtick="M3")
            st.plotly_chart(fig, use_container_width=True)
            st.caption('Fuente: Elaboración propia en base a datos de la EPH (2003-2022)')
         
         if 'Viviendas irrecuperables' in graficos_seleccionados:
            data = pd.read_csv('porcentajes_viv_irre.csv',sep=';')
            data = data.set_index(['DATE'])
            fig=go.Figure()
            fig.add_trace(go.Scatter(x=data.index,y=data[aglomerado],name=f'Viviendas irrecuperables para el aglomerado de {aglomerado}'))
            fig.add_trace(go.Scatter(x=data.index,y=data['Promedio Nacional'],name=f'Viviendas irrecuperables, promedio nacional'))
            fig.update_layout(title=f'Porcentaje de viviendas irrecuperables para el aglomerado de {aglomerado}',xaxis_title='Fecha',yaxis_title='Viviendas irrecuperables(%)', height=600)
            fig.update_layout(hovermode="x unified")
            fig.update_xaxes(
            tickformat="%m-%Y", 
            dtick="M3")
            st.plotly_chart(fig, use_container_width=True)
            st.caption('Fuente: Elaboración propia en base a datos de la EPH (2003-2022)')
         
         if 'Viviendas recuperables' in graficos_seleccionados:
            data = pd.read_csv('porcentajes_viv_recu.csv',sep=';')
            data = data.set_index(['DATE'])
            fig=go.Figure()
            fig.add_trace(go.Scatter(x=data.index,y=data[aglomerado],name=f'Viviendas recuperables para el aglomerado de {aglomerado}'))
            fig.add_trace(go.Scatter(x=data.index,y=data['Promedio Nacional'],name=f'Viviendas recuperables, promedio nacional'))
            fig.update_layout(title=f'Porcentaje de viviendas recuperables para el aglomerado de {aglomerado}',xaxis_title='Fecha',yaxis_title='Viviendas recuperables(%)', height=600)
            fig.update_layout(hovermode="x unified")
            fig.update_xaxes(
            tickformat="%m-%Y", 
            dtick="M3")
            st.plotly_chart(fig, use_container_width=True)
            st.caption('Fuente: Elaboración propia en base a datos de la EPH (2003-2022)')

         if 'Hacinamiento en viviendas' in graficos_seleccionados:
            data = pd.read_csv('porcentajes_viv_hac.csv',sep=';')
            data = data.set_index(['DATE'])
            fig=go.Figure()
            fig.add_trace(go.Scatter(x=data.index,y=data[aglomerado],name=f'Hacinamiento en viviendas para el aglomerado de {aglomerado}'))
            fig.add_trace(go.Scatter(x=data.index,y=data['Promedio Nacional'],name=f'Hacinamiento en viviendas, promedio nacional'))
            fig.update_layout(title=f'Porcentaje de Hacinamiento en viviendas para el aglomerado de {aglomerado}',xaxis_title='Fecha',yaxis_title='Hacinamiento en viviendas (%)', height=600)
            fig.update_layout(hovermode="x unified")
            fig.update_xaxes(
            tickformat="%m-%Y", 
            dtick="M3")
            st.plotly_chart(fig, use_container_width=True)
            st.caption('Fuente: Elaboración propia en base a datos de la EPH (2003-2022)')

   with tab4:
      st.subheader('Próximas incorporaciones')
      st.markdown('__- Dinámicas del mercado de suelos__')
      st.markdown('__- Acceso al crédito__')
      st.markdown('__- Crecimiento de la mancha urbana__')
      st.markdown('__- Modelos predictivos__')

if __name__ == '__main__':
    main()