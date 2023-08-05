import math
import sqlite3
import time
123







class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def get_name(self):
        sql = '''SELECT * FROM author'''

        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res:
                return res
        except ValueError as e:
            print('ошибка чтение из бд')
            raise e

        return []

    def addPost(self, title, text, url):

        try:
            self.__cur.execute(f'SELECT COUNT() as "count" FROM posts WHERE url LIKE "{url}"')
            res = self.__cur.fetchone()
            if res['count'] > 0:
                return False
            tm = math.floor(time.time())
            self.__cur.execute("INSERT INTO posts VALUES(NULL, ?, ?, ?, ?)", (title, text, url, tm))
            self.__db.commit()
        except sqlite3.Error as e:
            raise e
        return True

    def getPost(self, postId):
        try:
            self.__cur.execute(f"SELECT title, text from posts WHERE id = {postId} LIMIT 1")
            res = self.__cur.fetchone()
            if res:
                return res
        except sqlite3.Error as e:
            raise e

    def getPostAncone(self):
        try:
            self.__cur.execute(f'SELECT id, title, text FROM posts ORDER BY time DESC')
            res = self.__cur.fetchall()
            if res:
                return res
        except sqlite3.Error as e:
            raise e
        return []
