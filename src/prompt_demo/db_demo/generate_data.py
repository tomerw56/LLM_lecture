import random
from faker import Faker
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship


from  connection import connection_str

faker = Faker()
Base = declarative_base()

# DB Models
class Client(Base):
    __tablename__ = 'clients'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    location = Column(String)

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Float)

class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('clients.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer)
    timestamp = Column(DateTime)

    client = relationship("Client")
    product = relationship("Product")


engine = create_engine(connection_str)
Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)

# Generate data
products = [Product(name=faker.word(), price=random.uniform(10, 100)) for _ in range(100)]
clients = [Client(name=faker.name(), email=faker.email(), location=faker.city()) for _ in range(50)]

session.add_all(products + clients)
session.commit()

for _ in range(500):
    order = Order(
        client_id=random.choice(clients).id,
        product_id=random.choice(products).id,
        quantity=random.randint(1, 5),
        timestamp=faker.date_time_this_year()
    )
    session.add(order)

session.commit()
print("Data generated and inserted.")
