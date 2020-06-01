import os
import sqlite3
from src.misc.tools import *

class Database():
    def __init__(self):

        self.db_connection = sqlite3.connect(os.path.abspath('./_database/redict.db'))
        self.cursor = self.db_connection.cursor()

    def truncate_database(self):
        sql = ["DELETE FROM Dictionary",
              "DELETE FROM Word",
              "DELETE FROM Definition",
              "DELETE FROM Flection",
              "UPDATE sqlite_sequence  SET seq = 0 WHERE name IN ('Flection', 'Definition', 'Word', 'Dictionary')"
               ]

        for s in sql:
            self._execute(s)
        self._commit()

    def get_dictionaries(self):
        sql = 'SELECT DictionaryId, Name FROM Dictionary'
        return self.cursor.execute(sql).fetchall()

    def get_property(self, property_id):
        sql = f'SELECT Value FROM Property WHERE PropertyId = {property_id}'
        return self.cursor.execute(sql).fetchone()[0]

    def set_property(self, property_id, value):
        sql = f"UPDATE Property SET Value = '{value}'  WHERE PropertyId = {property_id}"
        self._execute(sql)
        self._commit()

    def create_property(self, property_id, value, description):
        sql = f"INSERT INTO Property (PropertyId, Value, Description) VALUES ({property_id}, '{value}', '{description}')"
        self._execute(sql)
        self._commit()

    def check_if_exists(self, table, whereColumn, value):
        self.cursor.execute(f"SELECT * FROM {table} WHERE {whereColumn} = '{el_qt(value)}'")
        data = self.cursor.fetchall()
        if len(data) == 0:
            return False
        else:
            return data

    def search_word(self, word, search_like):

        dbs = self.get_property(1)
        if dbs == '[]':
            return None

        sql = (f"""SELECT DISTINCT 
                                b.WordId, 
                                b.Word, 
                                c.Definition, 
                                d.Abstractive
                            FROM
                                Flection AS a 
                            INNER JOIN
                                Word AS b ON a.WordId = b.WordId
                            INNER JOIN
                                Definition AS c ON a.WordId = c.WordId
                            INNER JOIN 
                                Dictionary AS d ON c.DictionaryId = d.DictionaryId
                           WHERE
                                c.DictionaryId IN ({dbs}) AND """
               )

        if not search_like:
            sql = sql + f"Flection = '{el_qt(word)}'"
        else:
            sql = sql + f"Flection LIKE '%{el_qt(word)}%'"

        return self.cursor.execute(sql).fetchall()


    def write_dictionary(self, book_name, word_count, abstractive=0):
        sql = f"INSERT INTO Dictionary (Name, WordCount, Abstractive) VALUES ('{el_qt(book_name)}', {word_count}, {abstractive})"
        return self._execute(sql)

    def write_word(self, word):
        sql = f"INSERT INTO Word (Word) VALUES ('{el_qt(word)}')"
        return self._execute(sql)

    def write_definition(self, dictionary_id, word_id, definition):
        sql = f"INSERT INTO Definition (DictionaryId, WordId, Definition) VALUES ({dictionary_id}, {word_id}, '{el_qt(definition)}')"
        return self._execute(sql)

    def write_flection(self, word_id, form, description, is_flection = 0):
        sql = f"INSERT INTO Flection (WordId, Flection, Description, NoFlection) VALUES ({word_id}, '{el_qt(form)}', '{el_qt(description)}', {is_flection})"
        return self._execute(sql)

    def write_history(self, word_id):
        sql = f"DELETE FROM History WHERE WordId = {word_id}"
        self._execute(sql)
        sql = f"INSERT INTO History (WordId) VALUES ({word_id})"
        self._execute(sql)
        self._commit()

    def get_history(self):
        sql = """SELECT 
	                b.Word
                FROM 
	                History AS a 
                INNER JOIN
	                Word AS b ON a.WordId = b.WordId
                ORDER BY 
	                HistoryId DESC
        """
        return self.cursor.execute(sql).fetchall()

    def clear_history(self):
        sql = 'DELETE FROM History'
        self.cursor.execute(sql)
        self._commit()

    def read_database(self, sql):
        return self.cursor.execute(sql).fetchall()

    def _execute(self, sql):
        self.cursor.execute(sql)
        return self.cursor.lastrowid

    def _commit(self):
        self.db_connection.commit()

