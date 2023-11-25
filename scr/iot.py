import serial
import paho.mqtt.client as mqtt
import datetime
import re

last_detected_word = None

# Se crea una lista para agregar palabras
palabras = []

# Expresión regular para capturar las etiquetas y valores
pattern = re.compile(r"(\w+pr): (\d+\.\d+)")

# Functions
def on_publish(client, userdata, result):
    print("Data published to ThingsBoard\n")
    #pass

# Paramentros de la comunicacion serial
ser = serial.Serial(
    port='COM5',\
    baudrate=115200,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
    timeout=200
)
print("Conectado al puerto serial: " + ser.portstr)

broker = "iot.eie.ucr.ac.cr"
port = 1883
topic = "v1/devices/me/telemetry"
username = "Labo 5 Jose Eras y Daniela Rios"
token = "inw5pjc9ph9dd03vgy9f"

client = mqtt.Client()
client.on_publish = on_publish
client.username_pw_set(username, token)
client.connect(broker, port, keepalive=60)

#Archivo de texto
with open('palabras.txt', 'w') as file:
    for word in palabras:
        file.write(f"{word}\n")


switches = {
    'Luces': False,
    'Musica': False,
    'Puerta': False
}


while True:
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').rstrip()
        print(f"Dato recibido: {line}")  # Visualizar datos de entrada

        # Busca coincidencias en la línea actual
        matches = pattern.findall(line)

        # Muestra todas las coincidencias que superan el umbral
        detected_labels = []
        for match in matches:
            label, value = match
            probability = float(value)

            # Procesa las etiquetas detectadas
            process_detected_labels(detected_labels, label, probability)

        # Toma decisiones basadas en las etiquetas detectadas
        if detected_labels:
            print(f"Palabras detectadas: {detected_labels}")

            # Agrega las palabras detectadas a la lista global
            palabras.extend(detected_labels)
