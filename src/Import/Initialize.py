from ImportDictionary import import_dictionary_stardict
from ImportWriteFlections import WriteFlectionWithDeclination
from ImportWriteFlections import WriteFlectionWithoutDeclination
from ImportDictionary import import_dictionary_perseus
from DictionaryDatabase import Database

db = Database()
db.truncate_database()

########Dict 1
new_st_dict = import_dictionary_stardict('import_dictionaries/georges_de-lat', 'georges')
new_st_dict.add_words_to_dictionary()
new = WriteFlectionWithoutDeclination(1)
new.write()

#######Dict2

new_st_dict = import_dictionary_stardict('import_dictionaries/georges_lat-de', 'stardict')
new_st_dict.add_words_to_dictionary()

new = WriteFlectionWithDeclination(2)
new.write()

######Perseus Lewis Dictioanry

new = import_dictionary_perseus('Lewis, Charlton, T. - An Elementary Latin Dictionary', 17582)
new.add_words_to_dictionary()
new = WriteFlectionWithDeclination(3)
new.write()