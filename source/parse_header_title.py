#/usr/bin/env python
# -*- coding:utf-8 -*-

import sqlite3
import sys, time, re

conn = sqlite3.connect("../database.db")

# Ce programme prend des paramètres : 
# - 1er = fichier avec les header des PDB
# - 2e = fichier avec les titres des PDB
# - 3e = fichier avec le nom scientifiques des organismes dont sont issus les protéines
fileheader = sys.argv[1]
filetitle = sys.argv[2]
fileorganism = sys.argv[3]

with open(fileheader, "r") as header :
	print "HEADER FILE"
	for pdb in header :
		infos = pdb.split("\t")
		head = infos[1].split(" ")
		infos = []
		for h in head :
			if h != "" and h != "\n" and h != "HEADER":
				infos.append(h)
		pdbId = infos.pop(-1)
		date =  infos.pop(-1)
		types = " ".join(infos)
		cursor = conn.execute(''' SELECT * FROM Protein WHERE pdb_id = ? ''', (pdbId,))
		if len(cursor.fetchall()) > 0 :
			conn.execute(''' UPDATE Protein SET type = ? WHERE pdb_id = ?''', (types, pdbId))
			conn.execute(''' UPDATE Protein SET date = ? WHERE pdb_id = ?''', (date, pdbId))
			conn.commit()

with open(filetitle, "r") as title : 
	print "TITLE FILE"
	for pdb in title :
		infos = pdb.split("\t")
		pdbId = infos[0].strip(":")
		titre = infos[1]
		cursor = conn.execute(''' SELECT * FROM Protein WHERE pdb_id = ? ''', (pdbId,))
		if len(cursor.fetchall()) > 0 :
			conn.execute(''' UPDATE Protein SET title = ? WHERE pdb_id = ?''', (titre, pdbId))
			conn.commit()

with open(fileorganism, "r") as organism : 
	print "ORGANISM FILE"
	for pdb in organism :
		infos = pdb.split(": ")
		pdbId = infos[0]
		orga = infos[2].replace("\n", "")
		cursor = conn.execute(''' SELECT * FROM Protein WHERE pdb_id = ? ''', (pdbId,))
		if len(cursor.fetchall()) > 0 :
			conn.execute(''' UPDATE Protein SET organism = ? WHERE pdb_id = ?''', (orga, pdbId))
			conn.commit()









