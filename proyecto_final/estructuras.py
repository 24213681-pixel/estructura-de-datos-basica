class NodoBST:
    def __init__(self, clave, valor):
        self.clave = clave
        self.valor = valor
        self.izq = None
        self.der = None

def _bst_insertar(self, nodo, clave, valor):
    if nodo is None:
        return NodoBST(clave, valor)
    if clave < nodo.clave:
        nodo.izq = _bst_insertar(self, nodo.izq, clave, valor)
    else:
        nodo.der = _bst_insertar(self, nodo.der, clave, valor)
    return nodo

def _bst_rango(self, nodo, minv, maxv, resultado):
        if nodo is None:
            return
        if minv < nodo.clave:   # podar izquierda si no puede contener resultados
            _bst_rango(self, nodo.izq, minv, maxv, resultado)
        if minv <= nodo.clave <= maxv:
            resultado.append(nodo.valor)
        if nodo.clave < maxv:   # podar derecha si no puede contener resultados
            _bst_rango(self, nodo.der, minv, maxv, resultado)