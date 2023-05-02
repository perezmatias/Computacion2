import os
import argparse

# función para invertir una cadena
def reverse_string(string):
    return string[::-1]

# función para procesar una línea de entrada
def process_line(line, pipe_out):
    # invertir la línea
    reversed_line = reverse_string(line.strip())
    # enviar la línea invertida a través del pipe
    os.write(pipe_out, reversed_line.encode())

# función para procesar un archivo
def process_file(file_path):
    # abrir el archivo
    with open(file_path) as file:
        # leer todas las líneas del archivo
        lines = file.readlines()
        # crear una lista de pipes para comunicarse con los procesos hijos
        pipes = [os.pipe() for _ in range(len(lines))]
        # crear los procesos hijos
        for i, line in enumerate(lines):
            pid = os.fork()
            if pid == 0:
                # en el proceso hijo, cerrar el extremo de escritura del pipe y procesar la línea
                os.close(pipes[i][1])
                process_line(line, pipes[i][0])
                os._exit(0)
            else:
                # en el proceso padre, cerrar el extremo de lectura del pipe
                os.close(pipes[i][0])
        # esperar a que todos los procesos hijos terminen
        for _ in range(len(lines)):
            os.wait()
        # leer los resultados de los pipes y mostrarlos por pantalla
        for pipe in pipes:
            reversed_line = os.read(pipe[0], 1024).decode().strip()
            print(reversed_line)

# parsear los argumentos de línea de comandos
parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", help="archivo de entrada")
args = parser.parse_args()

# procesar el archivo si se proporciona
if args.file:
    process_file(args.file)
else:
    print("Debe proporcionar un archivo de entrada con la opción -f o --file")