import streamlit as st
import numpy as np
import pandas as pd
from typing import List
import pydeck as pdk
from PIL import Image


def mission(dataset,zoom_lat,zoom_long):
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
             latitude=zoom_lat,
             longitude=zoom_long,
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


if __name__ == '__main__':
    #Zoom info
    bbc_lat = 25.91275783
    bbc_long = -80.13782367
    lil_river_lat = 25.845469
    lil_river_long = -80.175492

    #August 2020
    aug20 = "Logs/BBC/ManualLog_11_05_09_92.csv"
    sep5 = "Logs/BBC/ManualLog_12_19_47_14.csv"

    #September 2020
    sep18_1 = "Logs/BBC/20200918_115659_PleaseWork_IVER2-218.csv"
    sep18_2 = "Logs/BBC/20200918_120605_PleaseWorkSRP_IVER2-218.csv"

    #October 2020
    oct3 = "Logs/LittleRiver/ManualLog_17_00_45_64.csv"
    oct4_1 = "Logs/LittleRiver/20201004_171844_TestForLittleRiver_IVER2-218.csv"
    oct4_2 = "Logs/LittleRiver/20201004_180324_LittleRiverOct4_IVER2-218.csv"

    option=st.sidebar.selectbox("Select the Date/Location",
                         ("","Aug 20, BBC","Sep 5, BBC","Sep 18 A, BBC",
                          "Sep 18 B, BBC","Oct 3, Little River",
                          "Oct 4 Test, Little River", "Oct 4, Little River"))

    st.title("FIU - Marine Robotics Lab")
    st.header("Rescuing Biscayne Bay Project")

    st.write("This project aims at developing algorithms to effectively and efficiently collect water data using "
            "autonomous underwater and surface robots. Professor Gregory Murad Reis (gregoryreis.com) is leading a team of "
            "students and researchers to collect, analyze and develop visualization tools for the data collected in"
            "Biscayne Bay, FL. This effort is motivated by the environmental issues that have happening in the bay area."
            "\nPlease select a mission in the top left menu to visualize the dataset.")
    # st.subheader("Photos of the Mission")
    # image1 = Image.open('IMG_1885.jpg')
    # image2 = Image.open('IMG_1886.jpg')
    # image3 = Image.open('IMG_1887.jpg')
    # st.image(image1, use_column_width=True)
    # st.image(image2, use_column_width=True)
    # st.image(image3, caption='YSI Ecomapper executing mission in Biscayne Bay, FL, Sep 2020', use_column_width=True)

    if option == "Aug 20, BBC":
        mission(aug20,bbc_lat,bbc_long)
    elif option == "Sep 5, BBC":
        mission(sep5,bbc_lat,bbc_long)
    elif option == "Sep 18 A, BBC":
        mission(sep18_1,bbc_lat,bbc_long)
    elif option == "Sep 18 B, BBC":
        mission(sep18_2,bbc_lat,bbc_long)
    elif option == "Oct 3, Little River":
        mission(oct3,lil_river_lat,lil_river_long)
    elif option == "Oct 4 Test, Little River":
        mission(oct4_1,lil_river_lat,lil_river_long)
    elif option == "Oct 4, Little River":
        mission(oct4_2,lil_river_lat,lil_river_long)