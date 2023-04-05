import sqlite3 as sql3
from contextlib import closing
import datetime as dt

conn = sql3.connect("images.db")
select = "select * from images"


def fetch():
    with closing(conn.cursor()) as cursor:
        for row in cursor.execute(select):
            print(row)


def getId():
    with closing(conn.cursor()) as cursor:
        rowCount = cursor.execute("select count(*) from images")
        values = rowCount.fetchone()
        return values[0]+1


def insert():
    file_name = input("Enter file name \n")
    dimension = input("Enter dimensions \n")
    created_at = str(dt.datetime.now())

    insert = 'INSERT INTO images(id,file_name,dimension,created_at) VALUES (?,?,?,?)'
    values = [getId(), file_name, dimension, created_at]
    with closing(conn.cursor()) as cursor:
        cursor.execute(insert, values)
        conn.commit()


def update():
    id = input("Enter student id \n")
    toChange = input("New file name \n")

    update = "UPDATE images set file_name = ? where id = ?"
    values = [toChange, id]
    with closing(conn.cursor()) as cursor:
        cursor.execute(update, values)
        conn.commit()


def delete():
    id = input("Enter image id \n")
    delete = "DELETE FROM images where id = ?"
    values = [id]
    with closing(conn.cursor()) as cursor:
        cursor.execute(delete, values)
        conn.commit()


def creatTable():
    sql = """CREATE TABLE IMAGES(
        ID INTEGER,
        FILE_NAME TEXT,
        DIMENSION TEXT ,
        FILTER TEXT null,
        IMAGE TEXT null,
        CREATED_AT DATETIME NULL
        );"""
    with closing(conn.cursor()) as cursor:
        cursor.execute(sql)
        conn.commit()
