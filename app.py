from flask import Flask
from flask import flash, render_template, url_for, session, redirect

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = b'aj(>,m87hJn9+-alkjns*jkj90($'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/restaurant.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


def set_session_table_id(table_id=None):
    if table_id is None:
        session.pop('table_id', None)
    else:
        session['table_id'] = table_id


def get_session_table_id():
    return session.get('table_id', None)


class Table(db.Model):
    '''A class representing a table in a restaurant.
    Its fields should include an indication whether the table is occupied
    or not.'''
    # To do: table definition (class properties)
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Text)

    @classmethod
    def get_free_table(cls):
        '''Get the first found Table which is unoccupied (free).'''
        # To do: method definition
        free_table = Table.query.filter_by(status='free').first()
        return free_table



class MenuItem(db.Model):
    '''A class representing a menu item in a restaurant (eg. cheese sandwich).
    Its fields should include a name, price, image, and any others you think
    are relevant.'''
    # To do: table definition (class properties)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    price = db.Column(db.Integer)
    image = db.Column(db.Text)
    category = db.Column(db.Text)



class Order(db.Model):
    '''A class representing an order in a restaurant (eg. coffee to table 5).
    Its fields include relationships with other tables.'''
    id = db.Column(db.Integer, primary_key=True)
    menu_item_id = db.Column(db.Integer, db.ForeignKey('menu_item.id'), nullable=False)
    table_id = db.Column(db.Integer, db.ForeignKey('table.id'), nullable=False)
    menu_item = db.relationship('MenuItem', backref='orders')
    table = db.relationship('Table', backref='orders')


@app.route('/')
def customer_index():
    '''Customer index page (for customers who visit the site).
    To do:
    If customer is already at a table, redirect to /table/<id>, where
    <id> is the id of the table that this visitor is already at.
    If not, try to find a free table to seat this visitor at.

    If a free table can be found, seat the visitor at the table.
    (Record this information on both the table and the **session**).
    Then redirect to /table/<id>, where <id> is the id of the found table.
    If not, render the index page, with a message saying that all the
    tables are full, etc.'''
    table_id = get_session_table_id()
    if table_id != None:
        return redirect(url_for('show_table', table_id=table_id))
    else:
        free_table = Table.get_free_table()
        free_table.status ='occupied'
        db.session.add(free_table)
        db.session.commit()
        set_session_table_id(free_table.id)
        table_id = get_session_table_id()
        return redirect(url_for('show_table', table_id=table_id))
    return render_template('customer/index.html')


@app.route('/table/<int:table_id>/')
def show_table(table_id):
    '''Show the table page: Display the restaurant's menu, as well as
    a listing of the orders that the table has already made.

    To do:
    Validation:
     - if the session's table id does not match table_id,
    redirect to the customer index page with a (flash) descriptive message.
     - if the table record shows that it's not occupied, clear the session
     table id, then redirect to the customer index page.

    Page:
    Show a list of menu items, in at least 2 categories, reading them from
    the database. Display them nicely formatted. Clicking on a menu item
    should place an order for that item for the current table.
    Also show, beneath the menu, a list of the orders already made for
    the table.
    Also display a link/button to leave the table.'''
    session_table_id = get_session_table_id()
    table = Table.query.get(table_id)
    if session_table_id != table_id:
        flash('This is not your table!')
        return redirect(url_for('customer_index'))
    elif table.status == 'free':
        set_session_table_id(None)
        return redirect(url_for('customer_index'))

    menu = MenuItem.query.all()
    orders = Order.query.filter_by(table_id=table_id).all()
    return render_template('customer/table.html', menu=menu, orders=orders)


@app.route('/table/<int:table_id>/leave/')
def leave_table(table_id):
    '''Leave the table, clearing its data from the database.

    To do:
    Delete all orders for the table.
`   Clear the session table id.
    Render the 'bye' template.'''
    Order.query.filter_by(table_id=table_id).delete()
    table = Table.query.get(table_id)
    table.status = 'free'
    db.session.commit()
    return render_template('customer/bye.html')


@app.route('/order/<int:menu_item_id>/')
def make_order(menu_item_id):
    '''Place an order for the given menu item, for the current table.
    To do:
    Validation:
     - if the session table is None, redirect to the customer index page.
     - if there is no table matching the session table id, or if the
       table matching the id is not occupied, redirect to the customer index
       page.
     - if there is no menu item matching menu_item_id, redirec to the
       show table page.
    Create an Order object with the menu item and the table as arguments
    (use the objects, not their ids).
    Save this new Order object to the database.
    Add a flash message telling the customer that their order has been placed.
    Redirect to the show table page.'''
    session_table_id = get_session_table_id()
    table = Table.query.get(session_table_id)
    table_id = table.id
    menu_item = MenuItem.query.get(menu_item_id)
    if session_table_id == None:
        return redirect(url_for('customer_index'))
    elif table == None or table.status is 'free':
        return redirect(url_for('customer_index'))
    elif menu_item == None:
        return redirect(url_for('show_table', table_id=table_id))

    order = Order(menu_item=menu_item, table=table)
    db.session.add(order)
    db.session.commit()
    flash('Your item has been added to your order')
    return redirect(url_for('show_table', table_id=table_id))


@app.route('/kitchen/')
def kitchen_index():
    '''Show the home page for the kitchen staff, listing all orders.
    This is a BONUS function. Please attempt only after completing the other
    site functionality.'''
    pass
