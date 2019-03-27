from app import db
from app import Table, MenuItem


# db.create_all()


def create_tables():
    '''Create 10 Table objects, and commit to database.'''
    tables = []
    for i in range(1,11):
        table = 'table{}'.format(i)
        tables.append(table)
    for table in tables:
        table = Table()
        db.session.add(table)
    db.session.commit()


def create_menu_items():
    '''Create a few menu items.'''
    menu_item1 = MenuItem('Pizza', 35, 'https://api-content.prod.pizzahutaustralia.com.au//umbraco/api/Image/Get2?path=assets/products/menu/Meat-Super-Supreme-Pizza-3250-menu.jpg')
    menu_item2 = MenuItem('Pasta', 40, 'https://thebusybaker.ca/wp-content/uploads/2018/08/easy-15-minute-pasta-carbonara-fbig1.jpg')
    menu_item3 = MenuItem('Salad', 25, 'https://www.halfbakedharvest.com/wp-content/uploads/2018/01/Rejuvenating-Winter-Broccoli-Salad-1-500x500.jpg')
    menu_item4 = MenuItem('Burger', 30, 'https://www.kitchensanctuary.com/wp-content/uploads/2018/03/Asian-Sticky-Belly-Pork-Burger-with-Pickled-Vegetables-recipe-square-FS.jpg')
    menu_item5 = MenuItem('Coffee', 15, 'https://static.independent.co.uk/s3fs-public/thumbnails/image/2018/04/15/16/china-coffee-cup.jpg?w968h681')
    menu_item6 = MenuItem('Tea', 10, 'https://oxygenyogaandfitness.com/wp-content/uploads/2015/02/brown-brewed-tea.jpg')
    menu_item7 = MenuItem('Beer', 20, 'https://media-cdn.tripadvisor.com/media/photo-s/0d/a2/a8/ec/cold-beer.jpg')
    menu_items = [menu_item1, menu_item2, menu_item3, menu_item4, menu_item5, menu_item6, menu_item7]
    for menu_item in menu_items:
        db.session.add(menu_item)
    db.session.commit()

create_tables()
# create_menu_items()
