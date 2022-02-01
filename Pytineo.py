# -*- coding: utf-8 -*-
"""
Created on Thu Nov 11 17:27:47 2021

@author: Gilles
"""
# -*- coding: utf-8 -*-

#Début du code
import streamlit as st
import streamlit.components.v1 as components

import pandas as pd

import threading
import time
import plotly.express as px
from PIL import Image

import sys
sys.path.append('https://github.com/Gilukun/Pytineo/blob/main/Pytineo')
import Pytineo_module_clustering
import Pytineo_module_itineraires
import Pytineo_module_cartes

#affichage de la page sur toute sa largeur. Ce code doit toujour être le premier à être entré après l'import des modules
st.set_page_config(layout="wide")

Logo = Image.open("Pytineo_Logo_2.png")
st.sidebar.image(Logo, width=100)
#creation de la navigation du site (menu de gauche)
sidebar = st.sidebar.radio("Navigation", ["Acceuil", "Analyse de données", "Application Pytineo"]) 

#Premère page
if sidebar=="Acceuil":
    intro = st.container()
    with intro:
        col1, col2, col3= st.columns([1,1,1])
        with col2:
            Logo = Image.open("Pytineo_Logo_2.png")
            st.image(Logo, width=500,output_format="auto")
            
        st.markdown("<h1 style='text-align: center;'>Application de création d itinéraires</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center;'>Réalisée en language Python</h3>", unsafe_allow_html=True)
        st.markdown("<h4 style='text-align: center;'>Gaëlle Lehur</h4>", unsafe_allow_html=True)
        st.markdown("<h4 style='text-align: center;'>Gilles Virassamy</h4>", unsafe_allow_html=True)
        st.markdown("<h4 style='text-align: center;'>Laurent Berrezaie</h4>", unsafe_allow_html=True)
    
        
        footlogo1, footlogo2, footlogo3= st.columns([1,1,1])
        with footlogo2:
            st.image("DataScientest_logo.png", caption=None, width=300, clamp=False, channels="RGB", output_format="auto")

#Seconde page 
if sidebar=="Analyse de données":
    my_bar = st.progress(0)

    for percent_complete in range(100):
         time.sleep(0.1)
         my_bar.progress(percent_complete + 1)
        
    #ouverture du Dataset
    df = pd.read_csv("datatourisme.POI_OK_20210921.PACA.csv")
    
    analysis = st.container()

    with analysis:
        st.markdown("<h1 style='text-align: center;'>Exploration des données</h1>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center;'>Données clés</h1>", unsafe_allow_html=True)
        
        #affichage de quelques data clés
        data1,data2,data3= st.columns((1,1,1))
        with data1 :
            label1 = '<p style="font-family:sans-serif; color:#9999CC ; font-size: 24px;">Nombre Total de POI</p>'
            st.markdown(label1, unsafe_allow_html=True) 
            nb_POI = df['Nom_du_POI'].nunique()
            st.metric(label="",value=nb_POI)
            
        with data2:
            nb_POI = df['Thématique_POI'].nunique()
            label1 = '<p style="font-family:sans-serif; color:#FF5733 ; font-size: 24px;">Nombre Total de Thématique</p>'
            st.markdown(label1, unsafe_allow_html=True) 
            st.metric(label="", value=nb_POI)
        
        with data3:
            nb_POI = df['Nom_commune'].nunique()
            label1 = '<p style="font-family:sans-serif; color:#336699 ; font-size: 24px;">Nombre Total de Commune</p>'
            st.markdown(label1, unsafe_allow_html=True) 
            st.metric(label="", value=nb_POI)
        
        #insertion d'une ligne de sépartion
        st.markdown("""---""")
        st.markdown("<h2 style='text-align: center;'>Aperçu du DataSet</h1>", unsafe_allow_html=True)  
        st.dataframe(data=df.head(10))
    
    
    
#---------------------
#Camembert avec Plotly
#---------------------
    st.markdown("""---""")
    st.markdown("<h2 style='text-align: center;'>Répartition des type de POI</h1>", unsafe_allow_html=True)
    #Création de 2 colonnes sur la page
    #(2,1) => la première colonne sera 2 fois plus grande que la seconde colonne
    
    #liste des modalités des Thématique
    theme_count = df['Thématique_POI'].value_counts().sort_values()
    

    PACA_pie = px.pie(theme_count, 
                             values=theme_count, 
                             names=theme_count.index, 
                             title="Répartition des thèmes de POI",
                             width=800, 
                             height=700)

    PACA_pie.update_traces(textposition='outside', textinfo='percent')
    PACA_pie.update_layout(xaxis_title="Répartition des thèmes des POIs", 
                           font=dict(family="Verdana", 
                                size=13,
                                color="Black"),
                           title={
                             'y':0.95,
                             'x':0.43,
                             'xanchor': 'center',
                             'yanchor': 'top'},
                           title_font_family="Verdana",
                           title_font_color="Black",
                           legend_title_font_color="#3C738D")

    st.plotly_chart(PACA_pie)
    

#---------------------------
#Histogramme avec Plotly
#---------------------------
    st.markdown("""---""") 
    st.markdown("<h2 style='text-align: center;'>Répartition des type de POI par départements</h1>", unsafe_allow_html=True)

    PACA_Hist= px.histogram(df, x=['Nom_département'], 
                          color= df ['Thématique_POI'],
                          width=1000,
                          height=600,
                          title="Répartition des POIs par départements")

    #triage des données du plus grand au plus petit (nb total de POI)
    PACA_Hist.update_xaxes(categoryorder='total descending')

    #Modification des labels / couleurs/ Police etc...
    PACA_Hist.update_layout(xaxis_title="Nom du département",
                      yaxis_title="Thématiques des points d intérêt",
                      font=dict(family="Verdana", 
                                size=13,
                                color="Black"),
                      title={
                             'y':0.95,
                             'x':0.43,
                             'xanchor': 'center',
                             'yanchor': 'top'},
                      title_font_family="Verdana",
                      title_font_color="Black",
                      legend_title_font_color="#3C738D")

    #Affichage du graph
    st.plotly_chart(PACA_Hist)

#---------------------------
#DensityMap avec Plotly
#---------------------------  
    st.markdown("""---""")
    st.markdown("<h2 style='text-align: center;'>Carte de densité des POIs</h1>", unsafe_allow_html=True)
    #Création d'un dataframe contenant le total du nombre de chaque thématiques par commune
    dfheat = pd.crosstab (df['Nom_commune'], df['Thématique_POI']).reset_index()
    dfheat['sum']=dfheat.sum(axis=1)

#Ajout du total dans le df principal
    dico= dict(zip(dfheat['Nom_commune'], dfheat['sum']))
    df['Sum']= df['Nom_commune'].map(dico)
    col1, col2 = st.columns((2,1))
    with col1 : 
        #Création du DensityMap
        PACA_density= px.density_mapbox(df, 
                                lat='Latitude', lon='Longitude', 
                                z='Sum', 
                                radius=10,
                                center=dict(lat=43.55, lon=5.41),
                                zoom=7,
                                mapbox_style="open-street-map",
                                color_continuous_scale = "Sunset",
                                width=950,
                                height=950)
        PACA_density.update_layout(title= "Densité des Points d'intérêt en France", 
                          title_x= 0.5,
                          font=dict(size=18))

        st.plotly_chart(PACA_density)

#Page 3            
if sidebar=="Application Pytineo":
    #Création des menus de sélection des variables
    df_POI= pd.read_csv("datatourisme.POI_OK_20210921.PACA.csv")
    
    reg1, reg2, day = st.columns((1,1,1))
    with reg1: 
        #Menu de selection du département
        dep = df_POI['Nom_département'].drop_duplicates()
        choix_departement = st.selectbox('Selectionnez votre département:', dep.sort_values())
        nom_dep_reference = choix_departement
        df_POI= df_POI.loc[df_POI['Nom_département'].isin([nom_dep_reference])]
        
    with reg2 : 
        #Menu de sélection de la commune
        commune = df_POI['Nom_commune'].drop_duplicates()
        
        choix_commune = st.selectbox('Selectionnez votre commune:', commune.sort_values())
        nom_commune_reference = choix_commune
    
    with day:
        #menu de sélection des jours
        selection_nb_jour = st.number_input("Nombre de jour de visite", min_value=1, max_value=7, step=1)
        duree_du_sejour  = selection_nb_jour  
        
    th, sth = st.columns((1,1))
    #menu de selection des thèmes
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
        choix_theme = st.multiselect('Selectionnez votre thème:',sous_theme, default= sous_theme )
        list_sous_theme_reference = choix_theme
        
        sous_theme_boolean=[]
        for i in sous_theme: 
            if i in list_sous_theme_reference:
                sous_theme_boolean.append (True)
            else:
                sous_theme_boolean.append (False)
        
        dict_sous_themes =  dict(zip(sous_theme , sous_theme_boolean))
    
    #affichage de la légende des cartes
    with st.expander("Cliquez pour afficher la légende"):
        img1,img2,img3,img4,img5,img6,img7= st.columns((1,1,1,1,1,1,1))
        with img1:
            st.image("Logo_POIs/logo_commerce_service.png", caption="Commerce",width=75)
        with img2:
            st.image("Logo_POIs/logo_culture_social.png", caption="Culture/Social",width=75)
        with img3:
            st.image("Logo_POIs/logo_evt_sportif.png", caption="Evènement Sportif",width=75)
        with img4:
            st.image("Logo_POIs/logo_itineraire.png", caption="Itinéraires",width=75)
        with img5:
            st.image("Logo_POIs/logo_loisir.png", caption="Loisir",width=75)
        with img6:
            st.image("Logo_POIs/logo_marche_a_pied.png", caption="Marche à pied",width=75)
        with img7:
            st.image("Logo_POIs/logo_patrimoine.png", caption="Patrimoine",width=75)
          
       
        img8,img9,img10,img11,img12,img13,img14= st.columns((1,1,1,1,1,1,1)) 
        with img8:
            st.image("Logo_POIs/logo_restauration_rapide.png", caption="Retauration Rapide",width=75)
        with img9:
            st.image("Logo_POIs/logo_restauration.png", caption="Gastronomie",width=80)
        with img10:
            st.image("Logo_POIs/logo_site_naturel.png", caption="Site Naturel",width=75)
        with img11:
            st.image("Logo_POIs/logo_sports.png", caption="Sport",width=75)
        with img12:
            st.image("Logo_POIs/logo_terroir.png", caption="Terroir",width=75)
        with img13:
            st.image("Logo_POIs/logo_velo.png", caption="Velo",width=75)
        with img14:
            st.image("Logo_POIs/logo_voiture.png", caption="Voiture",width=75)
        
                                                                 
    #Code de l'application Pytineo
    
    ##-------------------------------
    ## Mise en forme des paramètres 
    ##-------------------------------
    degre_alea_itineraire = 'faible'                                                                      ## valeurs possibles : 'sans', 'faible', 'moyen', 'fort'
    valeurs_degre_alea = {'sans':1, 'faible':2, 'moyen':3, 'fort':4}                                      ## plus l'aléa est elevé, plus les itinéraires s'éloignent du centre de la commune
    for cle, valeur in valeurs_degre_alea.items():
        if cle == degre_alea_itineraire:
            alea_construction_itineraire = valeur  
    
    dict_parametres_techniques = {'max_POI_TOUR_par_itineraire':1, 'alea_construction_itineraire':alea_construction_itineraire, 'max_POI_par_itineraire':8, 'min_distance_entre_2_POI':0.05, 'distance_max_POI_reference':20, 'nbre_POI_resto_dans_perimetre_iti':3}
    
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
    
        #print('--------------------------------------------------------')
        #print('Itinéraire numéro', no_itineraire, 'du centroïd', no_centroid)
        #print(pos_geo_itineraire) 
        #print(long_itineraire)
        #if carte_openrouteservice:
            #print('Cet itinéraire s\'appuie sur le réseau routier')
        #else:
            #print('Cet itinéraire ne peut pas s\'appuiyer sur le réseau routier')    
        #print('Nom des POI de l\'itinéraire :', POI_itineraire)
        #print('--------------------------------------------------------', '\n')
      
        if not no_centroid_deja_traite:
            no_centroid_deja_traite = True
            
            #print('--------------------------------------------------------')
            #print('Répartition des POI par mot_clé dans le centroïd', no_centroid)
            #print('--------------------------------------------------------')
            #print(df_POI_zoom_sur_centroid['Mot_clé_POI'][df_POI_zoom_sur_centroid['POI_dans_itineraire'] == True].value_counts(),'\n')        
    
            #print('--------------------------------------------------------')
            #print('Répartition des POI par thématique dans le centroïd', no_centroid)
            #print('--------------------------------------------------------')
            #print(df_POI_zoom_sur_centroid['Thématique_POI'][df_POI_zoom_sur_centroid['POI_dans_itineraire'] == True].value_counts(), '\n') 
            #print('Nombre de POI total : ', df_POI_zoom_sur_centroid[df_POI_zoom_sur_centroid['POI_dans_itineraire'] == True].shape[0],'\n')   
        
        return no_centroid_deja_traite
     
        
    def analyse_resultats_par_carte(no_centroid, no_itineraire, POI_resto_itineraire, liste_theme_POI_resto, liste_mot_cle_POI_resto, dict_attributs_sejour):    
        
        
        #print('--------------------------------------------------------')
        #print('Itinéraire numéro', no_itineraire, 'du centroïd', no_centroid) 
        #print('Nom des POI "Restauration" ou "Gastronomie" :', POI_resto_itineraire)
        #print('--------------------------------------------------------', '\n')   
                  
        cpt_gastronomie = 0
        for thématique in liste_theme_POI_resto:
            if thématique == dict_attributs_sejour['Gastronomie']:
                cpt_gastronomie +=1
        #print('Nombre de POI de type', dict_attributs_sejour['Gastronomie'], ': ', cpt_gastronomie)      
               
        cpt_resto = 0  
        cpt_resto_rapide = 0
        for mot_cle in liste_mot_cle_POI_resto:
            if mot_cle == dict_attributs_sejour['Restauration']:
                cpt_resto +=1
            if mot_cle == dict_attributs_sejour['Restauration rapide']:
                cpt_resto_rapide +=1
        #print('Nombre de POI de type', dict_attributs_sejour['Restauration'], ': ', cpt_resto) 
        #print('Nombre de POI de type', dict_attributs_sejour['Restauration rapide'], ': ', cpt_resto_rapide, '\n')   
    
    
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
            components.html(fmap._repr_html_(), height=600, width=1000)
            #fmap.save(filename)
            no_centroid_deja_traite = analyse_resultats_par_itineraire(cle, i, itineraire, globals()[f"df_POI_zoom_sur_centroid_{cle}"], carte_openrouteservice, pos_geo_itineraire, long_itineraire, no_centroid_deja_traite)
            analyse_resultats_par_carte(cle, i, liste_nom_POI_resto, liste_theme_POI_resto, liste_mot_cle_POI_resto, dict_attributs_sejour)
    
   
            

