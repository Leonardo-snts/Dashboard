import pandas as pd
import time
from geopy.geocoders import Nominatim
from dash import Dash, html, dcc
import plotly.express as px

# Inicializar o app Dash
app = Dash(__name__)

# Função para carregar e preparar os dados
def load_data(filepath):
    # Carregar os dados do CSV
    data = pd.read_csv(filepath)
    
    # Garantir que a coluna 'Date' seja reconhecida como data
    data['Date'] = pd.to_datetime(data['Date'], errors='coerce')
    
    return data

# Função para inicializar o geocodificador
def init_geolocator():
    return Nominatim(user_agent="geoapiExercises")

# Função para obter latitude e longitude a partir do nome da cidade
def get_coordinates(city, geolocator):
    try:
        location = geolocator.geocode(city)
        if location:
            return location.latitude, location.longitude
        else:
            print(f"Coordenadas não encontradas para {city}")
            return None, None
    except Exception as e:
        print(f"Erro ao obter coordenadas para {city}: {e}")
        return None, None

# Aplicar a geocodificação com intervalo de tempo
def geocode_with_delay(cities, geolocator, delay=1):
    latitudes, longitudes = [], []
    for city in cities:
        lat, lon = get_coordinates(city, geolocator)
        latitudes.append(lat)
        longitudes.append(lon)
        time.sleep(delay)  # Evitar sobrecarga do serviço com um delay entre as consultas
    return latitudes, longitudes

# Função para processar as coordenadas e limpar os dados
def process_coordinates(data):
    geolocator = init_geolocator()
    data['Latitude'], data['Longitude'] = geocode_with_delay(data['City'], geolocator)
    
    # Remover cidades que não têm coordenadas (Latitude e Longitude nulas)
    data = data.dropna(subset=['Latitude', 'Longitude'])
    
    return data

# Função para gerar os gráficos
def generate_graphs(data):
    # Gráfico 1: Volume de vendas por status
    sales_status = data.groupby('Status')['Amount'].sum().reset_index()
    fig1 = px.bar(sales_status, x='Status', y='Amount', title='Volume de Vendas por Status')

    # Gráfico 2: Top 10 SKUs vendidos
    top_sku_sales = data.groupby('SKU')['Amount'].sum().nlargest(10).reset_index()
    fig2 = px.bar(top_sku_sales, x='SKU', y='Amount', title='Top 10 SKUs Vendidos')

    # Gráfico 3: Distribuição de vendas por categoria de produto
    sales_by_category = data.groupby('Category')['Amount'].sum().reset_index()
    fig3 = px.pie(sales_by_category, values='Amount', names='Category', title='Distribuição de Vendas por Categoria')

    # Gráfico 4: Comparação de vendas ao longo do tempo
    sales_over_time = data.groupby('Date')['Amount'].sum().reset_index()
    fig4 = px.line(sales_over_time, x='Date', y='Amount', title='Vendas ao Longo do Tempo')

    # Gráfico 5: Mapa das vendas por cidade com cores
    sales_by_city = data.groupby(['City', 'Latitude', 'Longitude'])['Amount'].sum().reset_index()
    fig5 = px.scatter_geo(
        sales_by_city,
        lat='Latitude',
        lon='Longitude',
        size='Amount',
        hover_name='City',
        color='Amount',
        title='Distribuição Geográfica das Compras no Mundo',
        scope='world',
        projection='natural earth'
    )

    return fig1, fig2, fig3, fig4, fig5

# Função para configurar o layout do app
def create_layout(fig5):
    return html.Div(children=[
        html.H1(children='Dashboard de Vendas E-commerce'),
        html.Div(children='Dash: Um exemplo de visualização de dados com dados falsos'),
        dcc.Graph(id='graph5', figure=fig5)
    ])

# Função principal para executar o app
def run_dashboard():
    fake_data = load_data('dataset/fake_ecommerce_data_with_coordinates.csv')
    fake_data = process_coordinates(fake_data)
    
    # Gerar gráficos
    _, _, _, _, fig5 = generate_graphs(fake_data)

    # Definir o layout do app
    app.layout = create_layout(fig5)

    # Iniciar o servidor
    if __name__ == '__main__':
        app.run_server(debug=True)

# Executar o dashboard
run_dashboard()
