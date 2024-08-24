import pandas as pd
import requests
import json
import pydeck as pdk
import streamlit as st

st.write("# 서울시 따릉이 대여소")

api_key = "757766614b74616c374a46696a55"
bike_dict = {"rackTotCnt":[], "stationName":[],
             "parkingBikeTotCnt":[], "shared":[],
             "latitude":[], "longitude":[]}
num = 0
while True:
    url = f"http://openapi.seoul.go.kr:8088/{api_key}/json/bikeList/{1 + 1000 * num}/{1000 + 1000 * num}/"
    data = requests.get(url)
    result = json.loads(data.text)  # json --> dict
    for row in result["rentBikeStatus"]["row"]:
        bike_dict["rackTotCnt"].append(int(row["rackTotCnt"]))
        bike_dict["stationName"].append(row["stationName"])
        bike_dict["parkingBikeTotCnt"].append(int(row["parkingBikeTotCnt"]))
        bike_dict["shared"].append(int(row["shared"]))
        bike_dict["latitude"].append(float(row["stationLatitude"]))
        bike_dict["longitude"].append(float(row["stationLongitude"]))
    if len(result["rentBikeStatus"]["row"]) != 1000:
        break
    num += 1

df = pd.DataFrame(bike_dict)
st.write(df)

layer = pdk.Layer(
    "ScatterplotLayer",
    df,
    get_position=["longitude", "latitude"],
    get_fill_color=["255-shared", "255-shared", "255"],
    get_radius="60*shared/100",
    pickable=True
)
init = pdk.ViewState(latitude=df["latitude"].mean(), longitude=df["longitude"].mean(), zoom=10)
map = pdk.Deck(initial_view_state=init, layers=[layer],tooltip={"text":"[{stationName}]\n현재 주차 대수 : {parkingBikeTotCnt}"})
st.pydeck_chart(map)
