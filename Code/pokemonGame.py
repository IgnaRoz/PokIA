from brain import *


def inicializar(brain):
    brain.add_categoria("jugador")
    brain.add_individuo(Individuo("judador1"),"jugador")
    brain.add_individuo(Individuo("judador2"),"jugador")

    brain.add_categoria("pokemon",atributos=["vida"])
    brain.add_categoria("pikachu", padre="pokemon")
    brain.add_categoria("eevee", padre="pokemon")
    brain.add_categoria("ratata", padre="pokemon")
    brain.add_categoria("piggy", padre="pokemon")

    
    #categoria_pikachu = brain.get_categoria("pikachu")
    #categoria_eevee = brain.get_categoria("eevee")
    #categoria_ratata = brain.get_categoria("ratata")
    #categoria_piggy = brain.get_categoria("piggy")
    

    brain.add_individuo(Individuo("pikachu_1"),"pikachu",{"vida":IndividuoNumerico(10)})
    brain.add_individuo(Individuo("eevee_1"),"eevee",{"vida":IndividuoNumerico(10)})
    brain.add_individuo(Individuo("ratata_1"),"ratata",{"vida":IndividuoNumerico(10)})
    brain.add_individuo(Individuo("ratata_2"),"ratata",{"vida":IndividuoNumerico(10)})
    brain.add_individuo(Individuo("piggy_1"),"piggy",{"vida":IndividuoNumerico(10)})
    brain.add_individuo(Individuo("piggy_2"),"piggy",{"vida":IndividuoNumerico(10)})

    brain.add_proposicion("pokemon_activo")
    brain.add_proposicion("pokemon_banco")
    brain.add_proposicion("jugador_rival")
    brain.add_proposicion("turno_actual")

    
    accion_atacar = Accion("atacar",
                           [Condicion(brain.get_proposicion("pokemon"),[Variable("Pokemon")]),
                            Condicion(brain.get_proposicion("turno_actual"),[Variable("JugadorTurno")]),
                            Condicion(brain.get_proposicion("pokemon_activo"),[Variable("Pokemon"),Variable("JugadorTurno")]),
                            Condicion(brain.get_proposicion("jugador_rival"),[Variable("JugadorTurno"),Variable("Rival")]),
                            Condicion(brain.get_proposicion("pokemon"), 
                            [Variable("PokemonRival")]),
                            Condicion(brain.get_proposicion("pokemon_activo"),
                            [Variable("PokemonRival"),Variable("Rival")])
                            ],                           
                           [ConsecuenciaEliminacion(brain.get_proposicion("turno_actual"),[Variable("JugadorTurno")]),
                            ConsecuenciaAsignacion(brain.get_proposicion("turno_actual"),[Variable("Rival")])])
    def bajar_vida(elemento,parametro_posicion,damage):
        if not isinstance(elemento[parametro_posicion],IndividuoNumerico):
            raise TypeError("Solo se puede modificar Individuos Numericos")
        elemento[parametro_posicion] = IndividuoNumerico(elemento[parametro_posicion].valor - damage)
        return elemento

    contingencia = Contingencia("pokemon_muerto",
                                [Condicion(brain.get_proposicion("pokemon_vida"),   [Variable("PokemonRival"),Variable("NuevaVidaPokemonRival")]),
                                CondicionFuncion(lambda x: x.valor <=0,(Variable("NuevaVidaPokemonRival"),))],
                                [ConsecuenciaEliminacion(brain.get_proposicion("pokemon_activo"),[Variable("PokemonRival"),Variable("Rival")])],postcondiciones=True, callBack=lambda: print("Se ha eliminado el pokemon rival"))

    accion= Accion("impactrueno",
                                [Condicion(brain.get_proposicion("pikachu"),[Variable("Pokemon")]),
                                 Condicion(brain.get_proposicion("pokemon_vida"),[Variable("PokemonRival"),Variable("VidaPokemonRival")])],
                                [ConsecuenciaFuncion(brain.get_proposicion("pokemon_vida"),[Variable("PokemonRival"),Variable("VidaPokemonRival")],funcion= lambda elemento: bajar_vida(elemento,1,50))],
                                padre=accion_atacar, callBack=lambda: print("Se va a realizar el ataque impactrueno"))
    accion.add_contingencia(contingencia)
    #brain.add_accion(accion_atacar)#solo para pruebas, atacar no es una accion ejecutable
    brain.add_accion(accion)

    accion= Accion("placaje",
                                [Condicion(brain.get_proposicion("eevee"),[Variable("Pokemon")]),
                                 Condicion(brain.get_proposicion("pokemon_vida"),[Variable("PokemonRival"),Variable("VidaPokemonRival")])],
                                [ConsecuenciaFuncion(brain.get_proposicion("pokemon_vida"),[Variable("PokemonRival"),Variable("VidaPokemonRival")],funcion= lambda elemento: bajar_vida(elemento,1,20))],
                                padre=accion_atacar, callBack=lambda: print("Se va a realizar el ataque placaje"))
    accion.add_contingencia(contingencia)

    brain.add_accion(accion)

    # Agregar nueva acción tornado
    accion = Accion("tornado",
                    [Condicion(brain.get_proposicion("piggy"), [Variable("Pokemon")]),
                     Condicion(brain.get_proposicion("pokemon_vida"), [Variable("PokemonRival"), Variable("VidaPokemonRival")])],
                    [ConsecuenciaFuncion(brain.get_proposicion("pokemon_vida"), [Variable("PokemonRival"), Variable("VidaPokemonRival")],
                                         funcion=lambda elemento: bajar_vida(elemento, 1, 30))],
                    padre=accion_atacar, callBack=lambda: print("Se va a realizar el ataque tornado"))
    accion.add_contingencia(contingencia)
    brain.add_accion(accion)

    # Agregar nueva acción mordisco
    accion = Accion("mordisco",
                    [Condicion(brain.get_proposicion("ratata"), [Variable("Pokemon")]),
                     Condicion(brain.get_proposicion("pokemon_vida"), [Variable("PokemonRival"), Variable("VidaPokemonRival")])],
                    [ConsecuenciaFuncion(brain.get_proposicion("pokemon_vida"), [Variable("PokemonRival"), Variable("VidaPokemonRival")],
                                         funcion=lambda elemento: bajar_vida(elemento, 1, 10))],
                    padre=accion_atacar, callBack=lambda: print("Se va a realizar el ataque mordisco"))
    accion.add_contingencia(contingencia)
    brain.add_accion(accion)

    accion= Accion("cambiar_pokemon",
                   [Condicion(brain.get_proposicion("pokemon"),[Variable("Pokemon")]),
                    Condicion(brain.get_proposicion("turno_actual"),[Variable("Jugador")]),
                    Condicion(brain.get_proposicion("pokemon_banco"),[Variable("Pokemon"),Variable("Jugador")])],
                    [ConsecuenciaEliminacion(brain.get_proposicion("pokemon_banco"),[Variable("Pokemon"),Variable("Jugador")]),
                     ConsecuenciaAsignacion(brain.get_proposicion("pokemon_activo"),[Variable("Pokemon"),Variable("Jugador")])], callBack=lambda: print("Se va a cambiar el pokemon activo"))
    
    contingencia = Contingencia("cambiar_pokemon_activo",
            [Condicion(brain.get_proposicion("pokemon_activo"),[Variable("PokemonActivo"),Variable("Jugador")])],
            [ConsecuenciaEliminacion(brain.get_proposicion("pokemon_activo"),[Variable("PokemonActivo"),Variable("Jugador")]),
            ConsecuenciaAsignacion(brain.get_proposicion("pokemon_banco"),[Variable("PokemonActivo"),Variable("Jugador")])])
    accion.add_contingencia(contingencia)
    brain.add_accion(accion)


    brain.get_proposicion("turno_actual").add_elemento(("jugador1",))
    #Falta el resto de proposiciones iniciales para poder ejecutar la accion atacar
    brain.get_proposicion("pokemon_activo").add_elemento(("pikachu_1","jugador1"))

    brain.get_proposicion("pokemon_activo").add_elemento(("eevee_1","jugador2"))
    brain.get_proposicion("jugador_rival").add_elemento(("jugador1","jugador2"))
    brain.get_proposicion("jugador_rival").add_elemento(("jugador2","jugador1"))
    #brain.get_proposicion("pokemon_banco").add_elemento(("piggy_1","jugador1"))
    #brain.get_proposicion("pokemon_banco").add_elemento(("piggy_2","jugador1"))
#
    #brain.get_proposicion("pokemon_banco").add_elemento(("ratata_1","jugador2"))
    #brain.get_proposicion("pokemon_banco").add_elemento(("ratata_2","jugador2"))

  
def estado(brain):
    turno = next(iter(brain.get_proposicion("turno_actual").elementos))[0]
    print("Turno del jugador:", turno)
    
    # Obtener la proposición de vida
    conjunto_vida = brain.get_proposicion("pokemon_vida").elementos

    # Pokémon activo del jugador
    conjunto_activo = brain.get_proposicion("pokemon_activo").elementos
    pokemon_activo_jugador = list(filter(lambda tupla: tupla[1] == turno, conjunto_activo))
    if pokemon_activo_jugador:
        activo = pokemon_activo_jugador[0][0]
        print("Pokemon activo del jugador:", activo)
        # Buscar la vida del Pokémon activo
        vida = list(filter(lambda t: t[0] == activo, conjunto_vida))
        if vida:
            print("  Vida:", vida[0][1])
        else:
            print("  Vida: no registrada")
    else:
        print("No hay pokemon activo para el jugador.")
    
    # Pokémon en la banca del jugador
    conjunto_banco = brain.get_proposicion("pokemon_banco").elementos
    pokemon_banco_jugador = list(filter(lambda tupla: tupla[1] == turno, conjunto_banco))
    print("Pokemon en la banca del jugador:")
    for poke in pokemon_banco_jugador:
        nombre = poke[0]
        print(" -", nombre, end=" ")
        # Buscar la vida para cada Pokémon en la banca
        vida = list(filter(lambda t: t[0] == nombre, conjunto_vida))
        if vida:
            print(f"(Vida: {vida[0][1]})")
        else:
            print("(Vida: no registrada)")
    
    # Obtén el jugador rival: se asume que en "jugador_rival" se guarda como (jugador, rival)
    conjunto_rival = brain.get_proposicion("jugador_rival").elementos
    rival_mapping = list(filter(lambda tupla: tupla[0] == turno, conjunto_rival))
    if rival_mapping:
        rival = rival_mapping[0][1]
        print("Jugador rival:", rival)
        
        # Pokémon activo del rival
        pokemon_activo_rival = list(filter(lambda tupla: tupla[1] == rival, conjunto_activo))
        if pokemon_activo_rival:
            activo_rival = pokemon_activo_rival[0][0]
            print("Pokemon activo del rival:", activo_rival)
            vida = list(filter(lambda t: t[0] == activo_rival, conjunto_vida))
            if vida:
                print("  Vida:", vida[0][1])
            else:
                print("  Vida: no registrada")
        else:
            print("No hay pokemon activo para el rival.")
        
        # Pokémon en la banca del rival
        pokemon_banco_rival = list(filter(lambda tupla: tupla[1] == rival, conjunto_banco))
        print("Pokemon en la banca del rival:")
        for poke in pokemon_banco_rival:
            nombre = poke[0]
            print(" -", nombre, end=" ")
            vida = list(filter(lambda t: t[0] == nombre, conjunto_vida))
            if vida:
                print(f"(Vida: {vida[0][1]})")
            else:
                print("(Vida: no registrada)")
    else:
        print("No se encontró jugador rival para el turno.")

def previsualizar_solucion(solucion,tab=0):
    taburaciones = "\t"*tab
    for i in solucion.indice:
        for elemento in solucion.conjunto:
            print(f"{taburaciones}(Variable){i} = {elemento[solucion.indice[i]]}")

def is_over(brain):
    # Recopilar todos los jugadores a partir de las proposiciones "turno_actual" y "jugador_rival"
    jugadores = set()
    for tupla in brain.get_proposicion("turno_actual").elementos:
        jugadores.add(tupla[0])
    for tupla in brain.get_proposicion("jugador_rival").elementos:
        jugadores.add(tupla[0])
        jugadores.add(tupla[1])
    
    # Obtener la proposición del Pokémon activo y de la banca
    activos = brain.get_proposicion("pokemon_activo").elementos
    banca = brain.get_proposicion("pokemon_banco").elementos

    # Comprobar para cada jugador si tiene algún Pokémon 
    jugadores_sin_pokemon = []
    for jugador in jugadores:
        tiene_activo = any(tupla[1] == jugador for tupla in activos)
        tiene_banca = any(tupla[1] == jugador for tupla in banca)
        if not (tiene_activo or tiene_banca):
            jugadores_sin_pokemon.append(jugador)
    
    if jugadores_sin_pokemon:
        print("El juego ha terminado. Los siguientes jugadores no tienen Pokémon:")
        for j in jugadores_sin_pokemon:
            print(" -", j)
        return True
    return False

if __name__ == "__main__":

    brain = Brain()

    inicializar(brain)


    acciones = brain.acciones_disponibles()
    fin = False
    print("Bienvenido al juego de Pokémon!")
    print("Escribe 'help' para ver los comandos disponibles.")
    while not fin:
        #comprobamos si el juego ha terminado
        if is_over(brain):
            print("El juego ha terminado.")
            break
        # Mostramos el estado actual del juego
        comando = input(">> ").strip()
        if not comando:
            continue
        # Dividimos la entrada en palabras para extraer el comando y sus argumentos.
        tokens = comando.split()
        cmd = tokens[0].lower()

        if cmd == "acciones":
            acciones = brain.acciones_disponibles()
            brain.mostrar_acciones(acciones)        
        elif cmd == "accion":
            if len(tokens) != 2 or not tokens[1].isdigit():
                print("formato incorrecto")
                print("Uso: accion <numero>")
                continue
            numero =  int(tokens[1])
            if numero < 0 or numero >len(acciones): 
                print("opcion no valida")
            accion,argumentos = acciones[numero-1]
            if len(argumentos.conjunto) > 1:
                numero_elementos = len(argumentos.conjunto)
                #falta mostrar los elementos de la solucion parcial y pedir al usuario que elija uno
                soluciones = argumentos.get_soluciones()
                n=1
                for solucion in soluciones:
                    print(f"argumentos {n}")
                    n +=1
                    previsualizar_solucion(solucion,tab=1)
                seleccion_input = input(f"Ingrese un número entre 1 y {numero_elementos}: ")
                try:
                    seleccion = int(seleccion_input)
                    if not (1 <= seleccion <= numero_elementos):
                        print("El número ingresado está fuera de rango.")
                        continue
                    argumentos = soluciones[seleccion -1]
                except ValueError:
                    print("Valor inválido. Se esperaba un número entero.")
                    continue

            accion.ejecutar(argumentos)

        elif cmd == "estado":
            estado(brain)
        elif cmd == "reset":
            brain = Brain()
            inicializar(brain)
            print("Juego reiniciado.")
        elif cmd == "help":
            print("Comandos disponibles:")
            print("  acciones - Muestra las acciones disponibles.")
            print("  accion <numero> - Ejecuta la acción seleccionada.")
            print("  estado - Muestra el estado actual del juego.")
            print("  reset - Reinicia el juego.")
            print("  exit - Sale del juego.")
        elif cmd == "exit":
            fin = True
