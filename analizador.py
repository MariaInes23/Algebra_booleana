from nodos import Constante, Variable, No, Y, O

class AnalizadorLexico:
    def __init__(self, cadena):
        cadena = cadena.replace('’', "'").replace('´', "'")
        self.cadena = ''.join(ch for ch in cadena if ch not in [' ', '\t', '\n'])
        self.i = 0

    def mirar(self):
        return self.cadena[self.i] if self.i < len(self.cadena) else None

    def obtener(self):
        ch = self.mirar()
        if ch is not None:
            self.i += 1
        return ch


def analizar_expresion(texto):
    lx = AnalizadorLexico(texto)
    nodo = analizar_o(lx)
    if lx.mirar() is not None:
        raise ValueError(f"Entrada inesperada en posición {lx.i}: '{lx.mirar()}'")
    return nodo


def analizar_o(lx):
    izquierda = analizar_y(lx)
    while lx.mirar() == '+':
        lx.obtener()
        derecha = analizar_y(lx)
        izquierda = O(izquierda, derecha)
    return izquierda


def analizar_y(lx):
    izquierda = analizar_factor(lx)
    while True:
        ch = lx.mirar()
        if ch is None or ch in [')', '+']:
            break
        if ch == '*':
            lx.obtener()
            derecha = analizar_factor(lx)
            izquierda = Y(izquierda, derecha)
        else:
            if ch.isalpha() or ch == '(' or ch == '0' or ch == '1' or ch == '~' or ch == "'":
                derecha = analizar_factor(lx)
                izquierda = Y(izquierda, derecha)
            else:
                break
    return izquierda


def analizar_factor(lx):
    ch = lx.mirar()
    if ch is None:
        raise ValueError("Expresión incompleta.")

    if ch == '(':
        lx.obtener()
        nodo = analizar_o(lx)
        if lx.obtener() != ')':
            raise ValueError("Falta cerrar paréntesis.")
        if lx.mirar() == "'":
            lx.obtener()
            return No(nodo)
        return nodo

    if ch == '0' or ch == '1':
        lx.obtener()
        nodo = Constante(int(ch))
        if lx.mirar() == "'":
            lx.obtener()
            return No(nodo)  
        return nodo

    if ch == '~':  
        lx.obtener()
        return No(analizar_factor(lx))

    if ch == "'": 
        lx.obtener()
        return No(analizar_factor(lx))

    if ch.isalpha():
        nombre = lx.obtener()
        nodo = Variable(nombre.upper())
        if lx.mirar() == "'":
            lx.obtener()
            nodo = No(nodo)
        return nodo

    raise ValueError(f"Carácter inesperado: '{ch}' en posición {lx.i}")
