import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc

# Inicializar o app Dash
app = Dash(__name__)

# Carregar os dados falsos gerados no CSV
fake_data = pd.read_csv('dataset/fake_ecommerce_data.csv')

# Garantir que a coluna 'Date' seja reconhecida como data
fake_data['Date'] = pd.to_datetime(fake_data['Date'], errors='coerce')

# Gráfico 1: Volume de vendas por status
sales_status = fake_data.groupby('Status')['Amount'].sum().reset_index()
fig1 = px.bar(sales_status, x='Status', y='Amount', title='Volume de Vendas por Status')

# Gráfico 2: Top 10 SKUs vendidos
top_sku_sales = fake_data.groupby('SKU')['Amount'].sum().nlargest(10).reset_index()
fig2 = px.bar(top_sku_sales, x='SKU', y='Amount', title='Top 10 SKUs Vendidos')

# Gráfico 3: Distribuição de vendas por categoria de produto
sales_by_category = fake_data.groupby('Category')['Amount'].sum().reset_index()
fig3 = px.pie(sales_by_category, values='Amount', names='Category', title='Distribuição de Vendas por Categoria')

# Gráfico 4: Comparação de vendas ao longo do tempo
sales_over_time = fake_data.groupby('Date')['Amount'].sum().reset_index()
fig4 = px.line(sales_over_time, x='Date', y='Amount', title='Vendas ao Longo do Tempo')

# Gráfico 5: Mapa das vendas por cidade com coloração baseada no valor de vendas
fig5 = px.choropleth(
    fake_data,
    locations="Pais",  # Nome dos países
    locationmode="country names",  # Modo baseado no nome dos países
    color="Amount",  # Coluna para definir a cor (percentual de vendas)
    hover_name="Pais",  # Nome a ser exibido ao passar o mouse
    title='Distribuição Geográfica das Vendas por País',
    color_continuous_scale=px.colors.sequential.Plasma  # Escala de cores
)

# Ajustar o layout do mapa
fig5.update_layout(
    geo=dict(
        showframe=False,
        showcoastlines=False,
        projection_type='natural earth'  # Projeção do mapa
    ),
    coloraxis_colorbar=dict(
        title="Percentual de Vendas",
        ticks="outside"
    )
)

# Layout do app
app.layout = html.Div(children=[
    html.H1(children='Dashboard de Vendas E-commerce'),

    html.Div(children='Dash: Um exemplo de visualização de dados com dados falsos'),

    # Exibir gráfico 1 (Volume de Vendas por Status)
    dcc.Graph(
        id='graph1',
        figure=fig1
    ),

    # Exibir gráfico 2 (Top 10 SKUs Vendidos)
    dcc.Graph(
        id='graph2',
        figure=fig2
    ),

    # Exibir gráfico 3 (Distribuição de Vendas por Categoria)
    dcc.Graph(
        id='graph3',
        figure=fig3
    ),

    # Exibir gráfico 4 (Vendas ao Longo do Tempo)
    dcc.Graph(
        id='graph4',
        figure=fig4
    ),

    # Exibir gráfico 5 (Distribuição Geográfica das Compras)
    dcc.Graph(
        id='graph5',
        figure=fig5
    ),
])

# Iniciar o servidor
if __name__ == '__main__':
    app.run_server(debug=True)
