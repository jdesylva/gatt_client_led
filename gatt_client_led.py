#!/usr/bin/python3
import asyncio
import tkinter as tk
import threading
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
        self.loop = None

        # Interface utilisateur
        self.status_label = tk.Label(root, text="🔍 Appuyez sur 'Scanner' pour trouver le serveur...")
        self.status_label.pack(pady=5)

        self.scan_button = tk.Button(root, text="Scanner", command=self.start_scan)
        self.scan_button.pack(pady=5)

        self.led_button = tk.Button(root, text="Allumer LED", command=self.toggle_led, state="disabled")
        self.led_button.pack(pady=5)

        self.led_state = False

        # Handle application close
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)


    def start_scan(self):
        print("start_scan(self):")
        self.status_label.config(text="🔍 Scan en cours...")
        #asyncio.run(self.scan_and_connect())
        #threading.Thread(target=lambda: asyncio.run(self.scan_and_connect()), daemon=True).start()
        if self.loop is None:
            self.loop = asyncio.new_event_loop()
            threading.Thread(target=self._run_loop, daemon=True).start()
        asyncio.run_coroutine_threadsafe(self.scan_and_connect(), self.loop)

    def _run_loop(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

    async def scan_and_connect(self):
        devices = await BleakScanner.discover(timeout = 15.0)
        print(f"devices == {devices}")
        for d in devices:
            print(f"Adresse == {d.address}")
            try:

                client = BleakClient(d.address)
                await client.connect()
                print(f"Connexion : {client.is_connected}")
                print(f"Services == {client.services}")
                for service in client.services:
                    print(f"    {service.uuid}")
                if SERVICE_UUID in [s.uuid for s in client.services]:
                    self.client = client
                    self.device = d
                    self.root.after(0, lambda: self.status_label.config(text=f"✅ Connecté à {d.name} ({d.address})"))
                    self.root.after(0, lambda: self.led_button.config(state="normal"))
                    return
                else:
                    await client.disconnect()


            except Exception as e:
                print("Exception!!!")
                print(e)
                continue
        #self.status_label.config(text="❌ Aucun serveur trouvé.")
        self.root.after(0, lambda: self.status_label.config(text="❌ Aucun serveur trouvé."))

    def toggle_led(self):
        if self.client is None:
            return
        value = bytes([1]) if not self.led_state else bytes([0])
        try:
            #asyncio.run(self.client.write_gatt_char(CHAR_UUID, value))
            future = asyncio.run_coroutine_threadsafe(
                self.client.write_gatt_char(CHAR_UUID, value), self.loop
            )
            future.result()
            self.led_state = not self.led_state
            self.led_button.config(text="Éteindre LED" if self.led_state else "Allumer LED")
        except Exception as e:
            self.status_label.config(text=f"Erreur : {str(e)}")


    def on_close(self):
        if self.client is not None:
            try:
                asyncio.run(self.client.disconnect())
            except Exception:
                pass
        self.root.destroy()
            
# Création de la fenêtre principale
root = tk.Tk()
app = BLEClientGUI(root)
root.mainloop()
