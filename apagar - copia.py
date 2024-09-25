import ctypes
import time
from datetime import datetime

# Define la hora en la que deseas apagar la pantalla (formato 24 horas)
hora_apagar = "03:35"

# Constantes necesarias para el apagado de pantalla
HWND_BROADCAST = 0xFFFF
WM_SYSCOMMAND = 0x0112
SC_MONITORPOWER = 0xF170
MONITOR_OFF = 2

def apagar_pantalla():
    # Llama a la función SendMessageA de user32.dll
    ctypes.windll.user32.SendMessageW(HWND_BROADCAST, WM_SYSCOMMAND, SC_MONITORPOWER, MONITOR_OFF)

while True:
    # Obtén la hora actual
    hora_actual = datetime.now().strftime("%H:%M")

    # Verifica si la hora actual coincide con la hora de apagado
    if hora_actual == hora_apagar:
        apagar_pantalla()
        break

    # Espera 60 segundos antes de verificar nuevamente
    time.sleep(60)
