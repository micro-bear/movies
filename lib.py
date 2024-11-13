import sqlite3
import json
import os

DB_PATH = os.getcwd()
JSON_IN_PATH = os.getcwd()
JSON_OUT_PATH = os.getcwd()

def connect_db():
    connection = sqlite3.connect(DB_PATH + '\movies.db')
    connection.row_factory = sqlite3.Row
    database = connection.cursor()
    create_table(database)
    return connection, database

def list_rpt():
    database = connect_db()
    database.execute('SELECT * FROM movies')
    rows = database.fetchall()
    database.close()
    return rows

def create_table(database):
    try:
        database.execute('''
            CREATE TABLE IF NOT EXISTS "movies" (
                "id"	INTEGER,
                "title"	TEXT NOT NULL,
                "director"	TEXT NOT NULL,
                "genre"	TEXT NOT NULL,
                "year"	INTEGER NOT NULL,
                "rating"	REAL,
                PRIMARY KEY("id" AUTOINCREMENT),
                CONSTRAINT "check rating" CHECK("rating" >= 1.0 AND "rating" <= 10.0)
            );
        ''')
    except sqlite3.OperationalError:  # 捕捉不合法的數值輸入
        print("資料表movies新增失敗")
    

def import_movies():
    try:
        connection, database = connect_db()
        with open(JSON_IN_PATH + '\movies.json', 'r', encoding='UTF-8') as f:
            movies = json.load(f)
        for movie in movies:
            database.execute("SELECT * FROM `movies` WHERE `title` = ?;", [movie['title']])
            data = database.fetchone()
            if data is None:
               add_movie(connection, database, movie)
        print("電影已匯入")
    except sqlite3.OperationalError as err:  # 捕捉不合法的數值輸入
        print("資料表匯入失敗::")
        print(err)

def search_movies(name = ''):
    connection, database = connect_db()
    sql = "SELECT title,director,genre,year,rating FROM `movies`"
    if(name is ''): 
        database.execute(sql)
    else:
        sql += " Where `title` like ?"
        database.execute(sql, ["%" + name + "%"])
    return [dict(row) for row in database.fetchall()]

def add_movie(connection, database, data):
    try:
        database.execute("INSERT INTO movies (title,director,genre,year,rating) VALUES (?,?,?,?,?);", [data['title'], data['director'], data['genre'], data['year'], data['rating']])
        connection.commit()
    except sqlite3.OperationalError as err:
        print("資料表新增失敗::")
        print(err)

def modify_movie(connection, database, data, id):
    try:
        if(data):
            set_clause = ", ".join([f"{key} = ?" for key, value in data.items()])
            sql = "Update movies SET " + set_clause + " Where title = ?"
            database.execute(sql, list(data.values()) + [id])
            connection.commit()
    except sqlite3.OperationalError as err:
        print("資料表更新失敗")
        print(err)

def delete_movies(connection, database,id = ''):
    try:
        sql = "DELETE FROM movies"
        data = []
        if(id):
            sql += " Where title = ?"
            data.append(id)

        database.execute(sql, data)
        connection.commit()
    except sqlite3.OperationalError as err:
        print("資料表刪除失敗")
        print(err)

def export_movies(movies):
    with open(JSON_OUT_PATH + '\exported.json', 'w', encoding='utf-8') as f:
        json.dump(movies, f, ensure_ascii=False, indent=4)
    return True
