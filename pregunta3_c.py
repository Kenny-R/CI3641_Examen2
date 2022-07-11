def ins(e ,ls):
    yield [e, *ls]
    if ls:
        for i in ins(e,ls[1:]):
            yield [ls[0],*i]

def misterio(ls):    
    if ls:
        for m in misterio(ls[1:]):
            for i in ins(ls[0],m):
                yield i
    else:
        yield []

def bienParentizadas(n):
    ls = ["("]*n + [")"]*n
    impresos = []
    for m in misterio(ls):
        abierto,cerrado,imprimir = 0, 0, True
        if m not in impresos:
            for parentesis in m:
                if parentesis == ")":
                    if cerrado + 1 > abierto: 
                        imprimir = False
                        break
                    cerrado += 1
                else:
                    abierto += 1
            
            if imprimir: 
                impresos.append(m)
                yield " ".join(m)