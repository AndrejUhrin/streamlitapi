import streamlit as st
import requests
import pandas as pd
import pydeck as pdk

# Title and description
st.title("People in Space")
st.markdown("This part shows the current number of people in space and their names.")

people_response = requests.get("http://api.open-notify.org/astros.json")
people_data = people_response.json()
st.subheader(f"Number of people in space: {people_data['number']}")
st.write("Names of people in space:")
for person in people_data['people']:
    st.write(f"- {person['name']}")

iss_response = requests.get("http://api.open-notify.org/iss-now.json")
iss_data = iss_response.json()
iss_position = iss_data['iss_position']
latitude = float(iss_position['latitude'])
longitude = float(iss_position['longitude'])
st.subheader("Current location of the ISS")
st.write(f"Latitude: {latitude}, Longitude: {longitude}")
st.write("Map is showing the current location of the ISS:")

layer = pdk.Layer(
    "ScatterplotLayer",
    data=pd.DataFrame({'lat': [latitude], 'lon': [longitude]}),
    get_position='[lon, lat]',
    get_color='[200, 30, 0, 160]',
    get_radius=10000,  
    pickable=True
)

view_state = pdk.ViewState(
    latitude=latitude,
    longitude=longitude,
    zoom=4,  
    pitch=0  
)

r = pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip={"text": "ISS Location"})
st.pydeck_chart(r)