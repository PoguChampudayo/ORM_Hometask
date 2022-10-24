from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from SQLAlchemy_models import create_tables

        
def connect_to_db(db, login, password, db_name):
    '''Подключение к БД интересующего типа'''
    
    DSN = f'{db}://{login}:{password}@localhost:5432/{db_name}'
    return create_engine(DSN)

def fill_db(engine):

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

def find_shop_by_publisher(engine, name:str=None, id:int=None):
    '''Поиск магазинов с книгами, выпущенными искомым издателем'''
    
    from SQLAlchemy_models import Publisher, Book, Shop, Stock
    
    session = sessionmaker(bind=engine)()
    if id:
        for c in (session.query(Shop).join(Stock.shop).join(Stock.book)
            .join(Book.publisher).filter(Publisher.id == id)):
            print(c)
    elif name:
        for c in (session.query(Shop).join(Stock.shop).join(Stock.book)
            .join(Book.publisher).filter(Publisher.name == name)):
            print(c)
    session.close()
    
def get_publisher(engine, name:str=None, id:int=None):
    '''Поиск издателя по имени или id'''
    
    from sqlalchemy.orm import sessionmaker
    from SQLAlchemy_models import Publisher
    
    session = sessionmaker(bind=engine)()
    if name:
        print(*session.query(Publisher).filter(Publisher.name == name).all())
    if id:
        print(*session.query(Publisher).filter(Publisher.id == id).all())
    if not name and not id:
        print('Request something already!')
    session.close()
    
    
if __name__ == '__main__':
    with open('password.txt') as pw:
        password = pw.read()
    engine = connect_to_db('postgresql', 'postgres', password, 'book_shop')
    request = input('Введите имя или идентификатор издателя: ')
    param = {}
    if request.isnumeric():
        param['id'] = int(request)
    else:
        param['name'] = request

    # create_tables(engine)
    # fill_db(engine)
    get_publisher(engine, **param)
    find_shop_by_publisher(engine, **param)
    