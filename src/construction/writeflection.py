import cltk
from cltk.stem.latin.declension import CollatinusDecliner
from tqdm import tqdm

import src.misc.tools as tl
from src.database.database import Database

class WriteFlection():

    def __init__(self, dictionary_id):
        self.db = Database()
        self.decliner = CollatinusDecliner()
        self._get_all_words(dictionary_id)

    def _get_all_words(self, dictionary_id):
        self.data = self.db.read_database("""select distinct
	                                            a.WordId ,
	                                            a.Word
                                            from
                                                Word as a
                                            inner join
                                                Definition as b on a.WordId = b.WordId
                                            left outer join
                                                Flection as c on a.WordId = c.WordId
                                            where
                                                b.DictionaryId = {0} and
                                                c.FlectionId is null""".format(dictionary_id))

class WriteFlectionWithDeclination(WriteFlection):
    def __init__(self, DictionaryId):
        WriteFlection.__init__(self, DictionaryId)

    def write(self):
        for d in tqdm(self.data):
            word_id, word = d
            word = tl.rpl_chunk(word)
            try:
                declined_word = self.decliner.decline(word)
                for dw in declined_word:
                    form, description = dw
                    if form != '':
                        self.db.write_flection(word_id, form, description)
                    else:
                        raise cltk.exceptions.UnknownLemma


            except(cltk.exceptions.UnknownLemma, KeyError) as e:
                self.db.write_flection(word_id, word, '', 1)
                continue

        self.db._commit()

class WriteFlectionWithoutDeclination(WriteFlection):
    def __init__(self, DictionaryId):
        WriteFlection.__init__(self, DictionaryId)

    def write(self):
        for d in tqdm(self.data):
            word_id, word = d
            word = tl.rpl_chunk(word)
            self.db.write_flection(word_id, word, '', 1)
        self.db._commit()