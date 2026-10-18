from turtle import pos

import habitalidad_casa_transporte.interface.tui.console_view as interface_view
import habitalidad_casa_transporte.core.map_downloader as downloader
import habitalidad_casa_transporte.core.graph_builder as buider
import habitalidad_casa_transporte.core.calc_route as route_graph
import habitalidad_casa_transporte.interface.ui.flet_matploit_view as view_map_route     
import habitalidad_casa_transporte.interface.ui.flet_matploit_view as view_map
import habitalidad_casa_transporte.core.assing_weight as weight 

class controller:

    City = "Bogota"
    Country = "Colombia"
    start_node_cords = (-74.221, 4.627)
    end_node_cords = (-74.162, 4.664)
    G = None
    route = None
    
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
        
        self.G = downloader.download_map(f"{self.City}, {self.Country}")
        
        self.G = buider.build_graph_map(self.G)
        print("Grafo construido con éxito.")
        print(list(self.G.nodes(data=True))[:2])
        def calcular(origen, destino):
            print("Calcular ruta:", origen, "->", destino)

        elegidos = view_map.mostrar_interfaz(
            self.G,
            on_calcular=calcular,
            on_mapa_calor=lambda: print("Mapa de calor"),
            on_seleccion=lambda s: print("Selección:", s),
        )
        print("Selección final:", elegidos)
        
    def change_config_menu(self):
        interface_view.change_parameters_menu()
