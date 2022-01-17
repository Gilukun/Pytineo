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
import matplotlib.pyplot as plt
import seaborn as sns

import folium
from streamlit_folium import folium_static

#import openrouteservice 
#from openrouteservice import client

from sklearn.cluster import KMeans

import streamlit.components.v1 as components

import threading
import time

import sys
sys.path.append('/Documents/GitHub/Pytineo')
import Pytineo_module_clustering
import Pytineo_module_itineraires
import Pytineo_module_cartes




#affichage de la page sur toute sa largeur. Ce code doit toujour être le premier à être entré après l'import des modules
st.set_page_config(layout="wide")


#creation de la navigation du site (menu de gauche)
sidebar = st.sidebar.radio("Navigation", ["Acceuil", "Visualisations", "Démos", "Test cartes multiples"]) 

#Premère page
if sidebar=="Acceuil":
    intro = st.container()
    with intro:
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            st.image("Pytineo_logo_2.png", caption=None, width=700, use_column_width=700, clamp=False, channels="RGB", output_format="auto")
        
        col1, col2, col3 = st.columns([1,1,1])
        with col2:
            st.write("Gaëlle Le Hur")
            st.write("Gilles Virassamy")
            st.write("Laurent Berrezaie")
        with col3: 
            st.image("DataScientest_logo.png", caption=None, width=300, use_column_width=300, clamp=False, channels="RGB", output_format="auto")
           
        
       
    

#Seconde page 
if sidebar=="Visualisations":
    col1, col2, col3 = st.columns([3,1,1])
    with col1:
        st.write("")
    with col2:
        st.write("")
    with col3:
        st.image("Pytineo_logo_2.png", caption=None, width=100, use_column_width=100, clamp=False, channels="RGB", output_format="auto")
            
    
    df = pd.read_csv("datatourisme.POI_OK_20210921.PACA.csv")
    
    
    analysis = st.container()

    with analysis:
        st.header("Analyse de données")
        st.write('Analyse des datasets pour définir notre projet')
        st.dataframe(data=df.head(10))
    
    theme_count = df['Thématique_POI'].value_counts().sort_values()
    
#---------------------
#Camembert avec Plotly
#---------------------
    #Création de 2 colonnes sur la page
    #(2,1) => la première colonne sera 2 fois plus grande que la seconde colonne
    col1, col2 = st.columns((2,1))
    with col1 : 
        plotlypie_theme = px.pie(theme_count, 
                                 values=theme_count, 
                                 names=theme_count.index, 
                                 title="Répartition des thèmes de POI",
                                 width=1000, 
                                 height=500)
        
        plotlypie_theme.update_traces(textposition='outside', textinfo='percent')
        st.plotly_chart(plotlypie_theme)
        st.caption('Répartition des POIs du DataSet')
    
    with col2:
        #Création d'une zone de texte pour commenter le graphique
        st.write("Note expliquant le graphique")
    
#---------------------------
#Histogramme avec Matplotlib
#---------------------------
#Création du menu de sélection des thématique
    #Df ne contenant que les valeurs unique des thématiques
    theme = df["Thématique_POI"].drop_duplicates()
    
    #Création du menu avec par défaut l'affichage de tous les thèmes
    themeselect= st.multiselect("Thématique POI",theme, default = theme)
    
    #Création du dataframe ne contenant que les thématiques sélectionnées
    themenotselect=[]
    for i in theme:
        if i not in themeselect:
            themenotselect.append(i)
    df_com_bar = df[~df['Thématique_POI'].isin(themenotselect)]
    
    #séparation de la page en 2 colonnes
    col1, col2 = st.columns((2,1))
    
    with col1 :
        fig= plt.figure(figsize=(90,40))
        
        bar = sns.countplot(x=df_com_bar ['Nom_département'],
                           hue=df_com_bar ['Thématique_POI'], 
                           palette='Set2',
                           order=pd.value_counts(df['Nom_département']).iloc[:10].index)
        
        plt.title("Répartitions de POI par Départements ")
        plt.legend(bbox_to_anchor = (1, 1), 
                  loc = 'upper right', 
                  prop = {'size': 40})
        plt.xticks(rotation=45, fontsize=40)
        plt.yticks(fontsize=40)
        st.pyplot(fig)
    
    with col2:
        st.write("Note expliquant le graphique")
        

#---------------------------
#Histogramme avec Plotly
#---------------------------
    st.header("test de Plotly pour l'affichage dynamique des infos")
    
    figtest= px.histogram(df_com_bar, x=['Nom_département'], 
                          color= df_com_bar ['Thématique_POI'],
                          width=1500,
                          height=900,
                          title="Répartition des POIs par départements")
    
    #triage des données du plus grand au plus petit (nb total de POI)
    figtest.update_xaxes(categoryorder='total descending')
    
    #Modification des labels / couleurs/ Police etc...
    figtest.update_layout(xaxis_title="Nom du département",
                      yaxis_title="Thématiques des points d intérêt",
                      font=dict(family="Courier New, monospace", 
                                size=13,
                                color="#2B3232"),
                      title={
                             'y':0.95,
                             'x':0.43,
                             'xanchor': 'center',
                             'yanchor': 'top'},
                      title_font_family="Times New Roman",
                      title_font_color="#263A91",
                      legend_title_font_color="#3C738D")
    
    #Affichage du graph
    st.plotly_chart(figtest)
 
#---------------------------
#DensityMap avec Plotly
#---------------------------   
    st.write("Test d une Heatmap")
    #Création d'un dataframe contenant le total du nombre de chaque thématiques par commune
    dfheat = pd.crosstab (df['Nom_commune'], df['Thématique_POI']).reset_index()
    dfheat['sum']=dfheat.sum(axis=1)
    
    #Ajout du total dans le df principal
    dico= dict(zip(dfheat['Nom_commune'], dfheat['sum']))
    df['Sum']= df['Nom_commune'].map(dico)

    #Création du DensityMap
    figheat = px.density_mapbox(df, 
                            lat='Latitude', lon='Longitude', 
                            z='Sum', 
                            radius=10,
                            center=dict(lat=48.6, lon=2.19),
                            zoom=5,
                            mapbox_style="open-street-map",
                            color_continuous_scale = "Sunset",
                            width=1300,
                            height=1000)
    st.plotly_chart(figheat)

#Page 3   
if sidebar=="Démos":
    st.title('Affichage de la carte avec HTML_file function')
    html_file = open("carte_centroid_itineraire_0_1.html", 'r', encoding='utf-8')
    source_code = html_file.read()
    components.html(source_code, height=600, width=1000)
    #le df.csv est créé et sauvegardé dans le répertoire du projet Streamlit, on peu simplement le rappeler sans relancer le code initial
    df = pd.read_csv("df.datatourisme.POI_OK_20210921.PACA.csv")
    centroid= pd.read_csv("Data/CentroidFrance.csv")
    
    #DROP DOWN MENU
    commune = df['Nom_commune'].drop_duplicates()
    choix_commune = st.selectbox('Selectionnez votre commune:', commune)
    
    theme = df["Thématique_POI"].drop_duplicates()
    #choix_theme = st.sidebar.selectbox('Sélectionnez votr type d itinéraire', theme)
    
    col1, col2= st.columns((1,2))

    #AFFICHAGE DE LA CARTE
    with col1 : 
        #création du slide de dsélection des jours
        jourselect = st.radio("Nombre de jour de visites", (1,2,3,4,5,6,7))
        
        #création du menu pour sélectionner les thèmatiqes
        themeselect= st.multiselect("Sélection des thématiques",theme, default = theme)
        themenotselect=[]
        for i in theme:
            if i not in themeselect:
                themenotselect.append(i)
        
        
        #création de la carte
        with col2: 
            cartes=st.container()
            with cartes:
                st.header('Carte des Points d intêrets selon la commune et le thème choisi')
                def intineraire (choix_commune):
                    #Obtention du centroide de la commune choisie
                    centroid_list = centroid['nom_com'].drop_duplicates(keep='first')
                    for value in centroid_list:
                      if choix_commune == value:
                          com = centroid[centroid['nom_com'] == value]
                          
                    #Selection de la commune
                    commune_list = df['Nom_commune'].drop_duplicates(keep='first')
                    for value in commune_list:
                        if choix_commune == value:
                            df_com = df [df['Nom_commune'] == value]

                    #Selection de la thématique selon la commune
                    df_com = df_com[~df_com['Thématique_POI'].isin(themenotselect)]
                 
                    #création des clusters en utilisant le KMeans
                    #On a une randomisation des résultats naturellement avec le KMeans
                    X= df_com[['Latitude', 'Longitude']]
                    k = round((df_com[['Latitude', 'Longitude']].shape[0])/10)
                    kmeans = KMeans(k)
                    kmeans.fit(X)
                    clusters = kmeans.predict(X)
                    df_com['Clusters'] = clusters
                    random = list(df_com['Clusters'].sample(n=jourselect, random_state=1).values) #On choisi un n= nombre de jour pour avoir un cluster par jour
                    df_com = df_com.loc[df_com['Clusters'].isin(random)]
                
                    #Création de la carte
                    #centrage de la carte sur le centroide de la commune recherchée
                    for index, row in com.iterrows():
                      maps= folium.Map(location=[row.loc['latitude'], row.loc['longitude']], tiles='cartodbpositron', zoom_start=12)
                
                  #création de la colonne couleur qui servira à changer les couleurs des iconnes
                      color_list= ['red', 'blue', 'green', 'purple', 'orange', 'darkred', 'lightred',
                          'beige', 'darkblue', 'darkgreen', 'cadetblue', 'darkpurple','white', 
                          'pink', 'lightblue', 'lightgreen', 'gray', 'black', 'lightgray']
                      clusters_id = list(df_com["Clusters"].unique())
                      color_dic = dict(zip (clusters_id, color_list))
                      df_com['Couleur']= df_com['Clusters'].map(color_dic)
                
                  #création de la colonne qui servira à différencier les icones
                      icon_dic= {'Itinéraire touristique':'hiking', 
                                 'Loisir':'film', 
                                 'Sport':'futbol',
                                 'Site naturel':'tree',
                                 'Service pratique':'question', 
                                 'Évènement social':'elementor', 
                                 'Évènement culturel':'palette',
                                 'Restauration':'utensils', 
                                 'Patrimoine':'monument', 
                                 'Culture':'archway', 
                                 'Commerce':'cash-register', 
                                 'Gastronomie':'star',
                                 'Mobilité':'wheelchair', 
                                 'Information':'info'}
                      df_com['icons']= df_com['Thématique_POI'].map(icon_dic)
                      
                    for i in df_com.itertuples(): 
                      folium.Marker(location=[i.Latitude, i.Longitude], 
                                     tooltip= i.Nom_du_POI,
                                     icon=folium.Icon(icon=i.icons, prefix="fa", color = i.Couleur)).add_to(maps)
                
                
                    return folium_static(maps)
                                
                st.write(intineraire (choix_commune))
     
    
  

#Page 4            
if sidebar=="Test cartes multiples":
    df_POI= pd.read_csv("datatourisme.POI_OK_20210921.PACA.csv")
    nom_commune_reference = 'Arles'
    duree_du_sejour  = 5                                                                               
    
    dict_themes = {"Commerce":True,                                                                       ## thématiques de POI souhaitées par l'utilisateur
                   "Culture et social":True,
                   "Gastronomie":True,
                   "Loisir":True,
                   "Patrimoine":True,
                   "Site naturel":True,
                   "Sport":True}
    
    dict_sous_themes = {"Itinéraire touristique":True,                                                    ## sous-thématiques de POI souhaitées par l'utilisateur
                        "Itinéraire pédestre":True,                                                                        
                        "Itinéraire cyclable":True,                                                                       
                        "Itinéraire routier":True,                                                                        
                        "Restauration":True,     
                        "Restauration rapide":True}
    ##!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    ##!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    
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
    def analyse_resultats_par_itineraire(no_centroid, no_itineraire, POI_itineraire, df_POI_zoom_sur_centroid, carte_openrouteservice, pos_geo_itineraire, long_itineraire, no_centroid_deja_traite):
    
        print('--------------------------------------------------------')
        print('Itinéraire numéro', no_itineraire, 'du centroïd', no_centroid)
        print(pos_geo_itineraire) 
        print(long_itineraire)
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
    
    
    ##----------------------------------------------------------------------------------------------------------
    ## Implémentation de la méthode de clustering (KMEANS) pour identifier les principaux regroupements de POI
    ##----------------------------------------------------------------------------------------------------------
    dict_final_centroids_nbre_itineraires, dict_df_POI_zoom_sur_centroid, dict_attributs_sejour = Pytineo_module_clustering.StartPoint(nom_commune_reference, duree_du_sejour, dict_themes, dict_sous_themes, df_POI, dict_parametres_techniques)    
    
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
                       
    ##---------------------------------------
    ## Constitution des cartes interactives 
    ##---------------------------------------      
    for cle, valeur in dict_final_centroids_nbre_itineraires.items(): 
        i = 0
        no_centroid_deja_traite = False
        for itineraire in globals()[f"liste_itineraires_centroid_{cle}"]:
            i +=1
            dict_attributs_itineraire = {'no_centroid':cle, 'lat_centroid':dict_final_centroids_nbre_itineraires[cle][0], 'long_centroid':dict_final_centroids_nbre_itineraires[cle][1], 'POI_itineraire':itineraire}
            fmap, carte_openrouteservice, pos_geo_itineraire, long_itineraire, liste_nom_POI_resto, liste_theme_POI_resto, liste_mot_cle_POI_resto = Pytineo_module_cartes.StartPoint(globals()[f"df_POI_zoom_sur_centroid_{cle}"], dict_attributs_itineraire, dict_attributs_sejour) 
            no_FMAP = str(cle)+ '_' + str(i)
            filename = ("carte_centroid_itineraire_%s.html" % no_FMAP)
            fmap.save('Streamlit/'+filename)
            no_centroid_deja_traite = analyse_resultats_par_itineraire(cle, i, itineraire, globals()[f"df_POI_zoom_sur_centroid_{cle}"], carte_openrouteservice, pos_geo_itineraire, long_itineraire, no_centroid_deja_traite)
            analyse_resultats_par_carte(cle, i, liste_nom_POI_resto, liste_theme_POI_resto, liste_mot_cle_POI_resto, dict_attributs_sejour)
            

            

            

