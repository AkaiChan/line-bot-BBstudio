from psycopg2.extras import RealDictCursor

def get_stores(conn):
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("SELECT id, name, description FROM OMS_stores")
        return cur.fetchall()

def get_store_products(conn, store_id):
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("""
            SELECT id, name, price, stock_quantity 
            FROM OMS_products 
            WHERE store_id = %s
        """, (store_id,))
        return cur.fetchall()

def add_to_cart(user_carts, user_id, product_id, quantity):
    if user_id not in user_carts:
        user_carts[user_id] = {}
    
    if product_id in user_carts[user_id]:
        user_carts[user_id][product_id] += quantity
    else:
        user_carts[user_id][product_id] = quantity

def get_cart_contents(conn, user_carts, user_id):
    if user_id not in user_carts:
        return []
    
    cart_items = []
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        for product_id, quantity in user_carts[user_id].items():
            cur.execute("""
                SELECT name, price 
                FROM OMS_products 
                WHERE id = %s
            """, (product_id,))
            product = cur.fetchone()
            if product:
                cart_items.append({
                    'name': product['name'],
                    'price': product['price'],
                    'quantity': quantity,
                    'subtotal': product['price'] * quantity
                })
    return cart_items

def add_store(conn, name, description=None):
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("""
            INSERT INTO OMS_stores (name, description) 
            VALUES (%s, %s)
            RETURNING id, name
        """, (name, description))
        conn.commit()
        return cur.fetchone()
def add_product(conn, store_id, name, description, price, stock_quantity):
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("""
            INSERT INTO OMS_products (store_id, name, description, price, stock_quantity) 
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id, name, description, price, stock_quantity
        """, (store_id, name, description, price, stock_quantity))
        conn.commit()
        return cur.fetchone()

def get_store_products(conn, store_id):
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("""
            SELECT id, name, description, price, stock_quantity 
            FROM OMS_products 
            WHERE store_id = %s
        """, (store_id,))
        return cur.fetchall()
