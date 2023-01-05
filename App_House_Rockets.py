import pandas as pd
import streamlit as st
import numpy as np
import folium
import geopandas
import plotly.express as px
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster

# Configura o layout da pagina onde será plotado os dados e gráficos
st.set_page_config(layout = 'wide')

# Decorador do streamlit = st.cache
# Função leitor do arquivo de dados
@st.cache( allow_output_mutation=True)
def get_data(path):
    data = pd.read_csv(path)

    return  data

@st.cache( allow_output_mutation=True )
def get_geofile( url ):
    geofile = geopandas.read_file( url )

    return geofile

# Criação de variável para sabermos o preço do imóvel por metro quadrado
def set_feature(df):
    data['price_m2'] = data['price'] / (data['sqft_lot'] * 0.093)

    return  data


# -----------------------------------------------------------------------
# Data Overview
# -----------------------------------------------------------------------
# Primeiras Requisições do CEO:

def overview_data(data):
    st.title('----------- HOUSE ROCKETS APP -----------')
    # Titulo
    st.title('Data Overview')

    # Filtro de colunas utilizando st.sidebar. Nomeando o filtro e utilizando os atributos como opções:
    f_attributes = st.sidebar.multiselect('Enter Columns (attributes)', data.columns)

    # Filtro da coluna 'ZipCode' utilizando st.sidebar. Nomeando o filtro e utilizando os dados da coluna como opções:
    f_zipcode = st.sidebar.multiselect('Enter ZipCode', data['zipcode'].unique())


    # attributes + zipcode = Seleciona colunas e linhas
    # attributes = Seleciona colunas
    # zipcode = Seleciona linhas
    # nenhum marcação (Default) = retorna o dataset original

    # Seleção colunas e linhas
    if (f_zipcode != []) & (f_attributes != []):
        data = data.loc[data['zipcode'].isin(f_zipcode), f_attributes]

    # Seleção apenas de linhas
    elif (f_zipcode != []) & (f_attributes == []):
        data = data.loc[data['zipcode'].isin(f_zipcode), :]

    # Seleção apenas de colunas
    elif (f_zipcode == []) & (f_attributes != []):
        data = data.loc[:, f_attributes]

    # Mostra o default
    else:
        data = data.copy()

    # Formatação do dataframe
    st.dataframe(data, height=200)
    c1, c2 = st.columns((1, 1))

    # Execução de Metricas
        # Cabeçalho
    c1.header('Average Values')

    df1 = data[['id', 'zipcode']].groupby('zipcode').count().reset_index()
    df2 = data[['price', 'zipcode']].groupby('zipcode').mean().reset_index()
    df3 = data[['sqft_living', 'zipcode']].groupby('zipcode').mean().reset_index()
    df4 = data[['price_m2', 'zipcode']].groupby('zipcode').mean().reset_index()

    # União dos atributos com o mesmo ZipCode
    m1 = pd.merge(df1, df2, on='zipcode', how='inner')
    m2 = pd.merge(m1, df3, on='zipcode', how='inner')
    df = pd.merge(m2, df4, on='zipcode', how='inner')

    # Renomeando dos atributos
    df.columns = ['ZipCode', 'TotalHouses', 'Price', 'SqftLiving', 'PriceM2']
    c1.dataframe(df, height=300)

    # Estatisticas
    c2.header('Descriptive Analysis')
    # Variável selecionando apenas valores numéricos
    num_attributes = df.select_dtypes(include=['int64', 'float64'])
    media = pd.DataFrame(num_attributes.apply(np.mean))
    mediana = pd.DataFrame(num_attributes.apply(np.median))
    std = pd.DataFrame(num_attributes.apply(np.std))

    # Metricas de dispersão dos dados
    _max = pd.DataFrame(num_attributes.apply(np.max))
    _min = pd.DataFrame(num_attributes.apply(np.min))

    df1 = pd.concat([_max, _min, media, mediana, std], axis=1).reset_index()
    df1.columns = ['Attributes', 'Max', 'Min', 'Mean', 'Median', 'Std']
    c2.dataframe(df1, height=300)

    return None

# ------------------------------------
# Densidade de Portfólio
# ------------------------------------
def portifolio_density(data, geofile):
    # Título Mapa
    st.title('Region Overview')

    c1, c2 = st.columns((1, 1))
    c1.header('Portfólio Density')

    df = data.sample(100)

    # Construcão Mapa
    # BaseMap - Folium

    density_map = folium.Map(location=[data['lat'].mean(),
                                       data['long'].mean()],
                             default_zoom_start=15)
    # Marcadores no Mapa
    marker_cluster = MarkerCluster().add_to(density_map)

    for name, row in df.iterrows():
        folium.Marker([row['lat'], row['long']],
                      popup='Sold R${0} On: {1}. Features: {2} Sqft,{3} Bedrooms, {4} Bathrooms, Year Built: {5}'.
                      format(row['price'],
                             row['date'],
                             row['sqft_living'],
                             row['bedrooms'],
                             row['bathrooms'],
                             row['yr_built'])).add_to(marker_cluster)

    with c1:
        folium_static(density_map)

    # Region Price Map
    c2.header('Price Density')

    df = data[['price', 'zipcode']].groupby('zipcode').mean().reset_index()
    df.columns = ['ZIP', 'PRICE']

    # Define através de um arquivo externo qual a delimitação das regiões.
    geofile = geofile[geofile['ZIP'].isin(df['ZIP'].tolist())]

    region_price_map = folium.Map(location=[data['lat'].mean(),
                                  data['long'].mean()],
                                  default_zoom_start=15)
    region_price_map.choropleth(data=df,
                                geo_data = geofile,
                                columns=['ZIP', 'PRICE'],
                                key_on='feature.properties.ZIP',
                                fill_color='YlOrRd',
                                fill_opacity=0.7,
                                line_opacity=0.2,
                                legend_name='AVG PRICE')
    with c2:
        folium_static( region_price_map )
    return None

# ---------------------------------------------
# Distribuição imóveis por categorias
# ---------------------------------------------
def comercial(data):
    st.sidebar.title('Comercial Options')
    st.title('Comercial attributes')

    min_year_built = int(data['yr_built'].min())
    max_year_built = int(data['yr_built'].max())
    st.sidebar.subheader('Select Max Year Built')
    f_yr_built = st.sidebar.slider('year built',
                                   min_year_built,
                                   max_year_built,
                                   min_year_built)
    # Média de preço pro ano de construção
    st.header('AVG Price / yr_built')

    # get data
    data['date'] = pd.to_datetime(data['date']).dt.strftime('%Y-%m%-%d')

    # -----  AVG price / year
    df = data.loc[data['yr_built'] < f_yr_built]
    df = df[['yr_built', 'price']].groupby('yr_built').mean().reset_index()

    fig = px.line(df, x='yr_built', y='price')
    st.plotly_chart(fig, use_container_width=True)

    return None

if __name__ == "__main__":
    title = 'House Rockets App'
    # ETL
    # Extration
    path = 'kc_house_data.csv'
    url = 'https://opendata.arcgis.com/datasets/83fc2e72903343aabff6de8cb445b81c_2.geojson'
    data = get_data(path)
    geofile = get_geofile( url )

    # Transformation
    data = set_feature(data)
    overview_data (data)

    portifolio_density(data, geofile)

    comercial(data)


