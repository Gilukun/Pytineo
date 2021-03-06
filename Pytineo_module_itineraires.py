# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import math
from decimal import *
from operator import itemgetter
import csv


##-------------
## Fonctions
##-------------

def StartPoint(no_centroid, lat_centroid_degre, lon_centroid_degre, nbre_jours_autour_centroid, df_POI_zoom_sur_centroid, distance_max_POI_reference, itineraire_pedestre, itineraire_cyclable, itineraire_routier, max_POI_TOUR_par_itineraire, alea_construction_itineraire, max_POI_par_itineraire, min_distance_entre_2_POI):
 
    df_POI_zoom_sur_centroid['POI_a_traiter'] = True                                                  ## colonne servant à discriminer les POI en cours de traitement
    df_POI_zoom_sur_centroid['POI_dans_itineraire'] = False                                           ## colonne servant à marquer les POI intégrés à un itinéraire 
    df_POI_zoom_sur_centroid['Numero_ordre_itineraire'] = 0                                           ## colonne servant à identifier le numéro de l'itinéraire   
  
    lat_centroid_radian = convert_degre_radian(lat_centroid_degre)                                    ## conversion des coordonnées géographiques de degrés en radians  
    lon_centroid_radian = convert_degre_radian(lon_centroid_degre) 

    lat_ref_radian = lat_centroid_radian                                                              ## dans la suite du traitement, les coordonnées de référence correspondent à celles du centroïd
    lon_ref_radian = lon_centroid_radian
       
   ## traitement spécifique des POI de types TOUR, correspondant à des itinéraires touristiques pédestres, cyclables ou routiers
    liste_POI_TOUR, itineraire_avec_POI_TOUR = traitement_POI_specifiques(lat_ref_radian, lon_ref_radian, df_POI_zoom_sur_centroid, itineraire_pedestre, itineraire_cyclable, itineraire_routier)
    
   ## construction des itinéraires autour des coordonnées des centroïds
    liste_des_itineraires, df_POI_zoom_sur_centroid, liste_no_ordre_itineraires = itineraires(df_POI_zoom_sur_centroid, lat_centroid_radian, lon_centroid_radian, nbre_jours_autour_centroid, distance_max_POI_reference, itineraire_avec_POI_TOUR, liste_POI_TOUR, max_POI_TOUR_par_itineraire, max_POI_par_itineraire, min_distance_entre_2_POI, alea_construction_itineraire)   
    
    ##liste_lat_lon_moyennes_iti = calcul_lat_lon_moyennes_iti(liste_no_ordre_itineraires, df_POI_zoom_sur_centroid)
      
    return liste_des_itineraires, df_POI_zoom_sur_centroid

def calcul_lat_lon_moyennes_iti(liste_no_ordre_itineraires, df_POI_zoom_sur_centroid):

    liste_lat_lon_moyennes_iti = []
    for no_ordre_iti in liste_no_ordre_itineraires:
        latitudes = list(df_POI_zoom_sur_centroid['Latitude'][df_POI_zoom_sur_centroid['Numero_ordre_itineraire'] == no_ordre_iti])
        longitudes = list(df_POI_zoom_sur_centroid['Longitude'][df_POI_zoom_sur_centroid['Numero_ordre_itineraire'] == no_ordre_iti])
        cumul_latitudes = 0
        cumul_longitudes = 0
        for latitude in latitudes:
            cumul_latitudes += latitude
        for longitude in longitudes:
            cumul_longitudes += longitude
        latitude_moyenne = cumul_latitudes/len(latitudes)     
        longitude_moyenne = cumul_longitudes/len(longitudes)
        liste_temporaire = []
        liste_temporaire.append(latitude_moyenne)
        liste_temporaire.append(longitude_moyenne)
        liste_lat_lon_moyennes_iti.append(liste_temporaire)
        
    return liste_lat_lon_moyennes_iti    

def traitement_POI_specifiques(lat_ref_radian, lon_ref_radian, df_POI_zoom_sur_centroid, itineraire_pedestre, itineraire_cyclable, itineraire_routier):
    
    liste_POI_itineraire_pedestre = []
    liste_POI_itineraire_cyclable = []
    liste_POI_itineraire_routier = []
        
    ## recherche des noms de POI des itinéraires pédestres
    if itineraire_pedestre:

        liste_nom_POI_ped = list(df_POI_zoom_sur_centroid['Nom_du_POI'][df_POI_zoom_sur_centroid['Mot_clé_POI'] == 'Itinéraire pédestre'])

        type_POI_TOUR = 'Itinéraire pédestre'
        for i in range(0,len(liste_nom_POI_ped)):
           # stockage des caractéristiques des POI TOUR pédestre         
            stockage_lat_long_POI_TOUR(df_POI_zoom_sur_centroid, type_POI_TOUR, liste_nom_POI_ped[i], liste_POI_itineraire_pedestre, liste_POI_itineraire_cyclable, liste_POI_itineraire_routier)
            
        for i in range(0, len(liste_POI_itineraire_pedestre)): 
           # calcul de la distance entre le POI de référence et les POI TOUR pédestre 
            distance = calcul_distance_POI_ref_POI_TOUR(lat_ref_radian, lon_ref_radian, liste_POI_itineraire_pedestre[i][2], liste_POI_itineraire_pedestre[i][3])
            liste_POI_itineraire_pedestre[i].append(distance)  
                      
    ## recherche des noms de POI des itinéraires cyclables   
    if itineraire_cyclable:

        liste_nom_POI_cycl = list(df_POI_zoom_sur_centroid['Nom_du_POI'][df_POI_zoom_sur_centroid['Mot_clé_POI'] == 'Itinéraire cyclable'])

        type_POI_TOUR = 'Itinéraire cyclable'
        for i in range(0,len(liste_nom_POI_cycl)):
           # stockage des caractéristiques des POI TOUR cyclable  
            stockage_lat_long_POI_TOUR(df_POI_zoom_sur_centroid, type_POI_TOUR, liste_nom_POI_cycl[i], liste_POI_itineraire_pedestre, liste_POI_itineraire_cyclable, liste_POI_itineraire_routier) 

        for i in range(0, len(liste_POI_itineraire_cyclable)): 
           # calcul de la distance entre le POI de référence et les POI TOUR cyclable
            distance = calcul_distance_POI_ref_POI_TOUR(lat_ref_radian, lon_ref_radian, liste_POI_itineraire_cyclable[i][2], liste_POI_itineraire_cyclable[i][3])    
            liste_POI_itineraire_cyclable[i].append(distance)   

    ## recherche des noms de POI des itinéraires routiers   
    if itineraire_routier:

        liste_nom_POI_rout = list(df_POI_zoom_sur_centroid['Nom_du_POI'][df_POI_zoom_sur_centroid['Mot_clé_POI'] == 'Itinéraire routier'])

        type_POI_TOUR = 'Itinéraire routier'
        for i in range(0,len(liste_nom_POI_rout)):
           # stockage des caractéristiques des POI TOUR routier  
            stockage_lat_long_POI_TOUR(df_POI_zoom_sur_centroid, type_POI_TOUR, liste_nom_POI_rout[i], liste_POI_itineraire_pedestre, liste_POI_itineraire_cyclable, liste_POI_itineraire_routier) 

        for i in range(0, len(liste_POI_itineraire_routier)): 
           # calcul de la distance entre le POI de référence et les POI TOUR routier
            distance = calcul_distance_POI_ref_POI_TOUR(lat_ref_radian, lon_ref_radian, liste_POI_itineraire_routier[i][2], liste_POI_itineraire_routier[i][3])
            liste_POI_itineraire_routier[i].append(distance)      

    ## concaténation des listes de types de POI TOUR
    liste_POI_TOUR = []
    if len(liste_POI_itineraire_pedestre) !=0:
        liste_POI_TOUR = liste_POI_itineraire_pedestre
        if len(liste_POI_itineraire_cyclable) != 0:
            liste_POI_TOUR += liste_POI_itineraire_cyclable
            if len(liste_POI_itineraire_routier) != 0:
                liste_POI_TOUR += liste_POI_itineraire_routier
    else:
        if len(liste_POI_itineraire_cyclable) != 0:
            liste_POI_TOUR += liste_POI_itineraire_cyclable
            if len(liste_POI_itineraire_routier) != 0:
                liste_POI_TOUR += liste_POI_itineraire_routier
        else:
            if len(liste_POI_itineraire_routier) != 0:
                liste_POI_TOUR = liste_POI_itineraire_routier             
              
    if len(liste_POI_TOUR) != 0:
        liste_POI_TOUR = sorted(liste_POI_TOUR, key=itemgetter(4))                                    ## tri de la liste sur la distance du POI au centroïd
        itineraire_avec_POI_TOUR = True                                                               ## traitement d'itinéraires avec POI TOUR
    else:
        itineraire_avec_POI_TOUR = False                                                              ## traitement d'itinéraires sans POI TOUR

    return liste_POI_TOUR, itineraire_avec_POI_TOUR 

def itineraires(df_POI_zoom_sur_centroid, lat_centroid_radian, lon_centroid_radian, nbre_jours_autour_centroid, distance_max_POI_reference, itineraire_avec_POI_TOUR, liste_POI_TOUR, max_POI_TOUR_par_itineraire, max_POI_par_itineraire, min_distance_entre_2_POI, alea_construction_itineraire):
    
    liste_des_itineraires = []
    liste_no_ordre_itineraires = []
    POI_eligibles = True
    POI_TOUR_eligibles = True
    nbre_max_itineraire_atteints = False
    no_ordre_itineraire = 0

    ## si l'un ou l'autre des types d'itinéraires TOUR sont souhaités, les itinéraires sont créés en les y intégrant
    if itineraire_avec_POI_TOUR:
      
        j = 0  
        for i in range(0, nbre_jours_autour_centroid):    
            no_ordre_itineraire +=1
            liste_no_ordre_itineraires.append(no_ordre_itineraire)
            
            for cpt_POI_TOUR_par_itineraire in range(1, max_POI_TOUR_par_itineraire+1):               ## boucle sur le nombre de POI TOUR max souhaités par itinéraire (en général, 1)

                if cpt_POI_TOUR_par_itineraire > 1:                                                   ## au delà du premier POI TOUR, dans la suite du traitement, les coordonnées                                                            
                    lat_ref_radian = convert_degre_radian(liste_POI_TOUR[j][2])                       ## de référence deviennent celles du POI TOUR courant                 
                    lon_ref_radian = convert_degre_radian(liste_POI_TOUR[j][3])
                    nbre_POI_a_completer = max_POI_par_itineraire - len(liste_des_itineraires[i])
                    type_trait = 'cible_nieme_POI_TOUR'
                else:
                    lat_ref_radian = lat_centroid_radian                                              ## dans la suite du traitement, les coordonnées de référence correspondent à celles du centroïd
                    lon_ref_radian = lon_centroid_radian
                    nbre_POI_a_completer = max_POI_par_itineraire
                    type_trait = 'cible_1er_POI_TOUR'

               ## constitution d'une partie de l'itinéraire : entre le centroïd et le premier POI TOUR ou entre deux POI TOUR
                preparation_construction_itineraire_avec_POI_TOUR(no_ordre_itineraire, df_POI_zoom_sur_centroid, type_trait, liste_des_itineraires, lat_ref_radian, lon_ref_radian, liste_POI_TOUR[j][2], liste_POI_TOUR[j][3], nbre_POI_a_completer, distance_max_POI_reference, alea_construction_itineraire, min_distance_entre_2_POI)     

                if POI_eligibles:
                    if len(liste_des_itineraires) == i+1:
                        liste_des_itineraires[i].append(liste_POI_TOUR[j][0])                 ## on ajoute en fin de première partie d'itinéraire le nom du POI TOUR en cours de traitement
                    else:
                        liste_temporaire = []
                        liste_temporaire.append(liste_POI_TOUR[j][0])
                        liste_des_itineraires.append(liste_temporaire)                        ## cas du POI TOUR étant le plus proche du centre de tous les POI

                    if len(liste_des_itineraires[i]) < max_POI_par_itineraire:                 ## si nbre de POI max atteints, on sort de la boucle
                       ## stockage du POI TOUR courant comme faisant partie d'un itinéraire
                        df_POI_zoom_sur_centroid['POI_dans_itineraire'][df_POI_zoom_sur_centroid['Nom_du_POI'] == liste_POI_TOUR[j][0]] = True
                        df_POI_zoom_sur_centroid['Numero_ordre_itineraire'][df_POI_zoom_sur_centroid['Nom_du_POI'] == liste_POI_TOUR[j][0]] = no_ordre_itineraire

                        lat_POI_TOUR_radian = convert_degre_radian(liste_POI_TOUR[j][2])  
                        lon_POI_TOUR_radian = convert_degre_radian(liste_POI_TOUR[j][3])

                       ## calcul de la distance entre le POI TOUR courant et chaque POI
                        type_gestion_POI = 'POI_sauf_restau_et_TOUR'
                        df_POI_zoom_sur_centroid['Distance'] = df_POI_zoom_sur_centroid.apply(lambda x: calcul_distance_POI_courant_autres_POI(x, lat_POI_TOUR_radian, lon_POI_TOUR_radian, type_gestion_POI, distance_max_POI_reference), axis=1)

                        if cpt_POI_TOUR_par_itineraire == max_POI_TOUR_par_itineraire:                     
                           ## construction de la fin de l'itinéraire : tous les POI de type non TOUR situés au delà du dernier POI TOUR inséré dans l'itinéraire
                            type_trait = 'cible_fin_itineraire'
                            construction_itineraire(no_ordre_itineraire, df_POI_zoom_sur_centroid, type_trait, liste_des_itineraires, lat_POI_TOUR_radian, lon_POI_TOUR_radian, 999, 999, 'inutilisé', max_POI_par_itineraire - len(liste_des_itineraires[i]), i, alea_construction_itineraire, min_distance_entre_2_POI, distance_max_POI_reference)                           

                        if j < len(liste_POI_TOUR)-1:                                                       ## tant qu'il reste des POI TOUR à traiter, on reste dans la boucle 
                            j +=1
                        else:                                                                               
                            POI_TOUR_eligibles = False                                                      
                    else:
                        nbre_max_itineraire_atteints = True                                                                                                         

                if (not POI_eligibles) | (not POI_TOUR_eligibles) | nbre_max_itineraire_atteints:           ## forçage de sortie de seconde boucle               
                    break

            if (not POI_eligibles) | (not POI_TOUR_eligibles) | (nbre_max_itineraire_atteints):             ## forçage de sortie de première boucle 
                break                          
                               
    ## si les types d'itinéraires TOUR ne sont pas souhaités, ou que le nombre d'itinéraires déjà construits avec POI TOUR est inférieur à la durée du séjour,
    ## les itinéraires complémentaires sont construits ci-après sans POI de type TOUR            

    lat_ref_radian = lat_centroid_radian                                                              ## dans la suite du traitement, les coordonnées de référence correspondent à celles du centroïd
    lon_ref_radian = lon_centroid_radian

    if len(liste_des_itineraires) < nbre_jours_autour_centroid:

        nbre_itineraires_restants = nbre_jours_autour_centroid - len(liste_des_itineraires)

        for i in range(0, nbre_itineraires_restants):       
            no_ordre_itineraire +=1
            liste_no_ordre_itineraires.append(no_ordre_itineraire)
            
           ## construction d'un itinéraire n'englobant pas de POI TOUR
            type_trait = 'cible_fin_itineraire'
            construction_itineraire(no_ordre_itineraire, df_POI_zoom_sur_centroid, type_trait, liste_des_itineraires, lat_ref_radian, lon_ref_radian, 999, 999, 'inutilisé', max_POI_par_itineraire, 999, alea_construction_itineraire, min_distance_entre_2_POI, distance_max_POI_reference)
            if not POI_eligibles:
                break             

    return liste_des_itineraires, df_POI_zoom_sur_centroid, liste_no_ordre_itineraires

def calcul_distance_POI_courant_autres_POI(x, lat_ref_radian, lon_ref_radian, type_gestion_POI, distance_max_POI_reference):      ## calcul distance entre le point de référence et les POI
    
    lat_POI_radian = convert_degre_radian(x['Latitude'])
    lon_POI_radian = convert_degre_radian(x['Longitude'])  
        
    mot_cle_POI = x['Mot_clé_POI']
    thematique_POI = x['Thématique_POI']
    nom_du_POI = x['Nom_du_POI']
 
   ## selon le cas, le calcul (ou recalcul) de la distance d'un POI à un autre porte sur la totalité des POI ou sur certains types d'entre eux, sélectionnés
   ## sur la base du mot clé qui les caractérise. Afin de ne traiter que ceux qui doivent l'être, les autres se voient forcer leur distance à une valeur élevée
   ## (ici, le paramètre ayant servi à centrer notre dataframe sur le centroïd. De cette façon, ils ne seront pas intégrés dans les itinéraires car trop éloignés
   ## du centroïd) 
    
    if type_gestion_POI == 'POI_sauf_restau_et_TOUR':
        if (thematique_POI == 'Restauration/Bar a theme') | (thematique_POI == 'Gastronomie') | (mot_cle_POI == 'Itinéraire pédestre') | (mot_cle_POI == 'Itinéraire cyclable') | (mot_cle_POI == 'Itinéraire routier'):
            return distance_max_POI_reference
        else:
            distance = formule_calcul_distance(lat_ref_radian, lon_ref_radian, lat_POI_radian, lon_POI_radian)                 
            return distance
    else:
        distance = formule_calcul_distance(lat_ref_radian, lon_ref_radian, lat_POI_radian, lon_POI_radian)                 
        return distance

def calcul_distance_POI_ref_POI_TOUR(lat_ref_radian, lon_ref_radian, latitude_POI_TOUR, longitude_POI_TOUR):
    
    lat_POI_TOUR_radian = convert_degre_radian(latitude_POI_TOUR)
    lon_POI_TOUR_radian = convert_degre_radian(longitude_POI_TOUR)
    distance = formule_calcul_distance(lat_ref_radian, lon_ref_radian, lat_POI_TOUR_radian, lon_POI_TOUR_radian)
    return distance

def convert_degre_radian(degre):                                                                      ## conversion des degrés en radian
    return (np.pi * degre)/180

def formule_calcul_distance(lat_ref_radian, lon_ref_radian, lat_POI_radian, lon_POI_radian):
    
    R = 6371                              ## rayon de la terre en kms
    
    ##distance = R * math.acos(math.sin(lat_ref_radian)*math.sin(lat_POI_radian) + math.cos(lat_ref_radian)*math.cos(lat_POI_radian)*math.cos(lon_POI_radian - lon_ref_radian)) 
    
    distance = R * 2 * math.asin(math.sqrt(math.sin((lat_ref_radian - lat_POI_radian)/2) * math.sin((lat_ref_radian - lat_POI_radian)/2)
                     + math.cos(lat_ref_radian) * math.cos(lat_POI_radian) * math.sin((lon_ref_radian - lon_POI_radian)/2) * math.sin((lon_ref_radian - lon_POI_radian)/2)))
    return distance
   
def construction_itineraire(no_ordre_itineraire, df_POI_zoom_sur_centroid, type_trait, liste_des_itineraires, lat_ref_radian, lon_ref_radian, lat_POI_TOUR_radian, lon_POI_TOUR_radian, dist_POI_ref_POI_TOUR, limitation_itineraire, index_itineraire, alea_construction_itineraire, min_distance_entre_2_POI, distance_max_POI_reference):
    
    liste_POI_itineraire = []          
     
   ## boucle jusqu'à atteindre le nombre de POI maximum par itinéraire ou jusqu'à épuisement des POI situés entre le POI de référence et le POI TOUR en cours de traitement  
    for k in range(0, limitation_itineraire):                                                     
 
       ## traitement du POI le plus proche du POI précédent : les POI ne sont correctement représentés sur le carte interactive qu'au delà d'une certaine distance (min_distance_entre_2_POI)        
        if alea_construction_itineraire == 1:
       ## l'utisateur a choisi une construction non aléatoire des itinéraires
            distance_mini = df_POI_zoom_sur_centroid['Distance'][(df_POI_zoom_sur_centroid['POI_a_traiter'] == True) & (df_POI_zoom_sur_centroid['Distance'] >= min_distance_entre_2_POI)].min()
        else:
       ## l'utisateur a choisi une construction aléatoire des itinéraires
            distance_mini = gestion_degre_alea_itineraire(df_POI_zoom_sur_centroid, min_distance_entre_2_POI, alea_construction_itineraire)                 
                      
        if pd.isna(distance_mini):                                                                    ## si plus de POI retourné, forçage de la sortie de boucle            
            POI_eligibles = False                                                                         
            break
            
        else:                         
            nom_POI_courant = list(df_POI_zoom_sur_centroid['Nom_du_POI'][(df_POI_zoom_sur_centroid['Distance'] == distance_mini)])
               
            if len(nom_POI_courant) != 0:
                latitude_POI_courant = list(df_POI_zoom_sur_centroid['Latitude'][df_POI_zoom_sur_centroid['Nom_du_POI'] == nom_POI_courant[0]])              
                longitude_POI_courant = list(df_POI_zoom_sur_centroid['Longitude'][df_POI_zoom_sur_centroid['Nom_du_POI'] == nom_POI_courant[0]])               
                
               ## prise en compte du POI suivant  
                lat_POI_radian = convert_degre_radian(latitude_POI_courant[0])                         
                lon_POI_radian = convert_degre_radian(longitude_POI_courant[0]) 
               
               ## calcul distance entre le POI courant et le point de référence  
                dist_POI_ref_POI_courant = formule_calcul_distance(lat_ref_radian, lon_ref_radian, lat_POI_radian, lon_POI_radian)
                                              
                if type_trait != 'cible_fin_itineraire':                    
                    POI_eligible = gestion_coherence_itineraire(lat_ref_radian, lon_ref_radian, lat_POI_TOUR_radian, lon_POI_TOUR_radian, lat_POI_radian, lon_POI_radian, dist_POI_ref_POI_TOUR, dist_POI_ref_POI_courant)                   
                else:
                    POI_eligible = False 
               
                if (type_trait != 'cible_fin_itineraire') & (not POI_eligible):                         ## si le POI courant ne satisfait pas aux conditions d'éligibilité, on essaie de trouver un autre POI éligible
                    
                    df_POI_zoom_sur_centroid['POI_a_traiter'].loc[(df_POI_zoom_sur_centroid['Distance'] == distance_mini) & (df_POI_zoom_sur_centroid['POI_a_traiter'] == True)] = False
                    type_gestion_POI = 'POI_sauf_restau_et_TOUR'
                    df_POI_zoom_sur_centroid['Distance'] = df_POI_zoom_sur_centroid.apply(lambda x: calcul_distance_POI_courant_autres_POI(x, lat_ref_radian, lon_ref_radian, type_gestion_POI, distance_max_POI_reference), axis=1)
                    
                else: 
                   ## stockage du Nom du POI courant                               
                    liste_POI_itineraire.append(nom_POI_courant[0])
                
                   ## stockage de l'information rendant compte du fait que le POI courant a intègré un itinéraire 
                    df_POI_zoom_sur_centroid['POI_dans_itineraire'][df_POI_zoom_sur_centroid['Nom_du_POI'] == nom_POI_courant[0]] = True
                    df_POI_zoom_sur_centroid['Numero_ordre_itineraire'][df_POI_zoom_sur_centroid['Nom_du_POI'] == nom_POI_courant[0]] = no_ordre_itineraire
           
                   ## marquage des POI ne devant pas intégrer l'itinéraire en construction car d'une distance inférieure au point de référence par-rapport au POI courant
                    df_POI_zoom_sur_centroid['POI_a_traiter'].loc[(df_POI_zoom_sur_centroid['Distance'] <= distance_mini) & (df_POI_zoom_sur_centroid['POI_a_traiter'] == True)] = False
                            
                   ## calcul de la distance entre le POI courant et les autres POI
                    type_gestion_POI = 'POI_sauf_restau_et_TOUR'
                    df_POI_zoom_sur_centroid['Distance'] = df_POI_zoom_sur_centroid.apply(lambda x: calcul_distance_POI_courant_autres_POI(x, lat_POI_radian, lon_POI_radian, type_gestion_POI, distance_max_POI_reference), axis=1)
  
    if ((type_trait == 'cible_1er_POI_TOUR') | (index_itineraire == 999)) & (len(liste_POI_itineraire) != 0):
        liste_des_itineraires.append(liste_POI_itineraire)                                            ## initialisation du stockage de la liste courante des POI dans la liste des itinéraires
                                                                                                      ## ou stockage de tous les POI de l'itinéraire de type non TOUR
    else:
        for nom_POI in liste_POI_itineraire:
            liste_des_itineraires[index_itineraire].append(nom_POI)                                   ## stockage des POI situés au delà du POI TOUR (si itinéraire avec POI TOUR)

def gestion_degre_alea_itineraire(df_POI_zoom_sur_centroid, min_distance_entre_2_POI, alea_construction_itineraire):
    
    distance_POI_prec_POI_courant = list(df_POI_zoom_sur_centroid['Distance'][(df_POI_zoom_sur_centroid['POI_a_traiter'] == True) & (df_POI_zoom_sur_centroid['Distance'] >= min_distance_entre_2_POI)])
    distance_POI_prec_POI_courant = sorted(distance_POI_prec_POI_courant)
    
    if len(distance_POI_prec_POI_courant) > 0:                                                        ## si POI éligibles

        index_degre_alea_trouve = False
        for rang in reversed(range(2, 5)):                                                            ## recherche de la distance minimale retournée, compatible avec le degré d'aléa souhaité
            if rang == alea_construction_itineraire:                                                  ## plus le degré d'aléa est élevé, plus l'itinéraire s'éloigne du centroïd
                index_degre_alea = int(np.random.randint(0, alea_construction_itineraire, 1))
                index_degre_alea_trouve = True
                break
            
        if index_degre_alea_trouve:
            if (len(distance_POI_prec_POI_courant) - index_degre_alea) >= 1:
                return distance_POI_prec_POI_courant[index_degre_alea]
            else:
                return distance_POI_prec_POI_courant[0]
        else:
            return distance_POI_prec_POI_courant[0]                                                       ## si la distance retournée n'est pas compatible avec le degré d'aléa souhaité >> construction d'un itinéraire sans aléa
    
def gestion_coherence_itineraire(lat_ref_radian, lon_ref_radian, lat_POI_TOUR_radian, lon_POI_TOUR_radian, lat_POI_radian, lon_POI_radian, dist_POI_ref_POI_TOUR, dist_POI_ref_POI_courant):
    
    lat_POI_eligible = False
    lon_POI_eligible = False
    distance_POI_eligible = False
                    
    min_lat_POI_ref_POI_TOUR = min(lat_ref_radian, lat_POI_TOUR_radian)
    max_lat_POI_ref_POI_TOUR = max(lat_ref_radian, lat_POI_TOUR_radian)
    min_lon_POI_ref_POI_TOUR = min(lon_ref_radian, lon_POI_TOUR_radian)
    max_lon_POI_ref_POI_TOUR = max(lon_ref_radian, lon_POI_TOUR_radian)
                                     
    if (lat_POI_radian >= min_lat_POI_ref_POI_TOUR) & (lat_POI_radian <= max_lat_POI_ref_POI_TOUR) :
        lat_POI_eligible = True
                        
    if (lon_POI_radian >= min_lon_POI_ref_POI_TOUR) & (lon_POI_radian <= max_lon_POI_ref_POI_TOUR) :
        lon_POI_eligible = True
                                        
    if dist_POI_ref_POI_courant < dist_POI_ref_POI_TOUR:    
        distance_POI_eligible = True
                
    if lat_POI_eligible & lon_POI_eligible & distance_POI_eligible:                                   ## le POI courant n'est intégré à l'itinéraire qu'à certainnes conditions de compatibilité    
        POI_eligible = True                                                                           ## entre ses latitude, longitude et distance par-rapport au POI de référence en lien avec le POI TOUR courant
    else:
        POI_eligible = False
    
    return POI_eligible    
    
def stockage_lat_long_POI_TOUR(df_POI_zoom_sur_centroid, type_POI_TOUR, nom_POI_TOUR, liste_POI_itineraire_pedestre, liste_POI_itineraire_cyclable, liste_POI_itineraire_routier):        
   
    lat_POI_TOUR = list(df_POI_zoom_sur_centroid['Latitude'][df_POI_zoom_sur_centroid['Nom_du_POI'] == nom_POI_TOUR])
    lon_POI_TOUR = list(df_POI_zoom_sur_centroid['Longitude'][df_POI_zoom_sur_centroid['Nom_du_POI'] == nom_POI_TOUR])
    
    liste_temp = []
    liste_temp.append(nom_POI_TOUR)
    liste_temp.append(type_POI_TOUR)
    liste_temp.append(lat_POI_TOUR[0])
    liste_temp.append(lon_POI_TOUR[0])
    
    if type_POI_TOUR == 'Itinéraire pédestre':
        liste_POI_itineraire_pedestre.append(liste_temp)
    
    elif type_POI_TOUR == 'Itinéraire cyclable':
        liste_POI_itineraire_cyclable.append(liste_temp)
    
    elif type_POI_TOUR == 'Itinéraire routier':
        liste_POI_itineraire_routier.append(liste_temp)
        
def preparation_construction_itineraire_avec_POI_TOUR(no_ordre_itineraire, df_POI_zoom_sur_centroid, type_trait, liste_des_itineraires, lat_ref_radian, lon_ref_radian, lat_POI_TOUR, lon_POI_TOUR, nbre_POI_a_completer, distance_max_POI_reference, alea_construction_itineraire, min_distance_entre_2_POI):
    
    lat_POI_TOUR_radian = convert_degre_radian(lat_POI_TOUR)  
    lon_POI_TOUR_radian = convert_degre_radian(lon_POI_TOUR)
    
    dist_POI_ref_POI_TOUR = formule_calcul_distance(lat_ref_radian, lon_ref_radian, lat_POI_TOUR_radian, lon_POI_TOUR_radian)    
   
   ## calcul de la distance entre le POI de référence et chaque POI
    type_gestion_POI = 'POI_sauf_restau_et_TOUR'
    df_POI_zoom_sur_centroid['Distance'] = df_POI_zoom_sur_centroid.apply(lambda x: calcul_distance_POI_courant_autres_POI(x, lat_ref_radian, lon_ref_radian, type_gestion_POI, distance_max_POI_reference), axis=1)     
           
    construction_itineraire(no_ordre_itineraire, df_POI_zoom_sur_centroid, type_trait, liste_des_itineraires, lat_ref_radian, lon_ref_radian, lat_POI_TOUR_radian, lon_POI_TOUR_radian, dist_POI_ref_POI_TOUR, nbre_POI_a_completer, 999, alea_construction_itineraire, min_distance_entre_2_POI, distance_max_POI_reference)


