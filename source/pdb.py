import Bio
from dssp_parse import DSSPData as dd
from Bio.PDB import PDBList


filename = "cullpdb_pc20_res1.6_R0.3_d170401_chains3057.18372.txt"
f = open(filename, 'r')
pdbcodes = []
pdbDB = {}
f.readline()
for line in f:
	pdbcodes.append(line.split()[0])
	pdbid = line.split()[0][0:4]
	pdbDB[pdbid] = {}
	pdbDB[pdbid]['id'] = pdbid
	pdbDB[pdbid]['chain'] = line.split()[0][4]
	pdbDB[pdbid]['length'] = line.split()[1]
	pdbDB[pdbid]['resolution'] = line.split()[3]

f.close()


'''Downloading structures from PDB'''
pdbl = PDBList()

for i in pdbcodes:
    pdbl.retrieve_pdb_file(i[0:4],pdir='PDB')

##### dssp parsing #####

for num, pdbid in enumerate(pdbDB):
	print str(num) + " " + pdbid
	pdb = pdbDB[pdbid]
	dssp_file_name = "PDB/pdb"+pdbid.lower()+".ent.dssp"
	dat = dd()
	dat.parseDSSP( dssp_file_name )
	chain = pdb['chain']
	indices = [i for i,c in enumerate(dat.getChain()) if c == chain]
	resnum = ""
	for i in indices:
		resnum = resnum + dat.getResnums()[i] + '-'
	pdb['resnum'] = resnum
	aa = ""
	for i in indices:
		aa = aa + dat.getAAs()[i]
	pdb['AA'] = aa
	phi = ""
	for i in indices:
		phi = phi + dat.getPHI()[i] + '/'
	pdb['PHI'] = phi
	psi = ""
	for i in indices:
		psi = psi + dat.getPSI()[i] + '/'
	pdb['PSI'] = psi
	secstruc = ""
	for i in indices:
		ss = dat.getSecStruc()[i][2]
		if ss == " ": ss = 'C'
		secstruc = secstruc + ss
	pdb['SS'] = secstruc

### write dssp.dat file ###

f = open('dssp.dat', 'w')
f.write('id\tchain\tlength\tresolution\tresnum\tAA\tSS\tPHI\tPSI\n')

for num, pdbid in enumerate(pdbDB):
	print str(num) + " " + pdbid
	pdb = pdbDB[pdbid]
	chain = pdb['chain']
	length = pdb['length']
	resolution = pdb['resolution']
	resnum = pdb['resnum']
	AA = pdb['AA']
	SS = pdb ['SS']
	PHI = pdb['PHI']
	PSI = pdb['PSI']
	f.write(pdbid+'\t'+chain+'\t'+length+'\t'+resolution+'\t'+resnum+'\t'+AA+'\t'+SS+'\t'+PHI+'\t'+PSI+'\n')

f.close()


### parse headers ###
header_f = open('headers.dat', 'w')
for num, pdbid in enumerate(pdbDB):
	print str(num) + " " + pdbid
	pdb = pdbDB[pdbid]
	pdb_file_name = "PDB/pdb"+pdbid.lower()+".ent"
	f = open(pdb_file_name, 'r')
	for line in f:
		if line.startswith('HEADER'):
			pdb['header'] = line
			break
	f.close()
	header_f.write(pdbid + ':\t' + line)

header_f.close()


#H = α-helix
#B = residue in isolated β-bridge
#E = extended strand, participates in β ladder
#G = 3-helix (310 helix)
#I = 5 helix (π-helix)
#T = hydrogen bonded turn
#S = bend
#C = coil
#P = PII