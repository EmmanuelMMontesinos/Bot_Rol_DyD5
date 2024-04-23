import sqlite3 as db


def init_db():
    with db.Connection("wiki.db") as wiki:
        cursor = wiki.cursor()
        solicitud = "CREATE TABLE IF NOT EXISTS wiki(id integer primary key autoincrement unique, seccion varchar(30))"
        cursor.execute(solicitud)


init_db()
