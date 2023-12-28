#importar las librerias
import streamlit as st
import plotly.express as px
import pandas as pd
import geopandas as gpd
import numpy as np
import plotly.graph_objs as go
import matplotlib.pyplot as plt

#disabling the warnings
import warnings
warnings.filterwarnings("ignore")

def main():
   st.set_page_config(
   page_title="OBSERVATORIO DEL HABITAT URBANO",
   page_icon="🌎",
   layout="wide",
   initial_sidebar_state="expanded",
   menu_items=None)

   st.header('__OBSERVATORIO DEL HÁBITAT URBANO__')

   tab1, tab2, tab3, tab4, tab5 = st.tabs(["Presentación", "Metodologías", "Series de Tiempo", "Mapas","Próximas incorporaciones"])

   with tab1:
      st.subheader('Presentación')
      st.markdown('El __Observatorio del Hábitat Urbano__ tiene como objetivo generar indicadores que permitan __visibilizar problemáticas__ vinculadas al hábitat urbano en la Argentina y __monitorear la efectividad__ de las políticas públicas aplicadas.')  
      st.markdown('Como primer paso, se avanzó en la construcción del primer indicador de __evolución del Déficit Habitacional__ en los aglomerados de la __Argentina__. La sección de _"Metodologías"_ detalla cómo se construyen el indicador y los gráficos de la sección _"Series de Tiempo"_. En breve se espera poder incorporar mapas para una mejor comprensión espacial de los datos.')
      st.markdown('Es intención de los y las investigadoras incrementar el número de indicadores a ser representados por lo que cualquier aporte es bienvenido.')
      st.markdown('Investigadorxs: Guadalupe __Atienza Rela__ | Santiago __Federico__')
   
   with tab2:
      st.subheader('Metodologías')
      
      opt_meto = st.selectbox('Seleccione __una de las opciones__ para visualizar la metodología utilizada para la construcción del indicador',('EPH - Déficit Habitacional', 'EPH - Alquileres formales'))
      
      if opt_meto == 'EPH - Déficit Habitacional':
         st.subheader('EPH - Déficit Habitacional')
         st.markdown('')
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
      
      if opt_meto == 'EPH - Alquileres formales':
         st.subheader('EPH - Alquileres formales')
         st.markdown('')
         st.markdown('Para la contrucción del indicador de porcentaje de hogares inquilinos formales, se optó por utilizar el campo __"Tipo de vivienda"__, considerando las variables de vivendas formales: __Casa__ y __Departamento__.')  
         st.markdown('A su vez, para el universo anteriomente mencionado se tomó el campo __"Régimen de Tenencia"__, tomando la variable  __"Inquilino / arrendatario de la vivienda"__')
         st.markdown('El resultado del cruce genera una nueva columna con __variables binarias__, que expresan la presencia o no de hogares inquilinos formales que luego se transforma a porcentajes.')

   with tab3:
      def plot_graph(title, csv_filename, aglomerado):
         data = pd.read_csv(csv_filename, sep=';')
         data = data.set_index(['DATE'])
         fig = go.Figure()
         fig.add_trace(go.Scatter(x=data.index, y=data[aglomerado], name=f'{title} para el aglomerado de {aglomerado}'))
         fig.add_trace(go.Scatter(x=data.index, y=data['Promedio Nacional'], name=f'{title}, promedio nacional'))
         fig.update_layout(
            title=f'Porcentaje de {title} para el aglomerado de {aglomerado}',
            xaxis_title='Fecha',
            yaxis_title=f'{title} (%)',
            height=600,
            hovermode="x unified"
         )
         fig.update_xaxes(tickformat="%m-%Y", dtick="M3")
         st.plotly_chart(fig, use_container_width=True)
         st.caption('Fuente: Elaboración propia en base a datos de la EPH (2003-2023)')

      st.markdown('Por tratarse de series de tiempo extensas e interactivas, __no__ se recomienda utilizar __celulares__ para visualizarlas.')

      opciones = {'Déficit Habitacional': ['Déficit Habitacional Consolidado', 'Hogares por vivienda', 'Viviendas irrecuperables', 'Viviendas recuperables', 'Hacinamiento en viviendas'],
                  'Dinámicas del Mercado de Suelos': ['Alquileres']}

      seleccion = st.multiselect('Seleccione la __serie de tiempo__ a visualizar:', opciones.keys())

      for dataset in seleccion:
         st.header(dataset)
         aglomerado = st.selectbox(
            "Selección del __aglomerado__ a visualizar",
            ('Gran La Plata', 'Bahía Blanca ‐ Cerri', 'Gran Rosario', 'Gran Santa Fé', 'Gran Paraná', 'Posadas', 'Gran Resistencia', 'Cdro. Rivadavia – Rada Tilly', 'Gran Mendoza',
               'Corrientes', 'Gran Córdoba', 'Concordia', 'Formosa', 'Neuquén – Plottier', 'S.del Estero ‐ La Banda', 'Jujuy ‐ Palpalá', 'Río Gallegos', 'Gran Catamarca', 'Salta',
               'La Rioja', 'San Luis ‐ El Chorrillo', 'Gran San Juan', 'Gran Tucumán ‐ T. Viejo', 'Santa Rosa ‐ Toay', 'Ushuaia ‐ Río Grande', 'Ciudad de Buenos Aires', 'Partidos del GBA',
               'Mar del Plata ‐ Batán', 'Río Cuarto', 'San Nicolás – Villa Constitución', 'Rawson – Trelew', 'Viedma – Carmen de Patagones'), key=0)

         graficos_seleccionados = st.multiselect(f'Selección de __Series de Tiempo__ para {dataset}:', opciones[dataset])

         for graph_type in graficos_seleccionados:
            if graph_type in opciones[dataset]:
                  if graph_type == 'Alquileres':
                     plot_graph('Hogares inquilinos', 'porcentajes_alquileres.csv', aglomerado)
                  elif graph_type == 'Déficit Habitacional Consolidado':
                     plot_graph('Déficit Habitacional', 'porcentajes_totales.csv', aglomerado)
                  elif graph_type == 'Hogares por vivienda':
                     plot_graph('viviendas con más de un hogar', 'porcentajes_hogarxviv.csv', aglomerado)
                  elif graph_type == 'Viviendas irrecuperables':
                     plot_graph('Viviendas irrecuperables', 'porcentajes_viv_irre.csv', aglomerado)
                  elif graph_type == 'Viviendas recuperables':
                     plot_graph('Viviendas recuperables', 'porcentajes_viv_recu.csv', aglomerado)
                  elif graph_type == 'Hacinamiento en viviendas':
                     plot_graph('Hacinamiento en viviendas', 'porcentajes_viv_hac.csv', aglomerado)
   with tab4:
      st.subheader('Mapas')
  
      # Importar Datasets
      df = pd.read_csv('mapa_inquilinos_prov.csv',sep=',')
      opt_censo = st.selectbox('Seleccione la __variable__ a visualizar:',('Alquileres','Otros'))

      st.caption('A mayor oscuridad en la escala de rojos, mayor es el porcentaje.')
      
      if 'Alquileres' in opt_censo:
         # Especifica la ruta de tu archivo CSV
         archivo_csv = 'mapa_inquilinos_prov.csv'
         # Lee el archivo CSV con geometría almacenada como texto (WKT o GeoJSON)
         mapa = gpd.read_file(archivo_csv, GEOM_POSSIBLE_NAMES="geometry", KEEP_GEOM_COLUMNS="NO")
         
         # Crear una figura con tres subgráficos en una fila
         fig, axes = plt.subplots(1, 3, figsize=(15, 5))

         # Dibujar cada mapa en un subgráfico diferente
         mapa.plot(column='Porcentaje inquilinos 2010', cmap='Reds', legend=False, ax=axes[0])
         mapa.plot(column='Porcentaje inquilinos 2022', cmap='Reds', legend=False, ax=axes[1])
         mapa.plot(column='Variacion intercensal', cmap='Reds', legend=False, ax=axes[2])
                
         # Añadir títulos a cada subgráfico
         axes[0].set_title('% Inquilinos | Censo 2010')
         axes[1].set_title('% Inquilinos | Censo 2022')
         axes[2].set_title('% Variación intercensal')

         # Eliminar el contorno alrededor de cada subgráfico
         for ax in axes:
            ax.set_frame_on(False)
            ax.set_xticks([])
            ax.set_yticks([])
         
         # Ajustar el espacio entre subgráficos
         plt.tight_layout()

         st.pyplot(fig)
      
      if 'Otros' in opt_censo:
         st.write('Proximamente...')

   with tab5:
      st.subheader('Próximas incorporaciones')
      st.markdown('__- Dinámicas del mercado de suelos__')
      st.markdown('__- Acceso al crédito__')
      st.markdown('__- Crecimiento de la mancha urbana__')
      st.markdown('__- Modelos predictivos__')

if __name__ == '__main__':
    main()