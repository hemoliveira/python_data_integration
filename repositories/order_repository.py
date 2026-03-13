from core.database import get_connection
from mysql.connector import Error

class OrderRepository:
    def save(self, customer_id, order_date, items):
        """
        Salva um pedido e seus itens.
        'items' deve ser uma lista de dicionários: [{'product_id': 1, 'quantity': 2}, ...]
        """
        conn = None
        try:
            conn = get_connection()
            conn.start_transaction() # Inicia transação manual
            cursor = conn.cursor()

            # 1. Inserir na tb_orders
            sql_order = "INSERT INTO tb_orders (customer_id, order_date) VALUES (%s, %s)"
            cursor.execute(sql_order, (customer_id, order_date))
            order_id = cursor.lastrowid

            # 2. Inserir na tb_order_items
            # O 'total' será calculado automaticamente pelo TRIGGER trg_calculate_total do MySQL
            sql_items = """
                INSERT INTO tb_order_items (order_id, product_id, quantity) 
                VALUES (%s, %s, %s)
            """
            
            item_data = [(order_id, item['product_id'], item['quantity']) for item in items]
            cursor.executemany(sql_items, item_data)

            conn.commit() # Salva ambas as tabelas
            return order_id

        except Error as e:
            if conn:
                conn.rollback() # Cancela tudo se houver erro nos itens
            print(f"Error saving order: {e}")
            return None
        finally:
            if conn:
                cursor.close()
                conn.close()

    def get_all_active(self):
        """Usa a VIEW vw_sales_report para trazer dados mastigados"""
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM vw_sales_report")
            return cursor.fetchall()
        except Error as e:
            print(f"Error fetching orders: {e}")
            return []
        finally:
            if conn:
                cursor.close()
                conn.close()

    def find_by_id(self, order_id):
        """Busca os detalhes de um pedido específico"""
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM vw_sales_report WHERE order_id = %s"
            cursor.execute(query, (order_id,))
            return cursor.fetchall() # Retorna todos os itens do pedido
        except Error as e:
            print(f"Error finding order: {e}")
            return None
        finally:
            if conn:
                cursor.close()
                conn.close()

    def soft_delete(self, order_id):
        """Marca o pedido como deletado"""
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            query = "UPDATE tb_orders SET deleted_at = NOW() WHERE order_id = %s"
            cursor.execute(query, (order_id,))
            conn.commit()
            return cursor.rowcount > 0
        except Error as e:
            if conn: conn.rollback()
            print(f"Error deleting order: {e}")
            return False
        finally:
            if conn:
                cursor.close()
                conn.close()