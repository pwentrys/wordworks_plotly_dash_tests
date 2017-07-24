from utilities.ReadWorks import ReadWorks
from utilities.SentenceWorks import SentenceWorks
from utilities.Word import Word


r = ReadWorks()
text = r.read_file('O:\\Code\\python\\plotly_dash\\utilities\\dummy.txt')
cleaned = r.citation_cleanup(text)

s = SentenceWorks(cleaned.splitlines())
extracted = s.extract_from_data()
extracted = sorted(extracted)
if len(extracted) > 5:
    extract = extracted[:5]

words = []
for item in extracted:
    words.append(Word(item))


logs = []
for word in words:
    logs.append(word.__log__())

print('\n'.join(logs))

s.close()
