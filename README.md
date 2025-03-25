# Motor de sentencias lógicas y lenguaje de modelado propio

Proyecto de un programa en Python para ejecutar sentencias lógicas inspirada en la lógica proposicional, pero con un enfoque más práctico, junto a una propuesta de lenguaje lógico basado en proposiciones, acciones, condiciones, consecuencias y contingencias (entre otros elementos)

Este lenguaje está pensado para modelar la lógica de juegos simples, como puede ser el famoso juego de cartas de Pokémon, el cual se ha tomado de ejemplo para demostrar la versatilidad del lenguaje.

El objetivo final será un programa capaz de procesar un archivo de texto plano con la lógica del juego y que sea capaz en tiempo de ejecución de mostrar las acciones que están disponibles en cada momento, así como registrar los efectos de estas y disparar eventos que indique al entorno de Python los sucesos que ha desatado las diferentes acciones.
también se plantea un generador de espacios de estados para que diferentes algoritmos clásicos de inteligencia artificial pueda recorrerlos para encontrar estrategias de juego que permitan la elaboración de bots capaces de jugar al juego modelado.


# Prueba de concepto

Se ha desarrollado una prueba de concepto mínima en la que se ha modelado una simplificación del juego de cartas de Pokémon en la cual no se usa energías, no hay mazo ni cartas en la mano y ya hay unos pocos Pokémon en juego.

La definición de las reglas están descritas en el archivo de texto "ejemploCombateSimplificado" pero se han incluido manualmente al motor lógico. Mas adelante será un procesador del lenguaje el encargado de esta tarea.

## Ejecución

1. Clonación del repositorio:
    - Ejecuta el siguiente comando en la terminal en la ruta donde deseas guardar el repositorio:
    ```
    git clone https://github.com/IgnaRoz/PokIA
    ```

2. Accede a la carpeta con el código:
    - El código ejecutable está en la carpeta Code:
    ```
    cd Code
    ```

3. Ejecución del juego:
    - Una vez dentro del directorio, ejecuta el siguiente comando para iniciar el juego:
    ```
    python pokemonGame.py
    ```
    - Entonces se activará una terminal interactiva, puedes usar la palabra "help" para ver los comandos disponibles

NOTA:

    - Asegúrate de tener instalada una versión compatible de Python.        
    - No es necesario instalar ningún tipo de dependencias.

# Lenguaje de POKEMON

En la carpeta Pokémon hay un ejemplo de lo que sería un proyecto completo que define la lógica del juego de cartas completo.

El desarrollo está en una etapa muy temprana y esta carpeta tenía el objetivo de ser tan solo un esbozo inicial con el que partir para el desarrollo por lo que está llena de anotaciones, ambigüedades y cosas ya descartadas pero que no ha sido aun documentadas correctamente.
