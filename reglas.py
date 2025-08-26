from nodos import Constante, Variable, No, Y, O 

def es_complemento(a, b): 
    return (isinstance(a, No) and a.hijo == b) or (isinstance(b, No) and b.hijo == a) 

def contiene(nodo, objetivo): 
    if nodo == objetivo: 
        return True 
    if isinstance(nodo, (Y, O)): 
        return any(contiene(c, objetivo) for c in nodo.hijos) 
    if isinstance(nodo, No): 
        return contiene(nodo.hijo, objetivo) 
    return False 

def a_cadena(expr): 
    return str(expr) 

def aplicar_reglas_una_vez(nodo): 

    if isinstance(nodo, No): 
        nuevo_hijo, regla = aplicar_reglas_una_vez(nodo.hijo) 
        if regla: 
            return (No(nuevo_hijo), regla) 

    if isinstance(nodo, Y) or isinstance(nodo, O): 
        for idx, h in enumerate(nodo.hijos): 
            nuevo_h, regla = aplicar_reglas_una_vez(h) 
            if regla: 
                nuevos_hijos = list(nodo.hijos) 
                nuevos_hijos[idx] = nuevo_h 
                nodo2 = Y(*nuevos_hijos) if isinstance(nodo, Y) else O(*nuevos_hijos) 
                return (nodo2, regla) 

    if isinstance(nodo, O): 
        pass   
    if isinstance(nodo, Y): 
        pass 

    if isinstance(nodo, O): 
        cs = nodo.hijos 
        for i in range(len(cs)): 
            for j in range(i+1, len(cs)): 
                if es_complemento(cs[i], cs[j]): 
                    return (Constante(1), "Complemento: A + A' = 1") 
    if isinstance(nodo, Y): 
        cs = nodo.hijos 
        for i in range(len(cs)): 
            for j in range(i+1, len(cs)): 
                if es_complemento(cs[i], cs[j]): 
                    return (Constante(0), "Complemento: A · A' = 0") 

    if isinstance(nodo, Y): 
        if any(isinstance(c, Constante) and c.valor == 1 for c in nodo.hijos): 
            resto = [c for c in nodo.hijos if not (isinstance(c, Constante) and c.valor == 1)] 
            if not resto: 
                resto = [Constante(1)] 
            return ((resto[0] if len(resto) == 1 else Y(*resto)), "Identidad: A · 1 = A") 
    if isinstance(nodo, O): 
        if any(isinstance(c, Constante) and c.valor == 0 for c in nodo.hijos): 
            resto = [c for c in nodo.hijos if not (isinstance(c, Constante) and c.valor == 0)] 
            if not resto: 
                resto = [Constante(0)] 
            return ((resto[0] if len(resto) == 1 else O(*resto)), "Identidad: A + 0 = A") 

    if isinstance(nodo, O): 
        if any(isinstance(c, Constante) and c.valor == 1 for c in nodo.hijos): 
            return (Constante(1), "Dominación: A + 1 = 1") 
    if isinstance(nodo, Y): 
        if any(isinstance(c, Constante) and c.valor == 0 for c in nodo.hijos): 
            return (Constante(0), "Dominación: A · 0 = 0") 

    if isinstance(nodo, Y): 
        ors = [c for c in nodo.hijos if isinstance(c, O)] 
        if ors: 
            or_nodo = ors[0] 
            otros = [c for c in nodo.hijos if c is not or_nodo] 
            nuevos = [] 
            for termino in or_nodo.hijos: 
                nuevos.append(Y(*(otros + [termino]))) 
            return (O(*nuevos), "Distributiva: A(B+C)=AB+AC") 

    if isinstance(nodo, O): 
        cs = nodo.hijos 
        for i in range(len(cs)): 
            for j in range(i+1, len(cs)): 
                a, b = cs[i], cs[j] 
                if isinstance(a, Y) and isinstance(b, Y): 
                    set_a = set(a.hijos) 
                    set_b = set(b.hijos) 
                    comunes = list(set_a.intersection(set_b)) 
                    if comunes: 
                        f = comunes[0] 
                        resto_a = [x for x in a.hijos if x != f] 
                        resto_b = [x for x in b.hijos if x != f] 
                        izq = Y(*resto_a) if len(resto_a) > 1 else (resto_a[0] if resto_a else Constante(1)) 
                        der = Y(*resto_b) if len(resto_b) > 1 else (resto_b[0] if resto_b else Constante(1)) 
                        nuevo = Y(f, O(izq, der)) 
                        otros = [cs[k] for k in range(len(cs)) if k not in (i, j)] 
                        if otros: 
                            return (O(nuevo, *otros), "Factorización: AB+AC=A(B+C)") 
                        else: 
                            return (nuevo, "Factorización: AB+AC=A(B+C)") 

    if isinstance(nodo, O): 
        cs = nodo.hijos 
        for i in range(len(cs)): 
            for j in range(len(cs)): 
                if i == j: 
                    continue 
                x, y = cs[i], cs[j] 
                if isinstance(y, Y) and any(ch == x for ch in y.hijos): 
                    otro = [ch for ch in y.hijos if ch != x] 
                    Y_ = otro[0] if len(otro) == 1 else Y(*otro) 
                    nuevo = Y(x, O(Constante(1), Y_)) 
                    otros = [cs[k] for k in range(len(cs)) if k not in (i, j)] 
                    if otros: 
                        return (O(nuevo, *otros), "Factorización: A + A·B = A(1+B)") 
                    return (nuevo, "Factorización: A + A·B = A(1+B)") 

    if isinstance(nodo, O): 
        cs = nodo.hijos 
        for i in range(len(cs)): 
            for j in range(len(cs)): 
                if i == j: 
                    continue 
                x, y = cs[i], cs[j] 
                if isinstance(y, Y) and any(ch == x for ch in y.hijos): 
                    return (x.copiar(), "Absorción: A + A·B = A") 
    if isinstance(nodo, Y): 
        cs = nodo.hijos 
        for i in range(len(cs)): 
            for j in range(len(cs)): 
                if i == j: 
                    continue 
                x, y = cs[i], cs[j] 
                if isinstance(y, O) and any(ch == x for ch in y.hijos): 
                    return (x.copiar(), "Absorción: A(A+B) = A") 

    if isinstance(nodo, No): 
        c = nodo.hijo 
        if isinstance(c, Y): 
            return (O(*[No(k) for k in c.hijos]), "De Morgan: ~(AB)=A'+B'") 
        if isinstance(c, O): 
            return (Y(*[No(k) for k in c.hijos]), "De Morgan: ~(A+B)=A'B'") 

    return (nodo, None) 


def simplificar_con_pasos(expr): 
    pasos = [] 
    actual = expr 
    pasos.append(("Expresión inicial", a_cadena(actual))) 
    MAX_PASOS = 60 
    for _ in range(MAX_PASOS): 
        nuevo, regla = aplicar_reglas_una_vez(actual) 
        if not regla: 
            break 
        pasos.append((regla, a_cadena(nuevo))) 
        actual = nuevo 
    return pasos, actual
