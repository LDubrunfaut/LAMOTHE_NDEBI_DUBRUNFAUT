filename = "cullpdb_pc20_res1.6_R0.3_d170401_chains3057.18372.txt"
f = open(filename, 'r')
pdbcodes = []
pdbDB = {}
f.readline()
for line in f:
	pdbcodes.append(line.split()[0][0:4])

f.close()


# parse pdb for title
title_f = open('titles.dat', 'w')
for num, pdbid in enumerate(pdbcodes):
	firstline=0
	title = []
	print str(num) + " " + pdbid
	pdb_file_name = "PDB/pdb"+pdbid.lower()+".ent"
	f = open(pdb_file_name, 'r')
	for line in f:
		if line.startswith('TITLE') and firstline == 0:
			fields = line.split()
			title.extend(fields[1:len(fields)])
			firstline=1
		if line.startswith('TITLE') and firstline == 1:
			fields = line.split()
			title.extend(fields[2:len(fields)])
	f.close()
	title_f.write(pdbid + ':\t')
	for word in title:
		title_f.write(word + ' ')
	title_f.write('\n')

title_f.close()

# parse pdb for scientific organism

sc_orga_f = open('scientific_organism.dat', 'w')
for num, pdbid in enumerate(pdbcodes):
	firstline=0
	print str(num) + " " + pdbid
	pdb_file_name = "PDB/pdb"+pdbid.lower()+".ent"
	f = open(pdb_file_name, 'r')
	found = 0
	for line in f:
		pos = line.find("ORGANISM_SCIENTIFIC")
		if pos != -1:
			found = 1
			if line.strip().endswith(';'):
				orga = line.strip()[pos:-1]
			else:
				orga = line.strip()[pos:len(line.strip())]
			break
	if found == 0:
		orga = 'ORGANISM_SCIENTIFIC: none'
	f.close()
	sc_orga_f.write(pdbid+': '+orga+'\n')

sc_orga_f.close()

# parse pdb for scientific organism

com_orga_f = open('common_organism.dat', 'w')
for num, pdbid in enumerate(pdbcodes):
	firstline=0
	print str(num) + " " + pdbid
	pdb_file_name = "PDB/pdb"+pdbid.lower()+".ent"
	f = open(pdb_file_name, 'r')
	found = 0
	for line in f:
		pos = line.find("ORGANISM_COMMON")
		if pos != -1:
			found = 1
			if line.strip().endswith(';'):
				orga = line.strip()[pos:-1]
			else:
				orga = line.strip()[pos:len(line.strip())]
			break
	if found == 0:
		orga = 'ORGANISM_COMMON: none'
	f.close()
	com_orga_f.write(pdbid+': '+orga+'\n')

com_orga_f.close()



