# Client GATT LED

Ce dépôt contient un simple client BLE GATT avec une interface Tkinter. Il recherche un serveur exposant les UUID `SERVICE_UUID` et `CHAR_UUID` définis dans `gatt_client_led.py` et bascule l’état d’une LED sur ce serveur.

## Installation

Assurez-vous que Python 3 est installé, puis installez la bibliothèque BLE :

```bash
pip install bleak

Tkinter est généralement fourni avec Python, mais sur les systèmes basés sur Debian, il peut être nécessaire d’exécuter sudo apt-get install python3-tk.

#Permissions
L’accès aux périphériques BLE nécessite souvent des privilèges élevés sous Linux. Vous pouvez soit lancer le programme avec sudo, soit attribuer les capacités nécessaires à l’interpréteur Python :

sudo setcap cap_net_raw,cap_net_admin+eip $(readlink -f $(which python3))

Après cela, vous pouvez exécuter le script en tant qu’utilisateur normal.

#Lancer le serveur
Démarrez un serveur BLE implémentant les mêmes UUID. Si vous utilisez l’exemple complémentaire gatt_server_led.py, exécutez-le d’abord sur la machine ou le microcontrôleur contrôlant la LED :

python3 gatt_server_led.py

Assurez-vous que le serveur est en mode publicité et détectable.

#Lancer le client
Une fois le serveur actif, lancez le client :

python3 gatt_client_led.py

Cliquez sur Scanner pour rechercher le serveur. Une fois connecté, utilisez Allumer LED pour activer ou désactiver la LED.

#Explication rapide
Ce programme recherche un périphérique BLE offrant le service SERVICE_UUID. Une fois trouvé, il se connecte et écrit dans la caractéristique CHAR_UUID pour allumer ou éteindre la LED distante. L’interface indique l’état de la connexion et propose un bouton pour changer l’état de la LED.

