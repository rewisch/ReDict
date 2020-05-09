import re

def el_qt(sql):
    return sql.replace("'", "''")

def rpl_chunk(_str):
    return re.sub('\d', '', _str).replace('(', '').replace(')', '').replace('ß', 'ss').replace('[', '').replace(']', '').replace("'", "''").replace('-','').replace('_', '')
