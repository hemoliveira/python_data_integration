from core.database import get_connection

def report_customers():

    conn = get_connection()
    cur = conn.cursor()

    sql = """
    SELECT name, city
    FROM tb_customers
    """

    cur.execute(sql)

    return cur.fetchall()