import streamlit as st
import pandas as pd
import geopandas as gpd
import plotly.express as px 
import plotly.graph_objects as go
import plotly.io as pio
pio.templates["custom"] = go.layout.Template(
    layout_colorway=["#731B26", "#CF4024", "#FF8830", "#FFD940", "#589482", "#53872A"])
pio.templates.default = "custom"
import numpy as np
import requests
from PIL import Image

### Config
st.set_page_config(
    page_title="Energy",
    page_icon="💡 ",
    layout="wide"
)

st.title("💡 Prédire la consommation électrique : Watt a job !")

st.markdown("""
Bienvenue sur cette application de prédiction de la consommation électrique en France pour les jours à venir.

Notre objectif est d'estimer au mieux la consommation pour éviter les coupures de courant.
""")

col1, col2, col3 = st.columns(3)
with col1:
    st.write("")
with col2:
    image = Image.open('img1.png')
    st.image(image, width=400, caption='Created with DALL-E')
with col3:
    st.write("")

@st.cache(allow_output_mutation=True)
def load_data(nrows):
    data = pd.read_csv('master_lag_regions.csv', index_col=0)
    data = data[data["Date"]!="2013-12-31"]
    return data


data_load_state = st.text('Loading data...')
data = load_data(1000)
data_load_state.text("") # change text from "Loading data..." to "" once the the load_data function has run

## Run the below code if the check is checked ✅
if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)  


st.header("Consommation électrique prévue demain")
reg_list = data['region_nom'].sort_values().unique().tolist()
reg = st.selectbox("Sélectionnez une région :", reg_list, key=1)
df = pd.read_csv('master_lag_ml_inversed_revu-final.csv')
df = df[df['Nom_region'] == reg]
response = requests.post("https://watt-a-job.herokuapp.com/predict", json = {
    "Nom_region": reg,
  "lag_1": df.iloc[-1]['lag_1'],
  "lag_2": df.iloc[-1]['lag_2'],
  "lag_3": df.iloc[-1]['lag_3'],
  "lag_4": df.iloc[-1]['lag_4'],
  "lag_5": df.iloc[-1]['lag_5'],
  "lag_6": df.iloc[-1]['lag_6'],
  "lag_7": df.iloc[-1]['lag_7'],
  "lag_8": df.iloc[-1]['lag_8'],
  "lag_9": df.iloc[-1]['lag_9'],
  "lag_10": df.iloc[-1]['lag_10'],
  "lag_11": df.iloc[-1]['lag_11'],
  "lag_12": df.iloc[-1]['lag_12'],
  "lag_13": df.iloc[-1]['lag_13'],
  "lag_14": df.iloc[-1]['lag_14'],
  "lag_15": df.iloc[-1]['lag_15'],
  "lag_364": df.iloc[-1]['lag_364'],
  "day": 6,
  "year": 2013,
  "month": 1,
  "day_of_week": 4
    })
pred = response.json()['prediction']
st.markdown(f"**Consommation estimée pour demain pour la région {reg} :**")
st.metric(label='', value=f"{round(pred):,} MW".replace(',', ' '))
st.markdown("""---""")


st.header("Quelques statistiques sur la consommation d'électricité en France...")

agg_dict = {"Thermique (MW)":"sum", "Nucléaire (MW)":"sum", "Eolien (MW)":"sum", "Solaire (MW)":"sum","Hydraulique (MW)":"sum", "Bioénergies (MW)":"sum"}
nat_evol_share = data.groupby("Date").agg(agg_dict).reset_index()
fig = px.area(nat_evol_share, x="Date", y=["Thermique (MW)", "Nucléaire (MW)", "Eolien (MW)", "Solaire (MW)", "Hydraulique (MW)", "Bioénergies (MW)" ])                  
fig.update_layout(yaxis={'title':'Mega Watts'},
                    title={'text':"Evolution de la consommation d'électricité par source depuis 2014",
                    'font':{'size':28},'x':0.5,'xanchor':'center'},
                    autosize=True,)
st.plotly_chart(fig, use_container_width=True)


nat_evol_eda = data.groupby("year").agg(agg_dict).reset_index()
nat_evol_eda = nat_evol_eda[nat_evol_eda["year"]<2023]
fig = px.area(nat_evol_eda, x="year", y=["Thermique (MW)", "Nucléaire (MW)", "Eolien (MW)", "Solaire (MW)", "Hydraulique (MW)", "Bioénergies (MW)" ])
fig.update_layout(yaxis={'title':'Mega Watts'},
                    title={'text':"Evolution de la consommation d'électricité par source et par année depuis 2014",
                    'font':{'size':28},'x':0.5,'xanchor':'center'},
                    autosize=True,)
st.plotly_chart(fig, use_container_width=True)

col1, col2 = st.columns(2)

with col1:
    # Donut
    st.markdown("**Sources d'électricité au fil des années**")
    inner = nat_evol_eda.iloc[0,1:] #year 2014
    inner2 = nat_evol_eda.iloc[3,1:] #year 2017
    outer = nat_evol_eda.iloc[6,1:] #year 2020
    outer2 = nat_evol_eda.iloc[8,1:] #year 2022
    labels = nat_evol_eda.columns[1:]
    pies = [# Portfolio (inner donut)
        go.Pie(values=inner, labels=labels, hole=0.3, textinfo = "none", direction="clockwise", sort=False),
        go.Pie(values=inner2, labels=labels, hole=0.45, textinfo = "none", direction="clockwise", sort=False),
        go.Pie(values=outer, labels=labels, hole=0.6, textinfo = "none", direction="clockwise", sort=False),
        go.Pie(values=outer2, labels=labels, hole=0.75, direction="clockwise", sort=False, showlegend=False)]

    fig = go.Figure(data=pies)
    fig.update_traces(marker=dict(line=dict(color='white', width=1)))#colors=df["colors"],
    fig.add_annotation(x=0.5, y=0.03,text="<b>2022<b>", showarrow=False, font = dict(size = 18))
    fig.add_annotation(x=0.5, y=0.15,text="<b>2020<b>", showarrow=False)
    fig.add_annotation(x=0.5, y=0.22,text="<b>2017<b>", showarrow=False)
    fig.add_annotation(x=0.5, y=0.29,text="<b>2014<b>", showarrow=False)

    st.plotly_chart(fig, use_container_width=True)
with col2:
    st.markdown("**Evolution du prix de l'électricité en euros par kWh**")
    prix_elec = data.groupby('year')['prix_kwh_elec'].mean()
    fig = px.line(prix_elec)
    fig.update_xaxes(range = [2014,2021])
    fig.update_layout(yaxis={'title':'Prix du kWh'})
    st.plotly_chart(fig, use_container_width=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Consommation moyenne quotidienne d'électricité par année en MW**")
    data['Consommation (MW)'] = data['Consommation (MW)'].astype(float)
    year = st.selectbox("Sélectionnez une année", [year for year in range(2014, 2023)], key=2)
    df = data[data['year'] == year]
    df = df.groupby('Code INSEE région').mean()
    sf = gpd.read_file('https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/regions-version-simplifiee.geojson')
    sf['code'] = sf['code'].astype(int)
    df = pd.DataFrame(df)
    df = df.merge(sf, left_on='Code INSEE région', right_on='code')
    df = gpd.GeoDataFrame(df, geometry = 'geometry')
    df.plot(column='Consommation (MW)', legend=True, cmap='Reds', vmin=80000)
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot()

with col2:
    st.markdown("**Production d'électricité par source en 2022 en MW**")
    source = st.selectbox("Sélectionnez une source d'énergie", df.columns[1:7], key=3)
    df = data[data['year'] == 2022]
    df = df.groupby('Code INSEE région').mean()
    df = df.merge(sf, left_on='Code INSEE région', right_on='code')
    df = gpd.GeoDataFrame(df, geometry = 'geometry')
    df.plot(column=f'{source}', legend=True, cmap='Wistia')
    st.pyplot()

st.header("... Et par région")  

with st.form("key"):
    region = st.selectbox("Selectionnez une région :", data["region_nom"].sort_values().unique(), key=4)
    date = st.date_input("Selectionnez une date :")
    submit = st.form_submit_button("Valider")
    data["Date"]= pd.to_datetime(data["Date"])

if submit:
    date = pd.to_datetime(date)
    maskdate = data["Date"]==date
    maskregion = data["region_nom"]==region

    col1, col2, col3 = st.columns(3)

    with col1:
        valeur_temp_max = data[maskdate & maskregion]["temp_max"].dropna().mean()
        st.metric(label="Température max", value=f"{round(valeur_temp_max)} °C")
    with col2:
        valeur_temp_min = data[maskdate & maskregion]["temp_min"].dropna().mean()
        st.metric(label="Température min", value=f"{round(valeur_temp_min)} °C")
    with col3:
        valeur_conso = data[maskdate & maskregion]["Consommation (MW)"].dropna().mean()
        st.metric(label="Consommation électrique", value=f"{round(valeur_conso):,} MW".replace(',', ' '))

    

