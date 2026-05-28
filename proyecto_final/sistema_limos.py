import heapq, time, random, statistics, random
from estructuras import NodoBST
from estructuras import _bst_insertar, _bst_rango

# APLICA-3: Clase SistemaLimos — inicialización
class SistemaLimos:
    def __init__(self):
        # Estructura 1: dict
        # DECISION: Se usa dict para hacer búsquedas directas por ID de restaurantes. 
        # Complejidad: O(1)
        self.catalogo = {}

        # Estructura 2: heapq
        # DECISION: Se usará heapq para implementar la cola de recomendaciones. Los números se harán
        # negativos para simular un max-heap (heapq es una implementación min-heap)
        # Complejidad: O(log n)
        self.cola_recomendaciones = []

        # Estructura 3: BST de puntuaciones
        # DECISION: El BST se usará para mantener los datos ordenados dinámicamente y 
        # hacer búsquedas por rango eficientes
        # Complejidad: O(log n + k)
        self.bst_raiz = None

        # Estructura 4: Pila 
        # DECISION: La pila se encargará de mantener un historial de las inserciones realizadas
        # Complejidad: O(1)
        self.historial = []          

    # APLICA-4: Método agregar_contenido — inserción consistente
    def agregar_contenido(self, id_restaurante, nombre, puntaje, categoria=None):
        """
        Punto de entrada único para agregar restaurantes al sistema.
        Actualiza TODAS las estructuras de forma consistente.
        
        Parámetros:
            id_restaurante (str): identificador único
            nombre       (str)  : nombre del restaurante
            puntaje    (float)  : puntuación 0.0-10.0
            categoria    (str)  : Tipo de comida que sirve el restaurante
        """
        # Validación de entrada
        if id_restaurante in self.catalogo:
            raise ValueError(f"ID '{id_restaurante}' ya existe en el catálogo")
        if not (0.0 <= puntaje <= 10.0):
            raise ValueError(f"Puntaje {puntaje} fuera de rango [0.0, 10.0]")

        restaurante = {
            'id': id_restaurante,
            'nombre': nombre,
            'puntaje': puntaje, 
            'categoria': categoria
            }

        # Paso 1: insertar en dict (O(1) amortizado)
        self.catalogo[id_restaurante] = restaurante
        # Paso 2: insertar en BST por puntaje (O(log n))
        self.bst_raiz = _bst_insertar(self, self.bst_raiz, puntaje, restaurante)
        # Paso 3: insertar recomendaciones a heap (O(k log k))
        heapq.heappush(
            self.cola_recomendaciones,
            (-puntaje, id_restaurante, restaurante)
        )
        # Paso 4: agregar al historial de inserciones (pila, O(1))
        self.historial.append(id_restaurante)

        return True


    # APLICA-5: Enrutador de operaciones
    def procesar_solicitud(self, tipo, param=None):
        """
        Enrutador de solicitudes — Patrón Fachada.
        Tipos soportados:
            'lookup'    → param: id_restaurante (str)
            'rango'     → param: (min_puntaje, max_puntaje) tupla
            'top_n'     → param: n (int) — los n mejores puntajes del catálogo de restaurantes
            'historial' → param: k (int) — últimas k inserciones
            'similares' → param: id — restaurantes con puntaje similar a uno en específico
            'recientes' → param: k (int) — devuelve la información completa de cada inserción del historial
        """
        if   tipo == 'lookup':
            return self.catalogo.get(param, None)         # O(1)

        elif tipo == 'rango':
            minv, maxv = param
            resultado = []
            _bst_rango(self, self.bst_raiz, minv, maxv, resultado)
            return resultado                               # O(log n + k)

        elif tipo == 'top_n':
            # n = param or 5
            # copia_heap = self.cola_recomendaciones.copy()
            # resultado = []
            # while copia_heap and len(resultado) < n:
            #     _, _, restaurante = heapq.heappop(copia_heap)
            #     resultado.append(restaurante)
            # return resultado
            n = param if param is not None else 5
            todos = sorted(self.catalogo.values(),
                        key=lambda x: x['puntaje'], reverse=True)
            return todos[:n]     

        elif tipo == 'historial':
            k = param or 10
            return self.historial[-k:][::-1] 
        
        elif tipo == 'similares': # O(k log k)
            id_restaurante = param
            # Paso 1: buscar restaurante origen
            origen = self.catalogo.get(id_restaurante)
            if origen is None:
                return []
            puntaje = origen['puntaje']
            # Paso 2: buscar restaurantes similares
            resultados = []
            _bst_rango(self,
                self.bst_raiz,
                puntaje - 0.3,
                puntaje + 0.3,
                resultados
            )
            # Paso 3: insertar en heap temporal
            heap_temporal = []
            for restaurante in resultados:
                if restaurante['id'] != id_restaurante:
                    heapq.heappush(
                        heap_temporal,
                        (-restaurante['puntaje'],
                        restaurante['id'],
                        restaurante)
                    )
            # Paso 4: extraer top-3
            similares = []
            while heap_temporal and len(similares) < 3:
                _, _, restaurante = heapq.heappop(heap_temporal)
                similares.append(restaurante)

            return similares

        elif tipo == 'recientes':
            k = param or 10

            # Paso 1: obtener últimas inserciones
            ids_recientes = self.historial[-k:]   # O(k)

            # Paso 2: resolver información completa
            resultado = []
            for id_restaurante in ids_recientes:
                restaurante = self.catalogo.get(id_restaurante)  # O(1)
                if restaurante:
                    resultado.append(restaurante)

            return resultado

        else:
            raise ValueError(f"Tipo de solicitud desconocido: '{tipo}'")

    

if __name__ == "__main__":
    # Verificación de inicialización
    s = SistemaLimos()
    print("catalogo tipo:", type(s.catalogo))
    print("bst vacío:", s.bst_raiz is None) == []   
    print("cola vacía:", len(s.cola_recomendaciones) == 0)
    print("✅ Sistema Limos inicializado correctamente")

    # ── Casos de prueba ───────────────────────────────────────────
    s = SistemaLimos()
    # Caso 1: inserción normal
    s.agregar_contenido("ID001", "Ohana", 8.5, "Sushi")
    s.agregar_contenido("ID002", "Eskuinapa", 7.2, "Mariscos")
    s.agregar_contenido("ID003", "Dos de asada", 9.1, "Tacos")

    assert len(s.catalogo) == 3,    "dict debe tener 3 entradas"
    assert s.bst_raiz is not None,  "BST no debe estar vacío"
    assert len(s.historial) == 3,   "historial debe tener 3 entradas"

    # Caso 2: ID duplicado debe lanzar error
    try:
        s.agregar_contenido("ID001", "Duplicado", 5.0)
        assert False, "Debió lanzar ValueError"
    except ValueError:
        print("✅ Caso 2 OK: duplicado rechazado")

    # Caso 3: puntaje fuera de rango
    try:
        s.agregar_contenido("ID004", "Fuera", 11.5)
        assert False, "Debió lanzar ValueError"
    except ValueError:
        print("✅ Caso 3 OK: puntaje inválido rechazado")

    print("✅ Todos los casos de agregar_contenido pasaron")

    # ── Casos de prueba A-5 ────────────────────────────────────────
    s = SistemaLimos()
    for id, nombre, puntaje in [("M1","Alpha",8.5),("M2","Beta",7.2),
                            ("M3","Gamma",9.1),("M4","Delta",6.0)]:
        s.agregar_contenido(id, nombre, puntaje)

    r1 = s.procesar_solicitud('lookup', 'M1')
    assert r1['nombre'] == "Alpha", "lookup falló"
    r2 = s.procesar_solicitud('rango', (7.0, 9.0))
    assert len(r2) == 2, f"rango esperaba 2, obtuvo {len(r2)}"
    r3 = s.procesar_solicitud('top_n', 2)
    assert r3[0]['puntaje'] >= r3[1]['puntaje'], "top_n no ordenado"
    r4 = s.procesar_solicitud('historial', 2)
    assert len(r4) == 2, "historial falló"
    # r5 = s.procesar_solicitud('similares', 'M1')
    # assert isinstance(r5, list), \
    #     "similares debe devolver una lista"
    # for restaurante in r5:
    #     diferencia = abs(restaurante['puntaje'] - 8.5)
    #     assert diferencia <= 0.3, \
    #         "similares devolvió restaurante fuera del rango"
    # print("✅ similares OK")

    print("✅ procesar_solicitud: todos los casos pasaron")

    
# IA-REFLEXION-A: La IA sugirió que se mantuviera un historial de búsqueda (o de consultas). No es
# una caracterísitca esencial para el funcionamiento del sistema así que no la implementaremos. 
# Especialmente porque no tenemos mucho tiempo.