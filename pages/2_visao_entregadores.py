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

st.set_page_config(page_title="Visão Entregadores", page_icon="🚚", layout="wide")

#-----------------
#Funções
#----------------

def top_delivers(df1, top_asc):
    df2 = ( df1.loc[:, ["Delivery_person_ID", "City", "Time_taken(min)"]]
                       .groupby(["City", "Delivery_person_ID"])
                       .max()
                       .sort_values(["City", "Time_taken(min)"], ascending=top_asc).reset_index() )
    df_aux01 = df2.loc[df2["City"] == "Metropolitian", :].head(10)
    df_aux02 = df2.loc[df2["City"] == "Urban", :].head(10)
    df_aux03 = df2.loc[df2["City"] == "Semi-Urban", :].head(10)
    df3 = pd.concat([df_aux01, df_aux02, df_aux03]).reset_index( drop=True )

    return df3

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

# Import dataset
df = pd.read_csv("dataset/train.csv")

# Cleaning data
df1 =  clean_code(df)

# ====================================================
# Barra lateral
# ====================================================

st.header("Marketplace - Visão Entregadores")

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

tab1, tab2, tab3 = st.tabs(["Visão Gerencial", " ", " "])

with tab1:
    with st.container():
        st.title("Overall Metrics")
        col1, col2, col3, col4 = st.columns(4, gap="large")
        with col1:
            # A maior idade dos entregadores
            maior_idade = df1.loc[:, "Delivery_person_Age"].max()
            col1.metric("Maior de idade", maior_idade)

        with col2:
            # A menor idade dos entregadores
            menor_idade = df1.loc[:, "Delivery_person_Age"].min()
            col2.metric("Menor de idade", menor_idade)
        with col3:
            # A melhor condição de veiculo
            melhor_condicao = df1.loc[:, "Vehicle_condition"].max()
            col3.metric("Melhor condição", melhor_condicao)
        with col4:
            # A pior condição de veiculo
            pior_condicao = df1.loc[:, "Vehicle_condition"].min()
            col4.metric("Pior condição", pior_condicao)
            
    with st.container():
        st.markdown("---")
        st.title("Avaliações")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("##### Avaliação médias por Entregador")
            df_aux = (df1.loc[:, ["Delivery_person_ID", "Delivery_person_Ratings"]]
                      .groupby("Delivery_person_ID")
                      .mean().reset_index())
            st.dataframe(df_aux)
        with col2:
            st.markdown("##### Avaliação média por transito")
            df_avg_rating_by_traffic = ( df1.loc[:, ["Delivery_person_Ratings", "Road_traffic_density"]]
                                        .groupby("Road_traffic_density")
                                        .agg({"Delivery_person_Ratings": ["mean", "std"]}))
            # mudança de nomes das colunas
            df_avg_rating_by_traffic.columns = ["delivery_mean", "delivery_std"]
            # reset do index
            df_avg_rating_by_traffic.reset_index()
            st.dataframe(df_avg_rating_by_traffic)
            
            st.markdown("##### Avaliação média por clima")

            df_aux = (df1.loc[:, ["Delivery_person_Ratings", "Weatherconditions"]]
                      .groupby("Weatherconditions")
                      .agg({"Delivery_person_Ratings": ["mean", "std"]}))
            df_aux.columns = ["delivery_mean", "delivery_std"]
            df_aux.reset_index()
            st.dataframe(df_aux)

    with st.container():
        st.markdown("---")
        st.title("Velocidade de Entrega")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("###### Top Entregadores mais rapidos")
            df3 = top_delivers(df1, top_asc=True)
            st.dataframe(df3)

        with col2:
            st.markdown("###### Top Entregadores mais lentos")
            df3 = top_delivers(df1, top_asc=False)
            st.dataframe(df3)
            





        







