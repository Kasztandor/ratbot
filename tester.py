import tinydb

db = tinydb.TinyDB('db.json')
table = db.table('bannedWords')

search = tinydb.Query()

bannedWords = []

for i in table.all():
    bannedWords.append(i['word'])

print(bannedWords)