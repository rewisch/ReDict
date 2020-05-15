from os.path import abspath, join

from bs4 import BeautifulSoup
from tqdm import tqdm

folder_path = abspath('../data/dictionaries/lewis_short/')

def perseus_xml_read():

    replaces = list()
    file = open(join(folder_path,'sed_commands.txt'), 'r', encoding='Utf-8')
    input = file.readlines()

    for i in input:
        if i != '\n':
            split = i.split(r"/")
            replaces.append((split[1], split[2]))

    file.close()

    _xml = open(join(folder_path, 'lewis.xml'), 'r', encoding='Utf-8')
    content = _xml.read()

    print('\nPrepare XML File:\n')
    for rep in tqdm(replaces):
        rep, rep_with = rep
        content = content.replace(rep, rep_with)

    _xmlNew = open(join(folder_path, 'lewis_rep.xml'), 'w', encoding='Utf-8')
    _xmlNew.write(content)

    print('\nRead XML File:\n')

    content = open(join(folder_path, 'lewis_rep.xml'), encoding='Utf-8')
    soup = BeautifulSoup(content, 'xml')

    lst_lewis = list()

    for res in tqdm(soup.find_all('entry')):
        _key = res.get('key')
        _res = res.getText().replace('\n', ' ').rstrip().lstrip().replace('   ', ' ').replace('  ', ' ')
        lst_lewis.append((_key, _res))

    return lst_lewis
