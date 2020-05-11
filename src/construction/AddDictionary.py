import os

from tqdm import tqdm
from pystardict import Dictionary

from src.database.database import Database
import src.misc.tools as tl
from src.construction.PreparePerseusXML import perseus_xml_read

class import_dictionary():
    def __init__(self):
        self.db = Database()

    def check_dictionary(self, name, word_count, abstractive=0):
        dict_exists = self.db.check_if_exists('Dictionary', 'Name', name)
        if dict_exists == False:
            dictionary_id = self.db.write_dictionary(name, word_count, abstractive)
            self.db._commit()
        else:
            dictionary_id = dict_exists[0][0]
        return dictionary_id

    def check_word(self, word):
        word = tl.rpl_chunk(word).lower()
        word_exists = self.db.check_if_exists('Word', 'Word',word)
        if word_exists == False:
            word_id = self.db.write_word(word)
        else:
            word_id = word_exists[0][0]
        return word_id


class stardict(import_dictionary):

    def __init__(self, path, stardict_db_folder, stardict_db_name):
        import_dictionary.__init__(self)
        self.dict1 = Dictionary(os.path.join(path, stardict_db_folder,stardict_db_name))

    def add_words_to_dictionary(self):
        try:
            dictionary_id = self.check_dictionary(self.dict1.ifo.bookname, self.dict1.ifo.wordcount, abstractive=1 )
            print("\n'Add all new words to Dictionary '{0}':\n".format(self.dict1.ifo.bookname))
            for w in tqdm(self.dict1.idx._idx):
                word = w.decode('Utf-8')
                word_id = self.check_word(word)
                definition = self.dict1.get(word)
                self.db.write_definition(dictionary_id, word_id, definition)
            self.db._commit()
            return dictionary_id
        except:
            self.db.db_connection.rollback()
            raise


class perseus(import_dictionary):


    def __init__(self, book_name, word_count):
        import_dictionary.__init__(self)
        self.dict = perseus_xml_read()
        self.book_name = book_name
        self.word_count = word_count

    def add_words_to_dictionary(self):
        try:
            dictionary_id = self.check_dictionary(self.book_name, self.word_count)
            print("\n'Add all new words to Dictionary '{0}':\n".format(self.book_name))
            for w in tqdm(self.dict):
                word = w[0]
                word_id = self.check_word(word)
                definition = w[1]
                self.db.write_definition(dictionary_id, word_id, definition)
            self.db._commit()
            return dictionary_id
        except:
            self.db.db_connection.rollback()
            raise


