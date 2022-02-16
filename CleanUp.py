#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  1 15:03:16 2022

@author: gillesv
"""
import streamlit as st
import pandas as pd 
import re 

####### definition de la fonction ##########

#date_extraction = '05122021'
#df_product_jour= pd.read_csv('datatourisme-product-20220201.csv')
#df_tour_jour= pd.read_csv('datatourisme-tour-20220201.csv')
#df_place_jour= pd.read_csv('datatourisme-place-20220201.csv')

#liste_departements = ['01', '02', '03', '04', '05', '06', 
                     #'07', '08', '09', '10', '11', '12', '13','14', '15', '16', '17', '18', '19', '2A', '2B', '21', '22', '23', 
                     #'24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', 
                     #'42', '43', '44', '45', '46', '47', '48', '49', '51', '52', '53', '54', '55', '56', '57', '58', '59', '60', 
                      #'61', '62', '63', '64', '65', '66', '67', '68', '69', '70', '71', '72', '73', '74', '75', '76', '77', '78', 
                     #'79', '80', '81', '82', '83', '84', '85', '86', '87', '88', '89', '90', '91', '92', '93', '94' ,'95']      #listes des départements choisis, ici PACA
def cleanup ():
##-----------------------
## Lecture des fichiers
##-----------------------
    df_TOUR_POI_mots_cle = pd.read_csv("datatourisme.tour.POI_mots_cle.PACA.csv", low_memory=False)
    df_PRODUCT_POI_mots_cle = pd.read_csv("datatourisme.product.POI_mots_cle.PACA.csv", low_memory=False)
    df_PLACE_POI_mots_cle = pd.read_csv("datatourisme.place.POI_mots_cle.PACA.csv",  low_memory=False)

    df_TOUR_POI = pd.read_csv('datatourisme-tour-20220201.csv', low_memory=False)
    df_PRODUCT_POI =  pd.read_csv('datatourisme-product-20220201.csv', low_memory=False)
    df_PLACE_POI = pd.read_csv('datatourisme-place-20220201.csv', low_memory=False)
    
    df_ref_cd_postal_commune = pd.read_csv("Communes_codes_postaux.csv", sep=';', dtype='object')    
    df_ref_cd_dept_nom = pd.read_csv("Départements.csv", sep=',') 

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
         
        liste_mots_cle = re.findall(r"[#][a-z]+", categorie_URL, re.I)                 ## recherche dans l'URL Catégorie de tous les mots clé en anglais précédés du caractère '#' 
        
        for i, mot_cle in enumerate(liste_mots_cle):
            liste_mots_cle[i] = mot_cle[1:]                                            ## extraction du mot clé sans le caractère '#' 
        
        for mot_cle in liste_mots_cle:
            if mot_cle not in liste_temporaire:
                liste_temporaire.append(mot_cle)    
        
        corr_mot_cle_dans_URL = False
        for i, mot_cle_anglais in enumerate(liste_mots_cle):                           ## recherche d'une correspondance entre l'un des mots clé anglais et son équivalent français 
              for cle,valeur in dictionnaire.items():                                
                    if mot_cle_anglais == cle:                                    
                        corr_mot_cle_dans_URL = True
                        valeur_OK_dans_URL = valeur                                    ## sauvegarde de la valeur trouvée 
         
        corr_mot_cle_fin_URL = False
        for i in reversed(range(0, len(categorie_URL))):                               ## recherche d'une correspondance entre le dernier mot anglais de l'URL et son équivalent français       
            if categorie_URL[i] == '/': 
                mot_cle_anglais = categorie_URL[i+1:len(categorie_URL)]
                for cle,valeur in dictionnaire.items():                                 
                    if mot_cle_anglais == cle:
                        corr_mot_cle_fin_URL = True
                        valeur_OK_fin_URL = valeur                                     ## sauvegarde de la valeur trouvée 
                        
        if corr_mot_cle_dans_URL:                                                      ## la catégorie retenue est en priorité celle correspondant au dernier mot anglais de l'URL 
            if corr_mot_cle_fin_URL:                                                    
                return valeur_OK_fin_URL
            else:
                return valeur_OK_dans_URL
        else:
            if corr_mot_cle_fin_URL:
                return valeur_OK_fin_URL
                        
    ## Traitement spécifique de la thématique du POI présente dans le dictionnaire 'dict_xxxx_POI_corr_mot_cle_francais_thematique'
    def fct_thematique(mot_cle, dictionnaire):  
        for cle,valeur in dictionnaire.items():         
            if mot_cle == cle:
                return valeur                                                          ## retourne la thématique associée au mot clé du POI 
    
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
           
    ## Traitement de la thématique "Sport" 
    def fct_thematique_sport(x):                                                       ## les POI dont la thématique est de type "Sport" et dont le nom comporte le mot "Salle" (ou "salle")
        if x['Thématique_POI'] == 'Sport':                                             ## ne sera pas retenue car il s'agit en général de gymnases que l'on ne souhaite pas considérer comme
            r = re.compile(r"(Salle)|(salle)")                                         ## des points d'intérêt touristique  
            occurences = r.findall(x['Nom_du_POI'])
            if len(occurences) != 0:
                return False
            else:
                return True
        else:
            return True
        
    ##--------------------------------------------------------------------------
    ##--------------------------------------------------------------------------
    
    liste_temporaire = []
    
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
    
    indices_booleens = df_POI['Thématique_POI'].notnull()                                            ## identification des colonnes pour lesquelles la thématique de POI est renseignée                                                                      
    df_POI = df_POI[indices_booleens]                                                                ## réduction du dataframe aux seules lignes dont la thématique est renseignée
                                                                                                     
    ##-----------------------------------------
    ## Ajout de colonnes au dataframe df_POI
    ##-----------------------------------------
    
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
    
    ##---------------------------------------------------------------------------------
    ## Réordonnancement des colonnes / élimination des colonnes inutiles / renommage
    ##---------------------------------------------------------------------------------
    
    ## Réordonnancement des colonnes et élimination des colonnes superflues
    df_POI = df_POI[['Nom_du_POI', 'Mot_clé_POI', 'Thématique_POI', 'URI_ID_du_POI', 'Latitude', 'Longitude', 'Adresse_postale', 'Code_département', 'Nom_département',
                                   'Code_postal', 'Nom_commune', 'Nbre_habitants', 'Nbre_touristes', 'Description']]
    
    ## Renommage des colonnes
    df_POI.columns = ['Nom_du_POI', 'Mot_clé_POI', 'Thématique_POI', 'URI_ID_du_POI', 'Latitude', 'Longitude', 'Adresse_postale', 'Code_département', 'Nom_département',
                                    'Code_postal', 'Nom_commune', 'Nbre_habitants', 'Nbre_touristes', 'Description_courte']
    
    ##------------------------------------------------------
    ## Traitement des valeurs manquantes du jeu de données 
    ##------------------------------------------------------
    df_POI = df_POI.dropna(subset = ['Mot_clé_POI'], axis=0)                                                      ## élimination des lignes avec mots clé non renseignés (types POI)
    
    df_POI['Adresse_postale'] = df_POI['Adresse_postale'].fillna('Adresse non précisée')                          ## gestion des adresses non renseignées
    df_POI['URI_ID_du_POI'] = df_POI['URI_ID_du_POI'].fillna('URI ID du POI non précisée')                        ## gestion de l'URI du POI
    df_POI['Description_courte'] = df_POI['Description_courte'].fillna('Description courte non précisée')         ## gestion des descriptions courtes non renseignées
    
    ## gestion des noms de commune non renseignés
    df_temp_cd_postal_commune = pd.DataFrame(columns=['Code_postal', 'Nom_commune'])                              ## création d'un dataframe temporaire
    df_temp_cd_postal_commune['Code_postal'] = df_POI['Code_postal'][df_POI['Nom_commune'].isna()]                ## alimentation de la colonne 'Code postal' du dataframe temporaire
    
    df_temp_cd_postal_commune['Nom_commune'] = df_temp_cd_postal_commune['Code_postal'].apply(fct_nom_commune)    ## alimentation de la colonne 'Nom_commune' du dataframe temporaire
    
    df_POI['Nom_commune'] = df_POI['Nom_commune'].fillna(df_temp_cd_postal_commune['Nom_commune'])                ## remplacement des noms de commune manquants par ceux contenus dans le df temporaire  
       
    df_POI = df_POI.dropna(subset = ['Nom_commune'], axis=0)                                                      ## élimination des lignes avec noms de commune non renseignés
    
    ##-------------------------------------------------------
    ## Prise en compte des doublons et autres incohérences
    ##-------------------------------------------------------
    
    ## suppression des lignes dupliquées sur la base de noms du POI identiques 
    print('shape_1 :', df_POI.shape)
    df_POI = df_POI.drop_duplicates(subset=['Nom_du_POI'])
    print('shape_2 :', df_POI.shape)
    
    ## suppression des lignes dupliquées sur la base d'adresses identiques + codes postaux identiques
    df_POI = df_POI.drop_duplicates(subset=['Adresse_postale', 'Code_postal'])
    print('shape_3 :', df_POI.shape)
    
    ## réduction des variables flotantes Latitude et Longiture au quatre premières décimales 
    df_POI['Latitude'] = round(df_POI['Latitude'],4)
    df_POI['Longitude'] = round(df_POI['Longitude'],4)
    df_POI = df_POI.drop_duplicates(subset=['Latitude', 'Longitude'])
    print('shape_4 :', df_POI.shape)
    
    ## suppression de certains types de POI sur la base de leur mot clé
    mot_cle_a_supprimer = ['Évènement culturel',
                           'Evènement culturel',
                           'Concert',
                           'Conférence',
                           'Spectacle',
                           'Pièce de théâtre',
                           'Évènement commercial',
                           'Evènement commercial',
                           'Évènement social',
                           'Evènement social',
                           'Évènement sports et loisirs',
                           'Evènement sports et loisirs'
                           'Evènement sportif',
                           'Évènement sportif',
                           'Fête et manifestation',
                           'Cinéma']
    
    indices_booleens = ~df_POI['Mot_clé_POI'].isin(mot_cle_a_supprimer)  
    df_POI = df_POI[indices_booleens]
    print('shape_6 :', df_POI.shape)
    
    ## suppression des POI dont la thématique est de type "Sport" et dont le nom comporte le mot "salle" (ou "salle")
    indices_booleens = df_POI.apply(fct_thematique_sport, axis=1)
    df_POI = df_POI[indices_booleens]
    print('shape_7 :', df_POI.shape)
    
    ## homogéinisation de variables hétérogènes 
    #df_POI['Mot_clé_POI'][df_POI['Mot_clé_POI'] == 'Site sportif - récréatif et de loisirs'] = 'Site sportif, récréatif et de loisirs'
    df_POI.loc[lambda x: x['Mot_clé_POI'] == 'Site sportif - récréatif et de loisirs', ['Mot_clé_POI']] = 'Site sportif, récréatif et de loisirs'
    print('shape_8 :', df_POI.shape)
       
    ## Export du fichier 
    ##-----------------------
    ## export du dataframe au format *.csv (sans index)
    df_POI.to_csv('Datatourisme.csv', index = False)


st.write(cleanup())

