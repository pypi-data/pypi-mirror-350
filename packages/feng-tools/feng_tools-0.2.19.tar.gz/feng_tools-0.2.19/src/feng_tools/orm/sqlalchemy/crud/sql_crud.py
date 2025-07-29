from sqlalchemy import Connection, text


def query_by_sql(sql, conn: Connection):
    """通过sql语句查找"""
    cursor = conn.execute(text(sql))
    return cursor.fetchall()


def exec_by_sql(sql, conn: Connection):
    """通过sql运行"""
    cursor = conn.execute(text(sql))
    return cursor.lastrowid

