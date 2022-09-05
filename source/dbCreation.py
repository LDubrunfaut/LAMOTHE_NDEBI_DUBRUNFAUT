#/usr/bin/env python
# -*- coding:utf-8 -*-

import sqlite3

# se connecte à la db, en créer une si non eexistante
conn = sqlite3.connect('../database_project.db')

try :
    conn.execute(''' DROP TABLE Protein;''')
except :
    print "Table Protein does not exist yet" 

conn.execute('''CREATE TABLE Protein
                    (pdb_id CHAR(4) PRIMARY KEY NOT NULL,
                    chain CHAR(2) NOT NULL,
                    sequence TEXT NOT NULL,
                    size INTEGER NOT NULL,
                    resolution FLOAT NOT NULL,
                    type TEXT,
                    organism TEXT,
                    title TEXT,
                    date TEXT);''')
print "Table Protein created"

try :
    conn.execute(''' DROP TABLE Assignation;''')
except :
    print "Table Assignation does not exist yet" 
conn.execute('''CREATE TABLE Assignation
                    (pk_assignation INTEGER PRIMARY KEY NOT NULL,
                    assignation_SS char(1) NOT NULL,
                    angle_phi FLOAT NOT NULL,
                    angle_psi FLOAT NOT NULL,
                    software TEXT NOT NULL);''')
print "Table Assignation created"

try :
    conn.execute(''' DROP TABLE AminoAcid;''')
except :
    print "Table AminoAcid does not exist yet" 
conn.execute('''CREATE TABLE AminoAcid
                    (pk_amino_acid INTEGER PRIMARY KEY NOT NULL,
                    fk_protein INTEGER, 
                    letter CHAR(2) NOT NULL,
                    position INTEGER NOT NULL,
                    fk_dssp INTEGER,
                    fk_pross INTEGER,
                    FOREIGN KEY(fk_dssp) REFERENCES Assignation(pk_assignation),
                    FOREIGN KEY(fk_pross) REFERENCES Assignation(pk_assignation),
                    FOREIGN KEY(fk_protein) REFERENCES Pdb(pk_protein));''')
print "Table AminoAcid created"
conn.commit()

