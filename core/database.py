import mysql.connector
from mysql.connector import Error
from core.config import Config

class DatabaseConnection:
    @staticmethod
    def get_connection():
        try:
            return mysql.connector.connect(
                host=Config.DB_HOST,
                user=Config.DB_USER,
                password=Config.DB_PASS,
                database=Config.DB_NAME
            )
        except Error as e:
            print(f"Erro na conexão: {e}")
            return None

    @staticmethod
    def execute_query(query, params=None):
        """Executa queries que não retornam dados (INSERT, UPDATE, DELETE)."""
        conn = DatabaseConnection.get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute(query, params or ())
                conn.commit()
                return cursor.rowcount
            except Error as e:
                print(f"Erro na execução da query: {e}")
                conn.rollback()
            finally:
                cursor.close()
                conn.close()
        return 0

    @staticmethod
    def fetch_all(query, params=None):
        """Executa queries de busca (SELECT) e retorna todos os resultados."""
        conn = DatabaseConnection.get_connection()
        if conn:
            try:
                # dictionary=True faz com que os resultados venham como dicionários Python
                cursor = conn.cursor(dictionary=True)
                cursor.execute(query, params or ())
                return cursor.fetchall()
            except Error as e:
                print(f"Erro na busca de dados: {e}")
            finally:
                cursor.close()
                conn.close()
        return []