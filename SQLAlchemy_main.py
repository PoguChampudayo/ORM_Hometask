from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from SQLAlchemy_models import Book, Publisher, Sale, Shop, Stock, create_tables
import json

        
def connect_to_db(db, login, password, db_name):
    '''Подключение к БД интересующего типа'''
    
    DSN = f'{db}://{login}:{password}@localhost:5432/{db_name}'
    return create_engine(DSN)

def fill_db_manually(engine):

    from SQLAlchemy_models import Publisher, Book, Shop, Stock, Sale
    
    session = sessionmaker(bind=engine)()
    publisher1 = Publisher(name='Фламинго')
    publisher2 = Publisher(name='Росмэн')
    book1 = Book(title='Черновик', publisher_id = 1)
    book2 = Book(title='Гарри Поттер и философский камень', publisher_id=2)
    shop1 = Shop(name='ЛитРес')
    shop2 = Shop(name='Читайгород')
    stock1 = Stock(book_id=1, shop_id=1, count=500)
    stock2 = Stock(book_id=2, shop_id=2, count=1000)
    sale1 = Sale(price=200, sale_date='10.10.2022', stock_id=1, count=200)
    sale2 = Sale(price=249.99, sale_date='15.10.2022', stock_id=2, count=300)
    session.add_all([publisher1, publisher2, book1, book2, shop1, shop2, stock1, stock2, sale1, sale2])
    session.commit()

def fill_db_from_json(engine, file_name):
    session = sessionmaker(bind=engine)()
    with open(file_name, 'r') as filler:
        data = json.load(filler)
    for element in data:
        model = {
            'publisher':Publisher,
            'book': Book,
            'shop': Shop,
            'stock': Stock,
            'sale': Sale
        }[element.get('model')]
        session.add(model(id=element.get('pk'), **element.get('fields'))) 
    session.commit() 
    
def define_params():
    '''Вспомогательная функция для поиска магазина и издателя'''
    request = input('Введите имя или идентификатор издателя: ')
    param = {}
    if request == '':
        return param
    elif request.isnumeric():
        param['id'] = int(request)
    else:
        param['name'] = request
    return param

def find_shop_by_publisher(engine):
    '''Поиск магазинов с книгами, выпущенными искомым издателем'''
    
    from SQLAlchemy_models import Publisher, Book, Shop, Stock
    params = define_params()
    session = sessionmaker(bind=engine)()
    if 'id' in params:
        for c in (session.query(Shop).join(Stock.shop).join(Stock.book)
            .join(Book.publisher).filter(Publisher.id == params.get('id'))):
            print(c)
    elif 'name' in params:
        for c in (session.query(Shop).join(Stock.shop).join(Stock.book)
            .join(Book.publisher).filter(Publisher.name == params.get('name'))):
            print(c)
    session.close()
    
def get_publisher(engine):
    '''Поиск издателя по имени или id'''
    
    from sqlalchemy.orm import sessionmaker
    from SQLAlchemy_models import Publisher
    
    params = define_params()
    session = sessionmaker(bind=engine)()
    if 'name' in params:
        print(*session.query(Publisher).filter(Publisher.name == params.get('name')).all())
    elif 'id' in params:
        print(*session.query(Publisher).filter(Publisher.id == params.get('id')).all())
    else:
        print('Request something already!')
    session.close()
    
    
if __name__ == '__main__':
    with open('password.txt') as pw:
        password = pw.read()
    engine = connect_to_db('postgresql', 'postgres', password, 'book_shop')
    # create_tables(engine, True)
    # fill_db_manually(engine)
    # fill_db_from_json(engine, 'book_shop_db.json')
    # get_publisher(engine)
    # find_shop_by_publisher(engine)
    