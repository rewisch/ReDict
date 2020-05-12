import re

def el_qt(sql):
    return sql.replace("'", "''")

def rpl_chunk(_str):
    _str = re.sub('\d', '', _str)
    _str = _str.replace('(', '')
    _str = _str.replace(')', '')
    _str = _str.replace('ß', 'ss')
    _str = _str.replace('[', '')
    _str = _str.replace(']', '')
    _str = _str.replace("'", "''")
    _str = _str.replace('-','')
    _str = _str.replace('_', '')
    return _str

def clpboard_cleanse(inp : str):
    inp = inp.replace(' ', '')
    inp = inp.replace('-', '')
    inp = inp.replace('.', '')
    inp = inp.replace(',', '')
    inp = inp.replace(':', '')
    inp = inp.replace('(', '')
    inp = inp.replace(')', '')
    inp = inp.replace('ß', 'ss')
    inp = inp.replace('[', '')
    inp = inp.replace(']', '')
    inp = inp.replace("'", "''")
    inp = inp.replace('_', '')
    inp = inp.replace('"', '')
    return inp
