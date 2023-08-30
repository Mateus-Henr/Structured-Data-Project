import os
import win32print
import win32api
import ctypes


class Printer:
    def __init__(self):
        self.printer_list = win32print.EnumPrinters(2)

    def exibir_popup_mensagem_erro(self, message):
        ctypes.windll.user32.MessageBoxW(0, message, "ERRO", 0x10)

    def list_printers(self):
        printer_list = []
        for i, printer in enumerate(self.printer_list):
            printer_list.append(printer[2])
        return printer_list

    def set_default_printer(self, printer_index):
        if not printer_index or not printer_index.isdigit():
            self.exibir_popup_mensagem_erro(f"Erro de leitura")
            return False
        elif 1 <= int(printer_index) <= len(self.printer_list):
            win32print.SetDefaultPrinter(str(self.printer_list[int(printer_index) - 1]))
            self.exibir_popup_mensagem_erro(f"Impressora {printer_index} definida como padrão.")
            return True
        else:
            self.exibir_popup_mensagem_erro("Impressora inválida selecionada.")
            return False

    def print_file(self, file_path):
        if not os.path.isfile(file_path):
            print("Caminho de arquivo inválido.")
            return

        folder_path, file_name = os.path.split(file_path)

        try:
            win32api.ShellExecute(0, "print", file_path, None, folder_path, 0)
        except win32api.error as e:
            mensagem_erro = "Ocorreu um erro ao imprimir o arquivo:\n\n"
            mensagem_erro += "Impressora não configurada ou não respondendo."
            self.exibir_popup_mensagem_erro(mensagem_erro)
