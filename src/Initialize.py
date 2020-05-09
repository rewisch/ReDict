#####
#####Important: not yet ensured, that the lemmata json is in the cltk folder, gotta do that

from pathlib import Path
from os import listdir
from os.path import abspath, join
import zipfile

from cltk.corpus.utils.importer import CorpusImporter

from src.construction.Initialize import Initialize
from src.database.database import Database
import src.Initialize as init


class init_database():

    def __init__(self):
        self.run()

    def run(self):
        corpus_importer = CorpusImporter('latin')
        corpus_importer.import_corpus('latin_text_latin_library')

        init = Initialize()

        dict_folder = abspath('../data/dictionaries/')
        dicts = listdir(dict_folder)

        for dic in dicts:
            with zipfile.ZipFile(join(dict_folder, dic, 'dict.zip'), 'r') as zip_ref:
                zip_ref.extractall(join(dict_folder, dic))
            init.import_db(dict_folder, dic)


def initialize():
    my_file = Path("_database/dictionaries_db.db")
    if not my_file.is_file():
        db = Database()

        file = open('database/CreateDB.sql', 'r')
        content = file.read()
        scripts = content.split('GO')
        for script in scripts:
            db._execute(script)
            db._commit()

        db.create_property(1, '1,2,3', 'Activated Dictionaries')
        db.create_property(2, '18', 'Fontsize')
        db.create_property(3, '1', 'Stylesheet')
        db.create_property(4, 'Lemmata', 'Completer: Lemmata or Declensions')

        init.init_database()

