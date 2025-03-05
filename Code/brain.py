class Individuo(str):
    pass
class Variable(str):
    pass
class SolucionParcial:
    #Cambiar el conjunto y el indice por un simple diccionario????
    
    def __init__(self, variables):
        self.conjunto = set()
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
            lista_vacia = [None]*len(self.indice)
            for variable, valor in elemento.items():
                lista_vacia[self.indice[variable]] = valor
            elemento = tuple(lista_vacia)
        if not isinstance(elemento, (list, tuple)):
            raise TypeError("El parámetro 'elemento' debe ser una lista o una tupla")
        #Deberia comprobar si elemento es un individuo?
        self.conjunto.add(elemento)
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
        
        

        solucion_parcial = SolucionParcial(variables_parcial)
        #conjunto_actual = set()

        for elemento_inicial in self.elementos:
            if len(elemento_inicial) != len(parametros):
                raise ValueError("El número de elementos del elemento no coincide con el número de parametros")

            elemento_solucion = {}
            for i, parametro in enumerate(parametros):
                if isinstance(parametro, Individuo):
                    if elemento_inicial[i] != parametro:
                        break
                elif isinstance(parametro, Variable):
                    elemento_solucion[parametro] = elemento_inicial[i]
            solucion_parcial.add_elemento(elemento_solucion.copy())

        #Combinar la solucion parcial con la solucion inicial
        variables_iniciales = set(solucion_inicial.indice.keys())
        variables_comunes = set(variables_iniciales).intersection(set(variables_parcial))
        variables_nuevas = set(variables_parcial).difference(variables_iniciales)
        solucion_final = SolucionParcial(list(variables_comunes))

        if len(solucion_inicial.conjunto) > 0:
            for elemento_inicial in solucion_inicial.conjunto:
                for elemento_parcial in solucion_parcial.conjunto:
                    candidato = {}
                    for variable in variables_comunes:
                        indice_Inicial = solucion_inicial.indice[variable]
                        indice_Parcial = solucion_parcial.indice[variable]
                        
                        if elemento_inicial[indice_Inicial] == elemento_parcial[indice_Parcial]:
                            candidato[variable] = elemento_inicial[indice_Inicial]
                        else:
                            break
                    if len(candidato.keys())!= len(variables_comunes):
                        continue

                    if variables_nuevas:
                        for variable in variables_nuevas:
                            indice_Nuevo = solucion_parcial.indice[variable]
                            candidato[variable] = elemento_parcial[indice_Nuevo]
                            solucion_final.add_variable(variable)
                    variables_restantes = variables_iniciales.difference(variables_comunes)
                    if variables_restantes:
                        for variable in variables_restantes:
                            indice_Restante = solucion_inicial.indice[variable]
                            candidato[variable] = elemento_inicial[indice_Restante]
                            solucion_final.add_variable(variable)
                    solucion_final.add_elemento(candidato.copy())
        return solucion_final
                    

                



            

# Eliminar metodo viejo
    def comprobar2(self,solucion_parcial,parametros):
        if not isinstance(solucion_parcial, SolucionParcial):
            raise TypeError("El parámetro 'solucion_parcial' debe ser del tipo SolucionParcial")
        if not isinstance(parametros, list):
            raise TypeError("El parámetro 'parametros' debe ser una lista")
        for parametro in parametros:
            if not isinstance(parametro, (Individuo, Variable)):
                raise TypeError("Todos los parámetros deben ser del tipo Individuo o Variable")
        elementos_proposicion = self.elementos.copy()#Puede que haga falta una copia profunda? 
        for i, parametro in enumerate(self.parametros):
            if isinstance(parametro, Individuo):
                #El parametro es un individuo
                for elemento in elementos_proposicion:
                    #para cada elemento del conjunto actual de elementos de la proposicion
                    if elemento[i] != parametro:
                        #Si el parametro no coincide con el individuo del elemento en la posicion i, este se deve de remover del conjunto actual
                        elementos_proposicion.remove(elemento)
                        if elemento in solucion_parcial.conjunto:
                            #tambien hay que comprobar si el elemento removida ya esta agregado en la solucion parcial y si es asi removerlo.
                            pass 
                
            elif isinstance(parametro, Variable):
                #El parametro es una variable
                if parametro in solucion_parcial.indice:
                    #Es una variable conocida
                    pass
                else:
                    #Es una variable desconocida
                    pass
                pass
            else:
                raise ValueError("Elemento no reconocido")


if __name__ == "__main__":
    X = Variable("X")
    Y = Variable("Y")
    Z = Variable("Z")
    ind_1 = Individuo("ind_1")
    ind_2 = Individuo("ind_2")
    ind_3 = Individuo("ind_3")
    proposicion = Proposicion("proposicion")
    proposicion.elementos.add((ind_1, ind_2))
    proposicion.elementos.add((ind_1, ind_3))
    proposicion.elementos.add((ind_2, ind_3))
    #print(proposicion.elementos)

    solucion_inicial = SolucionParcial([X])
    solucion_inicial.add_elemento((ind_1,))
    solucion_inicial.add_elemento((ind_3,))
    solucion_final=proposicion.comprobar(solucion_inicial, [X,Y])
    solucion_final.print()
