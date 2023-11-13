from multiprocessing import Process, Queue
from procesamiento_imagenes import convertir_a_escala_de_grises

def proceso_hijo(queue):
    while True:
        # Espera hasta que haya una imagen en la cola y luego procesa la imagen
        imagen_path = queue.get()
        imagen_procesada = convertir_a_escala_de_grises(imagen_path)
        # Envía la imagen procesada de vuelta al servidor HTTP o al cliente
