import sqlite3 as sql3
from contextlib import closing

# database connection
conn = sql3.connect("images.db")


def fetch():
    with closing(conn.cursor()) as c:
        rows = c.execute("SELECT * FROM images")
        response = []
        for row in rows:
            response.append({
                "ID": row[0],
                "FILE_NAME": row[1],
                "DIMENSION": row[2],
                "FILTER": row[3],
                "IMAGE": row[4],
                "CREATED_AT": row[5]
            })
        return response


def getId():
    with closing(conn.cursor()) as cursor:
        row_count = cursor.execute("select count(*) from images")
        values = row_count.fetchone()
        return values[0] + 1


def insert(insert_value):
    try:
        with closing(conn.cursor()) as c:
            sql_query = 'INSERT INTO images (FILE_NAME,DIMENSION,FILTER,IMAGE) VALUES (?,?,?,?)'  # SQL query to insert
            values = [insert_value['FILE_NAME'], insert_value['DIMENSION'], insert_value['FILTER'],
                      insert_value['IMAGE']]
            c.execute(sql_query, values)  # works for one record
            conn.commit()  # commit the executed query
        return True
    except Exception as e:
        print(Exception, e)
        return False


def delete(image_id):
    print(image_id)
    try:
        with closing(conn.cursor()) as cursor:
            sql_query = 'DELETE FROM IMAGES where ID = ?'
            values = [image_id]
            cursor.execute(sql_query, values)
            conn.commit()
        return True
    except Exception as e:
        print(Exception, e)
        return False


def createTable():
    sql = """CREATE TABLE IMAGES(
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        FILE_NAME TEXT NOT NULL,
        DIMENSION TEXT NOT NULL,
        FILTER LONGTEXT NOT NULL,
        IMAGE LONGTEXT NOT NULL,
        CREATED_AT DATETIME DEFAULT CURRENT_TIMESTAMP
        );"""
    with closing(conn.cursor()) as cursor:
        cursor.execute(sql)
        conn.commit()
