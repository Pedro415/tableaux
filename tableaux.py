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

	# OJO: DEBE INCLUIR SU CÓDIGO DE STRING2TREE EN ESTA PARTE!!!!!

	p = letrasProposicionales[0] # ELIMINE ESTA LINEA LUEGO DE INCLUIR EL CODIGO DE STRING2TREE
	return Tree(p, None, None) # ELIMINE ESTA LINEA LUEGO DE INCLUIR EL CODIGO DE STRING2TREE

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
	return False

def no_literales(l):
	# Esta función determina si una lista de fórmulas contiene
	# solo literales
	# Input: l, una lista de fórmulas como árboles
	# Output: None/f, tal que f no es literal
	return False

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

def clasifica_y_extiende(f):
	# clasifica una fórmula como alfa o beta y extiende listaHojas
	# de acuerdo a la regla respectiva
	# Input: f, una fórmula como árbol
	# Output: no tiene output, pues modifica la variable global listaHojas
	global listaHojas

def Tableaux(f):

	# Algoritmo de creacion de tableau a partir de lista_hojas
	# Imput: - f, una fórmula como string en notación polaca inversa
	# Output: interpretaciones: lista de listas de literales que hacen
	#		 verdadera a f
	global listaHojas
	global listaInterpsVerdaderas

	#A = string2Tree(f)
	#listaHojas = [[A]]

	return listaInterpsVerdaderas

print(clasifica(Tree('-',None,Tree('Y',Tree('-',None,Tree('a',None,None)),Tree('-',None,Tree('b',None,None))))))