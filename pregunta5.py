import manejadorDeTiposMk2 as mdt
msg1 = """Bienvenido al sistema de tipos Typy
intruciones Disponibles:
    - ATOMICO <nombre> <representacion> <alineacion> : Define un nuevo tipo atomico de nombre <nombre>, cuya representacion
                                                       ocupa <representacion> bytes y debe esta alineado a <alineacion> bytes.
                                                       
    - STRUCT <nombre> [<tipo>] : Define un nuevo registro de nombre <nombre>. La definición de los campos del
                                  registro viene dada por la lista en [<tipo>].

    - UNION <nombre> [<tipo>]: Define un nuevo registro variante de nombre <nombre>. La definición de los campos del 
                               registro variante viene dada por la lista en [<tipo>]. 
    - DESCRIBIR <nombre>: Da la informacion del tipo que tiene por nombre <nombre>.

    - SALIR: Permite salir de la simulacion.
"""

print(msg1)
manejador = mdt.manejadorDeTipos()
while True:
    ins = input(">>>") 

    ins = ins.split(" ")

    operacion = ins.pop(0)

    if operacion == "ATOMICO": 
        manejador.crear_atomico(ins[0],ins[1],ins[2])
    elif operacion == "STRUCT":
        manejador.crear_struct(ins.pop(0),ins)
    elif operacion == "UNION":
        manejador.crear_union(ins.pop(0),ins)
    elif operacion == "DESCRIBIR":
        manejador.descibir(ins.pop(0))
    elif operacion == "SALIR":
        print("Hasta luego")
        break
    else:
        print("intrucion no reconocida.")