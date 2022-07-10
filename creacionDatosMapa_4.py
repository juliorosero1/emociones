import pandas as pd

def cTabla(noticia):

    data= pd.read_csv("sentimientosTweet_3.csv", usecols=('pais','emocion', 'emocion2', 'noticia'))
    tabla=pd.DataFrame()


    data=porNoticia(noticia)
    paises=data.pais.value_counts().keys().tolist()
    tabla=tabla.assign(pais=paises)

    nMiedo=[]; nIra=[]; nExpectante=[]; nConfianza=[]; nSorpresa=[]; nTristeza=[]; nRepulsion=[];
    nAlegria=[]; nPositivo=[]; nNegativo=[]; nDepresion=[]; nAnsiedad=[]


    df=data.drop(columns=['noticia'])
    for pais in tabla.pais:
        miedo=df[(df.pais==pais) &(df.emocion2=='miedo')].value_counts().tolist()
        if not miedo : nMiedo.append(0)
        else: nMiedo.append(miedo[0])

        ira=df[(df.pais==pais) &(df.emocion2=='ira')].value_counts().tolist()
        if not ira: nIra.append(0)
        else: nIra.append(ira[0])

        expectante=df[(df.pais==pais) &(df.emocion2=='expectante')].value_counts().tolist()
        if not expectante: nExpectante.append(0)
        else: nExpectante.append(expectante[0])

        confianza=df[(df.pais==pais) &(df.emocion2=='confianza')].value_counts().tolist()
        if not confianza: nConfianza.append(0)
        else: nConfianza.append(confianza[0])

        sorpresa=df[(df.pais==pais) &(df.emocion2=='sorpresa')].value_counts().tolist()
        if not sorpresa: nSorpresa.append(0)
        else: nSorpresa.append(sorpresa[0])

        tristeza=df[(df.pais==pais) &(df.emocion2=='tristeza')].value_counts().tolist()
        if not tristeza: nTristeza.append(0)
        else: nTristeza.append(tristeza[0])

        repulsion=df[(df.pais==pais) &(df.emocion2=='repulsion')].value_counts().tolist()
        if not repulsion: nRepulsion.append(0)
        else: nRepulsion.append(repulsion[0])

        alegria=df[(df.pais==pais) &(df.emocion2=='alegria')].value_counts().tolist()
        if not alegria: nAlegria.append(0)
        else: nAlegria.append(alegria[0])

        positivo=df[(df.pais==pais) &(df.emocion2=='positivo')].value_counts().tolist()
        if not positivo: nPositivo.append(0)
        else: nPositivo.append(positivo[0])

        negativo=df[(df.pais==pais) &(df.emocion2=='negativo')].value_counts().tolist()
        if not negativo: nNegativo.append(0)
        else: nNegativo.append(negativo[0])

        depresion=df[(df.pais==pais) &(df.emocion2=='depresion')].value_counts().tolist()
        if not depresion: nDepresion.append(0)
        else: nDepresion.append(depresion[0])

        ansiedad=df[(df.pais==pais) &(df.emocion2=='ansiedad')].value_counts().tolist()
        if not ansiedad: nAnsiedad.append(0)
        else: nAnsiedad.append(ansiedad[0])


    noti=data.noticia.value_counts().keys().tolist()
    df=data.drop(columns=["emocion2"])

    nNavidad=[];nConfinamiento=[]; nGuayaquil=[]

    for pais in tabla.pais:
        navidad= df[(df.pais==pais)&(df.noticia=='Navidad')].value_counts().tolist()
        if not navidad: nNavidad.append(0)
        else: nNavidad.append(navidad[0])

        confinamiento= df[(df.pais==pais)&(df.noticia=='Nuevo confinamiento')].value_counts().tolist()
        if not confinamiento: nConfinamiento.append(0)
        else: nConfinamiento.append(confinamiento[0])

        guayaquil= df[(df.pais==pais)&(df.noticia=='Crisis Guayaquil')].value_counts().tolist()
        if not guayaquil: nGuayaquil.append(0)
        else: nGuayaquil.append(guayaquil[0])


    #tabla.pais=tabla.pais.map({'EEUU':'United States'},na_action=None)
    tabla.pais=tabla.pais.replace(['EEUU', 'España', 'Republica Dominicana'], ['United States', 'Spain', 'Dominican Rep.'] )

    tabla=tabla.assign(miedo=nMiedo)
    tabla=tabla.assign(ira=nIra)
    tabla=tabla.assign(expectante=nExpectante)
    tabla=tabla.assign(confianza=nConfianza)
    tabla=tabla.assign(sorpresa=nSorpresa)
    tabla=tabla.assign(tristeza=nTristeza)
    tabla=tabla.assign(repulsion=nRepulsion)
    tabla=tabla.assign(alegria=nAlegria)
#    tabla=tabla.assign(positivo=nPositivo)
#    tabla=tabla.assign(negativo=nNegativo)
    tabla=tabla.assign(depresion=nDepresion)
    tabla=tabla.assign(ansiedad=nAnsiedad)

    #NOTICIAS
    tabla=tabla.assign(N_guayaquil= nGuayaquil)
    tabla=tabla.assign(N_navidad= nNavidad)
    tabla=tabla.assign(N_confinamiento= nConfinamiento)


    return tabla

#noticia="Nuevo confinamiento"

def porNoticia(noticia):
    data= pd.read_csv("sentimientosTweet_3.csv", usecols=('pais','emocion', 'emocion2', 'noticia'))
    data=data[data.noticia==noticia]

    return data
