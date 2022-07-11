import math

class atomico:
    def __init__(self,nombre,representacion,alineacion) -> None:
        self.nombre = nombre
        self.representacion = representacion
        self.alineacion = alineacion

class struct:
    def __init__(self,nombre,tipos) -> None:
        self.nombre= nombre
        self.tipos = tipos
        self.alineacion = []
        self.tamanio = []
        self.desperdiciado = []

class union:
    def __init__(self,nombre,tipos) -> None:
        self.nombre= nombre
        self.tipos = tipos
        self.alineacion = []
        self.tamanio = []
        self.desperdiciado = []

class manejadorDeTipos:

    def __init__(self):
        self.atomicos = {}
        self.structs =  {}
        self.unions = {}
    
    # Permite crear un objeto de tipo atomico que representaria 
    # un tipo del sistema de tipos.
    def crear_atomico(self,nombre,representacion,alineacion):
        if nombre not in self.atomicos.keys() and nombre not in self.structs.keys() and nombre not in self.unions.keys() :
            self.atomicos[nombre] = atomico(nombre,int(representacion),int(alineacion))
            print(f"Se creo el Atomico {nombre}")
        else:
            print(f"Ya existe el tipo {nombre}") 
    
    # Permite crear un objeto de tipo struct que representa un registro
    # este registro almacenara su tamaño, alineacion y desperdicio basandose
    # en 3 formas de almacenar un registro en memoria.
    def crear_struct(self,nombre:str,tipos:list):
        if nombre not in self.atomicos.keys() and nombre not in self.structs.keys() and nombre not in self.unions.keys():
            for i in tipos:
                if i not in self.atomicos.keys() and i not in self.structs.keys() and i not in self.unions.keys():
                    print(f"No existe el tipo {i}")
                    return
            
            nuevoStruct = struct(nombre,tipos)

            # calculamos el espacio si almacenamos los tipos en el orden que se declararon
            espacioNormal = self.calcular_espacio_struct(tipos,"Normal")
            
            if tipos[0] in self.atomicos.keys(): nuevoStruct.alineacion.append(self.atomicos[tipos[0]].alineacion)
            elif tipos[0] in self.structs.keys(): nuevoStruct.alineacion.append(self.structs[tipos[0]].alineacion[0])
            elif tipos[0] in self.unions.keys(): nuevoStruct.alineacion.append(self.unions[tipos[0]].alineacion[0])
            
            nuevoStruct.tamanio.append(espacioNormal[0])
            nuevoStruct.desperdiciado.append(espacioNormal[1])

            # calculamos la combinacion de tipos que haga que el espacio desperdiciado sea menor
            min = math.inf
            espacioOptimizado = ()
            mejorCombinacion = []
            for m in self.combinaciones(tipos):
                valor = self.calcular_espacio_struct(m,"Optimizado")
                if valor[1] < min: 
                    espacioOptimizado = valor
                    mejorCombinacion = m
                    min = valor[1]

                if min == 0: break
            
            if mejorCombinacion[0] in self.atomicos.keys(): nuevoStruct.alineacion.append(self.atomicos[mejorCombinacion[0]].alineacion)
            elif mejorCombinacion[0] in self.structs.keys(): nuevoStruct.alineacion.append(self.structs[mejorCombinacion[0]].alineacion[1])
            elif mejorCombinacion[0] in self.unions.keys(): nuevoStruct.alineacion.append(self.unions[mejorCombinacion[0]].alineacion[1])
            
            nuevoStruct.tamanio.append(espacioOptimizado[0])
            nuevoStruct.desperdiciado.append(espacioOptimizado[1])

            # Calculamos el espacio sin respetar alineaciones
            espacioSinAlineacion = 0
            for i in tipos:
                if i in self.atomicos.keys():
                    espacioSinAlineacion += self.atomicos[i].representacion
                elif i in self.structs.keys():
                    espacioSinAlineacion += self.structs[i].tamanio[2]
                elif i in self.unions.keys():
                    espacioSinAlineacion += self.unions[i].tamanio[2]
            
            if tipos[0] in self.atomicos.keys(): nuevoStruct.alineacion.append(self.atomicos[tipos[0]].alineacion)
            elif tipos[0] in self.structs.keys(): nuevoStruct.alineacion.append(self.structs[tipos[0]].alineacion[2])
            elif tipos[0] in self.unions.keys(): nuevoStruct.alineacion.append(self.unions[tipos[0]].alineacion[2])
            
            nuevoStruct.tamanio.append(espacioSinAlineacion)
            nuevoStruct.desperdiciado.append(0)
            
            self.structs[nombre] = nuevoStruct
            print(f"Se creo el Struct {nombre}")

        else:
            print(f"ya existe el tipo {nombre}")
    
    # Permite crear un objeto de tipo union que representa un tipo Union 
    # este union almacenara su tamaño, alineacion y desperdicio basandose
    # en 3 formas de almacenar un registro en memoria. Si el union no 
    # contiene ningun registro las 3 versiones del union seran iguales
    def crear_union(self, nombre, tipos):
        if nombre in self.atomicos.keys() or nombre in self.structs.keys() or nombre in self.unions.keys():
            print(f"Ya existe el tipo {nombre}")
            return
        
        desperdicioNormal = 0
        desperdicioOptimizado = 0
        desperdicioSinAlineaciones = 0

        alineacionesNormal = []
        alineacionesOptimizado = []
        alineacionesSinAlineaciones = []

        tamanioNormal = 0
        tamanioOptimizado = 0
        tamanioSinAlineaciones = 0
        for i in tipos:
            if i in self.atomicos.keys():
                alineacionesNormal.append(self.atomicos[i].alineacion)
                alineacionesSinAlineaciones.append(self.atomicos[i].alineacion)
                alineacionesOptimizado.append(self.atomicos[i].alineacion)
                if tamanioNormal < self.atomicos[i].representacion: tamanioNormal = self.atomicos[i].representacion
                if tamanioOptimizado < self.atomicos[i].representacion: tamanioOptimizado = self.atomicos[i].representacion
                if tamanioSinAlineaciones < self.atomicos[i].representacion: tamanioSinAlineaciones = self.atomicos[i].representacion

            elif i in self.structs.keys():
                alineacionesNormal.append(self.structs[i].alineacion[0])
                alineacionesOptimizado.append(self.structs[i].alineacion[1])
                alineacionesSinAlineaciones.append(self.structs[i].alineacion[2])
                
                if desperdicioNormal > self.structs[i].desperdiciado[0]: desperdicioNormal = self.structs[i].desperdiciado[0]
                if desperdicioOptimizado > self.structs[i].desperdiciado[1]: desperdicioOptimizado = self.structs[i].desperdiciado[1]
                if desperdicioSinAlineaciones > self.structs[i].desperdiciado[2]: desperdicioSinAlineaciones = self.structs[i].desperdiciado[2]

                if tamanioNormal < self.structs[i].tamanio[0]: tamanioNormal = self.structs[i].tamanio[0]
                if tamanioOptimizado < self.structs[i].tamanio[1]: tamanioOptimizado = self.structs[i].tamanio[1]
                if tamanioSinAlineaciones < self.structs[i].tamanio[2]: tamanioSinAlineaciones = self.structs[i].tamanio[2]

            elif i in self.unions.keys():
                alineacionesNormal.append(self.unions[i].alineacion[0])
                alineacionesOptimizado.append(self.unions[i].alineacion[1])
                alineacionesSinAlineaciones.append(self.unions[i].alineacion[2])
                
                if desperdicioNormal > self.unions[i].desperdiciado[0]: desperdicioNormal = self.unions[i].desperdiciado[0]
                if desperdicioOptimizado > self.unions[i].desperdiciado[1]: desperdicioOptimizado = self.unions[i].desperdiciado[1]
                if desperdicioSinAlineaciones > self.unions[i].desperdiciado[2]: desperdicioSinAlineaciones = self.unions[i].desperdiciado[2]

                if tamanioNormal < self.unions[i].tamanio[0]: tamanioNormal = self.unions[i].tamanio[0]
                if tamanioOptimizado < self.unions[i].tamanio[1]: tamanioOptimizado = self.unions[i].tamanio[1]
                if tamanioSinAlineaciones < self.unions[i].tamanio[2]: tamanioSinAlineaciones = self.unions[i].tamanio[2]
            
        
        nuevoUnion = union(nombre,tipos)

        nuevoUnion.alineacion.append(math.lcm(*alineacionesNormal)) 
        nuevoUnion.alineacion.append(math.lcm(*alineacionesOptimizado)) 
        nuevoUnion.alineacion.append(math.lcm(*alineacionesSinAlineaciones)) 

        nuevoUnion.desperdiciado.append(desperdicioNormal)
        nuevoUnion.desperdiciado.append(desperdicioOptimizado)
        nuevoUnion.desperdiciado.append(desperdicioSinAlineaciones)

        nuevoUnion.tamanio.append(tamanioNormal)
        nuevoUnion.tamanio.append(tamanioOptimizado)
        nuevoUnion.tamanio.append(tamanioSinAlineaciones)

        self.unions[nombre] = nuevoUnion

        print(f"Se creo el Union {nombre}")
    
    def calcular_espacio_struct(self,tipos:list, tipoEspacio): 
        desperdiciado = 0
        byte = 0
        tamanio = 0
        for i in tipos:
            ocupado = 0
            # encontramos la alineacion y el espacio que ocupara
            if i in self.atomicos.keys():
                alineacion = self.atomicos[i].alineacion
                ocupado += self.atomicos[i].representacion
            elif i in self.structs.keys():
                if tipoEspacio == "Normal":
                    alineacion = self.structs[i].alineacion[0]
                    ocupado += self.structs[i].tamanio[0]
                elif tipoEspacio == "NoAlineacion":
                    alineacion = self.structs[i].alineacion[1]
                    ocupado += self.structs[i].tamanio[1]
                elif tipoEspacio == "Optimizado":
                    alineacion = self.structs[i].alineacion[2]
                    ocupado += self.structs[i].tamanio[2]
            elif i in self.unions.keys():
                if tipoEspacio == "Normal":
                    alineacion = self.unions[i].alineacion[0]
                    ocupado += self.unions[i].tamanio[0]
                elif tipoEspacio == "NoAlineacion":
                    alineacion = self.unions[i].alineacion[1]
                    ocupado += self.unions[i].tamanio[1]
                elif tipoEspacio == "Optimizado":
                    alineacion = self.unions[i].alineacion[2]
                    ocupado += self.unions[i].tamanio[2]
            
            # encontramos donde poner el tipo
            while byte % alineacion != 0:
                desperdiciado += 1
                byte += 1
            
            # sumamos el espacio ocupado
            byte += ocupado
            
            
            tamanio += ocupado
        tamanio += desperdiciado
        return (tamanio,desperdiciado)
    
    # Permite rodar por todas las posiciones de una lista
    # un valor especifico
    def combinacionesAux(self, e ,ls):
        yield [e, *ls]
        if ls:
            for i in self.combinacionesAux(e,ls[1:]):
                yield [ls[0],*i]

    # Permite calcular todas las posibles ordenes de
    # una lista de elementos.
    def combinaciones(self,ls):    
        if ls:
            for m in self.combinaciones(ls[1:]):
                for i in self.combinacionesAux(ls[0],m):
                    yield i
        else:
            yield []
    
    # Permite dar informacion sobre un tipo especifico del 
    # sistema de tipos
    def descibir(self,nombre):
        if nombre in self.atomicos.keys():
            print(f"nombre: {self.atomicos[nombre].nombre}")
            print(f"alineacion: {self.atomicos[nombre].alineacion}")
            print(f"tamanio: {self.atomicos[nombre].representacion}")
        elif nombre in self.structs.keys():
            print(f"nombre: {self.structs[nombre].nombre}")
            print(f"Con el almacenamiento normal se tiene:")
            print(f"    alineacion: {self.structs[nombre].alineacion[0]}")
            print(f"    tamanio: {self.structs[nombre].tamanio[0]}")
            print(f"    desperdicio: {self.structs[nombre].desperdiciado[0]}")
            print(f"Con el almacenamiento Optimizado respetando las alineaciones se tiene:")
            print(f"    alineacion: {self.structs[nombre].alineacion[1]}")
            print(f"    tamanio: {self.structs[nombre].tamanio[1]}")
            print(f"    desperdicio: {self.structs[nombre].desperdiciado[2]}")
            print(f"Con el almacenamiento Optimizado sin respetar las alineaciones se tiene:")
            print(f"    alineacion: {self.structs[nombre].alineacion[2]}")
            print(f"    tamanio: {self.structs[nombre].tamanio[2]}")
            print(f"    desperdicio: {self.structs[nombre].desperdiciado[2]}")
        elif nombre in self.unions.keys():
            print(f"nombre: {self.unions[nombre].nombre}")
            print(f"Con el almacenamiento normal se tiene:")
            print(f"    alineacion: {self.unions[nombre].alineacion[0]}")
            print(f"    tamanio: {self.unions[nombre].tamanio[0]}")
            print(f"    desperdicio: {self.unions[nombre].desperdiciado[0]}")
            print(f"Con el almacenamiento Optimizado respetando las alineaciones se tiene:")
            print(f"    alineacion: {self.unions[nombre].alineacion[1]}")
            print(f"    tamanio: {self.unions[nombre].tamanio[1]}")
            print(f"    desperdicio: {self.unions[nombre].desperdiciado[2]}")
            print(f"Con el almacenamiento Optimizado sin respetar las alineaciones se tiene:")
            print(f"    alineacion: {self.unions[nombre].alineacion[2]}")
            print(f"    tamanio: {self.unions[nombre].tamanio[2]}")
            print(f"    desperdicio: {self.unions[nombre].desperdiciado[2]}")
        else:
            print(f"No existe el tipo {nombre}")