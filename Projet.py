import utime #importer un module permettant d'effectuer des actions tel que "attendre 5sec"
import network #importer un module permettant de gerer la connexion réseau de notre raspberry pi Pico W
import machine #importer un module principal qui va gerer toutes les connectivité physique de notre carte (Electro-Aimant)
import socket #importer un module capable d'heberger un serveur web

#--------------------------------------------------------------------------------------------------------------------------------------#

# Constantes
PORT = 80 #Le port 80 va etre le port utiliser pour créer le site Web
ENABLE_PATH = '/magnet'
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <title>Mon Site Web</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      background-color: #f2f2f2;
      margin: 0;
      padding: 20px;
    }
    
    h1 {
      color: #333;
      text-align: center;
    }
    
    button {
      display: block;
      width: 200px;
      height: 40px;
      margin: 10px auto;
      background-color: #4CAF50;
      color: #fff;
      border: none;
      border-radius: 4px;
      font-size: 16px;
      cursor: pointer;
    }
    
    button:hover {
      background-color: #45a049;
    }
  </style>
</head>
<body>
  <h1>Titre de mon site</h1>
  
  <button type="button">Bouton 1</button>
  <button type="button">Bouton 2</button>
</body>
</html>

"""

#--------------------------------------------------------------------------------------------------------------------------------------#

# Broches
led = machine.Pin("LED", machine.Pin.OUT, value=1) # Ceci est la LED intégré à la carte. Valeur True pour nous indiqué que le programme est en cour d'éxecution
electromagnet_Pin = machine.Pin(16, machine.Pin.OUT) # Nous definissons la broche de l'électro-aimant sur la broche 16

#--------------------------------------------------------------------------------------------------------------------------------------#

# Connexion WiFi
ssid = "Bah alors t pauvre t a pas d co" # Nom du réseau Wifi auquel la carte va se connecté
password = "Tu vie en afrique?" # Mot de passe du réseau Wifi
def connect_to_wifi(): # Cette fonction va permettre à la carte de se connecter à Internet via un réseau Wifi
    wlan = network.WLAN(network.STA_IF) # Mettre la carte en mode "Station" pour capter un Wifi
    wlan.active(True) # Activer le composant Wifi de la carte
    wlan.connect(ssid, password) # Se connecter au réseau Wifi
    while not wlan.isconnected(): # Tant que la carte n'est pas connecté
        print('Waiting for connection...') # Afficher un message
        utime.sleep(1) # Attendre 1 seconde
    ip = wlan.ifconfig()[0] # La variable ip va contenir l'adresse IP de notre carte Pico W
    print(f'Connected on {ip}') # Afficher l'adresse IP à l'utilisateur
    return ip # Retourner l'adresse IP

#--------------------------------------------------------------------------------------------------------------------------------------#

# Socket
def open_socket(ip): #Cette fonction va ouvrir un "Socket"
    addr = (ip, PORT) # L'adresse du Socket va etre défini par l'adresse IP de la carte et le port choisi
    sock = socket.socket() # Creer un socket
    sock.bind(addr) # Attribué l'adresse à notre Socket
    sock.listen(1) # Ouvrir le Socket
    print("Socket opened successfully!") # Afficher un message dans la console
    return sock # Retourner notre Socket

#--------------------------------------------------------------------------------------------------------------------------------------#

# Serveur
def serve(sock): # Nous allons maintenant heberger notre page Web
    while True:
        client, addr = sock.accept() # Accepter une connnexion client
        print(f'Client connected: {addr}') # Afficher l'adresse auquel le client est connecté
        request = client.recv(1024).decode('utf-8') # Recevoir la requette du client
        request_path = request.split()[1] # Recevoir la requette du client
        print(f'Request received: {request_path}') # Afficher la requette recu par le client
        if request_path == ENABLE_PATH: # Gerer la requette
            params = request.split('?')[1]
            if 'state=on' in params:
                electromagnet_Pin.value(1)
                print('Electromagnet enabled')
            elif 'state=off' in params:
                electromagnet_Pin.value(0)
                print('Electromagnet disabled')
        client.sendall(HTML_TEMPLATE.encode('utf-8')) #Envoyer la réponse HTML au client
        client.close()

#--------------------------------------------------------------------------------------------------------------------------------------#
        
try:
    print('Starting...') 
    ip = connect_to_wifi() # Se connecter au Wifi
    print('WiFi connected')
    sock = open_socket(ip) # Ouvrir un Socket
    print('Listening on port', PORT)
    serve(sock) # Heberger le serveur Web
except KeyboardInterrupt:
    machine.reset()

