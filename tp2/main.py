import argparse, cgi, cv2, numpy as np
from http.server import SimpleHTTPRequestHandler, HTTPServer
from io import BytesIO
import socket, socketserver, threading
from queue import Queue
import base64
class MyTCPServer(socketserver.TCPServer):
    address_family = socket.AF_INET6



class ImageHandler:
    @staticmethod
    def process_image(image_data, scale_factor, queue):
        try:
            image_array = np.frombuffer(image_data, dtype=np.uint8)
            image = cv2.imdecode(image_array, cv2.IMREAD_GRAYSCALE)
            resized_image = cv2.resize(image, (0, 0), fx=scale_factor, fy=scale_factor)
            _, resized_image_data = cv2.imencode('.jpg', resized_image)
            queue.put(resized_image_data.tobytes())
        except Exception as e:
            print(f"Error al procesar la imagen: {e}")
class MyRequestHandler(SimpleHTTPRequestHandler):
    def do_POST(self):
        content_type, pdict = cgi.parse_header(self.headers['content-type'])
        if content_type == 'multipart/form-data':
            form_data = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST'}
            )
            if 'file' in form_data:
                file_item = form_data['file']
                original_filename = file_item.filename
                image_data = file_item.file.read()
                scale_factor = float(form_data.getvalue('scale_factor'))
                queue = Queue()
                image_thread = threading.Thread(target=ImageHandler.process_image, args=(image_data, scale_factor, queue))
                image_thread.start()
                resized_image_data = queue.get()
                filename = f"resized_image_{original_filename}.jpg"
                
                self.send_response(200)
                self.send_header("Content-Type", "text/html")
                self.end_headers()
            
                response_html = f"""
                <html>
                <head>
                    <title>Resultado de Redimension</title>
                </head>
                <body>
                    <h1>Resultado de Redimension</h1>
                    <img src="data:image/jpeg;base64,{base64.b64encode(resized_image_data).decode('utf-8')}" alt="Resized Image">
                </body>
                </html>
                """
                self.wfile.write(response_html.encode('utf-8'))
                



def run_server(ip, port):
    server_class = MyTCPServer if ":" in ip else socketserver.TCPServer
    with server_class((ip, port), MyRequestHandler) as httpd:
        httpd.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        ip = f"[{ip}]" if "::" in ip else ip
        print(f"Servidor HTTP escuchando en http://{ip}:{port}")
        httpd.serve_forever()



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Servidor HTTP para procesar imágenes y redimensionarlas.")
    parser.add_argument("-i", "--ip", required=True, help="Dirección IP de escucha.")
    parser.add_argument("-p", "--port", type=int, required=True, help="Número de puerto para escuchar.")
    args = parser.parse_args()
    run_server(args.ip, args.port)
