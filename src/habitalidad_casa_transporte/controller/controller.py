import habitalidad_casa_transporte.interface.tui.console_view as interface_view
import habitalidad_casa_transporte.core.map_downloader as downloader
import habitalidad_casa_transporte.core.graph_builder as buider
import habitalidad_casa_transporte.core.calc_route as route_graph
import habitalidad_casa_transporte.interface.ui.global_route_map_view as view_map_route
import habitalidad_casa_transporte.interface.ui.global_map_view as view_map

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
        
        #view_map.view_route_map(self.G)
        
        cords_nodes =  interface_view.get_cords_menu()
        
        self.start_node_cords = [cords_nodes[0], cords_nodes[1]]
        self.end_node_cords = [cords_nodes[2], cords_nodes[3]]
        
        self.route = route_graph.route_ideal(self.G, self.start_node_cords, self.end_node_cords)
        
        #view_map_route.view_route_map(self.G, self.route)
        
        
    def change_config_menu(self):
        interface_view.change_parameters_menu()
