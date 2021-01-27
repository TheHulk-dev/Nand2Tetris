import sys
import re
from pathlib import Path
import VMfunctions

# Récupère le nom du fichier à convertir en argv
if len(sys.argv) == 1:
    print('Syntax error : VMtranslator.py <fichier à convertir>')
    sys.exit()
else:
    p1 = Path(sys.argv[1])

if not p1.is_absolute():
    p1 = Path.cwd()/p1

# Crée le chemin du fichier .asm
p2 = p1.with_suffix('.asm')


# Code principal qui ouvre le fichier VM et écrit le fichier asm
try:
    with open(p1, 'r') as fileVM, open(p2, 'w') as fileASM:
        fileASM.write('// Traduction en assembleur du fichier ' +
                      p2.name + '\n\n')
        i = 0
        for line in fileVM:
            VMfunctions.parseur(line, fileASM, p1, i)
            i += 1

        fileASM.close()
        fileVM.close()

except FileNotFoundError as err:
    print('Fichier inconnu : '+str(err))
    sys.exit()

except IOError as err:
    print('Erreur IO : '+str(err))
    sys.exit()
