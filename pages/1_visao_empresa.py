# Libraries
#from haversine import haversine
import plotly.express as px
import streamlit as st
import datetime
import folium
import pandas as pd
#import ploty.graph_objects as go

# Necessary Libraries
from streamlit_folium import folium_static
from PIL import Image

st.set_page_config(page_title="Visão Empresa", page_icon="📈", layout="wide")

#-----------------
#Funções
#----------------

def country_maps(df1):
    df_aux = ( df1.loc[: , ["City", "Road_traffic_density", "Delivery_location_latitude", "Delivery_location_longitude"]]
                  .groupby(["City", "Road_traffic_density"])
                  .median().reset_index() )
    df_aux = df_aux.loc[df_aux["City"] != "NaN", :]
    df_aux = df_aux.loc[df_aux["Road_traffic_density"] != "NaN", :]
    df_aux = df_aux.head()
    
    map = folium.Map()
    
    for index, location_info in df_aux.iterrows():
        folium.Marker([location_info["Delivery_location_latitude"],
                         location_info["Delivery_location_longitude"]],
                         popup=location_info[["City", "Road_traffic_density"]]).add_to(map)
    folium_static(map, width=1024, height=600)

def order_share_by_week(df1):   
    # Quantidade de pedidos por semana / Numero único de entregadores por semana
    df_aux01 = ( df1.loc[:, ["ID", "week_of_year"]]
                .groupby("week_of_year")
                .count().reset_index() )
    df_aux02 = df1.loc[:, ["Delivery_person_ID", "week_of_year"]].groupby("week_of_year").nunique().reset_index()
    
    df_aux = pd.merge(df_aux01, df_aux02, how="inner")
    
    df_aux["order_by_deliver"] = df_aux["ID"] / df_aux["Delivery_person_ID"]
    
    fig = px.line(df_aux, x="week_of_year", y="order_by_deliver")
    return fig

def order_by_week(df1):
    df1["week_of_year"] = df1["Order_Date"].dt.strftime("%U")
        
    df_aux = df1.loc[:, ["ID", "week_of_year"]].groupby("week_of_year").count().reset_index()
    df_aux.head()
        
    fig = px.line(df_aux, x="week_of_year", y="ID")
    return fig

def traffic_order_city(df1):
    df_aux = ( df1.loc[:,["ID","City","Road_traffic_density"]]
                .groupby(["City","Road_traffic_density"])
                .count().reset_index())
    
    fig = px.scatter(df_aux, x="City", y="Road_traffic_density", size="ID", color="City")
    return fig

def traffic_order_share(df1):
    df_aux = ( df1.loc[:,["ID","Road_traffic_density"]]
              .groupby("Road_traffic_density")
              .count().reset_index() )
                
    df_aux = df_aux.loc[df_aux["Road_traffic_density"] != "NaN", :]
    df_aux["entregas_perc"] = df_aux["ID"] / df_aux["ID"].sum()
    
    fig = px.pie(df_aux, values="entregas_perc", names="Road_traffic_density")
    return fig

def order_metric(df1):
    # Order Metric
    #Colunas
    cols = ["ID", "Order_Date"]
            
    #Selecao de linhas
    df_aux = df1.loc[:, cols].groupby("Order_Date").count().reset_index()
            
    #desenhar o gráfico de linhas
    # Plotly
    fig = px.bar(df_aux, x="Order_Date", y="ID")
    return fig

def clean_code( df1 ):
    #1 Convertendo a coluna Age de texto para numero
    linhas_selecionadas = (df1["Delivery_person_Age"] != "NaN ")
    df1 = df1.loc[linhas_selecionadas, :].copy()
    
    linhas_selecionadas = (df1["Road_traffic_density"] != "NaN ")
    df1 = df1.loc[linhas_selecionadas, :].copy()
    
    linhas_selecionadas = (df1["City"] != "NaN ")
    df1 = df1.loc[linhas_selecionadas, :].copy()
    
    linhas_selecionadas = (df1["Festival"] != "NaN ")
    df1 = df1.loc[linhas_selecionadas, :].copy()
    
    df1["Delivery_person_Age"] = df1["Delivery_person_Age"].astype(int)
    
    #2 Convertendo a coluna Ratings de texto para numero decimal(float)
    df1["Delivery_person_Ratings"] = df1["Delivery_person_Ratings"].astype(float)
    
    #3 Convertendo a coluna order_date de texto para data
    df1["Order_Date"] = pd.to_datetime(df1["Order_Date"], format="%d-%m-%Y")
    
    #4 Convertendo multiple_deliveries de texto para numero inteiro(int)
    linhas_selecionadas = (df1["multiple_deliveries"] != "NaN ")
    df1 = df1.loc[linhas_selecionadas, :].copy()
    df1["multiple_deliveries"] = df1["multiple_deliveries"].astype(int)
    
    #5 Removendo os espaços dentro de strings/textos/object
    # df1 = df1.reset_index(drop=True)
    # for i in range(len(df1)):
    #   df1.loc[i, "ID"] = df1.loc[i, "ID"].strip()
    
    #6 Removendo os espaços dentro de strings/textos/object sem for
    df1.loc[:, "ID"] = df1.loc[:, "ID"].str.strip()
    # Removenso os espaços de dentro de string/textos/object
    df1.loc[:, "Road_traffic_density"] = df1.loc[:, "Road_traffic_density"].str.strip()
    df1.loc[:, "City"] = df1.loc[:, "City"].str.strip()
    df1.loc[:, "Type_of_order"] = df1.loc[:, "Type_of_order"].str.strip()
    df1.loc[:, "Type_of_vehicle"] = df1.loc[:, "Type_of_vehicle"].str.strip()
    df1.loc[:, "Festival"] = df1.loc[:, "Festival"].str.strip()
    
    #7 Limpandoa coluna de time taken
    df1["Time_taken(min)"] = df1["Time_taken(min)"].apply(lambda x: x.split("(min) ")[1])
    df1["Time_taken(min)"] = df1["Time_taken(min)"].astype(int)

    return df1

    #----------------Inicio da Estrutura lógica do código--------------------

# Import dataset
df = pd.read_csv("dataset/train.csv")

df1 = clean_code(df)

# ====================================================
# Barra lateral
# ====================================================

st.header("Marketplace - Visão Cliente")

# image_path = 'logo.png'
image = Image.open("logo.png")

st.sidebar.image(image, width=120)

st.sidebar.markdown("# Cury Company")
st.sidebar.markdown("## Fastest Delivery in Town")
st.sidebar.markdown("""---""")

st.sidebar.markdown("## Selecione uma data limite")
date_slider = st.sidebar.slider(
    "Até qual valor?",
    value=datetime.date(2022, 4, 13),
    min_value=datetime.date(2022, 2, 11),
    max_value=datetime.date(2022, 4, 6),
    format="DD-MM-YYYY"
)

st.sidebar.markdown("""---""")

traffic_options = st.sidebar.multiselect(
    "Quais as condições do trânsito",
    ["Low", "Medium", "High", "Jam"],
    default=["Low", "Medium", "High", "Jam"]
)

st.sidebar.markdown("""---""")

st.sidebar.markdown("### Powered By Thiago Souza")


# Filtro de data
date_slider_datetime = pd.to_datetime(date_slider)
linhas_selecionadas =  df1["Order_Date"] < date_slider_datetime
df1 = df1.loc[linhas_selecionadas, :]


#Filtro de transito
linhas_selecionadas = df1["Road_traffic_density"].isin(traffic_options)
df1 = df1.loc[linhas_selecionadas, :]

# ====================================================
# Layout com Streamlit
# ====================================================

tab1, tab2, tab3 = st.tabs(["Visão Gerencial", "Visão Tática", "Visão Geográfica"])

with tab1:
    with st.container():
        fig = order_metric(df1)
        st.markdown("# Orders by Day")
        st.plotly_chart(fig, use_container_width=True)

    with st.container():
        col1, col2 = st.columns(2)
    
        with col1:
            st.header("Traffic Order Share")
            fig = traffic_order_share(df1)
            st.plotly_chart(fig, use_container_with=True)
    
        with col2:
            st.header("Traffic Order City")
            fig = traffic_order_city(df1)
            st.plotly_chart(fig, use_container_with=True)
    
with tab2:
    with st.container():
        st.markdown("# Order by Week")
        fig = order_by_week(df1)
        st.plotly_chart(fig, user_container_with=True)
        
    with st.container():
        st.markdown("# Order Share By Weed")
        fig = order_share_by_week(df1)
        st.plotly_chart(fig, use_container_with=True)

with tab3:
    st.markdown("# Country Maps")
    country_maps(df1)


















