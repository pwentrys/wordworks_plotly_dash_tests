import dash
import dash_core_components as dcc
import dash_html_components as html
import os
from datetime import datetime
from utilities.WordWorks import WordWorks as wordings

from sqlalchemy import create_engine
import pandas as pd


time_start = datetime.now()
print(f'Starting At: {time_start}\n\n')
engine = create_engine('mysql+pymysql://gappi:92cf6cc2050f9830996b42433da09d03a4baa26e5524b3b8075c2f076451650a@192.168.1.172:3306/stocks?charset=utf8')
conn = engine.connect()
conn.execute('TRUNCATE stock_word;')
read = pd.read_sql('SELECT title, description FROM stock_scrape;', conn)

results = wordings.do_dicts([
    read.get('title').values,
    read.get('description').values
])
# pprint.pprint(results)


class StockWord:
    def __init__(self, name, count):
        self.name = name
        self.count = count

    def __get_insert_sql__(self):
        return f'(\'{self.name}\', {self.count}),'

insert_prefix = f'INSERT INTO stock_word (name, count) VALUES '
insert_suffix = f';'
stock_words = [StockWord(key, results[key]) for key in results]


def create_inserts(stock_words):
    count = 0
    inserts = []
    insert = []
    for word in stock_words:
        insert.append(word.__get_insert_sql__())
        count += 1
        if count > 50:
            last = insert[len(insert)-1]
            last = last[:-1]
            last = f'{last}{insert_suffix}'
            insert[len(insert)-1] = last
            inserts.append(''.join(insert))
            insert = []
            count = 0
    if count > 0:
        last = insert[len(insert)-1]
        last = last[:-1]
        last = f'{last}{insert_suffix}'
        insert[len(insert)-1] = last
        inserts.append(''.join(insert))
    return inserts

inserts = create_inserts(stock_words)
if len(inserts) > 0:
    for insert in inserts:
        query_string = ''
        try:
            query_string = ''.join([insert_prefix, insert])
            conn.execute(query_string)
        except Exception as error:
            print(f'ERROR INSERTING {query_string}')
            print(error)
            print('\n')

time_end = datetime.now()
print(f'Started: {time_start}\n' 
      f'Ended: {time_end}\n' 
      f'Duration: {time_end-time_start}')

# pprint.pprint(dir(read.get('description')))
# wordings.do_dicts(read)
# conn.execute()

# pprint.pprint(dir(read))
# print(type(read))

# print(read)
# print(dir(read))
# print(read.T)
# print(read._AXIS_NAMES)
# print(read.axes)
# print(read.blocks)
# print(read.columns)
# print(read.count)
# print(read.describe)
# print(read.div)
# print(read.hist)
# print(read.head)
# print(read.to_json)
# print(read.xs)

conn.close()
