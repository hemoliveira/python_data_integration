from core.database import get_connection
from mysql.connector import Error

class ProductRepository:
    def save(self, product):
        """Insere um novo produto usando o objeto Model"""
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            query = "INSERT INTO tb_products (name, category, price) VALUES (%s, %s, %s)"
            cursor.execute(query, (product.name, product.category, product.price))
            conn.commit()
            product.product_id = cursor.lastrowid
            return product
        except Error as e:
            if conn: conn.rollback()
            print(f"Error saving product: {e}")
            return None
        finally:
            if conn:
                cursor.close()
                conn.close()

    def get_all_active(self):
        """Retorna todos os registros da View de ativos"""
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM vw_active_products")
            return cursor.fetchall()
        except Error as e:
            print(f"Error fetching active products: {e}")
            return []
        finally:
            if conn:
                cursor.close()
                conn.close()

    def find_by_id(self, product_id):
        """Busca um registro específico pelo ID"""
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM tb_products WHERE product_id = %s AND deleted_at IS NULL"
            cursor.execute(query, (product_id,))
            return cursor.fetchone()
        except Error as e:
            print(f"Error finding product: {e}")
            return None
        finally:
            if conn:
                cursor.close()
                conn.close()

    def update(self, product):
        """Atualiza os dados de um produto usando o objeto Model"""
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            query = "UPDATE tb_products SET name = %s, category = %s, price = %s WHERE product_id = %s"
            cursor.execute(query, (product.name, product.category, product.price, product.product_id))
            conn.commit()
            return cursor.rowcount > 0
        except Error as e:
            if conn: conn.rollback()
            print(f"Error updating product: {e}")
            return False
        finally:
            if conn:
                cursor.close()
                conn.close()

    def soft_delete(self, product_id):
        """Marca como deletado (Soft Delete)"""
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            query = "UPDATE tb_products SET deleted_at = NOW() WHERE product_id = %s"
            cursor.execute(query, (product_id,))
            conn.commit()
            return cursor.rowcount > 0
        except Error as e:
            if conn: conn.rollback()
            print(f"Error deleting product: {e}")
            return False
        finally:
            if conn:
                cursor.close()
                conn.close()