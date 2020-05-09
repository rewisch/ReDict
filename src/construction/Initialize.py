from src.construction.AddDictionary import stardict, perseus
from src.construction.WriteFlection import WriteFlectionWithDeclination
from src.construction.WriteFlection import WriteFlectionWithoutDeclination
from src.database.database import Database

db = Database()
db.truncate_database()

########Dict 1
new_st_dict = stardict('dictionaries/georges_de-lat', 'georges')
new_st_dict.add_words_to_dictionary()
new = WriteFlectionWithoutDeclination(1)
new.write()

#######Dict2
new_st_dict = stardict('dictionaries/georges_lat-de', 'stardict')
new_st_dict.add_words_to_dictionary()
new = WriteFlectionWithDeclination(2)
new.write()

######Perseus Lewis Dictioanry
new = perseus('Lewis, Charlton, T. - An Elementary Latin Dictionary', 17582)
new.add_words_to_dictionary()
new = WriteFlectionWithDeclination(3)
new.write()