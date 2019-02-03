from flask import Flask
from flask import g
from flask import Response
import pyodbc
import json

app = Flask(__name__)

server = 'pay-r.database.windows.net'
database = 'pay-r'
username = 'pay-r'
password = 'Party123'
driver= '{SQL Server}'

def get_db():
    if not hasattr(g, 'conn'):
        g.conn = get_db_connection()

    return g.conn

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'connection'):
        g.conn.close()
    
def get_db_connection():
    return pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)

@app.route('/')
def hello_world():
    return 'Weclome to Pay-R'

@app.route('/shops/<shopId>', methods=['GET'])
def shop(shopId):
    conn = get_db()
    cursor = conn.cursor() 

    try:
        row = cursor.execute('SELECT * FROM shops WHERE ID=?', shopId).fetchone()   
        shop = { 
            'shop': {
                'id': row.id,
                'name': row.name,
                'email': row.email,
                'phone': row.phone,
            },
        }
        return Response(json.dumps(shop), mimetype='application/json')
    except:
        return Response(json.dumps({ 'shop': None, 'error': 'No shop with id {}'.format(shopId)}), mimetype='application/json')

@app.route('/shops', methods=['GET'])
def shops():
    conn = get_db()
    cursor = conn.cursor()

    try:   
        rows = cursor.execute('SELECT * FROM shops').fetchall()
        shops = {
            'shops': [{ 
                'id': row.id,
                'name': row.name,
                'email': row.email,
                'phone': row.phone,
            } for row in rows]
        }
        
        return Response(json.dumps(shops), mimetype='application/json')
    except:
        return Response(json.dumps({ 'shops': None, 'error': 'Error fetching shops' }), mimetype='application/json')

@app.route('/products', methods=['GET'])
def products():
    conn = get_db()
    cursor = conn.cursor()

    try:   
        rows = cursor.execute('SELECT * FROM products').fetchall()
        products = {
            'products': [{ 
                'id': row.id,
                'name': row.name,
                'price': float(row.price),
                'inventory_count': row.inventory_count,
                'description': row.description,
            } for row in rows]
        }
        
        return Response(json.dumps(products), mimetype='application/json')
    except Exception as e:
        print(e)
        return Response(json.dumps({ 'products': None, 'error': 'Error fetching products' }), mimetype='application/json')


@app.route('/products/<productId>', methods=['GET'])
def product(productId):
    conn = get_db()
    cursor = conn.cursor()

    try:   
        row = cursor.execute('SELECT * FROM products WHERE id=?', productId).fetchone()
        product = {
            'product': { 
                'id': row.id,
                'name': row.name,
                'price': float(row.price),
                'inventory_count': row.inventory_count,
                'description': row.description,
            }
        }
        
        return Response(json.dumps(product), mimetype='application/json')
    except:
        return Response(json.dumps({ 'product': None, 'error': 'Error fetching product with id {}'.format(productId) }), mimetype='application/json')

if __name__ == '__main__':
    app.run(debug=True)
