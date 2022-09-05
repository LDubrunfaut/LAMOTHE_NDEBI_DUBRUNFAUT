FILES='PDB/*'

for f in $FILES
do
echo $f
./dssppII.pl $f > $f.dssp
done