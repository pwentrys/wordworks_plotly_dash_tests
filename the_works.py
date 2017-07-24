from utilities.ReadWorks import ReadWorks
from utilities.SentenceWorks import SentenceWorks


r = ReadWorks()
text = r.read_file('O:\\Code\\python\\plotly_dash\\utilities\\dummy.txt')
cleaned = r.citation_cleanup(text)

s = SentenceWorks(cleaned.splitlines())
extracted = s.extract_from_data()
extracted = sorted(extracted)
print(extracted)

s.close()
