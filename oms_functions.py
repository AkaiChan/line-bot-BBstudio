from psycopg2.extras import RealDictCursor

def get_stores(conn):
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("SELECT id, name, description FROM OMS_stores")
        return cur.fetchall()

def get_store_products(conn, store_id):
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("""
            SELECT id, name, description, price, stock_quantity 
            FROM OMS_products 
            WHERE store_id = %s
        """, (store_id,))
        return cur.fetchall()

def add_to_cart(conn, user_id, product_id, quantity):
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        # 檢查購物車是否已存在
        cur.execute("SELECT id FROM OMS_carts WHERE user_id = %s", (user_id,))
        cart = cur.fetchone()
        
        if not cart:
            # 如果購物車不存在,創建一個新的
            cur.execute("INSERT INTO OMS_carts (user_id) VALUES (%s) RETURNING id", (user_id,))
            cart = cur.fetchone()
        
        # 檢查商品是否已在購物車中
        cur.execute("""
            SELECT quantity FROM OMS_cart_items 
            WHERE cart_id = %s AND product_id = %s
        """, (cart['id'], product_id))
        existing_item = cur.fetchone()
        
        if existing_item:
            # 如果商品已在購物車中,更新數量
            new_quantity = existing_item['quantity'] + quantity
            cur.execute("""
                UPDATE OMS_cart_items SET quantity = %s 
                WHERE cart_id = %s AND product_id = %s
            """, (new_quantity, cart['id'], product_id))
        else:
            # 如果商品不在購物車中,添加新項目
            cur.execute("""
                INSERT INTO OMS_cart_items (cart_id, product_id, quantity) 
                VALUES (%s, %s, %s)
            """, (cart['id'], product_id, quantity))
        
        conn.commit()
    return True

def get_cart_contents(conn, user_id):
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("""
            SELECT p.name, p.price, ci.quantity, (p.price * ci.quantity) as subtotal
            FROM OMS_carts c
            JOIN OMS_cart_items ci ON c.id = ci.cart_id
            JOIN OMS_products p ON ci.product_id = p.id
            WHERE c.user_id = %s
        """, (user_id,))
        return cur.fetchall()

def add_store(conn, name, description=None):
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("""
            INSERT INTO OMS_stores (name, description) 
            VALUES (%s, %s)
            RETURNING id, name
        """, (name, description))
        conn.commit()
        return cur.fetchone()

def check_product_exists(conn, store_id, name):
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("""
            SELECT id FROM OMS_products 
            WHERE store_id = %s AND LOWER(name) = LOWER(%s)
        """, (store_id, name))
        return cur.fetchone() is not None

def add_product(conn, store_id, name, description, price, stock_quantity):
    if check_product_exists(conn, store_id, name):
        return None  # 返回 None 表示商品已存在
    
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
    
def get_product(conn, product_id):
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("SELECT * FROM OMS_products WHERE id = %s", (product_id,))
        return cur.fetchone()