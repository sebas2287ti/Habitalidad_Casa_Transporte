
velocity_for_street_type = {
    "motorway": 80, 
    "motorway_link": 60, 
    "trunk": 60,
    "trunk_link": 50,  
    "primary": 50,  
    "primary_link": 40, 
    "secondary": 40,  
    "secondary_link": 30,  
    "tertiary": 30, 
    "residential": 30,  
    "unclassified": 30, 
    "living_street": 20, 
    "service": 20, 
}

def assing_weight_graft(G):
    for u, v, data in G.edges(data=True):
        length_street = data['length'] 
        street_type = data['highway']

        if isinstance(street_type, list):
            street_type = street_type[0]

        velocity = velocity_for_street_type.get(street_type, 30) 
        time_travel_min = length_street / (velocity / 3.6) 
        data['travel_time'] = time_travel_min

def change_weight_for_street_type(G):
    for u, v, data in G.edges(data=True):
        pass 