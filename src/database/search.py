from bs4 import BeautifulSoup
from src.gui.all_windows import AllWindows

class Search(AllWindows):

    def search_word(self, wrd, like):
        data = self.db.search_word(wrd, like)
        result = ''
        if len(data) != 0:
            for d in data:
                wordid, word, definition, abstractive = d
                if abstractive and int(self.db.get_property(8)):
                    result = result + self.get_abstraction(definition) + '<br>'
                result = result + definition.rstrip('<br />').replace('<br>', '') \
                         + '<br>---------------------------<br>'
            self.db.write_history(wordid)
        else:
            result = 'Not found'

        return result

    def get_abstraction(self, definition):
        font_size = int(self.db.get_property(2))
        font_size -= 5
        soup = BeautifulSoup(definition, 'html.parser')
        res = soup.findAll('b')
        # abstraction = '<i><b style="color: #548a3d"><p style="font-size:{0}px">'.format(font_size)
        abstraction = '<i><b style="color: #548a3d">'.format(font_size)
        for r in res:
            word = str(r).replace('<b style="color: #47A">', '').replace('</b>', '').rstrip().lstrip().rstrip(',')
            abstraction += word + ', '
        abstraction = abstraction.rstrip(' ').rstrip(',') + '</p></b></i><br>'
        return abstraction


