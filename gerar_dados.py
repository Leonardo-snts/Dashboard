import pandas as pd
import random
from faker import Faker

# Inicializar Faker
fake = Faker()

# Parâmetros
num_records = 300  # Número de registros a serem gerados
countries = [fake.country() for _ in range(50)] 
categories = ['Clothing', 'Electronics', 'Home & Kitchen', 'Books', 'Beauty', 'Toys', 'Sports', 'Automotive', 'Health', 'Office Supplies']

# Função para gerar dados falsos
def generate_fake_ecommerce_data(num_records):
    data = []
    for _ in range(num_records):
        order_id = fake.uuid4()  # ID único do pedido
        sku = fake.ean8()  # SKU (código de barras)
        product_name = fake.word().capitalize() + ' ' + fake.word().capitalize()  # Nome do produto
        category = random.choice(categories)  # Categoria aleatória
        amount = round(random.uniform(10.0, 500.0), 2)  # Preço aleatório entre 10 e 500
        status = random.choice(['Shipped', 'Pending', 'Cancelled', 'Returned'])  # Status aleatório do pedido
        date = fake.date_between(start_date='-1y', end_date='today')  # Data de venda nos últimos 12 meses
        customer_name = fake.name()  # Nome do cliente
        customer_email = fake.email()  # Email do cliente
        pais = fake.country()

        data.append({
            'Order ID': order_id,
            'SKU': sku,
            'Product Name': product_name,
            'Category': category,
            'Amount': amount,
            'Status': status,
            'Date': date,
            'Customer Name': customer_name,
            'Customer Email': customer_email,
            'Pais': pais,
        })
    
    return pd.DataFrame(data)

# Gerar os dados
fake_ecommerce_data = generate_fake_ecommerce_data(num_records)

# Salvar em um arquivo CSV
fake_ecommerce_data.to_csv('dataset/fake_ecommerce_data.csv', index=False)

print("Dados de e-commerce gerados e salvos em 'dataset/fake_ecommerce_data.csv'!")
