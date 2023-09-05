import ctypes


def popup(message):
    ctypes.windll.user32.MessageBoxW(0, message, "ERRO", 0x10)
