import threading
import math

def calcular_termino(n, x):
    termino = ((-1) ** n) * (x ** (2 * n + 1)) / math.factorial(2 * n + 1)
    return termino

def calcular_seno(x, num_terminos, resultado_compartido, lock):
    resultado_local = 0.0
    
    for n in range(num_terminos):
        termino = calcular_termino(n, x)
        resultado_local += termino
    
    with lock:
        resultado_compartido.append(resultado_local)

puntos = [
    {'cantidad_terminos': 12, 'x': 0.0, 'valor_referencia': 0.0},
    {'cantidad_terminos': 12, 'x': 0.7853981633974483, 'valor_referencia': 0.7071067811865475},
    {'cantidad_terminos': 12, 'x': 1.5707963267948966, 'valor_referencia': 1.0000000000000002},
    {'cantidad_terminos': 12, 'x': 3.141592653589793, 'valor_referencia': -1.7028581387855716e-13}
]

lock = threading.Lock()
hilos = []

for punto in puntos:
    cantidad_terminos = punto['cantidad_terminos']
    x = punto['x']
    valor_referencia = punto['valor_referencia']
    resultado_compartido = []

    for _ in range(cantidad_terminos):
        hilo = threading.Thread(target=calcular_seno, args=(x, 1, resultado_compartido, lock))
        hilo.start()
        hilos.append(hilo)

    for hilo in hilos:
        hilo.join()

    resultado = sum(resultado_compartido)
    diferencia = resultado - valor_referencia

    print(f"Para x = {x}, cantidad de términos = {cantidad_terminos}:")
    print(f"El desarrollo en serie de Taylor para sin({x}) es: {resultado}")
    print(f"Valor de referencia: {valor_referencia}")
    print(f"Diferencia: {diferencia}")
    print()