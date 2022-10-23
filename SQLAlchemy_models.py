from winreg import REG_LEGAL_OPTION
import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Publisher(Base):
    __tablename__ = 'publisher'
    
    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40), unique=True)
    
    def __str__(self) -> str:
        return f'Publisher {self.id}: {self.name}'
    
class Book(Base):
    
    __tablename__ = 'book'
    
    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(length=60), unique=True)
    publisher_id = sq.Column(sq.Integer, sq.ForeignKey('publisher.id'), nullable=False)
    
    publisher = relationship(Publisher, backref='books')
    
    def __str__(self) -> str:
        return f'Book {self.id}: {self.title}, {self.publisher_id}'
class Shop(Base):
    
    __tablename__ = 'shop'
    
    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40), unique=True)

    def __str__(self) -> str:
        return f'Shop {self.id}: {self.name}'
    
class Stock(Base):
    
    __tablename__ = 'stock'
    
    id = sq.Column(sq.Integer, primary_key=True)
    book_id = sq.Column(sq.Integer, sq.ForeignKey('book.id'), nullable=False)
    shop_id = sq.Column(sq.Integer, sq.ForeignKey('shop.id'), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)
    
    book = relationship(Book, backref='stock')
    shop = relationship(Shop, backref='stock')
    
    def __str__(self) -> str:
        return f'Stock {self.id}: {self.book_id}, {self.shop_id}, {self.count}'
    
class Sale(Base):
    
    __tablename__ = 'sale'
    
    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.Float, nullable=False)
    sale_date = sq.Column(sq.Date, nullable=False)
    stock_id = sq.Column(sq.Integer, sq.ForeignKey('stock.id'), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)
    
    sale = relationship(Stock, backref='sale')
    
    def __str__(self) -> str:
        return f'Sale {self.id}: {self.price}, {self.sale_date}, {self.stock_id}, {self.count}'
    
def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)