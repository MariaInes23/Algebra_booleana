class Nodo:
    def copiar(self):
        raise NotImplementedError

class Constante(Nodo):
    def __init__(self, valor):  
        self.valor = 1 if str(valor) == '1' else 0

    def __eq__(self, otro): 
        return isinstance(otro, Constante) and self.valor == otro.valor

    def __hash__(self): 
        return hash(('Constante', self.valor))

    def __str__(self): 
        return '1' if self.valor == 1 else '0'

    def copiar(self): 
        return Constante(self.valor)


class Variable(Nodo):
    def __init__(self, nombre):
        self.nombre = nombre

    def __eq__(self, otro): 
        return isinstance(otro, Variable) and self.nombre == otro.nombre

    def __hash__(self): 
        return hash(('Variable', self.nombre))

    def __str__(self): 
        return self.nombre

    def copiar(self): 
        return Variable(self.nombre)


class No(Nodo):
    def __init__(self, hijo):
        self.hijo = hijo

    def __eq__(self, otro): 
        return isinstance(otro, No) and self.hijo == otro.hijo

    def __hash__(self): 
        return hash(('No', self.hijo))

    def __str__(self):
        if isinstance(self.hijo, Variable):
            return f"{self.hijo}'"
        return f"({self.hijo})'"

    def copiar(self): 
        return No(self.hijo.copiar())


class Y(Nodo): 
    def __init__(self, *hijos):
        operaciones = []
        for h in hijos:
            if isinstance(h, Y):
                operaciones.extend(h.hijos)
            else:
                operaciones.append(h)

        unico = []
        visto = set()
        for o in operaciones:
            if o not in visto:
                unico.append(o)
                visto.add(o)

        self.hijos = sorted(unico, key=lambda x: str(x))

    def __eq__(self, otro):
        return isinstance(otro, Y) and self.hijos == otro.hijos

    def __hash__(self):
        return hash(('Y', tuple(self.hijos)))

    def __str__(self):

        partes = []
        for h in self.hijos:
            if isinstance(h, O):
                partes.append(f"({h})")
            else:
                partes.append(str(h))
        return ''.join(partes)

    def copiar(self): 
        return Y(*[h.copiar() for h in self.hijos])


class O(Nodo):  
    def __init__(self, *hijos):
        operaciones = []
        for h in hijos:
            if isinstance(h, O):
                operaciones.extend(h.hijos)
            else:
                operaciones.append(h)

        unico = []
        visto = set()
        for o in operaciones:
            if o not in visto:
                unico.append(o)
                visto.add(o)

        self.hijos = sorted(unico, key=lambda x: str(x))

    def __eq__(self, otro):
        return isinstance(otro, O) and self.hijos == otro.hijos

    def __hash__(self):
        return hash(('O', tuple(self.hijos)))

    def __str__(self):
        return ' + '.join(str(h) for h in self.hijos)

    def copiar(self): 
        return O(*[h.copiar() for h in self.hijos])
