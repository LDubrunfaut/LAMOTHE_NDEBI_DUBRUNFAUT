FILES='../PDB/*ent'

for f in $FILES
do
echo $f
python PROSS.py $f > $f.pross
done