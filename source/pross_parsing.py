import Bio
from Bio.PDB import PDBList


filename = "../cullpdb_pc20_res1.6_R0.3_d170401_chains3057.18372.txt"
f = open(filename, 'r')
pdbcodes = []
pdbDB = {}
f.readline()
for line in f:
	print line
	pdbcodes.append(line.split()[0])
	pdbid = line.split()[0][0:4]
	pdbDB[pdbid] = {}
	pdbDB[pdbid]['id'] = pdbid
	pdbDB[pdbid]['chain'] = line.split()[0][4]
	pdbDB[pdbid]['length'] = line.split()[1]
	pdbDB[pdbid]['resolution'] = line.split()[3]

f.close()

### convert to one letter code ###

d = {'CYS': 'C', 'ASP': 'D', 'SER': 'S', 'GLN': 'Q', 'LYS': 'K',
     'ILE': 'I', 'PRO': 'P', 'THR': 'T', 'PHE': 'F', 'ASN': 'N', 
     'GLY': 'G', 'HIS': 'H', 'LEU': 'L', 'ARG': 'R', 'TRP': 'W', 
     'ALA': 'A', 'VAL': 'V', 'GLU': 'E', 'TYR': 'Y', 'MET': 'M',
     'SEC': 'U', 'UNK': 'X', 'XAA': 'X', 'PYL': 'O'}

def shorten(x):
    if len(x) % 3 != 0: 
        raise ValueError('Input length should be a multiple of three')
    y = ''
    for i in range(len(x)/3):
        y += d[x[3*i:3*i+3]]
    return y


### PROSS parser ###


def prossParser(filename, pdb_dic):
	read_chain = 0
	resnum = ""
	aa = ""
	phi = ""
	psi = ""
	secstruc = ""
	f = open(filename, 'r')
	for line in f:
		fields = line.split()
		if len(fields) == 2 and fields[1] == pdb_dic['chain']:
			read_chain = 1
		if len(fields) == 2 and fields[1] != pdb_dic['chain']:
			read_chain = 0
		if len(fields) == 11 and read_chain == 1:
			resnum = resnum + fields[0] + '-'
			aa = aa + shorten(fields[1])
			phi = phi + fields[4] + '/'
			psi = psi + fields[5] + '/'
			secstruc = secstruc + fields[2]
	f.close()
	pdb_dic['resnum'] = resnum 
	pdb_dic['AA'] = aa
	pdb_dic['PHI'] = phi
	pdb_dic['PSI'] = psi
	pdb_dic['SS'] = secstruc
	return pdb_dic


### batch PROSS parsing ###

for num, pdbid in enumerate(pdbDB):
	print str(num) + " " + pdbid
	pdb = pdbDB[pdbid]
	pross_file_name = "../PDB/pdb"+pdbid.lower()+".ent.pross"
	pdb = prossParser(pross_file_name, pdb)

### write dssp.dat file ###

f = open('pross.dat', 'w')
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




