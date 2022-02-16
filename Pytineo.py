# -*- coding: utf-8 -*-
"""
Created on Thu Nov 11 17:27:47 2021

@author: Gilles
"""
# -*- coding: utf-8 -*-

#Début du code
import streamlit as st
import pandas as pd


import plotly.express as px
import seaborn as sns 
import matplotlib.pyplot as plt

import streamlit.components.v1 as components

import threading
import time

import sys
sys.path.append('https://github.com/Gilukun/Pytineo/blob/main/Pytineo')
import Pytineo_module_clustering
import Pytineo_module_itineraires
import Pytineo_module_cartes

from PIL import Image


#affichage de la page sur toute sa largeur. Ce code doit toujour être le premier à être entré après l'import des modules
st.set_page_config(layout="wide")

st.sidebar.image("Pytineo_Logo_2.png", width=100)
#creation de la navigation du site (menu de gauche)
sidebar = st.sidebar.radio("Navigation", ["Accueil", "Analyse de données","Méthodologie", "Application Pytineo"]) 

#Premère page
if sidebar=="Accueil":
    intro = st.container()
    #image = Image.open('https://github.com/Gilukun/Pytineo/blob/main/Pytineo_Logo_2.jpg')
    with intro:
        col1, col2, col3= st.columns([1,1,1])
        with col2:
            st.image("Pytineo_Logo_2.png", caption=None, width=500, channels="RGB", output_format="auto")
            
        st.markdown("<h1 style='text-align: center;'>Application de création d itinéraires</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center;'>Réalisée en language Python</h3>", unsafe_allow_html=True)
        st.markdown("<h4 style='text-align: center;'>Gaëlle Lehur</h4>", unsafe_allow_html=True)
        st.markdown("<h4 style='text-align: center;'>Gilles Virassamy</h4>", unsafe_allow_html=True)
        st.markdown("<h4 style='text-align: center;'>Laurent Berrezaie</h4>", unsafe_allow_html=True)
    
        
        footlogo1, footlogo2, footlogo3= st.columns((1.4,1,1))
        with footlogo2:
            st.image("DataScientest_logo.png", caption=None, width=200, channels="RGB", output_format="auto")
    

#Seconde page 
if sidebar=="Analyse de données":
    #test d'une barre de progression
    my_bar = st.progress(0)

    for percent_complete in range(100):
         time.sleep(0.1)
         my_bar.progress(percent_complete + 1)

    #ouverture du Dataset
    df = pd.read_csv("datatourisme.POI_OK_20210921.PACA.csv", low_memory=False)
    #df_limit = df.groupby(df['Nom_commune'], as_index= False).agg({'Nom_du_POI':'count'})
    #st.dataframe(data=df_limit.head(15))
    
    #dico_POIs= dict(zip(df_limit['Nom_commune'], df_limit['Nom_du_POI']))
    #df['Nbr POIs']= df['Nom_commune'].map(dico_POIs)
    #df= df.loc[df['Nbr POIs']>=100]
    
    
    analysis = st.container()

    with analysis:
        st.markdown("<h1 style='text-align: center;'>Exploration des données</h1>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center;'>Données clés</h1>", unsafe_allow_html=True)
        
        #affichage de quelques data clés
        data1,data2,data3= st.columns((1,1,1))
        with data1 :
            label1 = '<p style="font-family:sans-serif; color:#336699 ; font-size: 24px;">Nombre Total de POI*</p>'
            st.markdown(label1, unsafe_allow_html=True) 
            nb_POI = df['Nom_du_POI'].nunique()
            st.metric(label="",value=nb_POI)
            st.markdown("<p style='text-align: left ;color:#336699 ; font-size: 14px;'>*POI (Points D'intérêts)</p>", unsafe_allow_html=True)
        
        with data2:
            nb_POI = df['Nom_commune'].nunique()
            label1 = '<p style="font-family:Arial; color:#336699 ; font-size: 24px;">Nombre Total de Commune</p>'
            st.markdown(label1, unsafe_allow_html=True) 
            st.metric(label="", value=nb_POI)
        
        with data3:
            nb_POI = df['Thématique_POI'].nunique()
            label1 = '<p style="font-family:sans-serif; color:#336699 ; font-size: 24px;">Nombre Total de Thématique</p>'
            st.markdown(label1, unsafe_allow_html=True) 
            st.metric(label="", value=nb_POI)
 
#---------------------
#Affichage du dataframe
#---------------------
        #insertion d'une ligne de sépartion
        st.markdown("""---""")
        st.markdown("<h2 style='text-align: center;'>Travaux préparatoires</h1>", unsafe_allow_html=True)
        
        clean1, clean2, clean3= st.columns((1,1,1))
        
        with clean1:
            st.markdown("<h3 style='text-align: left;'>Recherche des datasets</h3>", unsafe_allow_html=True)

        with clean2:
            st.markdown("<h3 style='text-align: left;'>Vérification des données</h3>", unsafe_allow_html=True)
     
        with clean3:
            st.markdown("<h3 style='text-align: left;'>Nettoyage des données</h3>", unsafe_allow_html=True)
        
        clean4, clean5, clean6,clean7, clean8, clean9 = st.columns((.2,1,.2,1,.2,1))
        with clean4:
            st.image("Icones/search_dataset.png",width=60,caption=None, channels="RGB", output_format="auto")
        with clean5:   
            st.markdown("<p style='text-align: left;'>Aucun dataset fourni avec le projet</p>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: left;'>3 datasets obtenues sur: </p>", unsafe_allow_html=True) 
            st.markdown("https://www.datatourisme.gouv.fr")
        
        with clean6:  
           st.image("Icones/Analysis.png",width=60,caption=None, channels="RGB", output_format="auto")
        with clean7: 
           st.markdown("<p style='text-align: left;'>Verification et correction du format des données</p>", unsafe_allow_html=True)
           st.markdown("<p style='text-align: left;'>Les datasets contiennent toutes les informations nécessaires (Nom POI/ Adress / Lat/Lon /Region / Communes/Code Postaux/etc..)</p>", unsafe_allow_html=True)
            
        with clean8:  
            st.image("Icones/clean.png",caption=None, width=60, channels="RGB", output_format="auto")
        with clean9:
           st.markdown("<p style='text-align: left;'>Supression des colonnes inutiles au projet</p>", unsafe_allow_html=True)
           

       
        st.markdown("""---""")
        st.markdown("<h3 style='text-align: left;'>Catégorisation des POIs </h3>", unsafe_allow_html=True)
        cat1, cat2, cat3= st.columns((1,1,1))
        
        with cat1:
            st.markdown("<h3 style='text-align: left;'>Recupération du type de POI</h3>", unsafe_allow_html=True)

        with cat2:
            st.markdown("<h3 style='text-align: left;'>Création des Thématiques</h3>", unsafe_allow_html=True)
     
        with cat3:
            st.markdown("<h3 style='text-align: left;'>Association des Thématiques</h3>", unsafe_allow_html=True)
            
        cat4, cat5, cat6, cat7, cat8, cat9= st.columns((0.1,1,0.2,1,0.2,1))
        with cat4:  
           st.image("Icones/URL.png",width=35, channels="RGB", output_format="auto")
        with cat5:
            st.markdown("<p style='text-align: left;'>Recherche du type de POI basé sur mots clés présents dans l'URL </p>", unsafe_allow_html=True)
            st.markdown("https://www.datatourisme.gouv.fr/ontology/core#CulturalSite|")
        
        with cat6:  
           st.image("Icones/dataset.png",width=35, channels="RGB", output_format="auto")
        with cat7:
            st.markdown("<p style='text-align: left;'>Nouveau dataset contenant:</p>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: left;'>[Mot_clé] [Mot_clé_FR] [Thématique]</p>", unsafe_allow_html=True)
        
        with cat8:  
           st.image("Icones/Associate.png",width=35, channels="RGB", output_format="auto")
        with cat9:
            st.markdown("<p style='text-align: left;'>Association des thématiques du dataset intermédiaire aux POIs dans le dataset final</p>", unsafe_allow_html=True)


        classe= pd.read_csv("datatourisme.place.POI_mots_cle.PACA.csv")
        st.caption('Exemple dataset Thématiques intermédiaire')
        st.dataframe(data= classe.head(20))
        
        st.caption('Exemple dataset final')
        st.dataframe(data=df.head(15))
        
        
    
#---------------------
#Camembert avec Plotly
#---------------------
    st.markdown("""---""")
    st.markdown("<h2 style='text-align: center;'>Répartition des type de POI</h1>", unsafe_allow_html=True)
    theme_count = df['Thématique_POI'].value_counts().sort_values()
    
    pie1,pie2, pie3 = st.columns((1,2,1))
    
    with pie2:                            
        Global_pie = px.pie(theme_count,
                            values=theme_count, 
                            names=theme_count.index,
                            title="Répartition des thèmes de POI",
                            width=600,
                            height=600,
                            hole=.4)
        
        Global_pie.update_traces(textposition='outside', textinfo='percent')
        Global_pie.update_layout(xaxis_title="Répartition des thèmes des POIs",
                                 font= dict(family="Arial", 
                                           size=13,
                                           color="#9b4595"),
                                 title={'y':0.95,
                                        'x':0.43,
                                        'xanchor': 'center',
                                        'yanchor': 'top'},
                                 title_font_family="Arial",
                                 title_font_color="#9b4595",
                                 legend_title_font_color="#9b4595",
                                 legend=dict(yanchor="top",
                                             y=0.99,
                                             xanchor='right',
                                             x=0 ))
        
        st.plotly_chart(Global_pie)
        
    
    
#---------------------------
#Histogramme avec Plotly
#---------------------------  
    st.markdown("""---""") 
    st.markdown("<h2 style='text-align: center;'>Répartition des types de POI par départements</h1>", unsafe_allow_html=True)
    PACA_Hist= px.histogram(df, x=['Nom_département'], 
                          color= df ['Thématique_POI'],
                          width=1450,
                          height=790,
                          title="Répartition des POIs par départements")
    
    #triage des données du plus grand au plus petit (nb total de POI)
    PACA_Hist.update_xaxes(categoryorder='total descending')
    
    #Modification des labels / couleurs/ Police etc...
    PACA_Hist.update_layout(xaxis_title="Nom du département",
                      yaxis_title="Thématiques des points d intérêt",
                      font=dict(family="Arial", 
                                size=13,
                                color="#9b4595"),
                      title={
                             'y':0.95,
                             'x':0.43,
                             'xanchor': 'center',
                             'yanchor': 'top'},
                      title_font_family="Arial",
                      title_font_color="Black",
                      legend_title_font_color="#3C738D",
                      plot_bgcolor="#fff")
    
    #Affichage du graph
    st.plotly_chart(PACA_Hist)

 
#---------------------------
#DensityMap avec Plotly
#---------------------------   
    st.markdown("""---""")
    st.markdown("<h2 style='text-align: center;'>Cartes de densités</h1>", unsafe_allow_html=True)
    #Création d'un dataframe contenant le total du nombre de chaque thématiques par commune
    dfheat = pd.crosstab (df['Nom_commune'], df['Thématique_POI']).reset_index()
    dfheat['Nbr POIs']=dfheat.sum(axis=1)
    
    #Ajout du total dans le df principal
    dico= dict(zip(dfheat['Nom_commune'], dfheat['Nbr POIs']))
    df['Nbr POIs']= df['Nom_commune'].map(dico)
    
    col1, col2 = st.columns((1,1))
    with col1 : 
        #Création du DensityMap
        PACA_density= px.density_mapbox(df, 
                                lat='Latitude', lon='Longitude', 
                                z='Nbr POIs', 
                                radius=10,
                                center=dict(lat=43.9351691, lon=6.0679194),
                                zoom=6,
                                mapbox_style="carto-positron",
                                color_continuous_scale = "Blues",
                                width=700,
                                height=700)
        PACA_density.update_layout(title= "Densité des Points d'intérêt en France", 
                          title_x= 0.5,
                          font=dict(size=18),
                          legend_title_text='Nbr POIs')
        
        st.plotly_chart(PACA_density)
        
    with col2:
        dfheat2 = pd.crosstab (df['Nom_commune'], df['Nbre_touristes']).reset_index()
        dfheat2['Nbr Touriste']=dfheat2.sum(axis=1)
        
        #Ajout du total dans le df principal
        dico= dict(zip(dfheat2['Nom_commune'], dfheat2['Nbr Touriste']))
        df['Nbr Touriste']= df['Nom_commune'].map(dico)

        #Création du DensityMap
        PACA_density= px.density_mapbox(dfheat2, 
                                lat='Latitude', lon='Longitude', 
                                z='Nbr Touriste', 
                                radius=10,
                                center=dict(lat=43.9351691, lon=6.0679194),
                                zoom=6,
                                mapbox_style="carto-positron",
                                color_continuous_scale = "Tealgrn",
                                width=700,
                                height=700)
        PACA_density.update_layout(title= "Densité du nombre de touriste en France", 
                          title_x= 0.5,
                          font=dict(size=18),
                          legend_title_text='Nbr Touriste')
        
        st.plotly_chart(PACA_density)
        
#---------------------------
#Comparaison Paris vs PACA
 #--------------------------- 
    st.markdown("""---""")
    st.markdown("<h2 style='text-align: center;'>Comparaison Régions Parisienne et PACA</h1>", unsafe_allow_html=True)
    liste_departements1 =[75,92,78,77,91,93,94]
    liste_departements2 =[4,5,6,13,83,84]
    
    df_regionsparis  = df.loc[df['Code_département'].isin(liste_departements1)]
    df_paca  = df.loc[df['Code_département'].isin(liste_departements2)]   

    Paris= px.histogram(df_regionsparis,
                      x= 'Nom_département',
                      color= 'Thématique_POI',
                      width=1400,
                      height=500,
                      title="Comparaison des POIs: Paris / PACA",
                      barmode='group')

    #Modification des labels / couleurs/ Police etc...
    Paris.update_layout(xaxis_title="Départements(Paris)",
                              font=dict(family="Arial",
                                     size=13,
                                     color="#9b4595"),
                           title={'y':0.95,
                                  'x':0.43,
                                  'xanchor': 'center',
                                  'yanchor': 'top'},
                          title_font_family="Arial",
                          title_font_color="Black",
                          showlegend=True,
                          legend_title_text="Thématique des POIs",
                          plot_bgcolor="#fff")
                          
    Paris.update_xaxes(showgrid=True, zeroline=False, linecolor='black')
    Paris.update_yaxes(showgrid=True, zeroline=False, linecolor='black', gridcolor='#9b4595')
    
    Paris.update_layout(xaxis={'categoryorder':'total descending'})
    
    #Affichage du graph
    st.plotly_chart(Paris)
    PACA= px.histogram(df_paca,
                      x= 'Nom_département',
                      color= 'Thématique_POI',
                      width=1400,
                      height=500,
                      barmode='group')

    #Modification des labels / couleurs/ Police etc...
    PACA.update_layout(xaxis_title="Départements (PACA)",
                              font=dict(family="Arial",
                                     size=13,
                                     color="#9b4595"),
                           title={'y':0.95,
                                  'x':0.43,
                                  'xanchor': 'center',
                                  'yanchor': 'top'},
                          title_font_family="Arial",
                          title_font_color="Black",
                          showlegend=True,
                          legend_title_text="Thématique des POIs",
                          plot_bgcolor="#fff")
                          
    PACA.update_xaxes(showgrid=True, zeroline=False, linecolor='black')
    PACA.update_yaxes(showgrid=True, zeroline=False, linecolor='black', gridcolor='#9b4595')
    
    PACA.update_layout(xaxis={'categoryorder':'total descending'})
    
    #Affichage du graph
    st.plotly_chart(PACA)

#---------------------------
#Comparaison avec Plotly Bar
#---------------------------   
    st.markdown("""---""") 
    st.markdown("<h2 style='text-align: center;'>Outil de comparaison du nombre de POIs</h1>", unsafe_allow_html=True)
    
    
    
    comp1, comp2= st.columns((1,2))
    with comp1:
        #création des valeur des sélecteurs
        dep = df['Nom_département'].drop_duplicates().sort_values()
        
        #crétatoin des sélecteurs
        select_dep1 = st.selectbox('Selectionnez votre département:', dep, key=1,index =0)
        
        select_dep2 = st.selectbox('Selectionnez votre département:', dep, key=2,index=1)
        
        #création du dataframe d'alimentation du graphique en barre
        df_dep = df.groupby(df['Nom_département'], as_index= False).agg({'Nom_du_POI':'count'})             
        df_comp = df_dep.loc[(df_dep['Nom_département']==select_dep1) | (df_dep['Nom_département']==select_dep2)]
        
        #je renomme les colonnes pour plus de simplicité d'affichage du graphique
        df_comp.columns=['Nom_Département', 'Nombre_de_POI']
        
    with comp2: 
        Comp_bar= px.bar(df_comp,
                          x= 'Nom_Département',
                          y= 'Nombre_de_POI',
                          color= 'Nom_Département',
                          width=900,
                          height=500,
                          title="Comparaison du nombre de POI",
                          color_discrete_map={df_comp['Nom_Département'].iloc[0]: '#9999CC',
                                              df_comp['Nom_Département'].iloc[1]: '#55E8DC'},
                          #opacity= 0.5,
                          text='Nombre_de_POI')
    
        
        #Modification des labels / couleurs/ Police etc...
        Comp_bar.update_layout(xaxis_title="Nom du département",
                               yaxis_title="Nombre de POIs",
                               font=dict(family="Arial",
                                         size=13,
                                         color="#9b4595"),
                               title={'y':0.95,
                                      'x':0.43,
                                      'xanchor': 'center',
                                      'yanchor': 'top'},
                              title_font_family="Arial",
                              title_font_color="Black",
                              showlegend=False,
                              plot_bgcolor="#fff")
                              
        Comp_bar.update_xaxes(showgrid=True, zeroline=False, linecolor='black')
        Comp_bar.update_yaxes(showgrid=True, zeroline=False, linecolor='black', gridcolor='#9b4595')
        
        Comp_bar.update_layout(xaxis={'categoryorder':'total descending'})
        
        #Affichage du graph
        st.plotly_chart(Comp_bar)
        
        
        
if sidebar=="Méthodologie": 
    st.markdown("<h1 style='text-align: center;'> Principe de Construction d'un Itinéraire</h1>", unsafe_allow_html=True)
    prez1,middle,prez2, = st.columns((1,.6,1))
    with prez1:
        st.markdown("<h2 style='text-align: center;'>Etape 1</h1>", unsafe_allow_html=True)
        st.image("Presentation/Présentation_1.png",use_column_width=True)
        st.markdown("<p style='text-align: center;'>Les 2 POIs (POI1/ POI2) les plus proches du point de référence (ici, centre de la commune) sont potentiellement éligibles à l'intégration dans l'itinéraire</p>", unsafe_allow_html=True)
        
    with prez2:
        st.markdown("<h2 style='text-align: center;'>Etape 2</h2>", unsafe_allow_html=True)
        st.image("Presentation/Présentation_2.png",use_column_width=True)
        st.markdown("<p style='text-align: center;'>Aléatoirement POI1 ou POI2 est choisi pour intégrer l'itinéraire. Ici POI2 devient le nouveau point de référence. POI1 ne peut plus être intégré</p>", unsafe_allow_html=True)
    
    st.markdown("""---""") 
    prez3,middle, prez4 =st.columns((1,.4,1))
    with prez3:
        st.markdown("<h2 style='text-align: center;'>Etape 3</h2>", unsafe_allow_html=True)
        st.image("Presentation/Présentation_3.png",use_column_width=True)
        st.markdown("<p style='text-align: center;'>Les deux points les plus proche de POI2 sont POI4 et POI5. POI4 est choisi de façon aléatoire. POI5 ne peut plus être intégré</p>", unsafe_allow_html=True)
        
    with prez4:
        st.markdown("<h2 style='text-align: center;'>Etape 4</h2>", unsafe_allow_html=True)
        st.image("Presentation/Présentation_4.png", use_column_width=True)
        st.markdown("<p style='text-align: center;'>De proche en proche, construction d'un itinéraire complet comprenant 10 POIS</p>", unsafe_allow_html=True)
    
    st.markdown("""---""") 
    st.markdown("<h1 style='text-align: center;'>Intégration des POIs Pédestres/Cyclables/Routiers</h1>", unsafe_allow_html=True)
    prez5,middle,prez6= st.columns((1,.4,1))
    with prez5:
        st.markdown("<h2 style='text-align: center;'>Etape 1</h2>", unsafe_allow_html=True)
        st.image("Presentation/Présentation_5.png", use_column_width=True)
        st.markdown("<p style='text-align: center;'>Détection du POI du type itinéraire touristique (pédestre/ cyclable/routier) le plus proche du centre de la commune(POI6)</p>", unsafe_allow_html=True)
        
    with prez6:
        st.markdown("<h2 style='text-align: center;'>Etape 2/h1>", unsafe_allow_html=True)
        st.image("Presentation/Présentation_6.png", use_column_width=True)
        st.markdown("<p style='text-align: center;'>Construction de la première partie de l’itinéraire</p>", unsafe_allow_html=True)
    
    st.markdown("""---""") 
    prez7,middle,prez8= st.columns((1,.4,1))
    with prez7:
        st.markdown("<h2 style='text-align: center;'>Etape 3</h2>", unsafe_allow_html=True)
        st.image("Presentation/Présentation_7.png",use_column_width=True)
        st.markdown("<p style='text-align: center;'>Intégration du POI de type Itinéraire pédestre</p>", unsafe_allow_html=True)
        
    with prez8:
        st.markdown("<h2 style='text-align: center;'>Etape 4</h2>", unsafe_allow_html=True)
        st.image("Presentation/Présentation_8.png", use_column_width=True)
        st.markdown("<p style='text-align: center;'>Construction de la seconde partie de l’itinéraire</p>", unsafe_allow_html=True)
    
    st.markdown("""---""") 
    st.markdown("<h1 style='text-align: center;'>Machine Learning : KMeans</h1>", unsafe_allow_html=True)
    prez9,middle,prez10= st.columns((1,.4,1))
    with prez9:
        st.markdown("<h2 style='text-align: center;'>Etape 1</h2>", unsafe_allow_html=True)
        st.image("Presentation/Présentation_9.png",use_column_width=True)
        st.markdown("<p style='text-align: center;'>Implémentation de la méthode Kmeans sur autant de centroids que de journées de séjours (ici 7 jours)</p>", unsafe_allow_html=True)
        
    with prez10:
        st.markdown("<h2 style='text-align: center;'>Etape 2</h2>", unsafe_allow_html=True)
        st.image("Presentation/Présentation_10.png",use_column_width=True)
        st.markdown("<p style='text-align: center;'>Élimination des centroids ne comportant pas suffisamment de POI. Ici Centroid3/4.Construction de plusieurs itinéraires autour des centroids comportant le plus grand nombre de POIs.</p>", unsafe_allow_html=True)
    
    st.markdown("""---""") 
    st.markdown("<h1 style='text-align: center;'>Cas Particulier des Restaurants</h1>", unsafe_allow_html=True)
    prez11,middle,prez12= st.columns((1,.4,1))
    with prez11:
        st.markdown("<h2 style='text-align: center;'>Etape 1</h2>", unsafe_allow_html=True)
        st.image("Presentation/Présentation_11.png",use_column_width=True)
        st.markdown("<p style='text-align: center;'>Les POI de type Restauration ou Gastronomie ne sont pas intégrés aux itinéraires. Seuls les plus proches du barycentre de l’itinéraire sont matérialisés par une icone.</p>", unsafe_allow_html=True)
        
    
    
#Page 3            
if sidebar=="Application Pytineo":
    st.markdown("<h1 style='text-align: center;'>Pytineo</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>Démo de l'application</h1>", unsafe_allow_html=True)
    st.markdown("""---""") 
    
    #Création des menus de sélection des variables
    df= pd.read_csv("Datatourisme.csv",low_memory=False)
    df_POI = df[~df['Nom_commune'].str.contains('Arrondissement')]
    #df_limit = df.groupby(df['Nom_commune'], as_index= False).agg({'Nom_du_POI':'count'})
    #dico_POIs= dict(zip(df_limit['Nom_commune'], df_limit['Nom_du_POI']))
    #df['Nbr POIs']= df['Nom_commune'].map(dico_POIs)
    #df_POI= df.loc[df['Nbr POIs']>=200]
    #df_POI= df_POI.dropna()
    #st.dataframe(data=df_POI.head(30))
    #st.write(df_POI['Nom_département'].unique())
    
    reg1, reg2, day = st.columns((1,1,1))
    with reg1: 
        #Menu de selection du département
        dep = df_POI['Nom_département'].drop_duplicates().sort_values()
        
        choix_departement = st.selectbox('Selectionnez votre département:', dep)
        nom_dep_reference = choix_departement
        df_POI= df_POI.loc[df_POI['Nom_département'].isin([nom_dep_reference])]
        
    with reg2 : 
        #Menu de sélection de la commune
        commune = df_POI['Nom_commune'].drop_duplicates().sort_values()
        
        choix_commune = st.selectbox('Selectionnez votre commune:', commune)
        nom_commune_reference = choix_commune
    
    with day:
        #menu de sélection des jours
        selection_nb_jour = st.number_input("Nombre de jour de visite", min_value=1, max_value=7, step=1)
        duree_du_sejour  = selection_nb_jour  
        
    th, sth = st.columns((1,1))
    #menu de sleection des thèmes
    
    with th: 
        theme = ("Commerce", "Culture et social","Gastronomie","Loisir","Patrimoine","Site naturel","Sport")
        choix_theme = st.multiselect('Selectionnez votre thème:',theme, default= theme )
        list_theme_reference = choix_theme
        
        theme_boolean=[]
        for i in theme: 
            if i in list_theme_reference:
                theme_boolean.append (True)
            if i not in list_theme_reference:
                theme_boolean.append (False)
        
        dict_themes =  dict(zip(theme, theme_boolean))
        
           
    with sth: 
        sous_theme = ("Itinéraire touristique","Itinéraire pédestre","Itinéraire cyclable","Itinéraire routier","Restauration", "Restauration rapide")
        choix_theme = st.multiselect('Selectionnez votre sous-thème:',sous_theme, default= sous_theme )
        list_sous_theme_reference = choix_theme
        
        sous_theme_boolean=[]
        for i in sous_theme: 
            if  i in list_sous_theme_reference:
                sous_theme_boolean.append (True)
            else:
                sous_theme_boolean.append (False)
        
        dict_sous_themes =  dict(zip(sous_theme , sous_theme_boolean))
       
    #dict_themes = {"Commerce":True,                                                                       ## thématiques de POI souhaitées par l'utilisateur
               #"Culture et social":True,
               #"Gastronomie":True,
               #"Loisir":True,
               #Patrimoine":True,
               #"Site naturel":True,
               #"Sport":True}
    
    #dict_sous_themes = {"Itinéraire touristique":True,
                 #"Itinéraire pédestre":True,                                                                        
                 #"Itinéraire cyclable":True,                                                                       
                 #"Itinéraire routier":True,                                                                        
                 #"Restauration":True,     
                 #"Restauration rapide":True}
    
    
    #affichage de la légende des cartes
    with st.expander("Cliquez pour afficher la légende"):
        img1,img2,img3,img4,img5,img6,img7= st.columns((1,1,1,1,1,1,1))
        with img1:
            st.image("Logos_POIs/logo_commerce_service.png", caption="Commerce",width=100)
        with img2:
            st.image("Logos_POIs/logo_culture_social.png", caption="Culture/Social",width=100)
        with img3:
            st.image("Logos_POIs/logo_evt_sportif.png", caption="Evènement Sportif",width=100)
        with img4:
            st.image("Logos_POIs/logo_itineraire.png", caption="Itinéraires",width=120)
        with img5:
            st.image("Logos_POIs/logo_loisir.png", caption="Loisir",width=100)
        with img6:
            st.image("Logos_POIs/logo_marche_a_pied.png", caption="Marche à pied",width=100)
        with img7:
            st.image("Logos_POIs/logo_patrimoine.png", caption="Patrimoine",width=100)
          
       
        img8,img9,img10,img11,img12,img13,img14= st.columns((1,1,1,1,1,1,1)) 
        with img8:
            st.image("Logos_POIs/logo_restauration_rapide.png", caption="Retauration Rapide",width=100)
        with img9:
            st.image("Logos_POIs/logo_restauration.png", caption="Gastronomie",width=100)
        with img10:
            st.image("Logos_POIs/logo_site_naturel.png", caption="Site Naturel",width=100)
        with img11:
            st.image("Logos_POIs/logo_sports.png", caption="Sport",width=100)
        with img12:
            st.image("Logos_POIs/logo_terroir.png", caption="Terroir",width=100)
        with img13:
            st.image("Logos_POIs/logo_velo.png", caption="Velo",width=100)
        with img14:
            st.image("Logos_POIs/logo_voiture.png", caption="Voiture",width=100)
    
    ##-------------------------------
    ## Mise en forme des paramètres 
    ##-------------------------------
    degre_alea_itineraire = 'faible'                                                                      ## valeurs possibles : 'sans', 'faible', 'moyen', 'fort'
    valeurs_degre_alea = {'sans':1, 'faible':2, 'moyen':3, 'fort':4}                                      ## plus l'aléa est elevé, plus les itinéraires s'éloignent du centre de la commune
    for cle, valeur in valeurs_degre_alea.items():
        if cle == degre_alea_itineraire:
            alea_construction_itineraire = valeur  
    
    dict_parametres_techniques = {'max_POI_TOUR_par_itineraire':1, 'alea_construction_itineraire':alea_construction_itineraire, 'max_POI_par_itineraire':10, 'min_distance_entre_2_POI':0.05, 'distance_max_POI_reference':20, 'nbre_POI_resto_dans_perimetre_iti':15}
    
    ##----------
    ## Classes 
    ##----------
    ## les traitements de construction des itinéraires autour des centroids se font en parallèle afin d'optimiser le temps de réponse global
    class traitement_par_centroid (threading.Thread):
        def __init__(self, no_centroid, lat_centroid, lon_centroid, nbre_itineraires, dataframe):
            threading.Thread.__init__(self)
            self.no_centroid = no_centroid
            self.lat_centroid = lat_centroid
            self.lon_centroid = lon_centroid
            self.nbre_itineraires = nbre_itineraires
            self.dataframe = dataframe
            self.etat = False                                                                              ## l'état du thread est soit False (à l'arrêt)
            
        def run(self):
            self.etat = True                                                                               ## passage en mode marche (actif) 
            
           ## appel au module chargé de déterminer les POI des différents itinéraires 
            globals()[f"liste_itineraires_centroid_{self.no_centroid}"], globals()[f"df_POI_zoom_sur_centroid_{self.no_centroid}"] = Pytineo_module_itineraires.StartPoint(self.no_centroid, self.lat_centroid, self.lon_centroid, self.nbre_itineraires, self.dataframe, dict_parametres_techniques['distance_max_POI_reference'], dict_sous_themes["Itinéraire pédestre"], dict_sous_themes["Itinéraire cyclable"], dict_sous_themes["Itinéraire routier"], dict_parametres_techniques['max_POI_TOUR_par_itineraire'], dict_parametres_techniques['alea_construction_itineraire'], dict_parametres_techniques['max_POI_par_itineraire'], dict_parametres_techniques['min_distance_entre_2_POI']) 
            
            self.etat = False                                                                              ## retour en mode arrêt (passif)  
    
            
    ##------------
    ## Fonctions
    ##------------
    def analyse_resultats_par_itineraire(no_centroid, no_itineraire, POI_itineraire, df_POI_zoom_sur_centroid, carte_openrouteservice, pos_geo_itineraire, no_centroid_deja_traite):
    
        print('--------------------------------------------------------')
        print('Itinéraire numéro', no_itineraire, 'du centroïd', no_centroid)
        print(pos_geo_itineraire) 
        if carte_openrouteservice:
            print('Cet itinéraire s\'appuie sur le réseau routier')
        else:
            print('Cet itinéraire ne peut pas s\'appuiyer sur le réseau routier')    
        print('Nom des POI de l\'itinéraire :', POI_itineraire)
        print('--------------------------------------------------------', '\n')
      
        if not no_centroid_deja_traite:
            no_centroid_deja_traite = True
            
            print('--------------------------------------------------------')
            print('Répartition des POI par mot_clé dans le centroïd', no_centroid)
            print('--------------------------------------------------------')
            print(df_POI_zoom_sur_centroid['Mot_clé_POI'][df_POI_zoom_sur_centroid['POI_dans_itineraire'] == True].value_counts(),'\n')        
    
            print('--------------------------------------------------------')
            print('Répartition des POI par thématique dans le centroïd', no_centroid)
            print('--------------------------------------------------------')
            print(df_POI_zoom_sur_centroid['Thématique_POI'][df_POI_zoom_sur_centroid['POI_dans_itineraire'] == True].value_counts(), '\n') 
            print('Nombre de POI total : ', df_POI_zoom_sur_centroid[df_POI_zoom_sur_centroid['POI_dans_itineraire'] == True].shape[0],'\n')   
        
        return no_centroid_deja_traite
     
        
    def analyse_resultats_par_carte(no_centroid, no_itineraire, POI_resto_itineraire, liste_theme_POI_resto, liste_mot_cle_POI_resto, dict_attributs_sejour):    
    
        print('--------------------------------------------------------')
        print('Itinéraire numéro', no_itineraire, 'du centroïd', no_centroid) 
        print('Nom des POI "Restauration" ou "Gastronomie" :', POI_resto_itineraire)
        print('--------------------------------------------------------', '\n')   
                  
        cpt_gastronomie = 0
        for thématique in liste_theme_POI_resto:
            if thématique == dict_attributs_sejour['Gastronomie']:
                cpt_gastronomie +=1
        print('Nombre de POI de type', dict_attributs_sejour['Gastronomie'], ': ', cpt_gastronomie)      
               
        cpt_resto = 0  
        cpt_resto_rapide = 0
        for mot_cle in liste_mot_cle_POI_resto:
            if mot_cle == dict_attributs_sejour['Restauration']:
                cpt_resto +=1
            if mot_cle == dict_attributs_sejour['Restauration rapide']:
                cpt_resto_rapide +=1
        print('Nombre de POI de type', dict_attributs_sejour['Restauration'], ': ', cpt_resto) 
        print('Nombre de POI de type', dict_attributs_sejour['Restauration rapide'], ': ', cpt_resto_rapide, '\n')       
    
    
    def affichage_des_cartes(liste_cartes):
    
        col1, col2 = st.columns([1,1])
    
        with col1:
            if liste_cartes[0][2] == True:                                                              ## booléen carte en mode réseau routier
                st.markdown(":information_source:" + " " + "Itinéraire routier " + liste_cartes[0][1][11:])
            else:
                st.markdown(":small_orange_diamond:" + " " + "Itinéraire non routier " + liste_cartes[0][1][11:])
            components.html(liste_cartes[0][0]._repr_html_(), height=500, width=700)                    ## contenu de la carte
    
        with col2:
            if len(liste_cartes) > 1:
                if liste_cartes[1][2] == True:                                                          ## booléen carte en mode réseau routier
                    st.markdown(":information_source:" + " " + "Itinéraire routier " + liste_cartes[1][1][11:])
                else:
                    st.markdown(":small_orange_diamond:" + " " + "Itinéraire non routier " + liste_cartes[1][1][11:])
                components.html(liste_cartes[1][0]._repr_html_(), height=500, width=700)                ## contenu de la carte
    
    
    ##----------------------------------------------------------------------------------------------------------
    ## Implémentation de la méthode de clustering (KMEANS) pour identifier les principaux regroupements de POI
    ##----------------------------------------------------------------------------------------------------------
    POI_disponibles_sur_commune, dict_final_centroids_nbre_itineraires, dict_df_POI_zoom_sur_centroid, dict_attributs_sejour = Pytineo_module_clustering.StartPoint(nom_commune_reference, duree_du_sejour, dict_themes, dict_sous_themes, df_POI, dict_parametres_techniques)
    
    ## le traitement ne se poursuit que si le nombre de POI situé dans le périmètre élargie de la commune est suffisamment important (20 par défaut)
    if POI_disponibles_sur_commune:
    
        ##-----------------------------------------------------------
        ## Identification des POI qui constitueront les itinéraires
        ##-----------------------------------------------------------
        for cle, valeur in dict_final_centroids_nbre_itineraires.items():
            globals()[f"df_POI_zoom_sur_centroid_{cle}"] = dict_df_POI_zoom_sur_centroid[cle]
            globals()[f"trait_itineraires_centroid_{cle}"] =  traitement_par_centroid(cle, dict_final_centroids_nbre_itineraires[cle][0], dict_final_centroids_nbre_itineraires[cle][1], dict_final_centroids_nbre_itineraires[cle][2], globals()[f"df_POI_zoom_sur_centroid_{cle}"])
            globals()[f"trait_itineraires_centroid_{cle}"].start()
    
        ##----------------------------------
        ## Synchronisation des traitements
        ##----------------------------------
        for cle, valeur in dict_final_centroids_nbre_itineraires.items():
            while globals()[f"trait_itineraires_centroid_{cle}"].etat == False:
               # on attend que le thread démarre
                time.sleep(0.05)
    
        for cle, valeur in dict_final_centroids_nbre_itineraires.items():
            while globals()[f"trait_itineraires_centroid_{cle}"].etat == True:
               # on attend que le thread s'arrête, puis introduction de l'instruction time.sleep pour temporiser
               # Il n'est pas nécessaire de vérifier en continue que le thread soit toujours actif : il suffit de le vérifier tous les 100 millisecondes
                time.sleep(0.05)
    
        ##----------------------------------------------------
        ## Constitution et affichage des cartes interactives
        ##----------------------------------------------------
    
        st.title('Affichage des cartes interactives')
    
        nbre_itineraires_construits = 0
        for cle, valeur in dict_final_centroids_nbre_itineraires.items():
            nbre_itineraires_construits += valeur[2]
    
        liste_cartes_affichage_colonne = []
        cpt_nbre_itineraires = 0
    
        for cle, valeur in dict_final_centroids_nbre_itineraires.items():
            i = 0
            no_centroid_deja_traite = False
    
            for itineraire in globals()[f"liste_itineraires_centroid_{cle}"]:
                i +=1
                dict_attributs_itineraire = {'no_centroid':cle, 'lat_centroid':dict_final_centroids_nbre_itineraires[cle][0], 'long_centroid':dict_final_centroids_nbre_itineraires[cle][1], 'POI_itineraire':itineraire}
                fmap, carte_openrouteservice, pos_geo_itineraire, liste_nom_POI_resto, liste_theme_POI_resto, liste_mot_cle_POI_resto = Pytineo_module_cartes.StartPoint(globals()[f"df_POI_zoom_sur_centroid_{cle}"], dict_attributs_itineraire, dict_attributs_sejour)
    
                liste_temporaire = []
                liste_temporaire.append(fmap)
                liste_temporaire.append(pos_geo_itineraire)
                liste_temporaire.append(carte_openrouteservice)
                liste_cartes_affichage_colonne.append(liste_temporaire)
                cpt_nbre_itineraires += 1
    
                if  (nbre_itineraires_construits == 1) \
                    | ((cpt_nbre_itineraires / 2) - round(cpt_nbre_itineraires / 2) == 0) \
                    | ((len(liste_cartes_affichage_colonne) == 1 ) & (cpt_nbre_itineraires == nbre_itineraires_construits)):
    
                    affichage_des_cartes(liste_cartes_affichage_colonne)
                    liste_cartes_affichage_colonne = []
    
                no_centroid_deja_traite = analyse_resultats_par_itineraire(cle, i, itineraire, globals()[f"df_POI_zoom_sur_centroid_{cle}"], carte_openrouteservice, pos_geo_itineraire, no_centroid_deja_traite)
                analyse_resultats_par_carte(cle, i, liste_nom_POI_resto, liste_theme_POI_resto, liste_mot_cle_POI_resto, dict_attributs_sejour)
    else:
        st.title('Affichage des cartes interactives')
        st.markdown(":warning:" + " " + "Le nombre insuffisant de points d'intérêt touristique présents sur la commune sélectionnée ne permet pas de proposer des itinéraires")
        
           
