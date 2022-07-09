from unittest import result
import ManejadorBooleano as mb
msg1 = """Bienvenido al manejador de expresiones Boolenas Booly
inses Disponibles:
    - EVAL <orden> <expr> : Permite evaluar la expresion <expr>, que esta
                            escrita de acuerdo a <orden>.
    - MOSTRAR <orden> <expr> : Permite imprimir la expresion <expr>, que esta
                               escrita de acuerdo a <orden> en orden in-fijo.
    - SALIR: Permite salir de la simulacion.
"""

print(msg1)
hola = mb.ManejadorBooleano()
while True:
    ins = input(">>>") 

    ins = ins.split(" ")

    operacion = ins.pop(0)

    if operacion == "EVAL": 
        print(hola.evaluacion(" ".join(ins)))
    elif operacion == "MOSTRAR":
        print(hola.mostrar(hola.crearArbol(" ".join(ins))))
    elif operacion == "SALIR":
        print("Hasta luego")
        break
    else:
        print("ins no reconocida.")