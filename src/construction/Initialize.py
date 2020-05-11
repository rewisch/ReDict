from os import listdir, makedirs
from shutil import copy2
from os.path import abspath, join, normpath, expanduser
import zipfile
from pathlib import Path

from cltk.corpus.utils.importer import CorpusImporter

from src.construction.add_dictionary import stardict, perseus
from src.construction.writeflection import WriteFlectionWithDeclination
from src.construction.writeflection import WriteFlectionWithoutDeclination
from src.database.database import Database


class Initialize():

    def create_Database(self):
        my_file = Path("_database/redict.db")
        if not my_file.is_file():
            self.db = Database()

            file = open('database/createdb.sql', 'r')
            content = file.read()
            scripts = content.split('GO')
            for script in scripts:
                self.db._execute(script)
                self.db._commit()

            self.db.create_property(1, '1,2,3', 'Activated Dictionaries')
            self.db.create_property(2, '18', 'Fontsize')
            self.db.create_property(3, '1', 'Stylesheet')
            self.db.create_property(4, 'Lemmata', 'Completer: Lemmata or Declensions')
            self.db.create_property(5, '1', 'Clipboard enabled')
            self.db.create_property(6, '5', 'Clipboard Watcher Seconds')
            self.db.create_property(7, '2', 'Clipboard Watcher x-Times')
            self.db.create_property(8, '1', 'Show abstract of Dict-Entry')

            self._init_database()

    def _init_database(self):
        print('\nInstall Cltk Corpus\n')
        corpus_importer = CorpusImporter('latin')
        corpus_importer.import_corpus('latin_text_latin_library')

        print('\nInstall latin models\n')
        cltk_folder = expanduser(normpath('~/cltk_data'))
        try:
            makedirs(join(cltk_folder, 'latin/model/latin_models_cltk/lemmata/collatinus'))
        except:
            print('cltk-folder exists')

        copy2(abspath('../data/collected.json'), join(cltk_folder, 'latin/model/latin_models_cltk/lemmata/collatinus'))

        dict_folder = abspath('../data/dictionaries/')
        dicts = listdir(dict_folder)

        for dic in dicts:
            with zipfile.ZipFile(join(dict_folder, dic, 'dict.zip'), 'r') as zip_ref:
                zip_ref.extractall(join(dict_folder, dic))
            self._import_dict2db(dict_folder, dic)

    def _import_dict2db(self, path, folder_name):

        if folder_name == 'georges_de-lat':
            file_name = 'georges'
        elif folder_name == 'georges_lat-de':
            file_name = 'stardict'
        elif folder_name == 'lewis_short':
            file_name = ''
        else:
            raise FileNotFoundError('No Dictionary found')

        if folder_name == 'georges_de-lat':
            new_st_dict = stardict(path, folder_name, file_name)
            dictionary_id = new_st_dict.add_words_to_dictionary()
            new = WriteFlectionWithoutDeclination(dictionary_id)
            new.write()

        elif folder_name == 'georges_lat-de':
            new_st_dict = stardict(path, folder_name, file_name)
            dictionary_id = new_st_dict.add_words_to_dictionary()
            new = WriteFlectionWithDeclination(dictionary_id)
            new.write()

        elif folder_name == 'lewis_short':
            new = perseus('Lewis, Charlton, T. - An Elementary Latin Dictionary', 17582)
            dictionary_id = new.add_words_to_dictionary()
            new = WriteFlectionWithDeclination(dictionary_id)
            new.write()
