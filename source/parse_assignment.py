#/usr/bin/env python
# -*- coding:utf-8 -*-

import sqlite3
import sys, time

# Ce programme prend des paramètres : 
# - 1er = nom du logiciel (pross, dssp...)
# - 2e = chemin vers le fichier d'assignation

logiciel = sys.argv[1].lower()
filepath = sys.argv[2]
conn = sqlite3.connect('../database_project.db')

with open(filepath, 'r') as fichier :
	fichier.readline()
	cmb = 1
	for pdb in fichier :
		start = time.time()
		# récupération des informations sur la protéine
		infos = pdb.split("\t")
		pdbId = infos[0]
		chain = infos[1]
		size = int(infos[2])
		resolution = float(infos[3])
		resnum = infos[4].split("-")[:-1]
		sequence = infos[5]
		assignations = infos[6]
		phis = infos[7].split("/")[:-1]
		psis = infos[8].split("/")[:-1]

		print "Parsing of protein", pdbId, " numéro", cmb
		print len(resnum), len(sequence)

		# création de l'entré protéine 
		try :
				conn.execute('''INSERT INTO Protein (pdb_id, chain, sequence, size, resolution) 
								VALUES (?, ?, ?, ?, ?)''', (pdbId, chain, sequence, size, resolution))
		except :
				print pdbId, "already exists"
		conn.commit()

		# récupération de chaque informations sur les acides aminés
		for i in xrange(len(resnum)) :
			num = resnum[i]
			# Dans le cas où le numéro du résidu n'est pas indiqué
			if num != ""  and i < len(sequence):
				#print i, num
				aa = sequence[i]
				phi = float(phis[i])
				psi = float(psis[i])
				assi = assignations[i]    
				#print aa, phi, psi, assi
				cursor = conn.execute(''' SELECT pk_assignation FROM Assignation 
						                    WHERE (assignation_SS = ? and angle_phi = ? and angle_psi = ? and software = ?)''', (assi, phi, psi, logiciel))  
				resultats = cursor.fetchall()
				taille = len(resultats)

				if taille == 0 :
				    conn.execute(''' INSERT INTO Assignation (assignation_SS, angle_phi, angle_psi, software)
				    VALUES (?, ?, ?, ?)''', (assi, phi, psi, logiciel))
				    conn.commit()
				    cursor = conn.execute(''' SELECT pk_assignation FROM Assignation
				    WHERE (assignation_SS = ? and angle_phi = ? and angle_psi = ? and software = ?)''', (assi, phi, psi, logiciel))
				    fk_assi = cursor.fetchone()[0]

				elif taille == 1 :
				    fk_assi = resultats[0][0]
				else :
				    print "ERREUR : Trop de résultats trouvé pour cette assignation"

				cursor = conn.execute(''' SELECT pk_amino_acid FROM AminoAcid WHERE (fk_protein = ? AND letter = ? AND position = ?) ''', (pdbId, aa, int(num)))
				resultat = cursor.fetchall()
				pk_aa = 0

				if len(resultat) == 0 :
				    conn.execute(''' INSERT INTO AminoAcid (fk_protein, letter, position) 
				    VALUES (?, ?, ?);''', (pdbId, aa, int(num)))
				    conn.commit()
				    cursor = conn.execute(''' SELECT pk_amino_acid FROM AminoAcid WHERE (fk_protein = ? AND letter = ? AND position = ?) ''', (pdbId, aa, int(num)))
				    resultat = cursor.fetchall()

				pk_aa = resultat[0][0]  

				if logiciel == "dssp" :
				    conn.execute(''' UPDATE AminoAcid SET fk_dssp = ? WHERE pk_amino_acid = ?;''', (fk_assi, pk_aa))
				elif logiciel == "pross" :
				    conn.execute(''' UPDATE AminoAcid SET fk_pross = ? WHERE pk_amino_acid = ?;''', (fk_assi, pk_aa))
		end = time.time()
		print pdbId, "parse in", end-start
		cmb += 1
		        	
conn.close()








        
        
