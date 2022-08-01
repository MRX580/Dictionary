import sqlite3
from datetime import datetime


class Database:
    def __init__(self):
        self.conn = sqlite3.connect('C:\\Users\\andre\\PycharmProjects\\Dictionaries\\database\\dict.db')
        self.cur = self.conn.cursor()
        # статус в словаре нужен для того что бы узнать какой пользователь сделал выбор "просмотрено" или "Отметить
        # как выученое" added(когда юзер добавил слово вручную) viewed(когда юзер выбрал "просмотрено") learned(когда
        # юзер выбрал что он уже знает это слово)
        self.cur.execute("""CREATE TABLE IF NOT EXISTS Dictionary(number INTEGER PRIMARY KEY, user_id INT, 
        status TEXT, word TEXT, datetime TEXT)""")
        self.cur.execute("""CREATE TABLE IF NOT EXISTS Users(number INTEGER PRIMARY KEY, user_id INT, language TEXT, 
        notification TEXT, datetime TEXT)""")
        self.conn.commit()

    def turn_on_notification(self, user_id):
        self.cur.execute(f"""UPDATE Users SET notification = 'on' WHERE user_id = {user_id}""")
        self.conn.commit()

    def turn_off_notification(self, user_id):
        self.cur.execute(f"""UPDATE Users SET notification = 'off' WHERE user_id = {user_id}""")
        self.conn.commit()

    def get_all_words_user(self, user_id):
        table = self.cur.execute(f"""SELECT * FROM Dictionary""")
        all_words = []
        status = []
        for i in table:
            if i[1] == user_id:
                all_words.append(i[3])
                status.append(i[2])
        if all_words:
            return all_words, status
        else:
            return False

    def add_word(self, word, status, user_id):
        self.cur.execute(
            f"""INSERT INTO Dictionary(number, user_id, status, word, datetime) VALUES (null, {user_id}, '{status}','{word}', '{datetime.now()}');""")
        self.conn.commit()

    def add_new_user(self, language, user_id):
        table = self.cur.execute(f"""SELECT * FROM Users""")
        for i in table:
            if i[1] == user_id:
                return False
        self.cur.execute(
            f"""INSERT INTO Users(number, user_id, language, datetime) VALUES (null, {user_id}, '{language}', '{datetime.now()}');""")
        self.conn.commit()
        return True

    def set_status(self, user_id, word, status):
        if self.check_word(user_id, word):
            self.cur.execute(f"""UPDATE Dictionary SET status = "{status}" WHERE user_id = {user_id}""")
        else:
            self.cur.execute(
                f"""INSERT INTO Dictionary(number, user_id, status, word, datetime) VALUES (null, {user_id}, '{status}
                ', '{word}', '{datetime.now()}');""")
        self.conn.commit()

    def languageU(self, user_id):
        table = self.cur.execute(f"""SELECT * FROM Users""")
        for i in table:
            if i[1] == user_id:
                return i[2]

    def get_notification(self, user_id):
        table = self.cur.execute(f"""SELECT * FROM Users""")
        for i in table:
            if i[1] == user_id:
                return i[3]

    def get_all_user(self):
        table = self.cur.execute(f"""SELECT * FROM Users""")
        return table

    # def get_status(self):

    def check_all_dict(self):
        table = self.cur.execute(f"""SELECT * FROM Dictionary""")
        for i in table:
            print(i)

    def check_word(self, user_id, word):
        table = self.cur.execute(f"""SELECT * FROM Dictionary""")
        for i in table:
            if i[1] == user_id and i[3].lower() == word.lower():
                return True
        return False


if __name__ == "__main__":
    Database().check_all_dict()
