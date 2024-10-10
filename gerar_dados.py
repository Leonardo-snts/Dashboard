import pandas as pd
from faker import Faker
import random

# Criando um objeto Faker para gerar dados
fake = Faker()

# Dicionário de categorias e seus respectivos produtos
categories = {
    'Eletrônicos': ['Smartphone', 'Notebook', 'Tablet', 'SmartTV', 'Fones de Ouvido', 'Câmera', 'Console', 'Relógio Inteligente', 'Drone', 'Alexa'],
    'Vestuário': ['Camiseta', 'Calça', 'Tênis', 'Vestido', 'Jaqueta', 'Saia', 'Blusa', 'Meia', 'Óculos', 'Cintos'],
    'Alimentos': ['Arroz', 'Feijão', 'Macarrão', 'Leite', 'Ovos', 'Frutas', 'Verduras', 'Carne', 'Peixe', 'Pão'],
    'Casa': ['Sofá', 'Cama', 'Mesa', 'Cadeira', 'Armário', 'Geladeira', 'Fogão', 'Microondas', 'Liquidificador', 'Aspirador de Pó'],
    'Beleza': ['Shampoo', 'Condicionador', 'Maquiagem', 'Perfume', 'Hidratante', 'Sabonete', 'Esmalte', 'Batom', 'Máscara', 'Tônico'],
    'Brinquedos': ['Boneca', 'Carro', 'Jogo de tabuleiro', 'Video game', 'Lego', 'Boneco de ação', 'Pelúcia', 'Patinete', 'Bicicleta', 'Bola'],
    'Livros': ['Romance', 'Ficção', 'Não-ficção', 'Infantil', 'Didático', 'Religioso', 'Científico', 'História', 'Poesia', 'Autoajuda'],
    'Esporte': ['Bola de futebol', 'Raquete de tênis', 'Chuteira', 'Barra fixa', 'Aparelho de musculação', 'Tênis de corrida', 'Roupa esportiva', 'Protetor bucal', 'Óculos de sol esportivos', 'Skate'],
    'Escritório': ['Caderno', 'Caneta', 'Lápis', 'Borracha', 'Tesoura', 'Grampeador', 'Corretivo', 'Calculadora', 'Impressora', 'Computador'],
    'Viagens': ['Passagem aérea', 'Hospedagem', 'Seguro viagem', 'Aluguel de carro', 'Passeio turístico', 'Cruzeiro', 'Mochila de viagem', 'Adaptador de tomada', 'Guia de viagem', 'Mala']
}

# Função para gerar um dicionário com os dados de uma venda
def gerar_venda():
    categoria = random.choice(list(categories.keys()))
    produto = random.choice(categories[categoria])
    return {
        'código_venda': fake.uuid4(),
        'código_barras': fake.ean13(),
        'nome_produto': produto,
        'categoria_produto': categoria,
        'preço_produto': f"R${(fake.random_int(min=10, max=1000)):.2f}",
        'status_compra': fake.random_element(elements=('Concluída', 'Cancelada', 'Pendente')),
        'data_compra': fake.date_between(start_date='-1y', end_date='now'),
        'comprador': fake.name(),
        'email_comprador': fake.email(),
        'pais_compra': fake.country(),
        'quantidade_comprada': fake.random_int(min=1, max=10)  # Quantidade de produtos por compra
    }

# Gerando 1000 vendas
vendas = [gerar_venda() for _ in range(1000)]

# Criando um DataFrame
df = pd.DataFrame(vendas)

# Calculando as médias
df['média_por_categoria'] = df.groupby('categoria_produto')['quantidade_comprada'].transform('mean')
df['média_por_pais'] = df.groupby('pais_compra')['quantidade_comprada'].transform('mean')

# Salvando o DataFrame em um arquivo CSV
df.to_csv('dataset/vendas_com_quantidade.csv', index=False)

print("Arquivo CSV gerado com sucesso!")