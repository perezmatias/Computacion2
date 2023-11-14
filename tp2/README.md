Ejecucion:

cd TP2
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
./main.py -i 127.0.0.1 -p 8080

curl -X POST --data-binary "imagen.jpg" http://127.0.0.1:8080


Desactivar entorno:
deactivate
