import random
from sistema_limos import SistemaLimos

# VALIDA: Casos de prueba V-8
# ── 2 CASOS DADOS (ejemplo de formato) ────────────────────────

def caso_v1_lookup_inexistente(sistema):
    """Caso dado 1: lookup de ID que no existe → debe devolver None"""
    r = sistema.procesar_solicitud('lookup', 'ID_QUE_NO_EXISTE_XYZ')
    assert r is None, f"Esperado: None | Obtenido: {r}"
    print("✅ V-1: lookup inexistente → None")

def caso_v2_insercion_consistente(sistema):
    """Caso dado 2: insertar y verificar que los 3 índices lo ven"""
    sistema.agregar_contenido("VTEST_99", "Contenido Prueba", 5.5)
    en_dict = "VTEST_99" in sistema.catalogo
    en_bst  = len(sistema.procesar_solicitud('rango', (5.4, 5.6))) > 0
    en_hist = "VTEST_99" in sistema.historial
    assert en_dict and en_bst and en_hist,         f"Esperado: visible en los 3 índices | dict={en_dict} BST={en_bst} hist={en_hist}"
    print("✅ V-2: inserción consistente en dict, BST e historial")

# ── 3 CASOS A DISEÑAR POR EL EQUIPO ──────────────────────────
# Instrucciones:
#   1. Elegir 3 situaciones límite del sistema PROPIO del proyecto
#   2. Implementar cada caso como función con docstring describiendo
#      qué edge case prueba y por qué es relevante para el proyecto
#   3. Incluir: entrada → acción → assert con mensaje descriptivo
#
# Sugerencias (elegir las que apliquen al proyecto, o inventar otras):
#   - ¿Qué pasa si el catálogo está vacío y se pide top_n(5)?
#   - ¿Qué pasa si se pide un rango donde min > max?
#   - ¿Qué pasa con IDs que tienen espacios o caracteres especiales?
#   - ¿Qué pasa si top_n = 0?
#   - ¿Puntaje 0.0 y puntaje 10.0 exactos se almacenan correctamente?
#   - ¿Qué devuelve historial(k) si k > número de inserciones realizadas?

def caso_v3_catalogo_vacio(sistema):
    """
    Edge case:
        Se ejecuta una consulta top_n sobre un sistema sin ningún restaurante registrado.
    Relevancia:
        Este caso valida el comportamiento del sistema cuando está en su estado inicial.
    Resultado esperado:
        El sistema debe devolver una lista vacía sin errores ni excepciones.
    Resultado real:
        []
    """
    sistema_vacio = SistemaLimos()
    r = sistema_vacio.procesar_solicitud('top_n', 5)
    assert r == [], f"Esperado: [] | Obtenido: {r}"
    print("✅ V-3: top_n en catálogo vacío")

def caso_v4_top_n_cero(sistema):
    """
    Edge case:
        Se solicita top_n con valor 0, es decir, la función no devolverá ningún valor ni procesará datos
    Relevancia:
        Este caso valida manejo de entradas límite para asegurarse de que el sistema no falle en casos inesperados
    Resultado esperado:
        El sistema debe devolver una lista vacía sin procesar elementos.
    Resultado real:
        []
    """
    r = sistema.procesar_solicitud('top_n', 0)
    assert r == [], f"Esperado: [] | Obtenido: {r}"
    print("✅ V-4: top_n = 0")

def caso_v5_ids_especiales(sistema):
    """
    Edge case:
        Inserción y consulta de IDs con espacios, símbolos y caracteres Unicode.
    Relevancia:
        En sistemas reales, los IDs pueden venir de fuentes externas con formatos no controlados.
    Resultado esperado:
        El sistema debe almacenar todos los ID's sin importar el tipo de caracteres que tengan
    Resultado real:
        {'id': 'ID 123', 'nombre': 'Restaurante Espaciado', 'puntaje': 8.0, 'categoria': None}
    """
    sistema.agregar_contenido("ID 123", "Restaurante Espaciado", 8.0)
    sistema.agregar_contenido("ID@#$/ABC", "Restaurante Especial", 7.5)
    sistema.agregar_contenido("ÑANDÚ-01", "Restaurante Unicode", 9.0)
    r1 = sistema.procesar_solicitud('lookup', "ID 123")
    r2 = sistema.procesar_solicitud('lookup', "ID@#$/ABC")
    r3 = sistema.procesar_solicitud('lookup', "ÑANDÚ-01")
    assert r1 is not None and r2 is not None and r3 is not None, \
        "Fallo en manejo de IDs especiales"
    print("✅ V-5: IDs con caracteres especiales")

# VALIDA: verificar_invariante_cruzada v 9
# FUNCIÓN PRE-IMPLEMENTADA — no modificar
def contar_nodos_bst(nodo):
    if nodo is None: return 0
    return 1 + contar_nodos_bst(nodo.izq) + contar_nodos_bst(nodo.der)

def verificar_invariante_cruzada(sistema):
    """
    Verifica 3 invariantes:
      1. |dict| == |BST|  → todas las inserciones llegaron a ambas estructuras
      2. |historial| == |dict| → el historial tiene una entrada por cada inserción
      3. El BST está en orden (inorder ascendente)
    """
    errores = []
    n_dict = len(sistema.catalogo)
    n_bst  = contar_nodos_bst(sistema.bst_raiz)
    n_hist = len(sistema.historial)

    if n_dict != n_bst:
        errores.append(f"Inv-1 ❌: dict tiene {n_dict} pero BST tiene {n_bst} nodos")

    if n_hist != n_dict:
        errores.append(f"Inv-2 ❌: historial tiene {n_hist} pero dict tiene {n_dict}")

    # Verificar orden BST vía inorder
    inorder_result = []
    def inorder(nodo):
        if nodo: inorder(nodo.izq); inorder_result.append(nodo.clave); inorder(nodo.der)
    inorder(sistema.bst_raiz)
    if inorder_result != sorted(inorder_result):
        errores.append("Inv-3 ❌: BST no está en orden ascendente")

    if not errores:
        print(f"✅ Invariante cruzada OK: {n_dict} elementos en todos los índices")
    return errores

if __name__ == "__main__":
    s = SistemaLimos()
    for i in range(15):
        s.agregar_contenido(f"P{i}", f"Pelicula_{i}", round(i*0.6+1.0, 1))

    # Casos dados
    caso_v1_lookup_inexistente(s)
    caso_v2_insercion_consistente(s)
    # Casos del equipo 
    caso_v3_catalogo_vacio(s)
    caso_v4_top_n_cero(s)
    caso_v5_ids_especiales(s)
    print("✅ V-8: todos los casos ejecutados")

    # ── Ejecutar verificación tras 50 operaciones ──────────────────
    s = SistemaLimos()
    for i in range(50):
        s.agregar_contenido(f"ID{i:03d}", f"Titulo_{i}",
                            round(random.uniform(1.0, 10.0), 2))

    errores = verificar_invariante_cruzada(s)
    if errores:
        for e in errores: print(e)

# VALIDA: Invariante cruzada OK: 50 elementos en todos los índices
    # Invariante 1 (dict == BST):     ✅ 
    # Invariante 2 (hist == dict):    ✅ 
    # Invariante 3 (BST en orden):    ✅

# IA-REFLEXION-V: Respuesta de la IA: En un sistema real puede ocurrir que un nodo se guarde en el
# dict, pero falle la inserción en el BST por un error inesperado. luego otro nodo distinto 
# se inserta correctamente y los tamaños vuelven a coincidir.
# Sí es un escenario realista para el proyecto porque la verificación solo compara el tamaño de las
# estructuras pero no su contenido. El caso que menciona la IA puede ocurrir con la inserción
# de restaurantes. Creemos que es necesario que se agregue una comprobación adicional o más completa.