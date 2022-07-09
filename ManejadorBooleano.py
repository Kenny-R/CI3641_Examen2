class nodo:
    def __init__(self,valor,padre,hijoIzq,hijoDer):
        self.valor = valor
        self.padre = padre
        self.hijoDer = hijoDer
        self.hijoIzq = hijoIzq

# Implementa un manejador de expresiones boolenas
class ManejadorBooleano:    
    def evaluacion(self, instruccion:str)->bool:
        
        expresion = instruccion.split(" ")
        orden = expresion.pop(0)   
        stack = []
        
        if orden == "PRE": expresion.reverse()
        
        for i in expresion: 
                if i == "true":
                    stack.append(True)
                elif i == "false":
                    stack.append(False)
                elif i == "^":
                    stack[-1] = not stack[-1]
                elif i == "=>":                    
                    operando = stack.pop()
                    if orden == "POST": 
                        stack[-1] = (not stack[-1]) or operando 
                    else:
                        stack[-1] = (not operando) or stack[-1]
                elif i == "&":
                        operando = stack.pop()
                        stack[-1] = operando and stack[-1]
                elif i == "|":
                        operando = stack.pop()
                        stack[-1] = operando or stack[-1]
        
        return stack.pop()

    def crearArbol(self,instruccion):
        expresion = instruccion.split(" ")
        orden = expresion.pop(0)   
        stack = []
        if orden == "POST": 
            for i in expresion: 
                    if i == "true":
                        stack.append(nodo("true",None,None,None))
                    elif i == "false":
                        stack.append(nodo("false",None,None,None))
                    elif i == "^":
                        stack[-1] = nodo(i,None,stack[-1],None)
                    elif i == "=>":                    
                        operando = stack.pop()
                        nuevoNodo = nodo(i,None,stack[-1],operando)
                        stack[-1].padre = nuevoNodo
                        operando.padre = nuevoNodo
                        stack[-1] = nuevoNodo
                    elif i == "&":
                            operando = stack.pop()
                            nuevoNodo = nodo(i,None,stack[-1],operando)
                            stack[-1].padre = nuevoNodo
                            operando.padre = nuevoNodo
                            stack[-1] = nuevoNodo
                    elif i == "|":
                            operando = stack.pop()
                            nuevoNodo = nodo(i,None,stack[-1],operando)
                            stack[-1].padre = nuevoNodo
                            operando.padre = nuevoNodo
                            stack[-1] = nuevoNodo
        else: 
            expresion.reverse()
            for i in expresion: 
                    if i == "true":
                        stack.append(nodo("true",None,None,None))
                    elif i == "false":
                        stack.append(nodo("false",None,None,None))
                    elif i == "^":
                        stack[-1] = nodo(i,None,stack[-1],None)
                    elif i == "=>":                    
                        operando = stack.pop()
                        nuevoNodo = nodo(i,None,operando,stack[-1])
                        stack[-1].padre = nuevoNodo
                        operando.padre = nuevoNodo
                        stack[-1] = nuevoNodo
                    elif i == "&":
                            operando = stack.pop()
                            nuevoNodo = nodo(i,None,operando,stack[-1])
                            stack[-1].padre = nuevoNodo
                            operando.padre = nuevoNodo
                            stack[-1] = nuevoNodo
                    elif i == "|":
                            operando = stack.pop()
                            nuevoNodo = nodo(i,None,operando,stack[-1])
                            stack[-1].padre = nuevoNodo
                            operando.padre = nuevoNodo
                            stack[-1] = nuevoNodo
        
        return stack.pop()
    
    def mostrar(self,arbol):

        if arbol.valor == "true" or arbol.valor == "false":
            return arbol.valor

        if arbol.padre ==  None:
            return f"{self.mostrar(arbol.hijoIzq)} {arbol.valor} {self.mostrar(arbol.hijoDer)}"
        
        if arbol.valor == "=>":
            if arbol.padre == "&" or arbol.padre == "|" or arbol.padre == "^":
                return f"({self.mostrar(arbol.hijoIzq)} => {self.mostrar(arbol.hijoDer)})"
            else:
                if arbol.padre.hijoIzq == arbol:
                    return f"({self.mostrar(arbol.hijoIzq)} => {self.mostrar(arbol.hijoDer)})"
                else:
                    return f"{self.mostrar(arbol.hijoIzq)} => {self.mostrar(arbol.hijoDer)}"          
        elif arbol.valor == "^":
            return f"^ {self.mostrar(arbol.hijoIzq)}"
        else:
            if arbol.padre.valor == arbol.valor:
                return f"{self.mostrar(arbol.hijoIzq)} {arbol.valor} {self.mostrar(arbol.hijoDer)}"
            else:
                if arbol.padre.hijoIzq == arbol:
                      return f"{self.mostrar(arbol.hijoIzq)} {arbol.valor} {self.mostrar(arbol.hijoDer)}"
                else:
                      return f"({self.mostrar(arbol.hijoIzq)} {arbol.valor} {self.mostrar(arbol.hijoDer)})"