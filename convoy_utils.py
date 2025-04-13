# convoy_utils.py

import pickle
import osmnx as ox
import networkx as nx
from geopy.geocoders import Nominatim

# Load the trained model and encoders
model = pickle.load(open("convoy_rf_model.pkl", "rb"))
weather_enc = pickle.load(open("weather_encoder.pkl", "rb"))
traffic_enc = pickle.load(open("traffic_encoder.pkl", "rb"))
mode_enc = pickle.load(open("mode_encoder.pkl", "rb"))

def predict_travel_time(weather, traffic, mode):
    """Predict travel time using trained model."""
    input_data = [[
        weather_enc.transform([weather])[0],
        traffic_enc.transform([traffic])[0],
        mode_enc.transform([mode])[0]
    ]]
    prediction = model.predict(input_data)
    return prediction[0]

def get_route_map(source, destination):
    """Generate map using OSM and plot path between source and destination."""
    geolocator = Nominatim(user_agent="conway_map")
    src_loc = geolocator.geocode(source)
    dst_loc = geolocator.geocode(destination)

    if not src_loc or not dst_loc:
        raise ValueError("Could not find one or both locations on map.")

    G = ox.graph_from_point((src_loc.latitude, src_loc.longitude), dist=100000, network_type='drive')
    orig_node = ox.distance.nearest_nodes(G, src_loc.longitude, src_loc.latitude)
    dest_node = ox.distance.nearest_nodes(G, dst_loc.longitude, dst_loc.latitude)
    route = nx.shortest_path(G, orig_node, dest_node, weight="length")

    m = ox.plot_route_folium(G, route, route_color='blue', route_width=5, tiles="CartoDB dark_matter")
    folium.Marker([src_loc.latitude, src_loc.longitude], tooltip="Start", icon=folium.Icon(color='green')).add_to(m)
    folium.Marker([dst_loc.latitude, dst_loc.longitude], tooltip="End", icon=folium.Icon(color='red')).add_to(m)

    return m
