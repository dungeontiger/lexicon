import psycopg2
import os

conn = psycopg2.connect(os.environ['DATABASE_URL'])
cur = conn.cursor()

with open('data/books.csv', 'w') as f:
    # get list of books
    cur.execute("SELECT * FROM book")
    row = cur.fetchone()
    while row is not None:
        s = ''
        for col in row:
            if isinstance(col, str):
                s += '"' + str(col) + '",'
            else:
                s += str(col) + ','
        s = s.replace('\n', '\\n')
        f.write(s[:-1] + '\n')
        row = cur.fetchone()

with open('data/definitions.csv', 'w') as f:
    cur.execute("SELECT * FROM definition")
    row = cur.fetchone()
    while row is not None:
        s = ''
        for col in row:
            if isinstance(col, str):
                s += '"' + str(col) + '",'
            else:
                s += str(col) + ','
        s = s.replace('\n', '\\n')
        f.write(s[:-1] + '\n')
        row = cur.fetchone()

cur.close()
conn.close()
