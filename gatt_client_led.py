#!/usr/bin/python3
import asyncio
import tkinter as tk
from bleak import BleakClient, BleakScanner

# UUIDs à faire correspondre avec le serveur
SERVICE_UUID = "0000cafe-0000-1000-8000-00805f9b34fb"
CHAR_UUID = "0000feed-0000-1000-8000-00805f9b34fb"

class BLEClientGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Contrôle GATT LED")
        self.device = None
        self.client = None

        # Interface utilisateur
        self.status_label = tk.Label(root, text="🔍 Appuyez sur 'Scanner' pour trouver le serveur...")
        self.status_label.pack(pady=5)

        self.scan_button = tk.Button(root, text="Scanner", command=self.start_scan)
        self.scan_button.pack(pady=5)

        self.led_button = tk.Button(root, text="Allumer LED", command=self.toggle_led, state="disabled")
        self.led_button.pack(pady=5)

        self.led_state = False

    def start_scan(self):
        print("start_scan(self):")
        self.status_label.config(text="🔍 Scan en cours...")
        asyncio.run(self.scan_and_connect())

    async def scan_and_connect(self):
        devices = await BleakScanner.discover()
        for d in devices:
            try:
                async with BleakClient(d.address) as client:
                    services = await client.get_services()
                    if SERVICE_UUID in [s.uuid for s in services]:
                        self.client = client
                        self.device = d
                        self.status_label.config(text=f"✅ Connecté à {d.name} ({d.address})")
                        self.led_button.config(state="normal")
                        return
            except Exception as e:
                continue
        self.status_label.config(text="❌ Aucun serveur trouvé.")

    def toggle_led(self):
        if self.client is None:
            return
        value = bytes([1]) if not self.led_state else bytes([0])
        try:
            asyncio.run(self.client.write_gatt_char(CHAR_UUID, value))
            self.led_state = not self.led_state
            self.led_button.config(text="Éteindre LED" if self.led_state else "Allumer LED")
        except Exception as e:
            self.status_label.config(text=f"Erreur : {str(e)}")

# Création de la fenêtre principale
root = tk.Tk()
app = BLEClientGUI(root)
root.mainloop()
