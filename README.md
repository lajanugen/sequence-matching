Instructions for running code

`python find_matches.py <query string> <fasta file path> <number of flanking chars> <output file>`

Example

`python find_matches.py ctaac GCF_011064685.1_ZJU_Sfru_1.0_genomic.fna 0 output.txt`

Example output

\>NC\_049710.1 Spodoptera frugiperda isolate Faw-zju chromosome 1, ZJU\_Sfru\_1.0, whole genome shotgun sequence-3-28-+-ctaacc  
aaaccacacactaacccacccccccc  
\>NC\_049710.1 Spodoptera frugiperda isolate Faw-zju chromosome 1, ZJU\_Sfru\_1.0, whole genome shotgun sequence-28-57-+-ctaacctaac  
ccccacctaactaacctaacacctaaccta  
...
