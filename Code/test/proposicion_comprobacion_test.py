import sys
import os

# Agregar la carpeta raíz (GRAMATICA) al sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Ahora puedes importar la clase desde brain.py
from Code.brain import *

if __name__ == "__main__":
    X = Variable("X")
    Y = Variable("Y")
    Z = Variable("Z")
    ind_1 = Individuo("ind_1")
    ind_2 = Individuo("ind_2")
    ind_3 = Individuo("ind_3")
    Persona = Proposicion("proposicion")
    Persona.elementos.add((ind_1, ind_2))
    Persona.elementos.add((ind_1, ind_1))
    Persona.elementos.add((ind_1, ind_3))
    Persona.elementos.add((ind_2, ind_3))
    #print(proposicion.elementos)

    solucion_inicial = SolucionParcial([Y])
    solucion_inicial.add_elemento((ind_1,))
    solucion_inicial.add_elemento((ind_3,))
    solucion_final=Persona.comprobar(solucion_inicial, [X,Y])
    solucion_final.print()
