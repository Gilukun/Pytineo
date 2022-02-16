#!/usr/bin/env python
# coding: utf-8
##----------------------------------------------------------------------
## matérialisation des itinéraires sur une carte STREETMAP interactive
##----------------------------------------------------------------------
import numpy as np
import pandas as pd
import folium
from folium.plugins import MousePosition
import csv
import math
import openrouteservice 
from openrouteservice import client
from bs4 import BeautifulSoup
from urllib.request import urlopen
import time
import re

##------------
## Fonctions
##------------
def recherche_attributs_POI(no_centroid, lat_centroid, lon_centroid, df_POI_zoom_sur_centroid, nom_POI, df_themes_POI):
    
    dict_attributs_POI = {}
    
    adresse_POI = list(df_POI_zoom_sur_centroid['Adresse_postale'][df_POI_zoom_sur_centroid['Nom_du_POI'] == nom_POI])
    dict_attributs_POI['adresse_POI'] = adresse_POI[0] 
    
    lat_POI = list(df_POI_zoom_sur_centroid['Latitude'][df_POI_zoom_sur_centroid['Nom_du_POI'] == nom_POI])
    dict_attributs_POI['lat_POI'] = lat_POI[0]   
          
    lon_POI = list(df_POI_zoom_sur_centroid['Longitude'][df_POI_zoom_sur_centroid['Nom_du_POI'] == nom_POI])
    dict_attributs_POI['lon_POI'] = lon_POI[0]
    
    theme_POI_df_centroid = list(df_POI_zoom_sur_centroid['Thématique_POI'][df_POI_zoom_sur_centroid['Nom_du_POI'] == nom_POI])
    dict_attributs_POI['theme_POI'] = theme_POI_df_centroid[0] 
    
    mot_cle_POI_df_centroid = list(df_POI_zoom_sur_centroid['Mot_clé_POI'][df_POI_zoom_sur_centroid['Nom_du_POI'] == nom_POI])
    dict_attributs_POI['mot_cle_POI'] = mot_cle_POI_df_centroid[0]
    
    sous_theme_POI_df_themes = list(df_themes_POI['Sous_thème_POI'][df_themes_POI['Thématique_POI'] == theme_POI_df_centroid[0]])
       
    for sous_theme in sous_theme_POI_df_themes:
        if sous_theme == mot_cle_POI_df_centroid[0]:
            icone_POI = list(df_themes_POI['Icone_représentation_visuelle'][df_themes_POI['Sous_thème_POI'] == mot_cle_POI_df_centroid[0]])
            break
        else:
            icone_POI = list(df_themes_POI['Icone_représentation_visuelle'][df_themes_POI['Sous_thème_POI'] == theme_POI_df_centroid[0]])                                                                       
    dict_attributs_POI['icone_POI'] = icone_POI[0]
      
    description_courte = list(df_POI_zoom_sur_centroid['Description_courte'][df_POI_zoom_sur_centroid['Nom_du_POI'] == nom_POI])
    dict_attributs_POI['description_courte'] = description_courte[0]                                                                              
        
    ##URI_ID_POI = list(df_POI_zoom_sur_centroid['URI_ID_du_POI'][df_POI_zoom_sur_centroid['Nom_du_POI'] == nom_POI])
    ##dict_attributs_POI['URI_description'] = web_scraping_URI_POI(URI_ID_POI[0])
    dict_attributs_POI['URI_description'] = 'URI POI inexistante'
      
    return dict_attributs_POI

    
def web_scraping_URI_POI(URI_POI):
    
    page_SC = urlopen(URI_POI)
    soup = BeautifulSoup(page_SC, 'html.parser')
    noms_SC = soup.findAll(attrs = {'class': 'list-group-item'})
    
    URI_description_trouvee = False
    for contenu_balise_a in noms_SC:
        if 'a pour description courte ou longue' in contenu_balise_a.text:
            r = re.compile(r"data\:+[0-9a-z\-]+") 
            URI_partielle = r.findall(contenu_balise_a.text)
            if len(URI_partielle) !=0:
                URI_complete = 'https://data.datatourisme.gouv.fr/' + URI_partielle[0][5:]
                URI_description_trouvee = True

    if URI_description_trouvee:
        return URI_complete
    else:
        return 'URI POI inexistante'
           
                
def calcul_distance(lat_POI_precedente, lon_POI_precedente, lat_POI, lon_POI):
    
    lat_POI_pre_radian = convert_degre_radian(lat_POI_precedente)
    lon_POI_pre_radian = convert_degre_radian(lon_POI_precedente)
    lat_POI_radian = convert_degre_radian(lat_POI)
    lon_POI_radian = convert_degre_radian(lon_POI)
    
    distance = formule_calcul_distance(lat_POI_pre_radian, lon_POI_pre_radian, lat_POI_radian, lon_POI_radian)         
    
    return distance


def convert_degre_radian(degre):                                                                 ## conversion des degrés en radian
    return (np.pi * degre)/180


def formule_calcul_distance(lat_ref_radian, lon_ref_radian, lat_POI_radian, lon_POI_radian):
    
    R = 6371                                                                                     ## rayon de la terre en kms 
    
    distance = R * 2 * math.asin(math.sqrt(math.sin((lat_ref_radian - lat_POI_radian)/2) * math.sin((lat_ref_radian - lat_POI_radian)/2)
                     + math.cos(lat_ref_radian) * math.cos(lat_POI_radian) * math.sin((lon_ref_radian - lon_POI_radian)/2) * math.sin((lon_ref_radian - lon_POI_radian)/2)))
    return distance


def rech_position_geographique_itineraire(lat_POI_central_iti, lon_POI_central_iti, lat_centre_commune, lon_centre_commune):        
    
   # recherche de la distance entre le barycentre de l'itinéraire et le centre de la commune ou le centroid
    dist_centre_commune = calcul_distance(lat_centre_commune, lon_centre_commune, lat_POI_central_iti, lon_POI_central_iti)
    
   # recherche de la localisation globale de l'itinéraire par-rapport au centre de la commune de séjour
    if (lat_POI_central_iti > lat_centre_commune) & (lon_POI_central_iti > lon_centre_commune):
        loc_relative_centre_commune = 'nord-est'
        
    elif (lat_POI_central_iti > lat_centre_commune) & (lon_POI_central_iti < lon_centre_commune):
        loc_relative_centre_commune = 'nord-ouest'
            
    elif (lat_POI_central_iti < lat_centre_commune) & (lon_POI_central_iti < lon_centre_commune):
        loc_relative_centre_commune = 'sud-ouest'
            
    elif (lat_POI_central_iti < lat_centre_commune) & (lon_POI_central_iti> lon_centre_commune):
        loc_relative_centre_commune = 'sud-est'
     
    return dist_centre_commune, loc_relative_centre_commune   


def recherche_attributs_POI_resto(no_centroid, df_POI_zoom_sur_centroid, lat_POI_central_iti, lon_POI_central_iti, restauration_souhaitee, restauration_rapide_souhaitee, gastronomie_souhaitee, libelle_restauration, libelle_restauration_rapide, libelle_gastronomie ,nbre_POI_resto_dans_périmetre_iti, df_themes_POI):     
              
    liste_nom_POI_resto = []
    liste_liste_lat_lon_POI_resto = []
    liste_theme_POI_resto = []
    liste_mot_cle_POI_resto = []
    liste_icone_POI_resto = []
    liste_description_POI_resto = []   
    liste_distance_POI_resto = [] 
    liste_adresse_POI_resto = []
    cpt_POI_resto_traites = 0
    
    if restauration_souhaitee :
        nom_resto_gene = list(df_POI_zoom_sur_centroid['Nom_du_POI'][(df_POI_zoom_sur_centroid['Numéro_centroïd'] == no_centroid) & (df_POI_zoom_sur_centroid['Mot_clé_POI'] == libelle_restauration)])
        cpt_POI_resto_traites, liste_nom_POI_resto, liste_liste_lat_lon_POI_resto, liste_theme_POI_resto, liste_mot_cle_POI_resto, liste_icone_POI_resto, liste_description_POI_resto, liste_distance_POI_resto, liste_adresse_POI_resto = recherche_generique(nbre_POI_resto_dans_périmetre_iti, cpt_POI_resto_traites, df_POI_zoom_sur_centroid, lat_POI_central_iti, lon_POI_central_iti, nom_resto_gene, liste_nom_POI_resto, liste_liste_lat_lon_POI_resto, liste_theme_POI_resto, liste_mot_cle_POI_resto, liste_icone_POI_resto, liste_description_POI_resto, liste_distance_POI_resto, liste_adresse_POI_resto, df_themes_POI)

    if restauration_rapide_souhaitee & (cpt_POI_resto_traites < nbre_POI_resto_dans_périmetre_iti) :
        nom_resto_gene = list(df_POI_zoom_sur_centroid['Nom_du_POI'][(df_POI_zoom_sur_centroid['Numéro_centroïd'] == no_centroid) & (df_POI_zoom_sur_centroid['Mot_clé_POI'] == libelle_restauration_rapide)])
        cpt_POI_resto_traites, liste_nom_POI_resto, liste_liste_lat_lon_POI_resto, liste_theme_POI_resto, liste_mot_cle_POI_resto, liste_icone_POI_resto, liste_description_POI_resto, liste_distance_POI_resto, liste_adresse_POI_resto = recherche_generique(nbre_POI_resto_dans_périmetre_iti, cpt_POI_resto_traites, df_POI_zoom_sur_centroid, lat_POI_central_iti, lon_POI_central_iti, nom_resto_gene, liste_nom_POI_resto, liste_liste_lat_lon_POI_resto, liste_theme_POI_resto, liste_mot_cle_POI_resto, liste_icone_POI_resto, liste_description_POI_resto, liste_distance_POI_resto, liste_adresse_POI_resto, df_themes_POI)
        
    if gastronomie_souhaitee & (cpt_POI_resto_traites < nbre_POI_resto_dans_périmetre_iti) :
        nom_resto_gene = list(df_POI_zoom_sur_centroid['Nom_du_POI'][(df_POI_zoom_sur_centroid['Numéro_centroïd'] == no_centroid) & (df_POI_zoom_sur_centroid['Thématique_POI'] == libelle_gastronomie)])
        cpt_POI_resto_traites, liste_nom_POI_resto, liste_liste_lat_lon_POI_resto, liste_theme_POI_resto, liste_mot_cle_POI_resto, liste_icone_POI_resto, liste_description_POI_resto, liste_distance_POI_resto, liste_adresse_POI_resto = recherche_generique(nbre_POI_resto_dans_périmetre_iti, cpt_POI_resto_traites, df_POI_zoom_sur_centroid, lat_POI_central_iti, lon_POI_central_iti, nom_resto_gene, liste_nom_POI_resto, liste_liste_lat_lon_POI_resto, liste_theme_POI_resto, liste_mot_cle_POI_resto, liste_icone_POI_resto, liste_description_POI_resto, liste_distance_POI_resto, liste_adresse_POI_resto, df_themes_POI)

    if len(liste_nom_POI_resto) != 0:
        liste_distance_POI_resto, liste_nom, liste_liste_lat_lon, liste_theme, liste_mot_cle, liste_icone, liste_description, liste_adresse = zip(*sorted(zip(liste_distance_POI_resto, liste_nom_POI_resto, liste_liste_lat_lon_POI_resto, liste_theme_POI_resto, liste_mot_cle_POI_resto, liste_icone_POI_resto, liste_description_POI_resto, liste_adresse_POI_resto), key=lambda x: x[0]))

        liste_nom = list(liste_nom)
        liste_liste_lat_lon = list(liste_liste_lat_lon)
        liste_theme = list(liste_theme)
        liste_mot_cle = list(liste_mot_cle)
        liste_icone = list(liste_icone)
        liste_description = list(liste_description)
        liste_adresse = list(liste_adresse)
    else:
        liste_nom = []
        liste_liste_lat_lon = []
        liste_theme = []
        liste_mot_cle = []
        liste_icone = []
        liste_description = []
        liste_adresse = []

    return liste_nom, liste_liste_lat_lon, liste_theme, liste_mot_cle, liste_icone, liste_description, liste_adresse    


def recherche_generique(nbre_POI_resto_dans_périmetre_iti, cpt_POI_resto_traites, df_POI_zoom_sur_centroid, lat_POI_central_iti, lon_POI_central_iti, nom_resto_gene, liste_nom_POI_resto, liste_liste_lat_lon_POI_resto, liste_theme_POI_resto, liste_mot_cle_POI_resto, liste_icone_POI_resto, liste_description_POI_resto, liste_distance_POI_resto, liste_adresse_POI_resto, df_themes_POI):

    for nom_POI in nom_resto_gene:

        cpt_POI_resto_traites +=1

        if cpt_POI_resto_traites < nbre_POI_resto_dans_périmetre_iti:

            adresse_resto_gene = list(df_POI_zoom_sur_centroid['Adresse_postale'][df_POI_zoom_sur_centroid['Nom_du_POI'] == nom_POI])
            liste_adresse_POI_resto.append(adresse_resto_gene[0])

            lat_resto_gene = list(df_POI_zoom_sur_centroid['Latitude'][df_POI_zoom_sur_centroid['Nom_du_POI'] == nom_POI])
            lon_resto_gene = list(df_POI_zoom_sur_centroid['Longitude'][df_POI_zoom_sur_centroid['Nom_du_POI'] == nom_POI])

            distance = calcul_distance(lat_POI_central_iti, lon_POI_central_iti, lat_resto_gene[0], lon_resto_gene[0])
            liste_distance_POI_resto.append(distance)

            liste_nom_POI_resto.append(nom_POI)

            liste_temporaire = []
            liste_temporaire.append(lat_resto_gene[0])
            liste_temporaire.append(lon_resto_gene[0])
            liste_liste_lat_lon_POI_resto.append(liste_temporaire)

            theme_resto_gene = list(df_POI_zoom_sur_centroid['Thématique_POI'][df_POI_zoom_sur_centroid['Nom_du_POI'] == nom_POI])
            mot_cle_resto_gene = list(df_POI_zoom_sur_centroid['Mot_clé_POI'][df_POI_zoom_sur_centroid['Nom_du_POI'] == nom_POI])
            desc_courte_resto_gene = list(df_POI_zoom_sur_centroid['Description_courte'][df_POI_zoom_sur_centroid['Nom_du_POI'] == nom_POI])

            liste_theme_POI_resto.append(theme_resto_gene[0])
            liste_mot_cle_POI_resto.append(mot_cle_resto_gene[0])
            liste_description_POI_resto.append(desc_courte_resto_gene[0])

            icone_POI_resto = list(df_themes_POI['Icone_représentation_visuelle'][df_themes_POI['Sous_thème_POI'] == mot_cle_resto_gene[0]])

            if len(icone_POI_resto) != 0:
                liste_icone_POI_resto.append(icone_POI_resto[0])
            else:
                liste_icone_POI_resto.append('Pas d\'icone POI resto disponible')
        else:
            break

    return cpt_POI_resto_traites, liste_nom_POI_resto, liste_liste_lat_lon_POI_resto, liste_theme_POI_resto, liste_mot_cle_POI_resto, liste_icone_POI_resto, liste_description_POI_resto, liste_distance_POI_resto, liste_adresse_POI_resto
                                                                     
                                                                     
def construction_itineraire_carte(no_centroid, longueur_itineraire, liste_nom_POI, liste_adresse_POI, liste_tuple_lat_lon_POI, liste_liste_lat_lon_POI, liste_liste_lon_lat_POI, liste_theme_POI, liste_mot_cle_POI, liste_icone_POI, liste_description_POI, liste_URI_description_POI, lat_POI_central_iti, lon_POI_central_iti, dist_centre_commune, loc_relative_centre_commune, dict_attributs_sejour):                                                                                
   
   # le dictionnaire suivant permet de d'adapter le zoom de la carte à la longueur de l'itinéraire  
    dict_long_iti_valeur_zoom = {18.0:[0.0, 1.0], 17:[1.1, 2.0], 15.5:[2.1, 4.0], 15.0:[4.1, 6.0], 14.4:[6.1, 8.0], 14.0:[8.1, 10.0], 13.5:[10.1, 99]}
    for cle, valeur in dict_long_iti_valeur_zoom.items():
        if (longueur_itineraire >=  valeur[0]) & (longueur_itineraire <=  valeur[1]):
            valeur_de_zoom = cle

    if int(round(dist_centre_commune, 0)) <= 1:
        libelle_1_km = ' km au '
    else:
        libelle_1_km = ' kms au '

    if int(round(longueur_itineraire, 0)) <= 1:
        libelle_2_km = ' km '
    else:
        libelle_2_km = ' kms '

   # description de la position géographique relative de l'itinéraire                                                              
    liste_voyelles = ['A', 'E', 'I', 'O', 'U']
    nom_commune_reference = dict_attributs_sejour['nom_commune_reference']
    if nom_commune_reference[0] in liste_voyelles:
        pos_geo_itineraire = 'Itinéraire de ' + str(int(round(longueur_itineraire, 0))) + libelle_2_km + 'situé à ' + str(int(round(dist_centre_commune, 0))) + libelle_1_km + loc_relative_centre_commune + ' d\'' + nom_commune_reference
    else:
        pos_geo_itineraire = 'Itinéraire de ' + str(int(round(longueur_itineraire, 0))) + libelle_2_km + 'situé à ' + str(int(round(dist_centre_commune, 0))) + libelle_1_km + loc_relative_centre_commune + ' de ' + nom_commune_reference

   # implémentation de la fonctionnalité 'openrouteservice' pour matérialiser l'itinéraire en suivant les routes de POI en POI 
    client = openrouteservice.Client(key='5b3ce3597851110001cf62489585426c1497421aa8b3c7a5d4c5c5f0')
    
   # itinéraire fonction du mode de transport choisi : “driving-car”, “driving-hgv”, “foot-walking”, “foot-hiking”, “cycling-regular”, “cycling-road”,”cycling-mountain”, “cycling-electric”      
    try:
        carte_openrouteservice = True
        if longueur_itineraire <= 2:
            route = client.directions(coordinates = liste_liste_lon_lat_POI, profile = 'foot-walking', format = 'geojson', optimize_waypoints = True)   
        elif longueur_itineraire <= 5:       
            route = client.directions(coordinates = liste_liste_lon_lat_POI, profile = 'cycling-road', format = 'geojson', optimize_waypoints = True)  
        else:
            route = client.directions(coordinates = liste_liste_lon_lat_POI, profile = 'driving-car', format = 'geojson', optimize_waypoints = True)          
           
    except:  
       # le service openrouteservice ne peut pas relier deux points distants de plus de 350 mètres sans route openrouteservice disponible 
        carte_openrouteservice = False

   # Sélection du type de tuile à implémenter dans Folium
    import datetime
    date_jour = str(datetime.datetime.today())
    if date_jour[:10] > '2022-02-17':
        select_tile = 'OpenStreetMap'
    else:
        select_tile = 'cartodbpositron'

    fmap = folium.Map(location=[lat_POI_central_iti, lon_POI_central_iti], tiles=select_tile, zoom_start=valeur_de_zoom)

   # Création d'une carte centrée sur les coordonnées géographiques du centroïd de l'itinéraire

    formatter = "function(num) {return L.Util.formatNum(num, 6) + ' º ';};"                       ## fait apparaître les coordonnées géographiques des points cliqués ou survolés,
    MousePosition(                                                                                ## en haut à droite de la carte interactive
        position="topright",
        separator=" | ",
        empty_string="NaN",
        lng_first=False,
        num_digits=20,
        prefix="Coordonnées:",
        lat_formatter=formatter,
        lng_formatter=formatter,
    ).add_to(fmap)     

    icon_size=(25, 25)
    icon_size_centre_commune=(35, 35)
       
    for i in range(0, len(liste_nom_POI)):                                                           ## mise en forme des informations propres aux POI à afficher sur la carte

        nom_POI_HTML = '<center><strong><font size="3.5">' + liste_nom_POI[i] + '</font></strong><br>'     
        adresse_POI_HTML = liste_adresse_POI[i] + '</center>'
        
        description_POI= liste_description_POI[i]
        lng_ligne = 50
        if len(description_POI) > lng_ligne:
            lignes = [(description_POI[i:i+lng_ligne]) for i in range(0, len(description_POI), lng_ligne)]
            for j, ligne in enumerate(lignes):
                if j == 0:
                    description_POI_HTML = '<br><text-align: left>' + ligne
                elif j == len(lignes):
                    description_POI_HTML += '<br>' + ligne + '</<text-align: left>'                    
                else:
                    description_POI_HTML += '<br>' + ligne
        else:       
            description_POI_HTML = '<br><text-align: left><strong>' + description_POI + '</strong></text-align: left>'
            
        URI_description_POI = liste_URI_description_POI[i]        
        if URI_description_POI != 'URI POI inexistante':
            texte_acces_detail = '<br><br><center><strong>Cliquez pour plus de détail</center></strong>'
            prepa_popup = '<a href="'+ URI_description_POI + '" target="_blank">Description plus précise du point touristique</a>'
        
        ##if description_POI != 'Description longue non précisée':
        if description_POI != 'Description courte non précisée':
            if URI_description_POI != 'URI POI inexistante':
                prepa_tooltip = nom_POI_HTML + adresse_POI_HTML + description_POI_HTML + texte_acces_detail 
            else:   
                prepa_tooltip = nom_POI_HTML + adresse_POI_HTML + description_POI_HTML
        else:
            if URI_description_POI != 'URI POI inexistante':                
                prepa_tooltip = nom_POI_HTML + texte_acces_detail + adresse_POI_HTML 
            else:
                prepa_tooltip = nom_POI_HTML + adresse_POI_HTML
                
        folium.Marker(
        location = liste_liste_lat_lon_POI[i],
        tooltip = prepa_tooltip,  
        #popup = prepa_popup,
        icon = folium.features.CustomIcon(liste_icone_POI[i], icon_size)
        ).add_to(fmap)     

    folium.Marker(
        #location=[dict_attributs_sejour['lat_centre_commune_degre'], dict_attributs_sejour['lon_centre_commune_degre']], icon=folium.Icon(color="red"), tooltip='Centre approximatif de la commune'
        #).add_to(fmap)
        location = [dict_attributs_sejour['lat_centre_commune_degre'], dict_attributs_sejour['lon_centre_commune_degre']], icon = folium.features.CustomIcon("icone_centre_commune.png", icon_size_centre_commune), tooltip = 'Centre approximatif de la commune'
        ).add_to(fmap)

   # liste des coordonnées géographiques des points de l'itinéraire à relier (via openrouteservice)
    if carte_openrouteservice:
        folium.GeoJson(route,                                                                     ## construction de l'itinéraire à afficher
                       name='Itinéraire', style_function = lambda feature:{'color': 'blue', 'weight': 3.5, 'opacity': 0.8}).add_to(fmap)
    else:
        points = liste_tuple_lat_lon_POI
        
       # liste des coordonnées géographiques des points de l'itinéraire à relier (sans openrouteservices) 
        folium.PolyLine(points, color="green", weight=3.5, opacity=0.8).add_to(fmap)  
            
    return fmap, carte_openrouteservice, pos_geo_itineraire


def affichage_POI_restaurant_carte(fmap, liste_nom_POI_resto, liste_liste_lat_lon_POI_resto, liste_icone_POI_resto, liste_description_POI_resto, liste_adresse_POI_resto):
    
    icon_size=(25, 25) 
   
    for i in range(0, len(liste_nom_POI_resto)):       
       
        nom_POI_HTML = '<center><strong><font size="3.5">' + liste_nom_POI_resto[i] + '</font></strong><br>'     
        adresse_POI_HTML = liste_adresse_POI_resto[i] + '</center>'
        
        description_POI= liste_description_POI_resto[i]
        lng_ligne = 50
        if len(description_POI) > lng_ligne:
            lignes = [(description_POI[i:i+lng_ligne]) for i in range(0, len(description_POI), lng_ligne)]
            for j, ligne in enumerate(lignes):
                if j == 0:
                    description_POI_HTML = '<br><text-align: left>' + ligne
                elif j == len(lignes):
                    description_POI_HTML += '<br>' + ligne + '</<text-align: left>'                    
                else:
                    description_POI_HTML += '<br>' + ligne
        else:       
            description_POI_HTML = '<br><text-align: left><strong>' + description_POI + '</strong></text-align: left>'
        
        ##if description_POI != 'Description longue non précisée':
        if description_POI != 'Description courte non précisée':
            prepa_tooltip = nom_POI_HTML + adresse_POI_HTML + description_POI_HTML
        else: 
            prepa_tooltip = nom_POI_HTML + adresse_POI_HTML

        folium.Marker(
        location = liste_liste_lat_lon_POI_resto[i],
        tooltip = prepa_tooltip,  
        icon = folium.features.CustomIcon(liste_icone_POI_resto[i], icon_size)
        ).add_to(fmap)     
    
    return fmap


def enrichissement_carte_interactive(dict_attributs_itineraire, df_POI_zoom_sur_centroid, dict_attributs_sejour):
    
   #  référentiel des thèmes et sous_thèmes de POI
    df_themes_POI = pd.read_csv('referentiel_themes_sous_themes.csv')

    no_centroid = dict_attributs_itineraire['no_centroid']
    lat_centroid = dict_attributs_itineraire['lat_centroid']
    lon_centroid = dict_attributs_itineraire['long_centroid']    
    
    liste_nom_POI = []
    liste_adresse_POI = []
    liste_liste_lat_lon_POI = []
    liste_liste_lon_lat_POI = []
    liste_tuple_lat_lon_POI = []
    liste_theme_POI = []
    liste_mot_cle_POI = []
    liste_icone_POI = []
    liste_description_POI = []   
    liste_URI_description_POI = []
    
    lat_POI_precedente, lon_POI_precedente = 0, 0
    longueur_itineraire = 0
    nombre_POI_iti = 0
    cumul_lat_iti = 0
    cumul_lon_iti = 0
        
    for j in range(0, len(dict_attributs_itineraire['POI_itineraire'])):
        
        nombre_POI_iti +=1          
        nom_POI = dict_attributs_itineraire['POI_itineraire'][j]                                                                              
        liste_nom_POI.append(nom_POI)                                                                     
                                                                                 
        dict_attributs_POI = recherche_attributs_POI(no_centroid, lat_centroid, lon_centroid, df_POI_zoom_sur_centroid, nom_POI, df_themes_POI)                                                           
            
        liste_adresse_POI.append(dict_attributs_POI['adresse_POI'])
            
        cumul_lat_iti += dict_attributs_POI['lat_POI']
        cumul_lon_iti += dict_attributs_POI['lon_POI']
            
        tuple_lat_lon_POI = tuple([dict_attributs_POI['lat_POI'], dict_attributs_POI['lon_POI']])
        liste_tuple_lat_lon_POI.append(tuple_lat_lon_POI)
            
        liste_temporaire = []
        liste_temporaire.append(dict_attributs_POI['lat_POI'])
        liste_temporaire.append(dict_attributs_POI['lon_POI'])
        liste_liste_lat_lon_POI.append(liste_temporaire)
            
        liste_temporaire = []
        liste_temporaire.append(dict_attributs_POI['lon_POI'])
        liste_temporaire.append(dict_attributs_POI['lat_POI'])
        liste_liste_lon_lat_POI.append(liste_temporaire)
            
        liste_theme_POI.append(dict_attributs_POI['theme_POI'])
        liste_mot_cle_POI.append(dict_attributs_POI['mot_cle_POI'])           
        liste_icone_POI.append(dict_attributs_POI['icone_POI']) 
        liste_description_POI.append(dict_attributs_POI['description_courte'])
        liste_URI_description_POI.append(dict_attributs_POI['URI_description'])
                                          
        if (lat_POI_precedente != 0) | (lon_POI_precedente != 0):
            distance_entre_2_POI = calcul_distance(lat_POI_precedente, lon_POI_precedente, dict_attributs_POI['lat_POI'], dict_attributs_POI['lon_POI'])
            longueur_itineraire += distance_entre_2_POI

        lat_POI_precedente = dict_attributs_POI['lat_POI']
        lon_POI_precedente = dict_attributs_POI['lon_POI']

   ## recherche des attributs du barycentre du POI central de l'itinéraire
    lat_POI_central_iti = cumul_lat_iti / nombre_POI_iti
    lon_POI_central_iti = cumul_lon_iti / nombre_POI_iti
    dist_centre_commune, loc_relative_centre_commune = rech_position_geographique_itineraire(lat_POI_central_iti,
                                                                                             lon_POI_central_iti,
                                                                                             dict_attributs_sejour['lat_centre_commune_degre'],
                                                                                             dict_attributs_sejour['lon_centre_commune_degre'])
    ## construction des itinéraires sur les cartes interactives
    longueur_itineraire = round(longueur_itineraire, 1)
    fmap, carte_openrouteservice, pos_geo_itineraire  = construction_itineraire_carte(no_centroid, longueur_itineraire, liste_nom_POI, liste_adresse_POI, liste_tuple_lat_lon_POI, liste_liste_lat_lon_POI, liste_liste_lon_lat_POI, liste_theme_POI, liste_mot_cle_POI, liste_icone_POI, liste_description_POI, liste_URI_description_POI, lat_POI_central_iti, lon_POI_central_iti, dist_centre_commune, loc_relative_centre_commune, dict_attributs_sejour)
    
    ## affichage des POI de type Restaurant (au sens générique)
    if dict_attributs_sejour['Restauration souhaitee'] or dict_attributs_sejour['Restauration rapide souhaitee'] or dict_attributs_sejour['Gastronomie souhaitee']:
        liste_nom_POI_resto, liste_liste_lat_lon_POI_resto, liste_theme_POI_resto, liste_mot_cle_POI_resto, liste_icone_POI_resto, liste_description_POI_resto, liste_adresse_POI_resto = recherche_attributs_POI_resto(no_centroid, df_POI_zoom_sur_centroid, lat_POI_central_iti, lon_POI_central_iti,
                                                                                                                                                                                                                        dict_attributs_sejour['Restauration souhaitee'], dict_attributs_sejour['Restauration rapide souhaitee'],
                                                                                                                                                                                                                        dict_attributs_sejour['Gastronomie souhaitee'], dict_attributs_sejour['Restauration'],
                                                                                                                                                                                                                        dict_attributs_sejour['Restauration rapide'], dict_attributs_sejour['Gastronomie'],
                                                                                                                                                                                                                        dict_attributs_sejour['Nombre max POI resto-gastro souhaite'], df_themes_POI)
        fmap = affichage_POI_restaurant_carte(fmap, liste_nom_POI_resto, liste_liste_lat_lon_POI_resto, liste_icone_POI_resto, liste_description_POI_resto, liste_adresse_POI_resto)
    else:
        liste_nom_POI_resto = []
        liste_theme_POI_resto = []
        liste_mot_cle_POI_resto = []

    return fmap, carte_openrouteservice, pos_geo_itineraire, liste_nom_POI_resto, liste_theme_POI_resto, liste_mot_cle_POI_resto

##--------------------------------------------------
## préparation du contenu de la carte interactive
##--------------------------------------------------
def StartPoint(df_POI_zoom_sur_centroid, dict_attributs_itineraire, dict_attributs_sejour):
    
    fmap, carte_openrouteservice, pos_geo_itineraire, liste_nom_POI_resto, liste_theme_POI_resto, liste_mot_cle_POI_resto = enrichissement_carte_interactive(dict_attributs_itineraire, df_POI_zoom_sur_centroid, dict_attributs_sejour)
     
    return fmap, carte_openrouteservice, pos_geo_itineraire, liste_nom_POI_resto, liste_theme_POI_resto, liste_mot_cle_POI_resto