from controller.config_controller import *


class Command:

    def __init__(self):
        self.__content = []

    def set_content(self, user_input):
        self.__content = user_input.split(" ")

    def get_content(self):
        return self.__content

    def exec_command(self, db):
        return execute(self, db)
