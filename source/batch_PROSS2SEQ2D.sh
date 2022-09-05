FILES='../PDB/*pross'

for f in $FILES
do
echo $f
./extract_PROSS2SEQ2D.pl $f > $f.seq2d
done