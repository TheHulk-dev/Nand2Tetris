import sys
import re
from pathlib import Path

# Définition des tableaux de constantes
compDict = {
    "0": "0101010",
    "1": "0111111",
    "-1": "0111010",
    "D": "0001100",
    "A": "0110000",
    "!D": "0001101",
    "!A": "0110001",
    "-D": "0001111",
    "-A": "0110011",
    "D+1": "0011111",
    "A+1": "0110111",
    "D-1": "0001110",
    "A-1": "0110010",
    "D+A": "0000010",
    "D-A": "0010011",
    "A-D": "0000111",
    "D&A": "0000000",
    "D|A": "0010101",
    "M": "1110000",
    "!M": "1110001",
    "M+1": "1110111",
    "M-1": "1110010",
    "D+M": "1000010",
    "D-M": "1010011",
    "M-D": "1000111",
    "D&M": "1000000",
    "D|M": "1010101"
}

destDict = {
    "null": "000",
    "M": "001",
    "D": "010",
    "MD": "011",
    "A": "100",
    "AM": "101",
    "AD": "110",
    "AMD": "111"
}

jumpDict = {
    "null": "000",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111"
}

symbolTable = {
    "R0": "0",
    "R1": "1",
    "R2": "2",
    "R3": "3",
    "R4": "4",
    "R5": "5",
    "R6": "6",
    "R7": "7",
    "R8": "8",
    "R9": "9",
    "R10": "10",
    "R11": "11",
    "R12": "12",
    "R13": "13",
    "R14": "14",
    "R15": "15",
    "SCREEN": "16384",
    "KBD": "24576",
    "SP": "0",
    "LCL": "1",
    "ARG": "2",
    "THIS": "3",
    "THAT": "4"
}

# Récupère le nom du fichier à convertir en argv
if len(sys.argv) == 1:
    print('Syntax error : Assembler.py <fichier à convertir>')
    sys.exit()
else:
    p1 = Path(sys.argv[1])

if not p1.is_absolute():
    p1 = Path.cwd()/p1

# Crée le fichier .asm2 sans les commentaires et les espaces
p2 = p1.with_suffix('.asm2')

# Crée le fichier .asm3 sans les symboles de boucle
p3 = p1.with_suffix('.asm3')

# Crée le fichier .asm4 sans les symboles de variable
p4 = p1.with_suffix('.asm4')

# Crée le fichier .hack
p5 = p1.with_suffix('.hack')

# Expressions régulières pour supprimer les commentaires et les espaces
noComment = re.compile(r'//.*')
noSpace = re.compile(r'\s')

# Suppression des commentaires et espaces (asm->asm2)
try:
    with open(p1, 'r') as file2Convert, open(p2, 'w') as fileTrimed:
        for line in file2Convert:
            newLine = noSpace.sub('', noComment.sub('', line))
            if newLine != '':
                fileTrimed.write(newLine+'\n')
        fileTrimed.close()
        file2Convert.close()

except FileNotFoundError as err:
    print('Fichier inconnu : '+str(err))
    sys.exit()

except IOError as err:
    print('Erreur IO : '+str(err))
    sys.exit()

# Suppression des symboles de boucle (asm2->asm3)
try:
    with open(p2, 'r') as fileSansCommentaire, open(p3, 'w') as fileSansBoucle:
        i = 0
        for line in fileSansCommentaire:
            if line[0] == '(':
                nomBoucle = line[1:-2]
                symbolTable[nomBoucle] = str(i)
            else:
                fileSansBoucle.write(line)
                i += 1
        fileSansCommentaire.close()
        fileSansBoucle.close()

except FileNotFoundError as err:
    print('Fichier inconnu : '+str(err))
    sys.exit()

except IOError as err:
    print('Erreur IO : '+str(err))
    sys.exit()


# Suppression des symboles de variable (asm3->asm4)
try:
    with open(p3, 'r') as fileSansBoucle, open(p4, 'w') as fileSansSymbole:
        j = 16
        for line in fileSansBoucle:
            if line[0] == '@':
                if line[1:-1].isnumeric():
                    fileSansSymbole.write(line)
                else:
                    if line[1:-1] in symbolTable:
                        fileSansSymbole.write('@'+symbolTable[line[1:-1]]+'\n')
                    else:
                        symbolTable[line[1:-1]] = str(j)
                        fileSansSymbole.write('@'+symbolTable[line[1:-1]]+'\n')
                        j += 1
            else:
                fileSansSymbole.write(line)
        fileSansBoucle.close()
        fileSansSymbole.close()

except FileNotFoundError as err:
    print('Fichier inconnu : '+str(err))
    sys.exit()

except IOError as err:
    print('Erreur IO : '+str(err))
    sys.exit()

# Expressions régulières pour parser les instructions C
destRegex = re.compile(r'(^.{1,3}?)=')
compRegex = re.compile(r'')
jumpRegex = re.compile(r';(.{3}$)')


def parseurA(instruction, file01):
    """
    Parseur d'instructions A
    """
    instruction01 = format(int(instruction[1:]), '016b')
    file01.write(instruction01+'\n')


def parseurC(instruction, file01):
    """
    Parseur d'instructions C
    """
    resultRegexDest = destRegex.search(instruction)
    resultRegexJump = jumpRegex.search(instruction)

    comp = jumpRegex.sub('', destRegex.sub('', instruction))[:-1]
    instruction01 = '111'+compDict[comp]

    if resultRegexDest == None:
        dest = 'null'
    else:
        dest = resultRegexDest.group(1)
    instruction01 += destDict[dest]

    if resultRegexJump == None:
        jump = 'null'
    else:
        jump = resultRegexJump.group(1)
    instruction01 += jumpDict[jump]

    file01.write(instruction01+'\n')


# Transformation du fichier sans symbole en 0 et 1 (asm4->hack)
try:
    with open(p4, 'r') as fileTrimed, open(p5, 'w') as fileHack:
        for line in fileTrimed:
            if line[0] == '@':
                parseurA(line, fileHack)
            else:
                parseurC(line, fileHack)
        fileTrimed.close()
        fileHack.close()

except FileNotFoundError as err:
    print('Fichier inconnu : '+str(err))
    sys.exit()

except IOError as err:
    print('Erreur IO : '+str(err))
    sys.exit()

p2.unlink()
p3.unlink()
p4.unlink()
