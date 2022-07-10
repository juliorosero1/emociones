import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import squarify #implementar en "codigos necesarios"
from streamlit_folium import folium_static
import json
import folium
import plotly.graph_objects as go
import creacionDatosMapa_4 as crd
from stop_words import get_stop_words

#carpeta mapa3 se puede borrar

# Modo Wide
st.set_page_config(layout="wide",)

st.title("Análisis de emociones referentes a efectos psicológicos en una pandemia")
st.sidebar.title("Análisis de emociones acerca de efectos psicológicos en una pandemia")
#chart1="<a style='text-decoration:none' href='#inicio'><p style='color:white; line-height:125%'><font size=5><b>Análisis de emociones acerca de efectos psicológicos en una pandemia</b></font></p></a>"
#st.sidebar.markdown(chart1, unsafe_allow_html=True)

st.markdown(" Análisis de emociones basado en tweets 🐦")
#st.sidebar.markdown(" Análisis de sentimientos basado en tweets 🐦")

#@st.cache(persist=True)


def cargar_data():
    data=pd.read_csv("sentimientosTweet_3.csv")
    data['fecha']= pd.to_datetime(data['fecha'])
    return data

data= cargar_data()

#st.write(data)
#Selección de Tweets
#st.sidebar.subheader("Tweet aleatorio")
#randomTweet= st.sidebar.radio('Sentimientos',('positivo','neutro','negativo'))
#st.sidebar.markdown(data.query('polaridad== @randomTweet')[["tweet"]].sample(n=1).iat[0,0])

#seleccion0= st.sidebar.selectbox('Selección de tipo de resultados',['Generales', 'Por Noticias'], key='7')
seleccion0=st.sidebar.radio("Selección de Análisis",('General', 'Por Eventos'))
st.sidebar.markdown("___")

if seleccion0 == "General":
    ##################################################################
    ################ Polaridad #########################################
    ######################################################################

    #Enlace
    st.sidebar.markdown("### Emociones y Sentimientos")
    #chart1="<a style='text-decoration:none' href='#polaridad-de-tweets'><p style='color:white; line-height:125%'><font size=4><b>Polaridad de Tweets</b></font></p></a>"
    #st.sidebar.markdown(chart1, unsafe_allow_html=True)
    select= st.sidebar.selectbox('Tipo de Visualizacion',['Histograma', 'Diagrama de Pastel'], key='1')

    contadorSentimientos= data['polaridad'].value_counts()
    contadorEmociones= data['emocion'].value_counts()
    #st.write(contadorSentimientos)
    contadorSentimientos=pd.DataFrame({'Polaridad': contadorSentimientos.index, 'Tweets': contadorSentimientos.values})
    contadorEmociones=pd.DataFrame({'Emocion': contadorEmociones.index, 'Tweets': contadorEmociones.values})
    #a=data.polaridad.value_counts()

    colorP= '#636efa' #'#4040ff'
    colorN= '#ef553b'# '#ff4040'
    colorNeutro= '#ffa15a' #"#ff8c40"

    #if not st.sidebar.checkbox("Ocultar", True):
    st.markdown("## Emociones y Sentimientos")
    if select == "Histograma":
        fig= px.bar(contadorSentimientos, x= 'Polaridad', y='Tweets', color= 'Polaridad', height=600, width=600,
        color_discrete_map = {'negativo':colorN, 'neutro': colorNeutro, 'positivo':colorP} )
        fig.update_layout( font_size=20) #Tesis
        #fig.update_layout( font_size=15)


        fig2= px.bar(contadorEmociones, x= 'Emocion', y= 'Tweets',  height=600, width=700, color = 'Emocion',
        color_discrete_map = {'miedo':colorN, 'tristeza': colorN, 'expectante':colorP, 'confianza':colorP, 'repulsion': colorN, 'ira': colorN, 'alegria':colorP, 'sorpresa': colorP})
        fig2.update_layout( font_size=20) #tesis
        #fig2.update_layout( font_size=15)


        col1, col2= st.columns(2)
        #col1.subheader("Palabras frecuentes")
        col1.plotly_chart(fig)
        col2.plotly_chart(fig2)

    else:
        fig= px.pie(contadorSentimientos, values='Tweets', names='Polaridad', height=600, width=700, color ='Polaridad',
        color_discrete_map = {'negativo':colorN, 'neutro': colorNeutro, 'positivo':colorP}  )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout( font_size=25)
    #    st.plotly_chart(fig)

        fig2= px.pie(contadorEmociones, values='Tweets', names='Emocion', height=600, width=700, color='Emocion',
        color_discrete_map = {'miedo':'fd6c4c', 'tristeza': 'ff8c6e', 'expectante':'8685fc', 'confianza':'a29cfd', 'repulsion': 'ffa991', 'ira': 'ffc6b4', 'alegria':'bcb4fe', 'sorpresa':'d3ccff'})
        #fig2.update_traces(textposition='inside', textinfo='percent+label')
        fig2.update_traces(textinfo='percent+label')
        fig2.update_layout( font_size=25)
        #st.plotly_chart(fig2)

        col1, col2= st.columns(2)
        col1.plotly_chart(fig)
        col2.plotly_chart(fig2)

    #st.sidebar.markdown("___")

    ###################################################################
    ############# Palabras Frecuentes s#################
    ###################################################################
    #if not st.sidebar.checkbox("ocultar", True, key='10'):
    st.markdown("___")
    #st.header("Palabras y Frases Frecuentes")
    st.markdown("## Palabras y Frases Frecuentes")
    #st.sidebar.markdown("### Palabras y frases frecuentes")

    #@st.cache(persist=True)
    st.sidebar.markdown("### Palabras y Frases Frecuentes")
    select= st.sidebar.selectbox('Seleccion',['Frases frecuentes', 'Palabras frecuentes'], key='6')

    if select == "Palabras frecuentes":

        st.markdown("### Palabras frecuentes")
        #st.markdown("<h2 style='text-align: center;'>Palabras frecuentes</h2>", unsafe_allow_html=True)

        pal= pd.read_csv('frecuenciaPal.csv')
        #st.write(pal)

        labels = pal.palabra.head(10) #['Oxygen','Hydrogen','Carbon_Dioxide','Nitrogen']
        values = pal.frecuencia.head(10) #[4500, 2500, 1053, 500]

        # Diagrama Dona
        Layout=go.Layout(height = 500, width =700 ) #tamaño
        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.6, title='Top 10 palabras')], layout=Layout)
        fig.update_traces(textfont_size=15)
        fig.update_layout( title_text="Top 10 palabras frecuentes", font_size=15)
        #st.plotly_chart(fig)
        #fig.update_layout( title_text="Top 10 palabras frecuentes", font_size=20)

        col1, col2= st.columns(2)
        #col2.subheader("Palabras frecuentes")
        col2.text("\n \n .")
        #col1.write(pal, width=900, height=400)
        col2.dataframe(pal, width=900, height=400)

        col1.plotly_chart(fig)

    #st.sidebar.markdown("___")
    ##################################################################


    ################################################################
    ####### Frases frecuentes   #############################
    ##############################################################

    if select == "Frases frecuentes":
        st.markdown("### Frase frecuentes")
        #st.markdown("<h2 style='text-align: center;'> Frases frecuentes</h1>", unsafe_allow_html=True)

        frase= pd.read_csv('frecuenciaFra.csv')
        #st.write(pal)

        labels = frase.frase.head(10)
        values = frase.frecuencia.head(10)

        # Diagrama Dona
        Layout=go.Layout(height = 500, width = 700) #tamaño
        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.6, textfont_size=12, title='Top 10 tópicos')], layout=Layout)
        fig.update_traces(textfont_size=15)
        fig.update_layout( title_text="Top 10 tópicos frecuentes", font_size=15)

        col1, col2= st.columns(2)
        #col2.text(".")
        #col1.subheader("Frases frecuentes")
        col2.dataframe(frase, width=500, height=400)

    #    col1.plotly_chart(fig)###
        col1.plotly_chart(fig)

    #st.sidebar.markdown("___")

    #################################################################
    ###########       Nube de Palabras #############################
    ################################################################
    st.markdown("___")
    excluir=get_stop_words('spanish')
    lista_negra= ['covid', 'ansiedad', 'si', 'Covid_19']
    excluir.extend(lista_negra)

    st.sidebar.markdown("### Nube de Palabras por Emociones")

    #sentimientoPalabra= st.sidebar.radio('Observar nube de palabras?', data.emocion.value_counts().keys().tolist())
    sentimientoPalabra= st.sidebar.selectbox('Observar nube de palabras por:', data.emocion.value_counts().keys().tolist())

    st.markdown('## Nube de palabras por emociones: %s ' %(sentimientoPalabra) )
    df=data[data['emocion']== sentimientoPalabra]
    palabras= " ".join(df['tweet'])

    palabrasProcesadas=' '.join([palabra for palabra in palabras.split() if 'http' not in palabra and not palabra.startswith('@') and palabra!= 'RT'])
    nubePalabras= WordCloud(stopwords= excluir, background_color='white', height=720, width=1900).generate(palabrasProcesadas)
    plt.figure( figsize=(8,10) )
    plt.imshow(nubePalabras)
    plt.xticks([])
    plt.yticks([])
    st.set_option('deprecation.showPyplotGlobalUse', False) #Quita mensaje de advertencia
    st.pyplot()

    #st.sidebar.markdown("___")
    #############################################################################

elif seleccion0 == "Por Eventos" :
    ########################################################################
    ############ Visualizacion por mapa ####################################
    #####################################################################
    #Enlace
    st.sidebar.subheader("Mapa de Calor por Emociones")
    #chart1="<a style='text-decoration:none' href='#mapa-de-calor-por-emociones'><p style='color:white; line-height:125%'><font size=4><b>Mapa de calor por emociones</b></font></p></a>"
    #st.sidebar.markdown(chart1, unsafe_allow_html=True)

    opcion=data.noticia.value_counts().keys().tolist()
    noti=st.sidebar.selectbox("Selección de Noticia", (opcion))
    dataP= crd.cTabla(str(noti))

    porcen=dataP[['pais', 'miedo', 'ira', 'expectante', 'confianza', 'sorpresa', 'tristeza', 'repulsion', 'alegria']]
    porcen= porcen.assign(suma= porcen.sum(axis=1))
    porcen=porcen.assign(p_miedo= porcen.miedo/porcen.suma*100)
    porcen=porcen.assign(p_ira= porcen.expectante/porcen.suma*100)
    porcen=porcen.assign(p_expectante= porcen.expectante/porcen.suma*100)
    porcen=porcen.assign(p_confianza= porcen.confianza/porcen.suma*100)
    porcen=porcen.assign(p_sorpresa= porcen.sorpresa/porcen.suma*100)
    porcen=porcen.assign(p_tristeza= porcen.tristeza/porcen.suma*100)
    porcen=porcen.assign(p_repulsion= porcen.repulsion/porcen.suma*100)
    porcen=porcen.assign(p_alegria= porcen.alegria/porcen.suma*100)

    t_porcentaje= porcen[['pais', 'p_miedo', 'p_ira', 'p_expectante', 'p_confianza', 'p_sorpresa', 'p_tristeza', 'p_repulsion', 'p_alegria']]

    emociones= data.emocion.value_counts().keys().tolist()
    data_geo = json.load(open('hispano.geojson'))
    #world_map= folium.Map(width=750, height=1500)

    world_map= folium.Map(location=[17.57, -59.74], zoom_start= 2.4, tiles='cartodbpositron', width=700, height=500)

    #if not st.sidebar.checkbox("Ocultar", True, key='4'):
    #st.markdown("## Mapa de calor por emociones")
    #emocionOP=st.sidebar.radio("Selección de sentimiento",(emociones))
    st.markdown("## Selección de Emoción")
    emocionOP=st.selectbox("",(emociones))
    st.write("___")
    emoc=emocionOP
    emocionOP= 'p_'+emocionOP

    choropleth = folium.Choropleth(
        geo_data=data_geo,
        data=t_porcentaje,
        columns=['pais', emocionOP],
        key_on='feature.properties.name',
        fill_color= "YlOrRd",
        fill_opacity=0.7,
        line_opacity=0.4,
        legend_name="Porcentaje de "+emocionOP.split("_")[1],



    ).add_to(world_map)


    choropleth.geojson.add_child(folium.features.GeoJsonTooltip(['name'], labels=False ))
    #folium_static(world_map)

    #col1, col2= st.columns(2)

#    col1.folium_static(world_map)

    #col1=folium_static(world_map)

    ##################################
    #nueva nube de palabras
    ###################################
    excluir=get_stop_words('spanish')
    lista_negra= ['covid', 'ansiedad', 'si', 'Covid_19', 'cómo', 'yomequedoencasa']
    excluir.extend(lista_negra)



    #sentimientoPalabra= st.sidebar.radio('Observar nube de palabras?', data.emocion.value_counts().keys().tolist())
    #sentimientoPalabra= st.sidebar.selectbox('Observar nube de palabras?', data.emocion.value_counts().keys().tolist())

    #st.markdown('## Nube de palabras por emociones: %s ' %(sentimientoPalabra) )
    df=data[data['emocion']== emoc]
    df=data[data['noticia']== noti]
    palabras= " ".join(df['tweet'])

    st.sidebar.subheader("Nube de Palabras")
    numPalabras = st.sidebar.select_slider('Seleciona la cantidad de palabras:', options=[20, 30, 40, 50, 60, 70, 80, 90, 100])


    plt.figure( figsize=(8,10) )
    palabrasProcesadas=' '.join([palabra for palabra in palabras.split() if 'http' not in palabra and not palabra.startswith('@') and palabra!= 'RT'])
    nubePalabras= WordCloud(stopwords= excluir, background_color='white', height=860, width=1200, max_words=numPalabras).generate(palabrasProcesadas)

    plt.imshow(nubePalabras)
    plt.xticks([])
    plt.yticks([])
    st.set_option('deprecation.showPyplotGlobalUse', False) #Quita mensaje de advertencia
    #st.pyplot()


    col1, col2= st.columns(2)
    #folium_static(world_map)
    col1.markdown("## Mapa de calor por emociones")
    with col1: folium_static(world_map)
    col2.markdown("## Nube de Palabras")
    col2.pyplot()

    #st.sidebar.markdown("___")
    #######################################################################

    ################# PRUEBA TEXTO#############################


    ##############################


    #######################################################################tyle="overflow-y: scroll
    ############### Barras apiladas #######################################
    #st.sidebar.subheader("Descomposición de sentimientos por paises")


    #LP=data.pais.value_counts().keys().tolist()
    #LP.append('Todo')
    #opcion=st.sidebar.multiselect("Selección de país", LP, key='0')

    #if "Todo" in opcion:
    #    opcion=["Argentina","Bolivia","Chile","Colombia","Costa Rica","Ecuador","El Salvador","Guatemala","Honduras","Mexico","Nicaragua","Panama","Uruguay","Peru","Paraguay","Venezuela","España","EEUU"]


    #if len(opcion) > 0:
    #    st.markdown('### Sentimientos por países')
    #    opcionD= data[data.pais.isin(opcion)]
    #    figOpcion= px.histogram(opcionD, x='noticia', y='pais', histfunc='count', color='emocion2', barnorm='percent',
    #    facet_row = 'noticia', labels={'noticia': 'tweets'}, height=750, width=800, orientation='h')
    #    st.plotly_chart(figOpcion)

    #st.sidebar.markdown("___")
    ######################################################################

    #####################################################################
    #####################Barras #########################################
    ####################################################################
    st.markdown("___")
    st.sidebar.subheader("Comparación de Emociones por Países")

    LP=data.pais.value_counts().keys().tolist()
    LP.append('Todo')
    opcion=st.sidebar.multiselect("Selección de país", LP, key='0')

    if "Todo" in opcion:
        opcion= data.pais.value_counts().keys().tolist()


    if len(opcion) > 0:
        #st.markdown("<a id='histograma-por-pais'> </a>", unsafe_allow_html=True) ## enlace
        st.markdown('## Comparación de emociones por países')
        opcionD= data[data.pais.isin(opcion)]
        figOpcion= px.histogram(opcionD, x='pais', y='noticia', histfunc='count', color='emocion', barmode='group', barnorm="percent",
        #facet_col = 'noticia', labels={'noticia': 'tweets'}, height=600, width=800)
        facet_col = 'noticia', labels={'noticia': 'Evento'}, height=700, width=1300)

        figOpcion.update_layout(font_size=23)



        st.plotly_chart(figOpcion)


    #st.sidebar.markdown("___")
    #####################################################################


    #st.markdown("<div id='barra_iconos', style='overflow-y: scroll'>", unsafe_allow_html=True)


    ################################################################
    ################### Tree map #############################
    ##########################################################
    #Enlace
#    st.sidebar.markdown("### Mapa de árbol")
    #chart1="<a style='text-decoration:none' href='#mapa-de-rbol-por-polaridad-emoci-n-y-pa-s'><p style='color:white; line-height:125%'><font size=4><b>Mapa de árbol</b></font></p></a>"
    #st.sidebar.markdown(chart1, unsafe_allow_html=True)

#    if not st.sidebar.checkbox("ocultar", True, key='3'):
#        st.header("Mapa de árbol por polaridad, emoción y país")
#        fig = px.sunburst(
        #fig =px.treemap(
#            path=[data.polaridad, data.emocion, data.pais],
#            color= data.emocion,
#            color_discrete_map={'(?)':'#ef9998', 'tristeza':'#9cd4eb', 'Dinner':'darkblue', 'negativo':'blue', 'Mexico':'blue'},
            #color_continuous_scale= 'Inferno',
            #hover_name= data.emocion,
#            values=data.puntuacion,
#            height = 600,
#            width = 800,
#            )
#        fig.update_traces( textinfo='label+text+value+percent parent')
#        st.plotly_chart(fig)
#    st.sidebar.markdown("___")
    ####################################################################
