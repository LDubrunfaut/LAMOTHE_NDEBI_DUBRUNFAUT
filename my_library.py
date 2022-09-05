#!/usr/bin/env python
# -*- coding:utf-8 -*-
################################################################################
import sqlite3
import os
import random
import re
from flask import Flask, request, flash, redirect, url_for, render_template
################################################################################
COLORS =[]
################################################################################
# Fonction permettant de convertir de vérifier si une string est au format PDB
# Soit 4 caractères composés de chiffres et de lettres
def isPDB(s):
    '''
        Fonction permettant de vérifier si une chaîne de caractères ne contient
        que des caractères alphanumériques et a exactement 4 caractères

        Args : s : Chaîne de caractères à vérifier

        Returns : True si vrai et False sinon.
    '''
    if s.isalnum():
        if(len(s) * s[0]==4):
            return True;
        else :
            False;
    else :
        return False;

# Fonction permettant de nettoyer les valeurs métriques pour n'avoir que des
# entiers ou des floats
def clean_num(kw):
    '''
        Fonction permettant à partir d'une chaîne de caractère d'isoler les
        nombres.

        Args : kw : Chaîne de caractères ne contenant à priori que des valeurs
        numériques.

        Returns : keywords : Liste des mots ayant été conservés.

    '''
    num = re.compile('^[0-9]*[,.]?[0-9]*$')
    res = num.search(kw)
    if res != None :
        return kw
    else :
        return ""

# Fonction permettant de nettoyer les mots clés.
def clean_kw(kw):
    '''
        Fonction permettant à partir d'une chaîne de caractère d'isoler les mots
        en considérant les ";" et espaces comme séparateurs de mots clés.
        Ensuite ne conserve que les mots comportant descaractères
        alphanumériques et des "-".

        Args : kw : Chaîne de caractères contenant un ou plusieurs mots

        Returns : keywords : Liste des mots ayant été conservés.

    '''
    keywords = []
    kw=kw.replace("\n"," ")
    kw=kw.replace("\r"," ")
    kw=kw.replace("\t"," ")
    liste_key=kw.split()
    # alphanum = re.compile('^[a-zA-Z0-9][ A-Za-z0-9_-]*$')
    for word in liste_key :
        # Ne veut conserver que des termes alphanumériques
        res = isPDB(word)
        if res != False :
            keywords.append(word.upper())

    return keywords

# Fonction permettant d'afficher les informations associées à un PDB de la DB
def showpdb(cursor_object,liste):
    '''
        Fonction permettant de récupérer dans une liste de dictionnaires, les
        informations du PDB ou des PDB contenus dans la liste passée en
        argument.

        Args :
            cursor_object : objet de type cursor object contenant le ou les
                            résultat(s) d'une requête sql.
            liste : Chaîne de caractère qui vaut 'liste' dans le cas où l'objet
                    cursor contient plusieurs lignes de résultat.

        Returns : pdb : Liste des dictionnaires correspondants à l'ensemble
                          des informations de chaque pdb

    '''
    conn = sqlite3.connect('database.db')
    if liste=='liste':
        cursor_object=[cursor_object]
    pdb = {}
    for row in cursor_object:
        pdb['pdb_id'] = row[0]
        pdb['chain']=row[1]
        pdb['sequence']=row[2]
        pdb['length']=row[3]
        pdb['resolution']=row[4]
        pdb['type']=row[5]
        pdb['organism']=row[6]

    # On veut l'ensemble des assignation_SS pour la Protein
    cursor = conn.execute(''' SELECT assignation_SS FROM Assignation, AminoAcid WHERE (fk_protein = ? AND assignation_SS = "P" AND fk_dssp = pk_assignation)''',(pdb['pdb_id'],));

    flag=0
    for row in cursor:
        flag=flag+1

    pdb['dssp_ppi_n']=flag
    pdb['dssp_ppi_p']=pdb['dssp_ppi_n']*100/pdb['length']
    pdb['dssp_ppi_p']=round(pdb['dssp_ppi_p'],2)
    conn.commit()

    cursor = conn.execute(''' SELECT assignation_SS FROM Assignation, AminoAcid WHERE (fk_protein = ? AND assignation_SS = "P" AND fk_pross = pk_assignation )''',(pdb['pdb_id'],));

    flag=0
    for row in cursor:
        flag=flag+1

    pdb['pross_ppi_n']=flag/2
    pdb['pross_ppi_p']=pdb['pross_ppi_n']*100/pdb['length']
    pdb['pross_ppi_p']=round(pdb['pross_ppi_p'],2)
    conn.commit()
    conn.close()
    return pdb

# Fonction permettant de faire une recherche de type and
def andsearch(keys_s):
    '''
        Fonction de réaliser une recherche des mots clés avec l'option and, soit
        rechercher pour l'ensemble des mots clés saisis les pdb qui ont
        exactement tous les mots clés entrés.

        Args :
            keys_s : Chaîne de caractères contenant un ou plusieurs mots
        Returns :
            liste_id_ok : Liste contenant l'ensemble des id pdb qui ont
                          exactement tous les mots clés de keys_s

    '''
    # Le nombre de mots qui doivent matcher
    score=len(keys_s)
    liste_match=[]
    id_connu=[0]
    conn = sqlite3.connect('database.db')
    # Pour chaque mot clé les pdb avec lesquelles il match
    for word in keys_s :
        # Dans ce cas on ne veut pas de doublon mais seulement au sein d'une
        # meme requete mot
        no_doublon=[0]
        cursor = conn.execute('''SELECT pdb_id from Protein WHERE type LIKE ?
        ''',("%"+word+"%",));
        for row in cursor:
            # On supprime les possibles doublons dans la recherche
            if row[0] not in no_doublon :
                no_doublon.append(row[0])
                # Si c'est la première fois qu'on rencontre cette ID pdb
                if row[0] not in id_connu :
                    match_id={}
                    match_id['id']=row[0]
                    match_id['score']=1
                    liste_match.append(match_id)
                    id_connu.append(row[0])
                # Si on connait déjà cet ID pdb
                else :
                    for dico in liste_match:
                        if dico['id'] == row[0] :
                            dico['score'] = dico['score'] +1
                            break
        conn.commit()
    # On a regardé pour tous les mots clés, on regarde maintenant combien
    #de pdb ont eu le score attendu pour avoir matché avec toutes les valeurs
    liste_id_ok = []
    for dico in liste_match:
        if dico['score'] == score :
            liste_id_ok.append(dico['id'])
    conn.close()
    return liste_id_ok
