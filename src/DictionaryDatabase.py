import os
import sqlite3
import DictionaryTools

class Database():
    def __init__(self):
        self.db_connection = sqlite3.connect(os.path.abspath('database/dictionaries_db.db'))
        self.cursor = self.db_connection.cursor()

    def truncate_database(self):
        sql = ["delete From Dictionary",
              "delete From Word",
              "delete From Definition",
              "delete From Flection",
              "update sqlite_sequence  set seq = 0",
               ]

        for s in sql:
            self._execute(s)
        self._commit()

    def get_dictionaries(self):
        sql = 'select DictionaryId, Name From Dictionary'
        return self.cursor.execute(sql).fetchall()

    def get_property(self, property_id):
        sql = 'select Value From Property where PropertyId = {0}'.format(property_id)
        return self.cursor.execute(sql).fetchone()[0]

    def set_property(self, property_id, value):
        sql = "Update Property Set Value = '{0}'  where PropertyId = {1}".format(value, property_id)
        self._execute(sql)
        self._commit()

    def check_if_exists(self, table, whereColumn, value):
        self.cursor.execute("SELECT * FROM {0} WHERE {1} = '{2}'".format(table, whereColumn, DictionaryTools.el_qt(value)))
        data = self.cursor.fetchall()
        if len(data) == 0:
            return False
        else:
            return data

    def search_word(self, word, search_like):

        dbs = self.get_property(1)
        if dbs == '[]':
            return None

        sql = ("""select distinct 
                                b.WordId, 
                                b.Word, 
                                c.Definition, 
                                d.Abstractable
                            from
                                Flection as a 
                            inner join
                                Word as b on a.WordId = b.WordId
                            inner join
                                Definition as c on a.WordId = c.WordId
                            inner join 
                                Dictionary as d on c.DictionaryId = d.DictionaryId
                           where
                                c.DictionaryId in ({0}) and """.format(dbs))

        if not search_like:
            sql = sql + "Flection = '{0}'".format(DictionaryTools.el_qt(word))
        else:
            sql = sql + "Flection like '%{0}%'".format(DictionaryTools.el_qt(word))

        return self.cursor.execute(sql).fetchall()


    def write_dictionary(self, book_name, word_count):
        sql = "Insert Into Dictionary (Name, WordCount) Values ('{0}', {1}) ".format(DictionaryTools.el_qt(book_name), word_count)
        return self._execute(sql)

    def write_word(self, word):
        sql = "Insert Into Word (Word) Values ('{0}')".format(DictionaryTools.el_qt(word))
        return self._execute(sql)

    def write_definition(self, dictionary_id, word_id, definition):
        sql = "Insert Into Definition (DictionaryId, WordId, Definition) Values ({0}, {1}, '{2}')".format(dictionary_id, word_id, DictionaryTools.el_qt(definition))
        return self._execute(sql)

    def write_flection(self, word_id, form, description, is_flection = 0):
        sql = "Insert Into Flection (WordId, Flection, Description, NoFlection) Values ({0}, '{1}', '{2}', {3})".format(word_id, DictionaryTools.el_qt(form), DictionaryTools.el_qt(description), is_flection)
        return self._execute(sql)

    def write_history(self, word_id):
        sql = "Insert Into History (WordId) Values ({0}) ".format(word_id)
        self._execute(sql)
        self._commit()

    def get_history(self):
        sql = """select 
	                b.Word
                from 
	                History as a 
                inner join 
	                Word as b on a.WordId = b.WordId
                order by 
	                HistoryId desc
        """
        data = self.cursor.execute(sql).fetchall()
        return data

    def clear_history(self):
        sql = 'delete From History'
        self.cursor.execute(sql)
        self._commit()

    def read_database(self, sql):
        return self.cursor.execute(sql).fetchall()

    def _execute(self, sql):
        self.cursor.execute(sql)
        return self.cursor.lastrowid

    def _commit(self):
        self.db_connection.commit()

