from multiprocessing.context import assert_spawning
import ManejadorBooleano as mb

hola = mb.ManejadorBooleano()

def test_evaluacion():
    assert hola.evaluacion("PRE & true false") == False
    assert hola.evaluacion("PRE & true true") == True
    assert hola.evaluacion("POST true false |") == True
    assert hola.evaluacion("POST false false |") == False
    assert hola.evaluacion("PRE | & => true true false true") == True
    assert hola.evaluacion("POST true false => false | true false ^ | &") == False

def test_crearArbol():
    arbol = hola.crearArbol("PRE & true false")
    assert arbol.valor == "&"

    arbol = hola.crearArbol("PRE & true true")
    assert arbol.valor == "&"

    arbol = hola.crearArbol("POST true false |")
    assert arbol.valor == "|"

    arbol = hola.crearArbol("POST false false |")
    assert arbol.valor == "|"

    arbol = hola.crearArbol("PRE | & => true true false true")
    assert arbol.valor == "|"

    arbol = hola.crearArbol("POST true false => false | true false ^ | &")
    assert arbol.valor == "&"

def test_mostrar():
    assert hola.mostrar(hola.crearArbol("PRE & true false")) == "true & false"
    assert hola.mostrar(hola.crearArbol("PRE & true true")) == "true & true"
    assert hola.mostrar(hola.crearArbol("POST true false |")) == "true | false"
    assert hola.mostrar(hola.crearArbol("POST false false |")) == "false | false"
    assert hola.mostrar(hola.crearArbol("PRE | & => true true false true")) == "(true => true) & false | true"
    assert hola.mostrar(hola.crearArbol("POST true false => false | true false ^ | &")) == "(true => false) | false & (true | ^ false)"

    
    