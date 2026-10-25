"""Apaga la pantalla (el monitor) de Windows a una hora determinada.

Uso:
    python apagar.py                 # apaga a la hora por defecto (03:35), una vez
    python apagar.py 23:30           # apaga a las 23:30, una vez
    python apagar.py 23:30 --diario  # apaga todos los días a las 23:30
    python apagar.py --ahora         # apaga la pantalla inmediatamente
"""

import argparse
import ctypes
import sys
import time
from datetime import datetime, timedelta

# Hora por defecto en la que se apaga la pantalla (formato 24 horas)
HORA_POR_DEFECTO = "03:35"

# Constantes de la API de Windows para el apagado de pantalla
HWND_BROADCAST = 0xFFFF
WM_SYSCOMMAND = 0x0112
SC_MONITORPOWER = 0xF170
MONITOR_OFF = 2


def apagar_pantalla():
    # PostMessageW no espera respuesta de las ventanas, así el script
    # no se queda colgado si alguna aplicación no responde
    ctypes.windll.user32.PostMessageW(HWND_BROADCAST, WM_SYSCOMMAND, SC_MONITORPOWER, MONITOR_OFF)


def leer_hora(texto):
    try:
        return datetime.strptime(texto, "%H:%M").time()
    except ValueError:
        raise argparse.ArgumentTypeError(f"hora inválida '{texto}', usa el formato HH:MM (ej. 23:30)")


def proxima_ejecucion(hora):
    # Calcula el próximo momento en que llega esa hora (hoy o mañana)
    ahora = datetime.now()
    objetivo = ahora.replace(hour=hora.hour, minute=hora.minute, second=0, microsecond=0)
    if objetivo <= ahora:
        objetivo += timedelta(days=1)
    return objetivo


def esperar_hasta(objetivo):
    # Duerme en tramos cortos y compara con la hora real, así no se salta
    # el minuto aunque el reloj cambie o el equipo se suspenda un rato
    while True:
        restante = (objetivo - datetime.now()).total_seconds()
        if restante <= 0:
            return
        time.sleep(min(restante, 30))


def main():
    parser = argparse.ArgumentParser(description="Apaga la pantalla de Windows a una hora determinada.")
    parser.add_argument("hora", nargs="?", type=leer_hora, default=leer_hora(HORA_POR_DEFECTO),
                        help=f"hora de apagado en formato HH:MM (por defecto {HORA_POR_DEFECTO})")
    parser.add_argument("--diario", action="store_true", help="repetir todos los días a la misma hora")
    parser.add_argument("--ahora", action="store_true", help="apagar la pantalla inmediatamente")
    args = parser.parse_args()

    if sys.platform != "win32":
        sys.exit("Este script solo funciona en Windows.")

    if args.ahora:
        apagar_pantalla()
        return

    try:
        while True:
            objetivo = proxima_ejecucion(args.hora)
            print(f"La pantalla se apagará el {objetivo:%d/%m/%Y a las %H:%M}. Presiona Ctrl+C para cancelar.")
            esperar_hasta(objetivo)
            apagar_pantalla()
            print(f"Pantalla apagada a las {datetime.now():%H:%M}.")
            if not args.diario:
                break
    except KeyboardInterrupt:
        print("\nCancelado.")


if __name__ == "__main__":
    main()
