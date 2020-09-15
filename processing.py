import pandas as pd
import plotly.express as px
from typing import List

dataset0820 = "ManualLog_11_05_09_92.csv"
dataset0905 = "ManualLog_12_19_47_14.csv"
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
        # print(partial_ds.columns) #to print the head of the dataframe
        return partial_ds
    except ValueError:
        print("Oops!  Some selected water parameters do not exist in this dataset. Try again...")

partial_ds = selectDataframe(dataset0905, selected_parameters)  # calling function selectDataframe

fig = px.scatter_mapbox(partial_ds, lat="Latitude", lon="Longitude", hover_name="Time hh:mm:ss",
                        hover_data=["Total Water Column (m)", "Temperature (c)", "pH", "ODO mg/L", "Salinity (ppt)","Turbid+ NTU", "BGA-PC cells/mL"],
                        color_discrete_sequence=["navy"], center={'lat': partial_ds["Latitude"].iloc[200] , 'lon': partial_ds["Longitude"].iloc[200]} , zoom=16, height=1000)


fig.update_layout(mapbox_style="open-street-map")


# fig.update_layout(
#     mapbox_style="white-bg",
#     mapbox_layers=[
#         {
#             "below": 'traces',
#             "sourcetype": "raster",
#             "source": [
#                 "https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}"
#             ]
#         }
#       ])
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()

