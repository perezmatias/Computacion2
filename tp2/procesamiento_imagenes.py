from PIL import Image

def convertir_a_escala_de_grises(imagen_path):
    imagen = Image.open(imagen_path).convert("L")
    return imagen