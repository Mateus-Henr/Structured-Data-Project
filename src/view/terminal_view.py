from controller.config_controller import *
from model.command import *


def initial_print():
    print("Vulture's Pix configuration terminal\nType '\h' for help\n")


def print_help():
    print("\n \h -> help\n"
          " \i [name] [value] [quantity in stock] -> insert item\n"
          " \m [id] [new name] [new value] [new quantity in stock] -> modify item\n"
          " \m -n [id] [new name] -> modify item's name\n"
          " \m -v [id] [new value] -> modify item's value\n"
          " \m -s [id] [new quantity in stock] -> modify item's quantity in stock\n"
          " \\v -> view all products\n"
          " \\v [id] -> view product\n"
          " \\r [id] -> remove item\n"
          " \\t -> view all transitions\n"
          " \\t [id] -> view transition\n"
          " \q -> quit\n")


def user_input():
    return input()


class TerminalView:

    def __init__(self):
        self.command = Command()
        self.db = start_db()

    def main_loop(self):
        initial_print()

        while True:
            print("# ", end='')
            self.command.set_content(user_input())

            result = self.command.exec_command(self.db)

            if result[0] == 0:
                break
            if result[0] == 1:
                print_help()
            if result[0] == 2:
                print("\nProduto inserido\n")
            if result[0] == 3:
                print()
                for row in result[1]:
                    print("| {:>4} | {:<20} | {:>8} | {:>4} |".format(row.id, row.name, row.value, row.inventory))
                print()
            if result[0] == 4:
                print("\nProduto atualizado\n")
            if result[0] == 5:
                print("\nProduto removido\n")
            if result[0] == 6:
                print()
                for row in result[1]:
                    print("| {:>4} | {:>36} | {:>15} | {:<20} | {:>10} | {:>8}".format(row.id, row.transaction_id,
                                                                                       row.source_account, row.bank_name,
                                                                                       row.date, row.value))
            if result[0] == 7:
                print("\nComando inválido\n")
