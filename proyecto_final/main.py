""" 
# COMPRENDE-1:

Estructura | Datos que almacena               | Operación principal        | Complejidad     | Semana origen
------------------------------------------------------------------------------------------------------------
dict       | restaurante (por id)             | búsqueda directa           | O(1) amortizado | S12
heapq      | recomendaciones de restaurantes  | devuelve dato más "grande" | O(log n)        | S6
BST        | restaurantes en rango de puntaje | búsqueda por rango         | O(log n + k)    | S13
pila       | registro de inserciones          | almacenar inserciones      | O(1)            | S5

# COMPRENDE-2:

Operacion: "Mostrar información de restaurantes recientes"
─────────────────────────────────────────────────────
Paso 1: obtener las últimas inserciones del registro
        → pila[-k:] O(k) [estructura: Pila/list]

Paso 2: buscar información completa de cada restaurante
        → dict.get(id) O(k) [estructura: Hash/dict]

Complejidad total:
O(k) + O(k) ≈ O(k)


Operacion: "Recomendar restaurantes similares por calificacion"
─────────────────────────────────────────────────────
Paso 1: buscar el restaurante origen
        → dict.get(id_restaurante) O(1) [estructura: dict]

Paso 2: buscar restaurantes con calificacion similar
        → bst.buscar_rango(r-0.3, r+0.3) O(log n + k) [estructura: BST]

Paso 3: insertar resultados en heap de prioridad
        → heapq.heappush() O(k log k) [estructura: heapq]

Paso 4: extraer top-3 restaurantes
        → heapq.heappop() O(3 log k) [estructura: heapq]

Complejidad total:

O(1) + O(log n + k) + O(k log k) + O(3 log k) ≈ O(k log k)

# IA-REFLEXION-C: La IA nos mostró cómo es posible que haya inconsistencias entre los datos almacenados
# en una estructura y los almacenados en otra debido a fallos de inserción. Una manera de mitigar esto
# es mediante la creación de un registro de inserciones que nos indique si y en donde ocurrieron errores.
# O también se puede validar a través de la comparación de tamaños entre estructuras.
# Sí nos fue útil. Aunque no era difícil de notar, no le habíamos prestado atención a ese posible problema.

"""

# DECISIÓN: veredicto arquitectónico final
# (Sustituir el ejemplo con el veredicto real del proyecto del equipo)

# DECISIÓN-DICT:
#   Elegimos dict para búsquedas directas por ID porque tiene
#   complejidad O(1) amortizado.
#   Las operaciones de dict mantuvieron un tiempo constante (0.0001ms) 
#   entre todos los tamaños del benchmark
#   Descartamos arreglo dinámico [S2] (O(n) búsqueda secuencial)
#   y BST (O(log n)) [S13] porque el sistema necesita acceso inmediato
#   por una clave exacta, no búsquedas ordenadas.
#   Compromiso aceptado: El dict tiene que reservar más memoria y cuando hay muchos datos
#   pueden empezar a ocurrir colisiones entre las claves. La implementación dict de python se encarga
#   de mitigar esos problemas.


# DECISIÓN-HEAPQ:
#   Elegimos heapq para mantener recomendaciones y top dinámico
#   porque inserta y extrae prioridades en O(log n).
#   Para n = 10000 el heap tardó solo 0.0300ms
#   Descartamos arreglos [S2] porque mantener el top
#   requeriría ordenar constantemente.
#   También descartamos BST [S13] porque el proyecto solo necesita
#   acceder rápidamente a los mejores elementos, no recorrer
#   todo el árbol ordenado.
#   Compromiso aceptado: heapq no mantiene todos los datos
#   completamente ordenados, pero es aceptable porque solo
#   necesitamos recuperar los restaurantes con mayor puntaje.


# DECISIÓN-BST:
#   Elegimos BST para mantener restaurantes ordenados dinámicamente
#   por puntaje y permitir búsquedas por rango eficientes
#   con complejidad O(log n + k).
#   Su tiempo de ejecución real fue de 0.2891ms para n = 10000.
#   Descartamos dict [S12] porque no mantiene un orden lógico y obliga a recorrer
#   todos los elementos al hacer consultas por rango.
#   También descartamos arreglos [S2] ordenados porque insertar nuevos
#   restaurantes implicaría desplazamientos O(n).
#   Compromiso aceptado: el BST puede degradarse a O(n) si queda
#   desbalanceado, pero es aceptable porque el proyecto solo tiene
#   inserciones con tamaños moderados.


# IA-REFLEXION-P:
""" 
En lugar de usar una sola estructura para todo, decidimos combinar varias estructuras de datos porque cada una resuelve mejor una necesidad diferente del sistema. El dict permitió búsquedas rápidas por ID, el heapq ayudó a manejar recomendaciones dinámicas, el BST hizo eficientes las búsquedas por rango y la pila sirvió para guardar historial de inserciones.

También aprendimos que no existe una estructura perfecta para todo, sino que cada una tiene ventajas y desventajas dependiendo del problema. 
"""

from sistema_limos import SistemaLimos
from pruebas import verificar_invariante_cruzada

if __name__ == "__main__":

    sistema = SistemaLimos()

    # Base de datos de restaurantes  
    restaurantes = [
        ("R001", "Pujol", 9.8, "Mexicana"),
        ("R002", "Quintonil", 9.7, "Mexicana"),
        ("R003", "Contramar", 9.1, "Mariscos"),
        ("R004", "Rosetta", 9.0, "Italiana"),
        ("R005", "Sud 777", 8.9, "Contemporánea"),
        ("R006", "Animalón", 8.8, "Baja Med"),
        ("R007", "Fauna", 8.7, "Contemporánea"),
        ("R008", "La Docena", 8.5, "Mariscos"),
        ("R009", "Taquería Orinoco", 8.4, "Tacos"),
        ("R010", "El Califa", 8.3, "Tacos"),
        ("R011", "Mochomos", 8.2, "Sonorense"),
        ("R012", "Sonora Grill", 7.9, "Cortes"),
        ("R013", "Nicos", 8.6, "Mexicana"),
        ("R014", "Casa Oaxaca", 9.2, "Oaxaqueña"),
        ("R015", "Los Arcos", 7.8, "Mariscos"),
        ("R016", "Ilios", 8.1, "Mediterránea"),
        ("R017", "Campomar", 8.0, "Mariscos"),
        ("R018", "El Farallón", 9.3, "Mariscos"),
        ("R019", "Koli", 9.4, "Mexicana"),
        ("R020", "Maximo Bistrot", 9.0, "Internacional")
    ]

    # Insertar restaurantes 
    for id_r, nombre, puntaje, categoria in restaurantes:
        sistema.agregar_contenido(id_r, nombre, puntaje, categoria)

    # Operación 1: lookup 
    print("BÚSQUEDA:")
    resultado_lookup = sistema.procesar_solicitud("lookup", "R001")
    print(resultado_lookup)
    print()

    # Operación 2: rango 
    print("RANGO (8.8 - 9.5):")
    resultado_rango = sistema.procesar_solicitud("rango", (8.8, 9.5))

    for r in resultado_rango:
        print(r)

    print()

    # Operación 3: top_n 
    print("TOP 5 RESTAURANTES:")
    resultado_top = sistema.procesar_solicitud("top_n", 5)

    for r in resultado_top:
        print(r)

    print()

    # Operación 4: historial
    print("ÚLTIMAS 5 INSERCIONES:")
    resultado_historial = sistema.procesar_solicitud("historial", 5)

    for r in resultado_historial:
        print(r)

    print()

    print("RESTAURANTES SIMILARES A QUINTONIL:")
    resultado_similares = sistema.procesar_solicitud("similares", "R002")

    for r in resultado_similares:
        print(r)
        
    print()
    
    verificar_invariante_cruzada(sistema)