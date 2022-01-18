#!/usr/bin/env python
# coding: utf-8

# In[1]:

import warnings
warnings.filterwarnings('ignore')                                                                     ## ne pas faire apparaitre les messages de type Warning

import pandas as pd
import threading
import time
import Pytineo_module_clustering
import Pytineo_module_itineraires
import Pytineo_module_cartes

import streamlit as st
import streamlit.components.v1 as components

##---------------------------------------------
##  Lectude du fichier source
##---------------------------------------------
df_POI = pd.read_csv("datatourisme.POI_OK_20210921.PACA.csv")

##--------------------------------------------------------------------
## Paramètres A ADAPTER en fonction des choix faits par l'utlisateur  
##!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
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
         
##----------------------------------------------------
## Constitution et affichage des cartes interactives 
##----------------------------------------------------    

st.title('Affichage des cartes interactives')

for cle, valeur in dict_final_centroids_nbre_itineraires.items(): 
    i = 0
    no_centroid_deja_traite = False
    for itineraire in globals()[f"liste_itineraires_centroid_{cle}"]:
        i +=1
        dict_attributs_itineraire = {'no_centroid':cle, 'lat_centroid':dict_final_centroids_nbre_itineraires[cle][0], 'long_centroid':dict_final_centroids_nbre_itineraires[cle][1], 'POI_itineraire':itineraire}
        fmap, carte_openrouteservice, pos_geo_itineraire, long_itineraire, liste_nom_POI_resto, liste_theme_POI_resto, liste_mot_cle_POI_resto = Pytineo_module_cartes.StartPoint(globals()[f"df_POI_zoom_sur_centroid_{cle}"], dict_attributs_itineraire, dict_attributs_sejour) 
        no_FMAP = str(cle)+ '_' + str(i)

        filename = ("carte_centroid_itineraire_%s.html" % no_FMAP)
        html_file = open(filename, 'r', encoding='utf-8')
        contenu_html_FMAP = html_file.read()
       ## affichage de la carte interactive
        components.html(contenu_html_FMAP, height=600, width=1000)

        fmap.save(filename)
        ##webbrowser.open(filename)
        no_centroid_deja_traite = analyse_resultats_par_itineraire(cle, i, itineraire, globals()[f"df_POI_zoom_sur_centroid_{cle}"], carte_openrouteservice, pos_geo_itineraire, long_itineraire, no_centroid_deja_traite)
        analyse_resultats_par_carte(cle, i, liste_nom_POI_resto, liste_theme_POI_resto, liste_mot_cle_POI_resto, dict_attributs_sejour)