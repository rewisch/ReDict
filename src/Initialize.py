from pathlib import Path
from os import listdir, makedirs
from shutil import copy2
from os.path import abspath, join, normpath, expanduser
import zipfile

from cltk.corpus.utils.importer import CorpusImporter

from src.construction.Initialize import Initialize
from src.database.database import Database
import src.Initialize as init


class init_database():

    def __init__(self):
        self.run()

    def run(self):
        print('\nInstall Cltk Corpus\n')
        corpus_importer = CorpusImporter('latin')
        corpus_importer.import_corpus('latin_text_latin_library')

        print('\nInstall latin models\n')
        cltk_folder = expanduser(normpath('~/cltk_data'))
        try:
            makedirs(join(cltk_folder, 'latin/model/latin_models_cltk/lemmata/collatinus'))
        except:
            print('cltk-folder exists')

        copy2(abspath('../data/collected.json'), join(cltk_folder, 'latin/model/latin_models_cltk/lemmata/collatinus' ))


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
        db.create_property(5, '1', 'Clipboard enabled')
        db.create_property(6, '5', 'Clipboard Watcher Seconds')

        init.init_database()

