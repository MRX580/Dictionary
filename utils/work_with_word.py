from random import randint
from database.sqlite import Database
from utils.parser import get_word


class words:
    def __init__(self):
        self.word_1k = get_word()

    def give_1_rand_word(self, user_id):
        word = self.word_1k[randint(0, 980)]
        if self.check_isMark(user_id, word):
            self.give_1_rand_word(user_id)
        else:
            return word

    def check_isMark(self, user_id, word):
        if not Database().get_all_words_user(user_id):
            return False
        mass = Database().get_all_words_user(user_id)[0]
        status = Database().get_all_words_user(user_id)[1]
        for i in enumerate(mass):
            if word == i[1] and status[i[0]] == "learned":
                return True
        return False
    # ДОБАВИТЬ - ЕСЛИ ПОЛЬЗОВАТЕЛЬ ЗНАЕТ ВСЕ СЛОВА, ВЫДАВАТЬ ДРУГОЙ РЕЗУЛЬТАТ