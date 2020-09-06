import streamlit as st
import numpy as np
import pandas as pd
from typing import List
import pydeck as pdk
from PIL import Image

dataset = "ManualLog_12_19_47_14.csv"
parameters = [1,2,3,4,5,6,7]
water_parameters = {1: "Total Water Column (m)",
                    2: "Temperature (c)",
                    3: "pH",
                    4: "ODO mg/L",
                    5: "Salinity (ppt)",
                    6: "Turbid+ NTU",
                    7: "BGA-PC cells/mL"}
selected_parameters = [water_parameters.get(key) for key in
                       parameters]

def selectDataframe(dataset: str, selected_parameters: List[str]):
    entire_ds = pd.read_csv(dataset)  # read the entire dataset as a dataframe
    # print(entire_ds.columns) #to print the head of the dataframe

    selected_parameters.insert(0, "Latitude")
    selected_parameters.insert(1, "Longitude")
    selected_parameters.insert(2, "Time hh:mm:ss")

    try:
        partial_ds = entire_ds[selected_parameters]
        print("The dataframe was successfully created!")
        print(partial_ds.columns) #to print the head of the dataframe
        partial_ds=partial_ds.rename(columns={"Latitude": "lat", "Longitude": "lon"})
        return partial_ds
    except ValueError:
        print("Oops!  Some selected water parameters do not exist in this dataset. Try again...")

partial_ds = selectDataframe(dataset, selected_parameters)  # calling function selectDataframe
min_turb = partial_ds[["Turbid+ NTU"]].min()
partial_ds[["Turbid+ NTU"]]=partial_ds[["Turbid+ NTU"]]-min_turb

st.title('FIU Biscayne Bay Task Force')

st.header("Data Collection - September 5th 2020")

st.subheader("Summary Table")
options = st.multiselect(
     'Select Desired Parameters',
     ["Total Water Column (m)", "Temperature (c)", "pH", "ODO mg/L", "Salinity (ppt)","Turbid+ NTU", "BGA-PC cells/mL"])

# st.write('You selected:', options[0])

partial_ds[['lat','lon']+options]


see_stats = st.checkbox('Click here for descriptive statistics')
if see_stats:
    st.subheader("Descriptive Statistics Table")
    st.dataframe(partial_ds[["Total Water Column (m)", "Temperature (c)", "pH", "ODO mg/L", "Salinity (ppt)","Turbid+ NTU", "BGA-PC cells/mL"]].describe())

st.subheader("Map")
# st.map(partial_ds[['lat','lon']])

st.pydeck_chart(pdk.Deck(
     map_style='mapbox://styles/mapbox/streets-v11',
     #map_style='mapbox://styles/mapbox/light-v9',
     initial_view_state=pdk.ViewState(
         latitude=25.91275783,
         longitude=-80.13782367,
         zoom=16,
         pitch=50,
     ),
     layers=[
         # pdk.Layer(
         #    'HexagonLayer',
         #    data=partial_ds[['lat','lon']],
         #    get_position='[lon, lat]',
         #    radius=10,
         #    elevation_scale=4,
         #    elevation_range=[0, 1000],
         #    pickable=True,
         #    extruded=True,
         # ),
         pdk.Layer(
             'ScatterplotLayer',
             data=partial_ds[['lat','lon']],
             get_position='[lon, lat]',
             get_color='[200, 30, 0, 160]',
             get_radius=1,
         ),
     ],
 ))


st.subheader("Photos of the Mission")
image1 = Image.open('IMG_1885.jpg')
image2 = Image.open('IMG_1886.jpg')
image3 = Image.open('IMG_1887.jpg')
st.image(image1,use_column_width=True)
st.image(image2,use_column_width=True)
st.image(image3, caption='YSI Ecomapper executing mission in Biscayne Bay, FL, Sep 2020',use_column_width=True)

st.text("Developed by Gregory Murad Reis\n"
        "Mission designed by Adrian Perez\n"
        "Miami, FL\n"
        "2020")