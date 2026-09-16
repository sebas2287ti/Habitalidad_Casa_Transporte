import habitalidad_casa_transporte.interface.tui.console_view as interface_view

class controller:

    def __init__(self):
        pass

    def run(self):
        while True:
            option = interface_view.start_menu()

            match option:
                case "1":
                    self.start_program()
                case "2":
                    self.change_config_menu()
                case "3":
                    break 
                case _:
                    pass

    def start_program(self):
        pass
    
    def change_config_menu(self):
        pass
