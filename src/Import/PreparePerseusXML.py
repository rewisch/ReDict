from bs4 import BeautifulSoup
from tqdm import tqdm

def perseus_xml_read():

    replaces = list()
    file = open('import_dictionaries/lewis_short/sed_commands.txt', 'r')
    input = file.readlines()

    for i in input:
        if i != '\n':
            split = i.split(r"/")
            replaces.append((split[1], split[2]))

    file.close()

    _xml = open('import_dictionaries/lewis_short/lewis.xml', 'r')
    content = _xml.read()

    print('\nPrepare XML File:\n')
    for rep in tqdm(replaces):
        rep, rep_with = rep
        # print(rep + '---> ' + rep_with)
        content = content.replace(rep, rep_with)

    _xmlNew = open('import_dictionaries/lewis_short/lewis_rep.xml','w')
    _xmlNew.write(content)

    #
    # Read File and get keyword and entry (not so nice in terms of layout of the text, but the
    # perseus format really sucks.
    #

    print('\nRead XML File:\n')

    content = open('import_dictionaries/lewis_short/lewis_rep.xml')
    soup = BeautifulSoup(content, 'xml')

    lst_lewis = list()

    for res in tqdm(soup.find_all('entry')):

        _key = res.get('key')
        _res = res.getText().replace('\n', ' ').rstrip().lstrip().replace('   ', ' ').replace('  ', ' ')
        lst_lewis.append((_key, _res))

    return lst_lewis
