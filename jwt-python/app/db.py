import pymysql


def get_db_connection():
    connection = pymysql.connect(
        host="localhost",
        user="root",
        password="root",
        port=8889,
        database="jwt_learning",
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection