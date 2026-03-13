from core.database import get_connection
from mysql.connector import Error

class CustomerRepository:
    def save(self, name, city):
        """Insere um novo cliente"""
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            query = "INSERT INTO tb_customers (name, city) VALUES (%s, %s)"
            cursor.execute(query, (name, city))
            conn.commit()
            return cursor.lastrowid
        except Error as e:
            if conn: conn.rollback()
            print(f"Error saving customer: {e}")
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
            cursor.execute("SELECT * FROM vw_active_customers")
            return cursor.fetchall()
        except Error as e:
            print(f"Error fetching active customers: {e}")
            return []
        finally:
            if conn:
                cursor.close()
                conn.close()

    def find_by_id(self, customer_id):
        """Busca um registro específico pelo ID"""
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM tb_customers WHERE customer_id = %s AND deleted_at IS NULL"
            cursor.execute(query, (customer_id,))
            return cursor.fetchone()
        except Error as e:
            print(f"Error finding customer: {e}")
            return None
        finally:
            if conn:
                cursor.close()
                conn.close()

    def update(self, customer_id, name, city):
        """Atualiza os dados de um cliente"""
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            query = "UPDATE tb_customers SET name = %s, city = %s WHERE customer_id = %s"
            cursor.execute(query, (name, city, customer_id))
            conn.commit()
            return cursor.rowcount > 0
        except Error as e:
            if conn: conn.rollback()
            print(f"Error updating customer: {e}")
            return False
        finally:
            if conn:
                cursor.close()
                conn.close()

    def soft_delete(self, customer_id):
        """Marca como deletado (Soft Delete)"""
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            query = "UPDATE tb_customers SET deleted_at = NOW() WHERE customer_id = %s"
            cursor.execute(query, (customer_id,))
            conn.commit()
            return cursor.rowcount > 0
        except Error as e:
            if conn: conn.rollback()
            print(f"Error deleting customer: {e}")
            return False
        finally:
            if conn:
                cursor.close()
                conn.close()