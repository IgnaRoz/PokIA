'''
IMPORTANTE:
    -Eliminar la clase parametroCondicion y todas sus referencias, se va a sustituir por un nuevo tipo de condicion

Cosas por hacer:
    -Categorias y atributos
        -(hecho)Cuando se cre una categoria, se crea una proposicion con el mismo nombre
        -(hecho)Algun nuevo tipo de parametro o funcion para poder usar los atributos en las proposiciones
            -Se ha solucionado creando un nuevo tipo de condicion que acepta funciones y parametros
        -(hecho)Los individuos deberian almacenar las categorias a la que pertenecen
        -(hecho)Se tiene que tener en cuenta que una categoria puede heredar de otra
    -Proposiciones
        -Pensar como se podria añadir un not o un or
        -Negaciones de las proposiciones en las condiciones
        -(hecho)Deben de poder ejecutar consecuencias de las acciones
            -Se hacen desde la accion
        -Cuando se crea una proposicion, se deberia crear una accion del tipo consecuencia que pueda ejecutarse o es tarea de la accion saber que hacer cuando tiene una proposicion en la seccion de consecuencias?
    -Acciones
        -(hecho)Consecuencia de las acciones
        -(hechoComo diferencio una "asginacion" de una "eliminacion" de una proposicion en la seccion de consecuencias???
            -Las consecuencias tienen diferentes tippos, cada uno con su propio metodo ejecutar
        -Pensar como seria las acciones del tipo consecuencia(definidas) y contingencias
        -(hecho)Pensar como trabajar con parametros numericos
            -Se ha creado un nuevo tipo de individuo que acepta un valor numerico, este valor se puede comparar con otros valores numericos dentro de un nuevo tipo de condicion llamada CondicionFuncion
        -Pensar en las consecuencias tipo jugador_rival(rival).vida++
            -Puede que creando una consecuencia definida con la condicion jugador_rival(rival) y la consecuencia rival.vida++
            -Mejor: Se mete jugador_rival(rival) como condicion y ya se tiene la variable rival para poder hacer rival.vida ++

'''
import inspect

class Brain:

    def __init__(self):
            self.categorias = {}
            self.proposiciones = {}
            self.indiviuos = {}
            self.acciones = {}
    def add_categoria(self, nombre,atributos = None ,padre = None):
        categoria = Categoria(nombre,atributos,padre)
        self.categorias[nombre] = categoria
        self.add_proposicion(nombre)
    #def add_categoria(self, nombre, atributos):
        # falta añadir los atributos
    def get_categoria(self, nombre):
        return self.categorias[nombre]
    def add_proposicion(self, nombre):
        proposicion = Proposicion(nombre)
        self.proposiciones[nombre] = proposicion
    def get_proposicion(self, nombre):
        return self.proposiciones[nombre]
    def add_individuo(self, nombre_individuo, categoria,atributos=None):
        #atributos es un diccionario con claves el nombre de los atributos y el valor es el valor del atributo. Deben ser iguales a los de la categoria
        if not isinstance(nombre_individuo, str):
            raise ValueError("Individuo debe ser de tipo string")
        categoria = self.get_categoria(categoria)
        proposicion = self.get_proposicion(categoria.nombre)
        atributos_categoria = categoria.get_atributos()
        if atributos is None:
            atributos = {}
        for atributo in atributos_categoria:
            if atributo not in atributos:
                raise ValueError(f"El atributo '{atributo}' no se encuentra en el diccionario de atributos")
            setattr(self.indiviuos[nombre_individuo], atributo, atributos[atributo])


        proposicion.elementos.add((nombre_individuo,)) 
        self.indiviuos[nombre_individuo] = Individuo(nombre_individuo, categoria)  
    #Falta un metodo para crear una accion
    def add_accion(self,accion):
        self.acciones[accion.nombre] = accion
    def get_accion(self,nombre):
        return self.acciones[nombre]
    

        

    #Falta un metodo para mostar todas las acciones que se pueden ejecutar y sus parametros
    def acciones_disponibles(self):
        available_actions = []
        for accion in self.acciones.values():
            solucion = accion.comprobar()
            if not solucion.is_empty():
                print("Acción:", accion.nombre)
                solucion.print()
                available_actions.append((accion, solucion))
        return available_actions

class Categoria:
    def __init__(self, nombre, atributos=None, padre = None):
        self.nombre = nombre
        self.atributos = [] #De momento ignoramos los atributos
        self.padre = padre
        self.atributos = atributos #Atributos solo alamacena los atributos de la categoria pero no hereda la de los padres, para eso usar get_atributos
    def get_atributos(self):
        atributos = []
        if self.padre:
            atributos.extend(self.padre.atributos)
        atributos.extend(self.atributos)
        return atributos


class Individuo(str):
    #quizas deberia tener un atributo categoria o categorias, para poder comprobar si un individuo pertenece a una categoria y obtener sus parametros si fuera necesario.
    def __init__(self, nombre, categorias=None):
        self.nombre = nombre
        if categorias:
            self.categorias = categorias
class  IndividuoNumerico(Individuo):
    def __init__(self, valor):
        if not isinstance(valor, int):
            raise TypeError("El parámetro 'valor' debe ser un entero")
        self.valor = valor
        self.nombre = str(valor)
class Variable(str):
    pass

#Eliminar
class ParametroCondicion():
    def __init__(self,funcion,argumentos=None):
        if argumentos and isinstance(argumentos,tuple):
            self.argumentos = argumentos
        num_params = len(inspect.signature(funcion).parameters)
        if num_params != len(argumentos):
            raise TypeError("El numero de argumentos debe de ser igual al numero de parametros de la funcion")
        self.funcion = funcion
    def comparar(self):
        return self.funcion(*self.argumentos)
        
        

class SolucionParcial:
    #Cambiar el conjunto y el indice por un simple diccionario????
    
    def __init__(self, variables):
        self.conjunto = []
        self.indice = {}
        if not isinstance(variables, (list, tuple)):
            raise TypeError("El parámetro 'variables' debe ser una lista o una tupla")
        for i,variable in enumerate(variables):
            if not isinstance(variable, Variable):
                raise TypeError("Todos los elementos de 'variables' deben ser del tipo Variable")
            self.indice[variable] = i
        
        
        #self.indice = variables
    def add_elemento(self, elemento):
        if isinstance(elemento, dict):
            nuevo_elemento = [None]*len(self.indice)
            for variable, valor in elemento.items():
                #Comprobar que la variable esta en el indice
                if variable not in self.indice:
                    raise ValueError("La variable no esta en el indice")
                nuevo_elemento[self.indice[variable]] = valor
            elemento = nuevo_elemento
        if not isinstance(elemento, (list, tuple)):
            raise TypeError("El parámetro 'elemento' debe ser una lista o una tupla")
        #Deberia comprobar si elemento es un individuo?
        self.conjunto.append(elemento)
    def add_variable(self, variable):
        if not isinstance(variable, Variable):
            raise TypeError("El parámetro 'variable' debe ser del tipo Variable")
        if variable not in self.indice:
            self.indice[variable] = len(self.indice)
    def is_empty(self):
        return len(self.conjunto) == 0
    def print(self):
        for elemento in self.conjunto:
            print("Elemento:")
            for i, variable in enumerate(self.indice):
                print(f"{variable} = {elemento[i]}")
class Condicion:
    def __init__(self, proposicion, parametros):
        self.proposicion = proposicion
        self.parametros = parametros
    def comprobar(self, solucion_inicial):
        if not isinstance(solucion_inicial, SolucionParcial):
            raise TypeError("El parámetro 'solucion_inicial' debe ser del tipo SolucionParcial")
        return self.proposicion.comprobar(solucion_inicial, self.parametros)
class CondicionFuncion:
    def __init__(self, funcion, parametros):
        self.funcion = funcion
        self.parametros = parametros
    def comprobar(self, solucion_inicial):
        if not isinstance(solucion_inicial, SolucionParcial):
            raise TypeError("El parámetro 'solucion_inicial' debe ser del tipo SolucionParcial")
        variables_parcial = solucion_inicial.indice.keys()
        
        solucion_final = SolucionParcial(list(variables_parcial))
        for elemento in solucion_inicial.conjunto:
            argumentos = []
            for parametro in self.parametros:
                if isinstance(parametro, Variable):
                    if parametro not in solucion_inicial.indice.keys():
                        raise ValueError("La variable no esta en el indice")
                    solucion_final.add_variable(parametro)
                    indice_inicial =solucion_inicial.indice[parametro]
                    argumentos.append(elemento[indice_inicial])
                elif isinstance(parametro, Individuo):
                    argumentos.append(parametro)
                else:
                    raise TypeError("Todos los elementos de 'parametros' deben ser del tipo Variable o Individuo")
            if self.funcion(*argumentos):
                solucion_final.add_elemento(elemento)
        return solucion_final
            

class Accion:
    def __init__(self, nombre, condiciones,consecuencias,padre = None):
        self.nombre = nombre
        #habria que comprobar que todas las condiciones son del tipo Condicion o CondicionFuncion
        self.condiciones = condiciones
        self.consecuencias = consecuencias
        self.padre = padre
        self.contingencias = []
    def add_contingencia(self,condicion,consecuencia):
        self.contingencias.append((condicion,consecuencia))
    def get_condiciones(self):
        condiciones = []
        if self.padre:
            condiciones = self.padre.get_condiciones()
        
        condiciones.extend(self.condiciones)
        return condiciones
    def get_consecuencias(self):
        consecuencias = []
        if self.padre:
            consecuencias = self.padre.get_consecuencias()
        consecuencias.extend(self.consecuencias)
        return consecuencias
    def comprobar(self):
        solucion = SolucionParcial([])
        condiciones = self.get_condiciones()
        for condicion in condiciones:
            if not isinstance(condicion, (Condicion, CondicionFuncion)):
                raise TypeError("Todos los elementos de 'condiciones' deben ser del tipo Condicion o CondicionFuncion")
            solucion = condicion.comprobar(solucion)
        return solucion
    def ejecutar(self,argmunetos):
        #Falta implementar
        #Ejecuta las consecuencias hasta que se queden sin consecuencias o se encuentre un wait
        #Deberia devolver las consecuencias que quedan por ejecutar si se encuentra un wait
        consecuencias = self.get_consecuencias()
        for indice, consecuencia in enumerate(consecuencias):
            if isinstance(consecuencia, (ConsecuenciaAsignacion,ConsecuenciaEliminacion)):
                consecuencia.ejecutar(argmunetos)
            elif isinstance(consecuencia, ConsecuenciaWait):
                return self.consecuencias[indice:]
        return []

        
        
    #def get_consecuencias(self,argumentos):
class Consecuencia:
    #tipos posibles de consecuencias: Asignacion, Eliminacion, Incremento?Decremento?, Wait
    #Las consecuencias podrian ser una consecuencia definida y tener contingencias propias?
    pass
class ConsecuenciaAsignacion(Consecuencia):       
    def __init__(self,proposicion):
        self.proposicion = proposicion
    def ejecutar(self, argumentos):
        #habria que tener en cuenta aqui si la proposicion es del tipo single o unique
        self.proposicion.add_elemento(argumentos)
class ConsecuenciaEliminacion(Consecuencia):       
    def __init__(self,proposicion):
        self.proposicion = proposicion
    def ejecutar(self, argumentos):
        #habria que tener en cuenta aqui si la proposicion es del tipo single o unique
        self.proposicion.delete_elemento(argumentos)   
class ConsecuenciaWait(Consecuencia):
    pass   


#El tipo inclemento y decremento se hara despues de plantear el tipo single o unique.  


class ConsecuenciaDefinida(Consecuencia):
    def __init__(self,nombre,condiciones,consecuencias):
        self.nombre = nombre
        self.condiciones = condiciones
        self.consecuencias = consecuencias
    def ejecutar(self,argumentos):
        solucion = SolucionParcial([])
        for condicion in self.condiciones:
            if not isinstance(condicion, (Condicion, CondicionFuncion)):
                raise TypeError("Todos los elementos de 'condiciones' deben ser del tipo Condicion o CondicionFuncion")
            solucion = condicion.comprobar(solucion)
        for indice, consecuencia in enumerate(self.consecuencias):
            if isinstance(consecuencia, (ConsecuenciaAsignacion,ConsecuenciaEliminacion)):
                consecuencia.ejecutar(argumentos)
            elif isinstance(consecuencia, ConsecuenciaWait):
                return self.consecuencias[indice:]


        pass
class Proposicion:
    def __init__(self, nombre):
        
            
        self.elementos = set()
        self.nombre = nombre
    
    def add_elemento(self, elemento):
        if not isinstance(elemento, (list, tuple)):
            raise TypeError("El parámetro 'elemento' debe ser una lista o una tupla")
        self.elementos.add(elemento)
    def delete_elemento(self, elemento):
        if not isinstance(elemento, (list, tuple)):
            raise TypeError("El parámetro 'elemento' debe ser una lista o una tupla")
        self.elementos.remove(elemento)
    
    def comprobar(self, solucion_inicial,parametros):
        #Quitar el tipo de dado de SolucionParcial y usar un diccionario????
        if not isinstance(solucion_inicial, SolucionParcial):
            raise TypeError("El parámetro 'solucion_parcial' debe ser del tipo SolucionParcial")
        if not isinstance(parametros, list):
            raise TypeError("El parámetro 'parametros' debe ser una lista")
        variables_parcial = []
        for parametro in parametros:
            if not isinstance(parametro, (Individuo, Variable, ParametroCondicion)):
                raise TypeError("Todos los parámetros deben ser del tipo Individuo, Variable o ParametroCondicion")
            if isinstance(parametro, Variable):
                variables_parcial.append(parametro)
        
        
        # Eliminar variables repetidas mediante set, que no permite elementos repetidos
        variables_parcial = list(set(variables_parcial))
        solucion_parcial = SolucionParcial(variables_parcial)

        for elemento_inicial in self.elementos:
            if len(elemento_inicial) != len(parametros):#deberia bastar con hacerlo una unica vez, pero por si acaso se queda asi
                raise ValueError("El número de elementos del elemento no coincide con el número de parametros")

            elemento_solucion = {}
            valido = True
            for i, parametro in enumerate(parametros):
               
                if isinstance(parametro, Individuo):
                    if elemento_inicial[i] != parametro:
                        valido = False
                        break
                elif isinstance(parametro, Variable):

                    #De algun modo variable debe de tener un atributo, metodo, condicion o algo para poder representar cosas como X>5, X<Y o X.atributo == 2

                    #Variables repeditas.Se debe comprobar que si la variable ya ha sido añadida al elemento solucion
                    if parametro in elemento_solucion.keys():
                        #y si ya ha sido añadida, esta debe de coincidir con el valor del elemento inicial
                        if elemento_inicial[i] != elemento_solucion[parametro]:
                            valido = False
                            break
                        else:
                        #y si son iguales, no se debe de volver a añadir,aunque el resultado seria el mismo
                            continue
                    elemento_solucion[parametro] = elemento_inicial[i]
                elif isinstance(parametro,ParametroCondicion):
                    
                    #Se debe comprobar si dentro de los argumentos del pametroCodincion tiene alguna variable
                    #y si es asi, se debe de registrar
                    variables_Condicion = []
                    for arg in parametro.argumentos:
                        if isinstance(arg, Variable):
                            variables_Condicion.append(arg)
                    
                    if variables_Condicion:
                        for variable in variables_Condicion:
                            if variable in elemento_solucion.keys():
                                if elemento_inicial[i] != elemento_solucion[variable]:
                                    valido = False
                                    break
                                else:
                                    elemento_solucion[variable] = elemento_inicial[i]
                            #Se debe sustituir la variable por el valor del elemento inicial
                            variable = elemento_inicial[i]
                    #Ahora podemos comprobra si la condicion se cumple
                    if not valido or not parametro.comparar():
                        valido = False
                        break
                    elemento_solucion[parametro] = elemento_inicial[i]
            if not valido:
                continue
            solucion_parcial.add_elemento(elemento_solucion.copy())#creo que no es necesario hacer una copia

        #Combinar la solucion parcial con la solucion inicial
        variables_iniciales = set(solucion_inicial.indice.keys())
        variables_comunes = set(variables_iniciales).intersection(set(variables_parcial))
        variables_nuevas = set(variables_parcial).difference(variables_iniciales)
        solucion_final = SolucionParcial(list(variables_comunes))
        if len(solucion_inicial.conjunto) == 0:
            return solucion_parcial
        
        for elemento_inicial in solucion_inicial.conjunto:
            for elemento_parcial in solucion_parcial.conjunto:
                #Se compara cada elemento de la solucion inicial con cada elemento de la solucion parcial para buscar un nuevo candidato a la solucion final
                candidato = {}
                for variable in variables_comunes:
                    indice_Inicial = solucion_inicial.indice[variable]
                    indice_Parcial = solucion_parcial.indice[variable]
                    #Se compara variable a variable
                    #Y si coiniciden se agrega al nuevo candidato dicha variable
                    if elemento_inicial[indice_Inicial] == elemento_parcial[indice_Parcial]:
                        candidato[variable] = elemento_inicial[indice_Inicial]
                    else:
                        #Si no coinciden se deja de comparar las siguientes variables, para descartarlo despues
                        break
                #Si el numero de variables/individuos en el candidato no coincide con el numero de variables comunes, se descarta
                if len(candidato.keys())!= len(variables_comunes):
                    continue

                if variables_nuevas:#Si hay variables nuevas, se agregan al candidato
                    for variable in variables_nuevas:
                        indice_Nuevo = solucion_parcial.indice[variable]
                        candidato[variable] = elemento_parcial[indice_Nuevo]
                        solucion_final.add_variable(variable)#Aunque se intenta agregar varias veces la misma variable, no deberia haber problema pues solo se agrega una vez
                variables_restantes = variables_iniciales.difference(variables_comunes)
                if variables_restantes:#Si hay variables restantes, se agregan al candidato
                    for variable in variables_restantes:
                        indice_Restante = solucion_inicial.indice[variable]
                        candidato[variable] = elemento_inicial[indice_Restante]
                        solucion_final.add_variable(variable)
                solucion_final.add_elemento(candidato.copy())
        return solucion_final
                    


if __name__ == "__main__":

    brain = Brain()
    brain.add_categoria("pokemon",["vida","energia"])#incluir tipos como int o individuo?crear proposicion tipo pokemon_vida(pokemon,vida)???
    brain.add_categoria("pikachu", padre="pokemon")#añadir valores por defecto?
    brain.add_individuo("pikachu_1",brain.get_categoria("pikachu"),{"vida":100,"energia":"rayo"})
