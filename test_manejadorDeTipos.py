import manejadorDeTiposMk2 as mdt

a = mdt.manejadorDeTipos()

def test_crear_atomico():
    a.crear_atomico("bool",1,2)
    assert a.atomicos["bool"].representacion == 1
    assert a.atomicos["bool"].alineacion == 2
    
    a.crear_atomico("char2",2,2)
    assert a.atomicos["char2"].representacion == 2
    assert a.atomicos["char2"].alineacion == 2

    a.crear_atomico("int",4,4)
    assert a.atomicos["int"].representacion == 4
    assert a.atomicos["int"].alineacion == 4

    a.crear_atomico("double",8,8)
    assert a.atomicos["double"].representacion == 8
    assert a.atomicos["double"].alineacion == 8

def test_crear_struct():
    a.crear_struct("a",["int","char2","int","double","bool"])
    assert a.structs["a"].tamanio == [25, 19, 19]
    assert a.structs["a"].alineacion == [4, 4, 4] 
    assert a.structs["a"].desperdiciado == [6, 0, 0]

    a.crear_struct("b",["a","int"])
    assert a.structs["b"].tamanio == [32, 23, 23]
    assert a.structs["b"].alineacion == [4, 4, 4] 
    assert a.structs["b"].desperdiciado == [3, 0, 0]

def test_crear_union():
    a.crear_union("c",["int","char2","int","double","bool"])
    assert a.unions["c"].tamanio == [8, 8, 8]
    assert a.unions["c"].alineacion == [8, 8, 8]
    assert a.unions["c"].desperdiciado == [0, 0, 0]

    a.crear_union("d",["b","c","bool"])
    assert a.unions["d"].tamanio == [32, 23, 23]
    assert a.unions["d"].alineacion == [8, 8, 8]
    assert a.unions["d"].desperdiciado == [0, 0, 0]

test_crear_atomico()
test_crear_struct()
test_crear_union()