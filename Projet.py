import utime
import network
import machine
import socket

# Constantes
PORT = 80
ENABLE_PATH = '/magnet'
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Control Panel</title>
</head>
<body>
    <h1>Control Panel</h1>
    <button onclick="window.location.href='/magnet?state=on'">Enable Magnet</button>
    <button onclick="window.location.href='/magnet?state=off'">Disable Magnet</button>
</body>
</html>
"""

# Broches
led = machine.Pin("LED", machine.Pin.OUT, value=1)
electromagnet_Pin = machine.Pin(16, machine.Pin.OUT)

# Connexion WiFi
ssid = "Bah alors t pauvre t a pas d co"
password = "Tu vie en afrique?"

def connect_to_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while not wlan.isconnected():
        print('Waiting for connection...')
        utime.sleep(1)
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    return ip

# Socket
def open_socket(ip):
    addr = (ip, PORT)
    sock = socket.socket()
    sock.bind(addr)
    sock.listen(1)
    print("Socket opened successfully!")
    return sock

# Serveur
def serve(sock):
    while True:
        client, addr = sock.accept()
        print(f'Client connected: {addr}')
        request = client.recv(1024).decode('utf-8')
        request_path = request.split()[1]
        print(f'Request received: {request_path}')
        if request_path == ENABLE_PATH:
            params = request.split('?')[1]
            if 'state=on' in params:
                electromagnet_Pin.value(1)
                print('Electromagnet enabled')
            elif 'state=off' in params:
                electromagnet_Pin.value(0)
                print('Electromagnet disabled')
        client.sendall(HTML_TEMPLATE.encode('utf-8'))
        client.close()

try:
    print('Starting...')
    ip = connect_to_wifi()
    print('WiFi connected')
    sock = open_socket(ip)
    print('Listening on port', PORT)
    serve(sock)
except KeyboardInterrupt:
    machine.reset()

