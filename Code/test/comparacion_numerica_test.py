import sys
import os

# Agregar la carpeta raíz (GRAMATICA) al sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Ahora puedes importar la clase desde brain.py
from Code.brain import *
if __name__ == "__main__":

    nacho = Individuo("nacho")
    pablo = Individuo("pablo")
    juana = Individuo("juana")
    maria = Individuo("maria")
    Persona = Proposicion("Persona")
    Persona.elementos.add((nacho,))
    Persona.elementos.add((pablo,))
    Persona.elementos.add((juana,))
    Persona.elementos.add((maria,))

    Hombre = Proposicion("Hombre")
    Hombre.elementos.add((nacho,))
    Hombre.elementos.add((pablo,))
    Hombre.elementos.add((juana,))

    Mujer = Proposicion("Mujer") 
    Mujer.elementos.add((maria,))
    Mujer.elementos.add((juana,))

    Pareja = Proposicion("Pareja")
    Pareja.elementos.add((nacho, maria))
    Pareja.elementos.add((pablo, juana))

    edad_15 = IndividuoNumerico(15)
    edad_18 = IndividuoNumerico(18)
    edad_20 = IndividuoNumerico(20)
    edad_30 = IndividuoNumerico(30) 

    edad = Proposicion("edad")
    edad.elementos.add((nacho, edad_20))
    edad.elementos.add((pablo, edad_30))
    edad.elementos.add((juana, edad_15))    
    edad.elementos.add((maria, edad_20))

    X = Variable("X")
    Y = Variable("Y")
    Z = Variable("Z")

    condicion1 = Condicion(edad, [X,Y])
    condicionEsp = CondicionFuncion(lambda x: x.valor > 18, (Y,))
    accion = Accion("accion", [condicion1, condicionEsp])
    solucion = accion.comprobar()
    solucion.print()