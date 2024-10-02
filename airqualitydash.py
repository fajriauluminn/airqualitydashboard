import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from babel.numbers import format_currency
import seaborn as sns
sns.set(style='dark')

def create_monthly_quality(df):
    monthly_df = df.resample(rule='M', on='datetime').agg({
        "No": "nunique",
        "CO": "mean"
    })
    monthly_df = monthly_df.reset_index()
    monthly_df.rename(columns={
        "No": "total_entry",
        "CO": "CO_contains"
    }, inplace=True)
    
    return monthly_df

def create_mean_so2_param_df(df):
    mean_so2_param = df.groupby("station").SO2.mean().sort_values(ascending=False).reset_index()
    return mean_so2_param

def create_mean_co_param(df):
    mean_co_param = df.groupby("station").CO.mean().sort_values(ascending=False).reset_index()
    return mean_co_param

df_airquality = pd.read_csv("df_airquality.csv")

df_airquality['datetime'] = pd.to_datetime(df_airquality['datetime'])

df_airquality.sort_values(by="datetime", inplace=True)
df_airquality.reset_index(inplace=True)

min_date = df_airquality['datetime'].min().date()
max_date = df_airquality['datetime'].max().date()

with st.sidebar:
    st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQpVHPPDBolycTcCIcUvdZvvmX7hsDl6h8LNw&s")

    start_date, end_date = st.date_input(
        label='Range Time', min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = df_airquality[(df_airquality['datetime'] >= str(start_date)) &
                        (df_airquality['datetime'] <= str(end_date))]

monthly_df = create_monthly_quality(main_df)
mean_so2_param = create_mean_so2_param_df(main_df)
mean_co_param = create_mean_co_param(main_df)

st.header("Air Quality Filter")

st.subheader("Parameter Contains")
col1, col2 = st. columns(2)

with col1:
    mean_co = monthly_df.CO_contains.mean()
    st.metric("CO Contains Mean  μg/m3", value = mean_co)

with col2:
    input_co = monthly_df.total_entry.sum()
    st.metric("Total Daily Input", value=input_co)

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    monthly_df["datetime"],
    monthly_df["CO_contains"],
    marker = 'o',
    linewidth=2,
    color="#90CAF9"
)

ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x',labelsize=15)

st.pyplot(fig)

st.subheader("The Highest and The Lowest SO2 Contains")

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))

colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

average_so2 = df_airquality.groupby('station')['SO2'].mean().reset_index()
sorted_avg_so2 = average_so2.sort_values(by='SO2', ascending=True)

sns.barplot(x="SO2", y="station", data=sorted_avg_so2.head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("Lowest SO2 Contains", loc="center", fontsize=15)
ax[0].tick_params(axis ='y', labelsize=12)
 
sns.barplot(x="SO2", y="station", data=sorted_avg_so2.sort_values(by="SO2", ascending=False).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Highest SO2 Contains", loc="center", fontsize=15)
ax[1].tick_params(axis='y', labelsize=12)

st.pyplot(fig)


st.subheader("Best and Worst Air Quality Based on PM10 Indicator")

average_pm10 = df_airquality.groupby('station')['PM10'].mean().reset_index()
sorted_avg_pm10 = average_pm10.sort_values(by='PM10', ascending=True)
sorted_avg_pm10


fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))

colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
sns.barplot(x="PM10", y="station", data=sorted_avg_pm10.head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("Best Air Quality", loc="center", fontsize=15)
ax[0].tick_params(axis ='y', labelsize=12)
 
sns.barplot(x="PM10", y="station", data=sorted_avg_pm10.sort_values(by="PM10", ascending=False).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Worst Air Quality", loc="center", fontsize=15)
ax[1].tick_params(axis='y', labelsize=12)

st.pyplot(fig)
