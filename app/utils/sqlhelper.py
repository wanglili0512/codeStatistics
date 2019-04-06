from settings import Config
import pymysql


def create_conn():
    conn = Config.POOL.connection()
    cur = conn.cursor(cursor=pymysql.cursors.DictCursor)

    return conn, cur


def close_conn(conn, cur):
    cur.close()
    conn.close()


def insert(sql, args):
    conn, cur = create_conn()
    res = cur.execute(sql, args)
    conn.commit()       # 增、删、改 必须要提交
    close_conn(conn, cur)

    return res


def fetch_one(sql, args):
    conn, cur = create_conn()
    cur.execute(sql, args)
    res = cur.fetchone()
    close_conn(conn, cur)

    return res


def fetch_all(sql, args):
    conn, cur = create_conn()
    cur.execute(sql, args)
    res = cur.fetchall()
    close_conn(conn, cur)

    return res
