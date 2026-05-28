import time, random, statistics
from sistema_limos import SistemaLimos

# ── REFLEXIONA-1: Benchmark estabilizado con warm-up y P95 ────
# FUNCIÓN PRE-IMPLEMENTADA — no modificar, solo ejecutar
#
# ¿Por qué no basta un simple loop con perf_counter()?
# Un único loop de 1000 iteraciones suma tiempos contaminados por:
#   - Warm-up: las primeras llamadas pueden activar caché del SO o
#     JIT internos de CPython (para extensiones C como heapq).
#   - GC: Python puede ejecutar el recolector de basura durante el loop.
#   - Jitter del SO: interrupciones del sistema operativo.
# Solución: descartar warm-up + tomar el percentil 95 de muestras
# individuales para ignorar outliers por GC/SO.

def medir_p95(fn, repeticiones=200, warmup=20):
    """
    Mide el tiempo de fn() con rigor estadístico.
    - warmup: primeras N llamadas descartadas (caché/JIT)
    - repeticiones: muestras reales a recoger
    - retorna: (mediana_ms, p95_ms, min_ms)
    """
    # Fase warm-up: descartar
    for _ in range(warmup):
        fn()

    # Fase de medición: una muestra por iteración
    muestras = []
    for _ in range(repeticiones):
        t0 = time.perf_counter()
        fn()
        muestras.append((time.perf_counter() - t0) * 1000)

    muestras.sort()
    p95_idx = int(0.95 * repeticiones)
    return (statistics.median(muestras),
            muestras[p95_idx],
            muestras[0])

def benchmark_sistema(n):
    sistema = SistemaLimos()
    ids = []
    for i in range(n):
        id_ = f"C{i:05d}"
        sistema.agregar_contenido(id_, f"T_{i}", round(random.uniform(1.0,10.0),2))
        ids.append(id_)

    id_muestra = random.choice(ids)

    # Medir cada operación con P95
    r_lookup = medir_p95(lambda: sistema.procesar_solicitud('lookup', id_muestra))
    r_rango  = medir_p95(lambda: sistema.procesar_solicitud('rango', (7.0, 9.0)))
    r_topn   = medir_p95(lambda: sistema.procesar_solicitud('top_n', 10))
    r_simi   = medir_p95(lambda: sistema.procesar_solicitud('similares', id_muestra)) 
    
    return {'lookup': r_lookup, 'rango': r_rango, 'top_n': r_topn, 'similares': r_simi}

if __name__ == "__main__":
    print(f"{'Operación':<12} {'n':>7} {'Mediana':>10} {'P95':>10} {'Mín':>10}")
    print("-" * 55)
    for n in [1_000, 10_000]:
        r = benchmark_sistema(n)
        for op, (med, p95, mn) in r.items():
            print(f"{op:<12} {n:>7,} {med:>9.4f}ms {p95:>9.4f}ms {mn:>9.4f}ms")

""" 
REFLEXIONA-1: (completar con los resultados reales — usar columna Mediana)

| Operación | n=1,000 Mediana | n=1,000 P95 | n=10,000 Mediana | n=10,000 P95 | Complejidad |
|-----------|-----------------|-------------|------------------|--------------|-------------|
| lookup    |      0.0001 ms  |    0.0001 ms|      0.0001 ms   |    0.0001 ms | O(1) amort. |
| rango     |      0.0294 ms  |    0.0308 ms|      0.2811 ms   |    0.2951 ms | O(log n+k)  |
| top_n     |      0.0822 ms  |    0.906  ms|      1.2978 ms   |    1.3598 ms | O(n log n)  |
| similares |      0.230  ms  |    0.0234 ms|      0.2864 ms   |    0.3120 ms | O(k log k)  |

Observación sobre P95 vs Mediana: No parece haber mucha diferencia (~1.10x), pero P95 siempre es mayor
(¿La diferencia P95-Mediana es grande? ¿A qué se atribuye?) 
Cuello de botella: top_n      Big-O: O(n log n)  
"""

""" 
REFLEXIONA-2: 
Operacion: "Recomendar restaurantes similares por calificacion"
─────────────────────────────────────────────────────
Paso 1: dict.get(id_restaurante)           O(1) 
Paso 2: bst.buscar_rango(r-0.3, r+0.3)     O(log n + k)
Paso 3: heapq.heappush()                   O(k log k) 
Paso 4: heapq.heappop()                    O(3 log k)

T(n) = O(1) + O(log n + k) + O(k log k) + O(3 log k) 
= O(k log k) ← término dominante

Factor teórico  n=1,000→10,000: (1000 (log 1000)) / (100 log 100) ≈ 15x
Factor medido   n=1,000→10,000: 0.2864 / 0.0230 = 12.45x
¿Consistente?   No es exacto, pero sí es consistente. La diferencia entre la teoría y la realidad es de
solo 2.55 
"""

# IA-REFLEXION-R: La IA nos muestra que BST puede degradar mucho al programa cuando el rango es muy grande
# pero en la realidad no creemos que tenga mucho impacto ya que generalmente la búsqueda por rango se hace 
# con intervalos pequeños.