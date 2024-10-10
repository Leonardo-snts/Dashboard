import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc

app = Dash(__name__)

df = pd.read_csv('dataset/vendas_com_quantidade.csv')

#fake_data['Date'] = pd.to_datetime(fake_data['Date'], errors='coerce')

# Gráfico de barras: Quantidade de vendas por status
# Agrupando os dados por status e somando a quantidade
status_counts = df.groupby('status_compra')['quantidade_comprada'].sum().reset_index()

# Criando o gráfico de barras
fig1 = px.bar(status_counts, x='status_compra', y='quantidade_comprada', title='Quantidade de vendas por status')

# Gráfico de pizza: Percentual de vendas por categoria
fig2 = px.pie(df, names='categoria_produto', values='quantidade_comprada', title='Percentual de vendas por categoria')

# Gráfico de linha: Número de vendas ao longo do tempo
compras_ao_tempo = df.groupby('data_compra')['quantidade_comprada'].sum().reset_index()
fig3 = px.line(compras_ao_tempo, x='data_compra', y='quantidade_comprada', title='Número de vendas ao longo do tempo')

# Mapa de calor: Produtos mais vendidos por país (assumindo que você tem dados de país)
fig4 = px.choropleth(df, locations="pais_compra", color="quantidade_comprada",
                    hover_name="pais_compra",
                    locationmode = 'country names',
                    color_continuous_scale=px.colors.sequential.Plasma,
                    title='Produtos mais vendidos por país')

app.layout = html.Div([
    html.H1('Dashboard de Vendas'),
    dcc.Graph(id='grafico-barras', figure=fig1),
    dcc.Graph(id='grafico-pizza', figure=fig2),
    dcc.Graph(id='grafico-linha', figure=fig3),
    dcc.Graph(id='mapa-calor', figure=fig4)
])

if __name__ == '__main__':
    app.run_server(debug=True)
