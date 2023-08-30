import os
import threading
import time
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

from controller.alios import ALIOS, Alios
from controller.mercado_pago import PixMercadoPago, MERCADO_PAGO
from model.pdf import QR_PDF, create_qrcode_pdf, create_payment_validation_code
from model.printer import Printer
from db.bank_dao import BankDAO
import io

BANK_SCREEN = 0
VALUE_SCREEN = 1
QR_CODE_SCREEN = 2
CONFIRMATION_SCREEN = 3
ADD_BANK_SCREEN = 4
PRINTERS_SCREEN = 5


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.value_tab = None
        self.thread = None
        self.bank_tab = None
        self.add_bank_window = None
        self.tabs = None
        self.qr_code_label = None
        self.printer = Printer()
        self.value = None
        self.api = None
        self.bank = None
        self.slprinter = 0
        self.event = threading.Event()

        self.initialize_app()

    def initialize_app(self):
        self.title("PIX App")
        self.tabs = ttk.Notebook(self)
        self.create_widgets()
        self.tabs.pack(expand=True, fill="both")
        self.tabs.bind("<<NotebookTabChanged>>", self.tab_changed)
        self.tabs.tab(VALUE_SCREEN, state="disabled")
        self.tabs.tab(QR_CODE_SCREEN, state="disabled")
        self.tabs.tab(CONFIRMATION_SCREEN, state="disabled")

    def create_widgets(self):
        self.create_bank_tab()
        self.create_value_tab()
        self.create_qr_code_tab()
        self.create_confirmation_tab()
        self.create_add_bank_tab()
        self.create_printer_tab()

        self.tabs.select(BANK_SCREEN)

    def create_bank_tab(self):
        self.bank_tab = ttk.Frame(self.tabs)
        self.tabs.add(self.bank_tab, text="Bancos")
        self.show_banks()

    def reload_bank_tab(self):
        # Clear existing buttons in the tab
        for widget in self.bank_tab.winfo_children():
            widget.destroy()

        self.show_banks()

    def show_banks(self):
        for bank in BankDAO.get_banks():
            tk.Button(self.bank_tab, text=bank.name, command=lambda: self.select_value_screen(bank), bg="lightgray") \
                .pack(pady=5)

        tk.Button(self.bank_tab, text="Adicionar Banco", command=lambda: self.tabs.select(ADD_BANK_SCREEN),
                  bg="lightgray") \
            .pack(pady=0, side="left")

        # Adiciona um espaço entre os botões
        tk.Label(self.bank_tab, text=" ", width=5).pack(side="left")

        tk.Button(self.bank_tab, text="Mudar Impressora", command=lambda: self.tabs.select(PRINTERS_SCREEN),
                  bg="lightgray") \
            .pack(pady=0, side="left")

    def validate_value(self):
        value = self.value.get().replace(",", ".")
        try:
            float_value = float(value)
            if float_value > 0:
                self.select_qr_code_screen()
            else:
                self.select_value_screen(self.bank)
        except ValueError:
            self.select_value_screen(self.bank)

    def create_value_tab(self):
        self.value_tab = ttk.Frame(self.tabs)
        self.tabs.add(self.value_tab, text="Valor")
        self.show_value_tab()

    def reload_value_tab(self):
        # Clear existing buttons in the tab
        for widget in self.value_tab.winfo_children():
            widget.destroy()

        self.show_value_tab()

    def show_value_tab(self):
        value_label = tk.Label(self.value_tab, text="Digite o valor (R$):", font=("Arial", 16))
        value_label.pack(pady=50)

        self.value = tk.Entry(self.value_tab, font=("Arial", 16))
        self.value.pack(pady=10)

        save_button = tk.Button(self.value_tab, text="Confirma", command=self.validate_value, bg="lightgray")
        save_button.pack(pady=5)

    def create_qr_code_tab(self):
        tab = ttk.Frame(self.tabs)
        self.tabs.add(tab, text="QR Code")
        value_label = tk.Label(tab, text="Aguardando Pagamento...", font=("Arial", 16))
        value_label.pack(pady=50)
        self.qr_code_label = tk.Label(tab)
        self.qr_code_label.pack(pady=50)

    def print_confirmation(self):
        create_payment_validation_code(self.api.pix, self.bank)
        self.printer.print_file(QR_PDF)
        os.remove(QR_PDF)

    def create_add_bank_tab(self):
        tab = ttk.Frame(self.tabs)
        self.tabs.add(tab, text="Adicionar Banco")
        value_label = tk.Label(tab, text="", font=("Arial", 16))
        value_label.pack(pady=50)

        bank_selection_frame = ttk.Frame(tab)
        bank_selection_frame.pack(pady=10)

        bank_selection_label = tk.Label(bank_selection_frame, text="Selecione o banco:", font=("Arial", 12))
        bank_selection_label.pack(side="left")

        def toggle_menu():
            if treeview.identify_region(0, 0) == "tree":
                treeview.pack_forget()
            else:
                treeview.pack()

        bank_selection_button = ttk.Button(bank_selection_frame, text="▼", width=3, command=toggle_menu)
        bank_selection_button.pack(side="left")

        treeview = ttk.Treeview(tab)
        treeview.insert("", "end", text="Mercado Pago")
        treeview.insert("", "end", text="Ailos")

        def select_bank(event):
            selection = treeview.item(treeview.focus())["text"]
            toggle_menu()

            if selection == "Mercado Pago":
                self.create_mercado_pago_fields_window()
            elif selection == "Ailos":
                self.load_ailos_fields_window()

        treeview.bind("<<TreeviewSelect>>", select_bank)

        cancel_button = tk.Button(tab, text="Voltar", command=self.return_to_initial_screen, bg="lightgray")
        cancel_button.pack(pady=5)

    def create_bank_fields_window(self, bank_name):
        # Create a new window for the bank fields
        self.add_bank_window = tk.Toplevel(self)
        self.add_bank_window.title(f"{bank_name} Fields")

        def collapse_tab_save():
            # Get the values from the entry fields
            name = name_entry.get()
            api_key = api_key_entry.get()
            value = valor_salvar.get().replace(",", ".")

            # Validate the values
            if not name or not api_key or not value:
                self.printer.exibir_popup_mensagem_erro("Please fill in all the fields.")
                return
            try:
                BankDAO.insert_bank(name, float(value), api_key, bank_name)
            except ValueError:
                self.printer.exibir_popup_mensagem_erro("Valor inválido")
                return

            # Close the fields window
            self.close_fields_window()

        # Add the specific fields for the bank in this window
        name_label = tk.Label(self.add_bank_window, text="Nome", font=("Arial", 12))
        name_label.grid(row=0, column=0, padx=5, pady=5)
        name_entry = tk.Entry(self.add_bank_window, font=("Arial", 12))
        name_entry.grid(row=0, column=1, padx=5, pady=5)

        api_key_label = tk.Label(self.add_bank_window, text="chave_api", font=("Arial", 12))
        api_key_label.grid(row=1, column=0, padx=5, pady=5)
        api_key_entry = tk.Entry(self.add_bank_window, font=("Arial", 12))
        api_key_entry.grid(row=1, column=1, padx=5, pady=5)

        value_label = tk.Label(self.add_bank_window, text="valor", font=("Arial", 12))
        value_label.grid(row=2, column=0, padx=5, pady=5)
        valor_salvar = tk.Entry(self.add_bank_window, font=("Arial", 12))
        valor_salvar.grid(row=2, column=1, padx=5, pady=5)

        save_values_button = tk.Button(self.add_bank_window, text="Salvar Valores",
                                       command=collapse_tab_save, bg="lightgray")
        save_values_button.grid(row=3, column=0, columnspan=2, pady=5)

    def close_fields_window(self):
        # Close the bank fields window
        self.add_bank_window.destroy()

    def create_mercado_pago_fields_window(self):
        self.create_bank_fields_window(MERCADO_PAGO)

    def load_ailos_fields_window(self):
        self.create_bank_fields_window(ALIOS)

    def create_printer_tab(self):
        tab = ttk.Frame(self.tabs)
        self.tabs.add(tab, text="Impressoras")

        p_list = self.printer.list_printers()

        label = tk.Label(tab, text="Selecione uma impressora: ", font=("Arial", 16))
        label.grid(row=0, column=0, sticky="w")

        for i, printer in enumerate(p_list):
            label = tk.Label(tab, text="{}-{}".format(i, printer), font=("Arial", 16))
            label.grid(row=i + 1, column=0, sticky="w")

        self.slprinter = tk.Entry(tab, font=("Arial", 16))
        self.slprinter.grid(row=len(p_list) + 1, column=0, sticky="w")
        bt = tk.Button(tab, text="Modificar",
                       command=lambda: self.printer.set_default_printer(self.slprinter.get()), bg="lightgray")
        bt.grid(row=len(p_list) + 2, column=0, sticky="w")

    def unload_fields(self):
        self.tabs.forget(self.tabs.select())

    def create_confirmation_tab(self):
        tab = ttk.Frame(self.tabs)
        self.tabs.add(tab, text="Confirmação")
        value_label = tk.Label(tab, text="Pagamento Aprovado", font=("Arial", 16))
        value_label.pack(pady=50)
        print_button = tk.Button(tab, text="Imprimir", command=self.print_confirmation, bg="lightgray")
        print_button.pack(pady=5)

        cancel_button = tk.Button(tab, text="Voltar", command=self.return_to_initial_screen, bg="lightgray")
        cancel_button.pack(pady=5)

    def select_value_screen(self, bank):
        self.bank = bank
        self.tabs.tab(VALUE_SCREEN, state="normal")
        self.tabs.tab(QR_CODE_SCREEN, state="disabled")
        self.tabs.select(VALUE_SCREEN)  # Switch to the second tab (Value Entry)

    def select_qr_code_screen(self):
        self.tabs.tab(QR_CODE_SCREEN, state="normal")
        self.tabs.select(QR_CODE_SCREEN)

        self.await_response()

    def check_pix_status(self):
        while not self.api.is_done():
            time.sleep(1)

            if self.event.is_set():
                self.thread = None
                self.event.clear()
                return

        self.tabs.tab(QR_CODE_SCREEN, state="disabled")
        self.tabs.tab(CONFIRMATION_SCREEN, state="normal")

        self.tabs.select(CONFIRMATION_SCREEN)

    def await_response(self):
        if not self.bank:
            return
        try:
            value = float(self.value.get().replace(",", "."))
            if self.bank.bank_type == MERCADO_PAGO:
                self.api = PixMercadoPago(value, self.bank)
            elif self.bank.bank_type == ALIOS:
                self.api = Alios(value, self.bank)
            else:
                self.printer.exibir_popup_mensagem_erro("Banco não suportado")
        except Exception as e:
            print(e)
            self.printer.exibir_popup_mensagem_erro("Erro ao gerar QR Code")
            self.return_to_initial_screen()
            return
        self.thread = threading.Thread(target=self.check_pix_status)
        self.thread.start()

    def return_to_initial_screen(self):
        self.tabs.tab(BANK_SCREEN, state="normal")
        self.tabs.tab(VALUE_SCREEN, state="disabled")
        self.tabs.tab(QR_CODE_SCREEN, state="disabled")
        self.tabs.tab(CONFIRMATION_SCREEN, state="disabled")
        self.tabs.select(BANK_SCREEN)

    def tab_changed(self, e):
        current_tab = self.tabs.tab(self.tabs.select(), "text")
        if current_tab == "QR Code":
            self.load_qrcode_image()
        if current_tab == "Valor":
            self.tabs.tab(QR_CODE_SCREEN, state="disabled")
            self.kill_thread()
            self.reload_value_tab()
        if current_tab == "Bancos":
            self.tabs.tab(QR_CODE_SCREEN, state="disabled")
            self.kill_thread()
            self.reload_bank_tab()

    def kill_thread(self):
        if self.thread and not self.event.is_set():
            self.event.set()

    def load_qrcode_image(self):

        if not self.api:
            return

        qr_code_base_64 = self.api.pix.generate_jpg_from_qr_code64()

        if qr_code_base_64:
            result_image = Image.open(qr_code_base_64).resize((400, 400), Image.LANCZOS)
            result_image.save(io.BytesIO(), format="PNG")
            result_image = ImageTk.PhotoImage(result_image)

            self.qr_code_label.configure(image=result_image)
            self.qr_code_label.image = result_image

            create_qrcode_pdf(self.api.pix)
            self.printer.print_file(QR_PDF)
            os.remove(QR_PDF)
