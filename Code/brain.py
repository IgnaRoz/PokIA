class Individuo(str):
    pass
class Variable(str):
    pass
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
    def print(self):
        for elemento in self.conjunto:
            print("Elemento:")
            for i, variable in enumerate(self.indice):
                print(f"{variable} = {elemento[i]}")
        
class Proposicion:
    def __init__(self, nombre):
        
            
        self.elementos = set()
        self.nombre = nombre
    
    def comprobar(self, solucion_inicial,parametros):
        #Quitar el tipo de dado de SolucionParcial y usar un diccionario????
        if not isinstance(solucion_inicial, SolucionParcial):
            raise TypeError("El parámetro 'solucion_parcial' debe ser del tipo SolucionParcial")
        if not isinstance(parametros, list):
            raise TypeError("El parámetro 'parametros' debe ser una lista")
        variables_parcial = []
        for parametro in parametros:
            if not isinstance(parametro, (Individuo, Variable)):
                raise TypeError("Todos los parámetros deben ser del tipo Individuo o Variable")
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
                    #Se debe comprobar que si la variable ya ha sido añadida al elemento solucion
                    if parametro in elemento_solucion.keys():
                        #y si ya ha sido añadida, esta debe de coincidir con el valor del elemento inicial
                        if elemento_inicial[i] != elemento_solucion[parametro]:
                            valido = False
                            break
                        else:
                        #y si son iguales, no se debe de volver a añadir,aunque el resultado seria el mismo
                            continue

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
    X = Variable("X")
    Y = Variable("Y")
    Z = Variable("Z")
    ind_1 = Individuo("ind_1")
    ind_2 = Individuo("ind_2")
    ind_3 = Individuo("ind_3")
    proposicion = Proposicion("proposicion")
    proposicion.elementos.add((ind_1, ind_2))
    proposicion.elementos.add((ind_1, ind_1))
    proposicion.elementos.add((ind_1, ind_3))
    proposicion.elementos.add((ind_2, ind_3))
    #print(proposicion.elementos)

    solucion_inicial = SolucionParcial([Y])
    solucion_inicial.add_elemento((ind_1,))
    solucion_inicial.add_elemento((ind_3,))
    solucion_final=proposicion.comprobar(solucion_inicial, [X,Y])
    solucion_final.print()
