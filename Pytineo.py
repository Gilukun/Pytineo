# -*- coding: utf-8 -*-
"""
Created on Thu Nov 11 17:27:47 2021

@author: Gilles
"""
# -*- coding: utf-8 -*-

#Début du code
import streamlit as st
import pandas as pd
import numpy as np

from plotly.subplots import make_subplots
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

import folium
from streamlit_folium import folium_static

#import openrouteservice 
#from openrouteservice import client

from sklearn.cluster import KMeans
import re


from IPython.core.display import display, HTML
import streamlit.components.v1 as components

import threading
import time

import sys
sys.path.append('/Gilles/OneDrive/Datascientest/Streamlit')
import Pytineo_module_clustering
import Pytineo_module_itineraires
import Pytineo_module_cartes

from google_drive_downloader import GoogleDriveDownloader as gdd

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
    gdd.download_file_from_google_drive(file_id='1leVB4XiOYZdRFGZGLGIIqkEkH9duLX8j',
                                    dest_path="/Gilles/OneDrive/Datascientest/Streamlit")
    
    col1, col2, col3 = st.columns([3,1,1])
    with col1:
        st.write("")
    with col2:
        st.write("")
    with col3:
        st.image("Pytineo_logo_2.png", caption=None, width=100, use_column_width=100, clamp=False, channels="RGB", output_format="auto")
            
       
    date_extraction = '13122021'
    df_fma_jour= pd.read_csv("datatourisme.fma.20211213.csv")
    df_tour_jour= pd.read_csv("datatourisme.tour.20211213.csv")
    df_place_jour= pd.read_csv("datatourisme.place.20211213.csv")
    df_product_jour= pd.read_csv("datatourisme.product.20211213.csv")
    liste_departements = ['01', '02', '03', '04', '05', '06', 
                        '07', '08', '09', '10', '11', '12', '13','14', '15', '16', '17', '18', '19', '2A', '2B', '21', '22', '23', 
                        '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', 
                        '42', '43', '44', '45', '46', '47', '48', '49', '51', '52', '53', '54', '55', '56', '57', '58', '59', '60', 
                        '61', '62', '63', '64', '65', '66', '67', '68', '69', '70', '71', '72', '73', '74', '75', '76', '77', '78', 
                        '79', '80', '81', '82', '83', '84', '85', '86', '87', '88', '89', '90', '91', '92', '93', '94' ,'95']  
    
    ####### definition de la fonction ##########
    @st.cache(persist=True)
    def cleanup () :
      ## Trt fichier FMA
      df = df_fma_jour
      indices_booleens = df['Code_postal_et_commune'].str[0:2].isin(liste_departements)       ## le code postal de la colonne "Code_postal_et_commune" figure-t-il ou non dans la liste des départements (retour d'une Serie à TRUE ou FALSE
      df_fma = df[indices_booleens]                                                           ## création d'un dataframe ne contenant que les lignes dont le booléen a été retourné à TRUE            
    
    ## Trt idem pour fichier PRODUCT
      df = df_product_jour
      indices_booleens = df['Code_postal_et_commune'].str[0:2].isin(liste_departements)  ## idem
      df_product = df[indices_booleens]
    
    ## Trt idem pour fichier TOUR
      df = df_tour_jour
      indices_booleens = df['Code_postal_et_commune'].str[0:2].isin(liste_departements)  ## idem  
      df_tour = df[indices_booleens]
    
    ## Trt idem pour fichier PLACE
      df = df_place_jour
      indices_booleens = df['Code_postal_et_commune'].str[0:2].isin(liste_departements)  ## idem
      df_place = df[indices_booleens]
    
    
    ##-----------------------
    ## Lecture des fichiers
    ##-----------------------
    
      df_TOUR_POI_mots_cle = pd.read_csv("datatourisme.tour.POI_mots_cle.PACA.csv")
      df_PRODUCT_POI_mots_cle = pd.read_csv("datatourisme.product.POI_mots_cle.PACA.csv")
      df_PLACE_POI_mots_cle = pd.read_csv("datatourisme.place.POI_mots_cle.PACA.csv")
    
      df_TOUR_POI = df_tour
      df_PRODUCT_POI = df_product
      df_PLACE_POI = df_place 
    
    ##-----------------------------------------------------------------------
    ## Initialisation des dictionnaires de référentiels thématiques de POI 
    ##-----------------------------------------------------------------------
    
      dict_TOUR_POI_corr_mot_cle_URL_francais = {}                                       ## dataframe TOUR - correspondance entre le mot clé de POI contenu dans l'URL et le mot clé en français                                                           
      dict_TOUR_POI_corr_mot_cle_francais_thematique = {}                                ## correspondance entre le mot clé en français et la thématique du POI
    
      dict_PRODUCT_POI_corr_mot_cle_URL_francais = {}                                    ## idem pour dataframe PRODUCT                                                           
      dict_PRODUCT_POI_corr_mot_cle_francais_thematique = {}
    
      dict_PLACE_POI_corr_mot_cle_URL_francais = {}                                      ## idem pour dataframe PLACE                                                           
      dict_PLACE_POI_corr_mot_cle_francais_thematique = {}
    
    ##------------------------------------------------------------------------------------------
    ## Alimentation des dictionnaires à partir des dataframes référentiels thématiques de POI
    ##------------------------------------------------------------------------------------------
    
    ## TOUR
      for i in range(len(df_TOUR_POI_mots_cle)): 
    
    ## alimentation du dictionnaire 'dict_type_url_type_simplifie' à partir du dataframe 'df_TOUR_POI_mots_cle'
          dict_TOUR_POI_corr_mot_cle_URL_francais[df_TOUR_POI_mots_cle.loc[i,'Mot_clé']] = df_TOUR_POI_mots_cle.loc[i, 'Mot_clé_en_francais'] 
        
    ## alimentation du dictionnaire 'dict_type_simplifie_thematique' à partir du dataframe 'df_TOUR_POI_mots_cle'   
          dict_TOUR_POI_corr_mot_cle_francais_thematique[df_TOUR_POI_mots_cle.loc[i,'Mot_clé_en_francais']] = df_TOUR_POI_mots_cle.loc[i, 'Catégorie_thématique']   
        
    ## PRODUCT
      for i in range(len(df_PRODUCT_POI_mots_cle)): 
       
    ## alimentation du dictionnaire 'dict_type_url_type_simplifie' à partir du dataframe 'df_PRODUCT_POI_mots_cle'
          dict_PRODUCT_POI_corr_mot_cle_URL_francais[df_PRODUCT_POI_mots_cle.loc[i,'Mot_clé']] = df_PRODUCT_POI_mots_cle.loc[i, 'Mot_clé_en_francais'] 
        
    ## alimentation du dictionnaire 'dict_type_simplifie_thematique' à partir du dataframe 'df_PRODUCT_POI_mots_cle'   
          dict_PRODUCT_POI_corr_mot_cle_francais_thematique[df_PRODUCT_POI_mots_cle.loc[i,'Mot_clé_en_francais']] = df_PRODUCT_POI_mots_cle.loc[i, 'Catégorie_thématique']                 
        
    ## PLACE
      for i in range(len(df_PLACE_POI_mots_cle)):   
                      
    ## alimentation du dictionnaire 'dict_type_url_type_simplifie' à partir du dataframe 'df_PLACE_POI_mots_cle'
          dict_PLACE_POI_corr_mot_cle_URL_francais[df_PLACE_POI_mots_cle.loc[i,'Mot_clé']] = df_PLACE_POI_mots_cle.loc[i, 'Mot_clé_en_francais'] 
        
    ## alimentation du dictionnaire 'dict_type_simplifie_thematique' à partir du dataframe 'df_PLACE_POI_mots_cle'   
          dict_PLACE_POI_corr_mot_cle_francais_thematique[df_PLACE_POI_mots_cle.loc[i,'Mot_clé_en_francais']] = df_PLACE_POI_mots_cle.loc[i, 'Catégorie_thématique']   
    
    ##-----------------------
    ## Fonctions génériques
    ##-----------------------
    
    ## Traitement spécifique de l'URL de la catégorie des POI présente dans le dictionnaire 'dict_xxxx_POI_corr_mot_cle_URL_francais'
      def fct_categorie(categorie_URL, dictionnaire):    
          liste_mots_cle = re.findall(r"[#][a-z]+", categorie_URL, re.I)                 ## recherche dans l'URL de la catégorie des chaînes alphabétiques préfixées par le carctère '#'
        
          for i, mot_cle in enumerate(liste_mots_cle):
              liste_mots_cle[i] = mot_cle[1:]                                            ## élimination des chaînes retournées du caractère '#'
        
        
          for mot_cle in liste_mots_cle:
              for cle,valeur in dictionnaire.items():                                    ## l'une au moins des chaînes de carctères retournées est-elle présente dans le dictionnaire ?
                  if mot_cle == cle:                                                 
                      return valeur  
                 
    ## Traitement spécifique de la thématique du POI présente dans le dictionnaire 'dict_xxxx_POI_corr_mot_cle_francais_thematique'
      def fct_thematique(mot_cle, dictionnaire):  
          for cle,valeur in dictionnaire.items():   
              if mot_cle == cle:   
                  return valeur                                                          ## retourne la thématique assosiée au mot clé du POI 
     
    ## Traitement du nom du département
      def fct_nom_departement(code_departement):  
            for i, code_dept in enumerate(df_ref_cd_dept_nom['Code_département']):
                if code_dept == code_departement:
                    return df_ref_cd_dept_nom['Nom_département'][i]                        ## retourne le nom du département   
            
    ## Traitement du nombre d'habitants du département
      def fct_population_dept(code_departement):  
          for i, code_dept in enumerate(df_ref_cd_dept_nom['Code_département']):
              if code_dept == code_departement:
                  return df_ref_cd_dept_nom['Nombre_habitants'][i]                       ## retourne le nombre d'habitants du département
            
    ## Traitement du tourisme annuel
      def fct_tourisme_dept(code_departement):  
          for i, code_dept in enumerate(df_ref_cd_dept_nom['Code_département']):
              if code_dept == code_departement:
                  return df_ref_cd_dept_nom['Fréquentation_année_2010'][i]               ## retourne le nombre de touristes annules du département
            
    ## Traitement des noms de communes manquants   
      def fct_nom_commune(code_postal):                                                                                       
          liste = list(df_ref_cd_postal_commune['Nom_commune'][df_ref_cd_postal_commune['Code_postal'] == code_postal])       
          return liste[0]                                                                ## retourne la première occurrence du nom de commune correspondant au code postal passé en paramètre    
          
    ##--------------------------------------------------------------------------
    ## Traitement des mots clé des fichiers thématiques (TOUR, PLACE, PRODUCT)
    ##--------------------------------------------------------------------------
    
    ## Fichier TOUR - recherche dans le dictionnaire d'un mot clé de l'URL Catégorie
      df_TOUR_POI['Mot_clé_POI'] = df_TOUR_POI['Categories_de_POI'].apply(lambda x: fct_categorie(x,dict_TOUR_POI_corr_mot_cle_URL_francais))               ## ajout d'une colonne 'Mot clé' au dataframe
    
      df_TOUR_POI['Thématique_POI'] = df_TOUR_POI['Mot_clé_POI'].apply(lambda x: fct_thematique(x,dict_TOUR_POI_corr_mot_cle_francais_thematique))          ## ajout d'une colonne 'Thématique' au dataframe
    
    ## Fichier PRODUCT - idem
      df_PRODUCT_POI['Mot_clé_POI'] = df_PRODUCT_POI['Categories_de_POI'].apply(lambda x: fct_categorie(x,dict_PRODUCT_POI_corr_mot_cle_URL_francais))      ## ajout d'une colonne 'Mot clé' au dataframe
    
      df_PRODUCT_POI['Thématique_POI'] = df_PRODUCT_POI['Mot_clé_POI'].apply(lambda x: fct_thematique(x,dict_PRODUCT_POI_corr_mot_cle_francais_thematique)) ## ajout d'une colonne 'Thématique' au dataframe
    
    ## Fichier PLACE - idem
      df_PLACE_POI['Mot_clé_POI'] = df_PLACE_POI['Categories_de_POI'].apply(lambda x: fct_categorie(x,dict_PLACE_POI_corr_mot_cle_URL_francais))            ## ajout d'une colonne 'Mot clé' au dataframe
    
      df_PLACE_POI['Thématique_POI'] = df_PLACE_POI['Mot_clé_POI'].apply(lambda x: fct_thematique(x,dict_PLACE_POI_corr_mot_cle_francais_thematique))       ## ajout d'une colonne 'Thématique' au dataframe
    
    ##--------------------------------------------------------------------------
    ## Regroupement des fichiers thématiques (TOUR, PLACE, PRODUCT)
    ##--------------------------------------------------------------------------
    
      df_POI = pd.concat([df_TOUR_POI, df_PRODUCT_POI, df_PLACE_POI])
    
    ##-----------------------------------------
    ## Ajout de colonnes au dataframe df_POI
    ##-----------------------------------------
    
    ## création d'un dataframe par lecture du référentiel des communes INSEE
      df_ref_cd_postal_commune = pd.read_csv("Communes_codes_postaux.csv", sep=';', dtype='object')           
    
    ## création d'un dataframe par lecture du référentiel des départements
      df_ref_cd_dept_nom = pd.read_csv("Départements.csv",  sep=',', dtype='object')                      
           
    ## création colonne 'Code département'
      df_POI['Code_département'] = df_POI['Code_postal_et_commune'].apply(lambda x: x[0:2])  
    
    ## création colonne 'Nom département'
      df_POI['Nom_département'] = df_POI['Code_département'].apply(fct_nom_departement)
    
    ## création colonne 'Population du département'
      df_POI['Nbre_habitants'] = df_POI['Code_département'].apply(fct_population_dept)
    
    ## création colonne 'Population touristique du département'
      df_POI['Nbre_touristes'] = df_POI['Code_département'].apply(fct_tourisme_dept)
      
    ## création colonne 'Code postal'
      df_POI['Code_postal'] = df_POI['Code_postal_et_commune'].apply(lambda x: x.split('#')[0])
    
    ## création colonne 'Nom commune'
      df_POI['Nom_commune'] = df_POI['Code_postal_et_commune'].apply(lambda x: x.split('#')[1])
    
    ##---------------------------------------------------------------------
    ## Réordonnancement des colonnes / élimination des colonnes inutiles
    ##---------------------------------------------------------------------
    
      df_POI = df_POI[['Nom_du_POI', 'Mot_clé_POI', 'Thématique_POI', 'URI_ID_du_POI', 'Description', 'Latitude', 'Longitude', 'Adresse_postale', 'Code_département', 'Nom_département',
                     'Code_postal', 'Nom_commune', 'Nbre_habitants', 'Nbre_touristes']]
    
    ## Renommage des colonnes
      df_POI.columns = ['Nom_du_POI', 'Mot_clé_POI', 'Thématique_POI', 'Description_courte', 'Description_longue', 'Latitude', 'Longitude', 'Adresse_postale', 'Code_département', 'Nom_département',
                     'Code_postal', 'Nom_commune', 'Nbre_habitants', 'Nbre_touristes']
    
    ##------------------------------------------------------------------------
    ## Traitement des valeurs manquantes du jeu de données de type POI TOUR
    ##------------------------------------------------------------------------
      df_POI = df_POI.dropna(subset = ['Mot_clé_POI'], axis=0)                                                      ## élimination des lignes avec mots clé non renseignés (types POI)
    
      df_POI['Adresse_postale'] = df_POI['Adresse_postale'].fillna('Adresse non précisée')                          ## gestion des adresses non renseignées
      df_POI['Description_courte'] = df_POI['Description_courte'].fillna('Description courte non précisée')         ## gestion des descriptions courtes non renseignées
      df_POI['Description_longue'] = df_POI['Description_longue'].fillna('Description longue non précisée')         ## gestion des descriptions longues non renseignées
    
    ## gestion des noms de commune non renseignés
      df_temp_cd_postal_commune = pd.DataFrame(columns=['Code_postal', 'Nom_commune'])                              ## création d'un dataframe temporaire
      df_temp_cd_postal_commune['Code_postal'] = df_POI['Code_postal'][df_POI['Nom_commune'].isna()]                ## alimentation de la colonne 'Code postal' du dataframe temporaire
    
      df_temp_cd_postal_commune['Nom_commune'] = df_temp_cd_postal_commune['Code_postal'].apply(fct_nom_commune)    ## alimentation de la colonne 'Nom_commune' du dataframe temporaire
    
      df_POI['Nom_commune'] = df_POI['Nom_commune'].fillna(df_temp_cd_postal_commune['Nom_commune'])                ## remplacement des noms de commune manquants par ceux contenus dans le df temporaire  
        
      df_POI = df_POI.dropna(subset = ['Nom_commune'], axis=0)                                                      ## élimination des lignes avec noms de commune non renseignés
    
    ## suppression des lignes dupliquées sur le nom du POI et ses coordonnées géographiques
      df_POI = df_POI.drop_duplicates(subset=['Nom_du_POI', 'Latitude', 'Longitude'])
    
      print(df_POI.info())
        
    ## Export du fichier dans le répertoire du projet Streamlit
    ##-----------------------
      return df_POI.to_csv('df.csv', index = False) 
  
   #Création du dataframe pour la suite du code
    df = pd.read_csv("df.csv")
    
    
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
    df = pd.read_csv("df.csv")
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
    df_POI= pd.read_csv("df.csv")
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
            ##webbrowser.open(filename)
            no_centroid_deja_traite = analyse_resultats_par_itineraire(cle, i, itineraire, globals()[f"df_POI_zoom_sur_centroid_{cle}"], carte_openrouteservice, pos_geo_itineraire, long_itineraire, no_centroid_deja_traite)
            analyse_resultats_par_carte(cle, i, liste_nom_POI_resto, liste_theme_POI_resto, liste_mot_cle_POI_resto, dict_attributs_sejour)

