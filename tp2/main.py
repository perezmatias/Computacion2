from multiprocessing import Queue
from servidor_http import servidor_http_concurrente
from proceso_hijo import proceso_hijo

if __name__ == "__main__":
    cola = Queue()

    # Inicia el proceso hijo
    proceso = Process(target=proceso_hijo, args=(cola,))
    proceso.start()

    # Inicia el servidor HTTP
    servidor_http_concurrente(8080, cola)
