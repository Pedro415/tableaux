#-*-coding: utf-8-*-
from random import choice
import sys

##############################################################################
# Variables globales
##############################################################################

# Crea las letras minúsculas a-z
letrasProposicionales = [chr(x) for x in range(97, 123)]
# inicializa la lista de interpretaciones
listaInterpsVerdaderas = []
# inicializa la lista de hojas
listaHojas = []
#Conectivos logicos
negacion = ['-']
conectivos_bin = ['Y', 'O', '>', '=']

##############################################################################
# Definición de objeto tree y funciones de árboles
##############################################################################

class Tree(object):
	def __init__(self, label, left, right):
		self.left = left
		self.right = right
		self.label = label

def Inorder(f):
    # Imprime una formula como cadena dada una formula como arbol
    # Input: tree, que es una formula de logica proposicional
    # Output: string de la formula
	if f.right == None:
		return f.label
	elif f.label == '-':
		return f.label + Inorder(f.right)
	else:
		return "(" + Inorder(f.left) + f.label + Inorder(f.right) + ")"

def StringtoTree(A):
    # Crea una formula como tree dada una formula como cadena escrita en notacion polaca inversa
    # Input: A, lista de caracteres con una formula escrita en notacion polaca inversa
             # letrasProposicionales, lista de letras proposicionales
    # Output: formula como tree
    Conectivos = ['O','Y','>','=']
    Pila = []
    for c in A:
        if c in letrasProposicionales:
            Pila.append(Tree(c,None,None))
        elif c=='-':
            FormulaAux = Tree(c,None,Pila[-1])
            del Pila[-1]
            Pila.append(FormulaAux)
        elif c in Conectivos:
            FormulaAux = Tree(c,Pila[-1],Pila[-2])
            del Pila[-1]
            del Pila[-1]
            Pila.append(FormulaAux)
        else:
            print(u"Hay un problema: el símbolo {0} no se reconoce".format(c))
    return Pila[-1]

def Inorder2Tree(inorder):
    if len(inorder) == 1:
        return Tree(inorder[0], None, None)
    elif inorder[0] in negacion:
        return Tree(inorder[0], None, Inorder2Tree(inorder[1:]))
    elif inorder[0] == "(":
        counter = 0                     #Contador de parentesis
        for i in range(1, len(inorder)):
            if inorder[i] == "(":
                counter += 1
            elif inorder[i] == ")":
                counter -=1
            elif inorder[i] in conectivos_bin and counter == 0:
                return Tree(inorder[i], Inorder2Tree(inorder[1:i]), Inorder2Tree(inorder[i + 1:-1]))
    else:
        return -1

##############################################################################
# Definición de funciones de tableaux
##############################################################################

def imprime_hoja(H):
	cadena = "{"
	primero = True
	for f in H:
		if primero == True:
			primero = False
		else:
			cadena += ", "
		cadena += Inorder(f)
	return cadena + "}"

def complemento(f):
    #Esta función retorna el complemento de una formula
    #Input: f, literal como arbol
    #Output: complemento del literal
    if f.label == "-":
        return f.right
    elif es_literal(f):
        return Tree("-", None, f)
    else:
        print("Arbol invalido")
        sys.exit(1)

def par_complementario(l):
	# Esta función determina si una lista de solo literales
	# contiene un par complementario
	# Input: l, una lista de literales
	# Output: True/False
    comp = []
    for i in l:
        inord = Inorder(i)
        for j in comp:
            if inord == Inorder(j):
                return True
        comp.append(complemento(i))
    return False

def es_literal(f):
	# Esta función determina si el árbol f es un literal
	# Input: f, una fórmula como árbol
	# Output: True/False
    if f.label in letrasProposicionales:
        return True
    elif f.label == "-":
        return f.right.label in letrasProposicionales
    return False

def no_literales(l):
	# Esta función determina si una lista de fórmulas contiene
	# solo literales
	# Input: l, una lista de fórmulas como árboles
	# Output: None/f, tal que f no es literal
    for i in l:
        if not es_literal(i):
            return False
    return True

def clasifica(f):
    #Recibe una formula y la clasifica como alfa o beta
    #Input: f, una formula como arbol
    #Output: string "Nalfa" o "Nbeta", con N entre 1 y 4 para alfa y 1 y 3 para beta
    if f.label == "-":
        if f.right.label == "-":
            return "1alfa"
        elif f.right.label == "O":
            return "3alfa"
        elif f.right.label == ">":
            return "4alfa"
        elif f.right.label == "Y":
            return "1beta"
    if f.label == "Y":
        return "2alfa"
    if f.label == "O":
        return "2beta"
    if f.label == ">":
        return "3beta"
    print("Error en la clasificacion")
    sys.exit(1)

def clasifica_y_extiende(f, h):
	# Extiende listaHojas de acuerdo a la regla respectiva
	# Input: f, una fórmula como árbol
	# 		 h, una hoja (lista de fórmulas como árboles)
	# Output: no tiene output, pues modifica la variable global listaHojas

    global listaHojas
    
    print("Formula:", Inorder(f))
    print("Hoja:", imprime_hoja(h))

    assert(f in h), "La formula no esta en la lista!"

    clase = clasifica(f)
    print("Clasificada como:", clase)
    assert(clase != None), "Formula incorrecta " + imprime_hoja(h)

    if clase == '1alfa':
        aux = [x for x in h]
        listaHojas.remove(h)
        aux.remove(f)
        aux += [f.right.right]
        listaHojas.append(aux)
    # Aqui el resto de casos
    elif clase == "2alfa":
        aux = [x for x in h]
        listaHojas.remove(h)
        aux.remove(f)
        aux += [f.left, f.right]
        listaHojas.append(aux)
    elif clase == "3alfa":
        aux = [x for x in h]
        listaHojas.remove(h)
        aux.remove(f)
        aux += [Tree("-", None, f.right.left), Tree("-", None, f.right.right)]
        listaHojas.append(aux)
    elif clase == "4alfa":
        aux = [x for x in h]
        listaHojas.remove(h)
        aux.remove(f)
        aux += [f.right.left, Tree("-", None, f.right.right)]
        listaHojas.append(aux)
    elif clase == "1beta":
        aux1 = [x for x in h]
        aux2 = [x for x in h]
        listaHojas.remove(h)
        aux1.remove(f)
        aux2.remove(f)
        aux1 += [Tree("-", None, f.right.left)]
        listaHojas.append(aux1)
        aux2 += [Tree("-", None, f.right.right)]
        listaHojas.append(aux2)
    elif clase == "2beta":
        aux1 = [x for x in h]
        aux2 = [x for x in h]
        listaHojas.remove(h)
        aux1.remove(f)
        aux2.remove(f)
        aux1 += [f.left]
        listaHojas.append(aux1)
        aux2 += [f.right]
        listaHojas.append(aux2)
    elif clase == "3beta":
        aux1 = [x for x in h]
        aux2 = [x for x in h]
        listaHojas.remove(h)
        aux1.remove(f)
        aux2.remove(f)
        aux1 += [Tree("-", None, f.left)]
        listaHojas.append(aux1)
        aux2 += [f.right]
        listaHojas.append(aux2)
        
def Tableaux(f):
	# Algoritmo de creacion de tableau a partir de lista_hojas
	# Imput: - f, una fórmula como string en notación polaca inversa
	# Output: interpretaciones: lista de listas de literales que hacen
	#		 verdadera a f
    global listaHojas
    global listaInterpsVerdaderas
    
    try:
        listaHojas = [[StringtoTree(f)]]
    except:
        listaHojas = [[Inorder2Tree(f)]]
    

    run = True
    while run:
        run = False
        for i in listaHojas:
            if not no_literales(i):
                run = True
                print()
                for j in i:
                    if not es_literal(j):
                        clasifica_y_extiende(j, i)
                    break
    for i in listaHojas:
        if not par_complementario(i):
            return "abierto"
    return "cerrado"
                        
def imprime_listaHojas(l):
    for i in l:
        print(imprime_hoja(i), end = "")
    print()


l = "-(-pYq)"
print(Tableaux(l))
imprime_listaHojas(listaHojas)
