# app.py

import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import pickle
import networkx as nx
import osmnx as ox
from convoy_utils import predict_travel_time, get_route_map

st.set_page_config(page_title="Conway - CMP Optimizer", layout="wide", initial_sidebar_state="expanded")

# ---- Title & Logo ----
col1, col2 = st.columns([1, 8])
with col1:
    st.image("logo.png", width=80)
with col2:
    st.title("Conway - Convoy Movement Optimizer")
    st.markdown("Efficient. Predictive. Reliable.")

st.markdown("---")

# ---- Input Section ----
st.sidebar.header("🔍 Convoy Route Inputs")
source = st.sidebar.text_input("Enter Source Location", "Delhi")
destination = st.sidebar.text_input("Enter Destination Location", "Chandigarh")
weather = st.sidebar.selectbox("Weather Condition", ["Clear", "Rainy", "Foggy"])
traffic = st.sidebar.selectbox("Traffic Level", ["Low", "Medium", "High"])
mode = st.sidebar.selectbox("Mode of Movement", ["Road", "Rail", "Multi-modal"])

if st.sidebar.button("Start Movement"):
    with st.spinner("Calculating route and predicting..."):
        try:
            travel_time = predict_travel_time(weather, traffic, mode)
            st.success(f"🚚 Predicted Travel Time: {travel_time:.2f} hours")

            st.subheader("🗺️ Optimized Route Map")
            m = get_route_map(source, destination)
            st_folium(m, width=900, height=600)

        except Exception as e:
            st.error(f"Error: {e}")

st.markdown("---")
st.caption("Developed with ❤️ for CMP Logistics.")
