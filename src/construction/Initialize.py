from src.construction.AddDictionary import stardict, perseus
from src.construction.WriteFlection import WriteFlectionWithDeclination
from src.construction.WriteFlection import WriteFlectionWithoutDeclination
from src.database.database import Database

class Initialize():

    def __init__(self):
        db = Database()
        db.truncate_database()

    def import_db(self, path, folder_name):

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
            del new_st_dict
            del new

        elif folder_name == 'georges_lat-de':
            new_st_dict = stardict(path, folder_name, file_name)
            dictionary_id = new_st_dict.add_words_to_dictionary()
            new = WriteFlectionWithDeclination(dictionary_id)
            new.write()
            del new_st_dict
            del new

        elif folder_name == 'lewis_short':
            new = perseus('Lewis, Charlton, T. - An Elementary Latin Dictionary', 17582)
            dictionary_id = new.add_words_to_dictionary()
            new = WriteFlectionWithDeclination(dictionary_id)
            new.write()
