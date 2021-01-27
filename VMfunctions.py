# Définition des tableaux de constantes
TabMapping = {"local": "LCL",
              "argument": "ARG",
              "this": "THIS",
              "that": "THAT"}


def parseur(line, fileASM, p, i):
    """
    Parseur des instructions d'une ligne. Ecrit le code assembleur correspondant à une ligne dans le fichier asm. en appelant une des fonctions ci-dessus
    """
    LineAsList = line.split()
    
    if not(len(LineAsList) == 0 or LineAsList[0] == '//'):
        if LineAsList[0] == 'if-goto':
            LineAsList[0] = 'ifgoto'
        fileASM.write('// ' + line)
        eval('VM' + LineAsList[0] + '(LineAsList, fileASM, p, i)')

# Fonctions d'écriture du code asm pour les fonctions de la VM


def VMpush(ListWord, file, p, i):
    """
    Ecrit le code assembleur dans file pour la commande push
    """
    if ListWord[1] == 'constant':
        file.write('@' + ListWord[2] + '\n')
        file.write('D=A\n')
        file.write('@SP\n')
        file.write('A=M\n')
        file.write('M=D\n')
        file.write('@SP\n')
        file.write('M=M+1\n')

    elif ListWord[1] in ['local', 'argument', 'this', 'that']:
        file.write('@' + ListWord[2] + '\n')
        file.write('D=A\n')
        file.write('@' + TabMapping[ListWord[1]] + '\n')
        file.write('A=M+D\n')
        file.write('D=M\n')
        file.write('@SP\n')
        file.write('A=M\n')
        file.write('M=D\n')
        file.write('@SP\n')
        file.write('M=M+1\n')

    elif ListWord[1] == 'temp':
        file.write('@' + str(5 + int(ListWord[2])) + '\n')
        file.write('D=M\n')
        file.write('@SP\n')
        file.write('A=M\n')
        file.write('M=D\n')
        file.write('@SP\n')
        file.write('M=M+1\n')

    elif ListWord[1] == 'pointer':
        file.write('@' + str(3+int(ListWord[2])) + '\n')
        file.write('D=M\n')
        file.write('@SP\n')
        file.write('A=M\n')
        file.write('M=D\n')
        file.write('@SP\n')
        file.write('M=M+1\n')

    elif ListWord[1] == 'static':
        file.write('@' + p.stem + '.' + ListWord[2] + '\n')
        file.write('D=M\n')
        file.write('@SP\n')
        file.write('A=M\n')
        file.write('M=D\n')
        file.write('@SP\n')
        file.write('M=M+1\n')


def VMpop(ListWord, file, p, i):
    """
    Ecrit le code assembleur dans file pour la commande pop
    """
    if ListWord[1] in ['local', 'argument', 'this', 'that']:
        file.write('@' + ListWord[2] + '\n')
        file.write('D=A\n')
        file.write('@' + TabMapping[ListWord[1]] + '\n')
        file.write('D=M+D\n')
        file.write('@R13\n')
        file.write('M=D\n')
        file.write('@SP\n')
        file.write('AM=M-1\n')
        file.write('D=M\n')
        file.write('@R13\n')
        file.write('A=M\n')
        file.write('M=D\n')

    elif ListWord[1] == 'temp':
        file.write('@SP\n')
        file.write('AM=M-1\n')
        file.write('D=M\n')
        file.write('@' + str(5 + int(ListWord[2])) + '\n')
        file.write('M=D\n')

    elif ListWord[1] == 'pointer':
        file.write('@SP\n')
        file.write('AM=M-1\n')
        file.write('D=M\n')
        file.write('@' + str(3+int(ListWord[2])) + '\n')
        file.write('M=D\n')

    elif ListWord[1] == 'static':
        file.write('@SP\n')
        file.write('AM=M-1\n')
        file.write('D=M\n')
        file.write('@' + p.stem + '.' + ListWord[2] + '\n')
        file.write('M=D\n')


def VMadd(ListWord, file, p, i):
    """
    Ecrit le code assembleur dans file pour la commande add
    """
    file.write('@SP\n')
    file.write('AM=M-1\n')
    file.write('D=M\n')
    file.write('A=A-1\n')
    file.write('M=D+M\n')


def VMsub(ListWord, file, p, i):
    """
    Ecrit le code assembleur dans file pour la commande sub
    """
    file.write('@SP\n')
    file.write('AM=M-1\n')
    file.write('D=M\n')
    file.write('A=A-1\n')
    file.write('M=M-D\n')


def VMneg(ListWord, file, p, i):
    """
    Ecrit le code assembleur dans file pour la commande neg
    """
    file.write('@SP\n')
    file.write('A=M-1\n')
    file.write('M=-M\n')


def VMeq(ListWord, file, p, i):
    """
    Ecrit le code assembleur dans file pour la commande eq
    """
    file.write('@SP\n')
    file.write('AM=M-1\n')
    file.write('D=M\n')
    file.write('A=A-1\n')
    file.write('D=D-M\n')
    file.write('M=-1\n')
    file.write('@END' + str(i) + '\n')
    file.write('D; JEQ\n')
    file.write('@SP\n')
    file.write('A=M-1\n')
    file.write('M=0\n')
    file.write('(END' + str(i) + ')\n')


def VMgt(ListWord, file, p, i):
    """
    Ecrit le code assembleur dans file pour la commande gt
    """
    file.write('@SP\n')
    file.write('AM=M-1\n')
    file.write('D=M\n')
    file.write('A=A-1\n')
    file.write('D=D-M\n')
    file.write('M=-1\n')
    file.write('@END' + str(i) + '\n')
    file.write('D; JLT\n')
    file.write('@SP\n')
    file.write('A=M-1\n')
    file.write('M=0\n')
    file.write('(END' + str(i) + ')\n')


def VMlt(ListWord, file, p, i):
    """
    Ecrit le code assembleur dans file pour la commande lt
    """
    file.write('@SP\n')
    file.write('AM=M-1\n')
    file.write('D=M\n')
    file.write('A=A-1\n')
    file.write('D=D-M\n')
    file.write('M=-1\n')
    file.write('@END' + str(i) + '\n')
    file.write('D; JGT\n')
    file.write('@SP\n')
    file.write('A=M-1\n')
    file.write('M=0\n')
    file.write('(END' + str(i) + ')\n')


def VMand(ListWord, file, p, i):
    """
    Ecrit le code assembleur dans file pour la commande and
    """
    file.write('@SP\n')
    file.write('AM=M-1\n')
    file.write('D=M\n')
    file.write('A=A-1\n')
    file.write('M=D&M\n')


def VMor(ListWord, file, p, i):
    """
    Ecrit le code assembleur dans file pour la commande or
    """
    file.write('@SP\n')
    file.write('AM=M-1\n')
    file.write('D=M\n')
    file.write('A=A-1\n')
    file.write('M=D|M\n')


def VMnot(ListWord, file, p, i):
    """
    Ecrit le code assembleur dans file pour la commande not
    """
    file.write('@SP\n')
    file.write('A=M-1\n')
    file.write('M=!M\n')


def VMlabel(ListWord, file, p, i):
    """
    Ecrit le code assembleur dans file pour la commande label
    """
    file.write('(' + ListWord[1] + ')\n')


def VMgoto(ListWord, file, p, i):
    """
    Ecrit le code assembleur dans file pour la commande goto
    """
    file.write('@' + ListWord[1] + '\n')
    file.write('0; JMP\n')


def VMifgoto(ListWord, file, p, i):
    """
    Ecrit le code assembleur dans file pour la commande if-goto
    """
    file.write('@SP\n')
    file.write('AM=M-1\n')
    file.write('D=M\n')
    file.write('@' + ListWord[1] + '\n')
    file.write('D;JNE\n')
