
class Categoria:
    def __init__(self, nombre):
        self.nombre = nombre
        self.atributos = [] #De momento ignoramos los atributos
        #self.padre = None

        

class AtributoCategoria:
    def __init__(self, nombre):
        self.nombre = nombre


class Proposicion:
    #Falta atributo single
    def __init__(self,nombre,numero_parametros):
        self.elementos = set()
        self.nombre = nombre
        self.numero_parametros = numero_parametros
    def add(self,elemento):
        if not(isinstance(elemento, tuple)) and len(elemento) != self.numero_parametros:
        
            raise ValueError("Elemento debe ser una tupla con el mismo número de elementos que los parámetros")
        #faltaria validar tipos
        self.elementos.add(elemento)
    def check(self, elemento):
        #Comprueba que dentro del conjunto de elementos se encuentra el elemento
        return elemento in self.elementos
        
class ParametrosProposicion:
    def __init__(self, nombre, tipo=None):
        self.nombre = nombre
        self.tipo = tipo


class Brain:
    def __init__(self):
        self.categorias = {}
        self.proposiciones = {}
        self.indiviuos = {}

    def add_categoria(self, nombre):#atributos es una lista de tupla (nombre, tipo),de momento ignoramos los atributos
        categoria = Categoria(nombre)
        self.categorias[nombre] = categoria
        #crea una proposicion con el mismo nombre de la categoria
        self.add_proposicion(nombre, 1)
        
    def get_categoria(self, nombre):
        return self.categorias[nombre]
        
    def add_proposicion(self, nombre, numero_parametros):
        proposicion = Proposicion(nombre, numero_parametros)
        self.proposiciones[nombre] = proposicion
    def get_proposicion(self, nombre):
        return self.proposiciones[nombre]
    

    

    def add_individuo(self, nombre_individuo, categoria):
        if not isinstance(nombre_individuo, str):
            raise ValueError("Individuo debe ser de tipo string")
        categoria = self.get_categoria(categoria)
        proposicion = self.get_proposicion(categoria.nombre)
        proposicion.add((nombre_individuo,))
        #habria que comprobar que la categoria no tiene un padre y si lo tiene añadirlo a la proposicion del padre recursivamente
        #falta añadir los atributos
    def check_proposicion(self, nombre, elemento):
        proposicion = self.get_proposicion(nombre)
        #comprobar que el elemento es una tupla con el mismo número de elementos que la proposicion
        if not isinstance(elemento, tuple) and len(elemento) != proposicion.numero_parametros:
            raise ValueError("Elemento debe ser una tupla con el mismo número de elementos que los parámetros")
        return proposicion.check(elemento)
        
        
if __name__ == "__main__":
    brain = Brain()
    brain.add_categoria("Persona")
    brain.add_individuo("Nacho", "Persona")
    print()
    print("Nacho es una persona?", brain.check_proposicion("Persona", ("Nacho",)))
    brain.add_categoria("Estudios")
    brain.add_individuo("Nacho", "Estudios")
    brain.add_proposicion("estudia", 2)
    prop =brain.get_proposicion("estudia")
    prop.add(("Nacho", "Informatica"))
    print("Nacho estudia informatica?", brain.get_proposicion("estudia").check(("Nacho", "Informatica")))


