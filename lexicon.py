from flask import Flask, jsonify, request
import os
import psycopg2
from collections import OrderedDict

app = Flask(__name__)


@app.route('/')
def index():
    with open('index.html', 'r') as f:
        return f.read()


@app.route('/books')
def books():
    books = []
    conn = psycopg2.connect(os.environ['DATABASE_URL'])
    cur = conn.cursor()
    cur.execute("SELECT book_name from book ORDER BY book_name")
    book = cur.fetchone()
    while book is not None:
        books.append(book[0])
        book = cur.fetchone()
    cur.close()
    conn.close()
    return jsonify(books)


@app.route('/books/newBook', methods=['POST'])
def newBook():
    # check to see if a book with this name exists already
    result = ''
    conn = psycopg2.connect(os.environ['DATABASE_URL'])
    cur = conn.cursor()
    cur.execute("SELECT id FROM book WHERE book_name='{}'".format(request.form['name']))
    row = cur.fetchone()
    if row is not None:
        # send back an error
        result = 'A book with the name {} already exists. No new book was created.'.format(request.form['name'])
    else:
        # create the book entry
        cur.execute("INSERT INTO book (book_name) VALUES ('{}')".format(request.form['name']))
        conn.commit()
    cur.close()
    conn.close()
    return result


@app.route('/books/delete/<book>', methods=['DELETE'])
def deleteBook(book):
    # delete from both tables
    conn = psycopg2.connect(os.environ['DATABASE_URL'])
    cur = conn.cursor()
    # first get the id of the book
    cur.execute("SELECT id FROM book WHERE book_name='{}'".format(book))
    book_id = cur.fetchone()[0]
    cur.execute("DELETE FROM book WHERE id = {}".format(book_id))
    cur.execute("DELETE FROM definition WHERE book_id = {}".format(book_id))
    conn.commit()
    cur.close()
    conn.close()
    return ''


@app.route('/books/rename/<book>', methods=['POST'])
def renameBook(book):
    # check to see if the new name exists, if it does fail
    result = ''
    conn = psycopg2.connect(os.environ['DATABASE_URL'])
    cur = conn.cursor()
    cur.execute("SELECT id FROM book WHERE book_name='{}'".format(request.form['name']))
    row = cur.fetchone()
    if row is not None:
        # send back an error
        result = 'A book with the name {} already exists. No new book was created.'.format(request.form['name'])
    else:
        # create the book entry
        cur.execute("UPDATE book SET book_name = '{}' WHERE book_name = '{}'".format(request.form['name'], book))
        conn.commit()
    cur.close()
    conn.close()
    return result


@app.route('/books/<book>')
def getBook(book):
    conn = psycopg2.connect(os.environ['DATABASE_URL'])
    cur = conn.cursor()
    # first get the id of the book
    cur.execute("SELECT id FROM book WHERE book_name='{}'".format(book))
    book_id = cur.fetchone()[0]
    cur.execute("SELECT term, definition FROM definition WHERE book_id='{}' ORDER BY term".format(book_id))
    row = cur.fetchone()
    terms = {}
    while row is not None:
        terms[row[0]] = row[1]
        row = cur.fetchone()
    cur.close()
    conn.close()
    ordered = OrderedDict()
    for key in sorted(terms.keys(), key=str.casefold):
        ordered[key] = terms[key]
    return jsonify(ordered)


@app.route('/books/addDef/<book>', methods=['POST'])
def addDef(book):
    conn = psycopg2.connect(os.environ['DATABASE_URL'])
    cur = conn.cursor()
    # first get the id of the book
    cur.execute("SELECT id FROM book WHERE book_name='{}'".format(book))
    book_id = cur.fetchone()[0]
    result = ''
    word = request.form['word']
    notes = request.form['notes']
    # check and see if a definition for this already exists
    cur.execute("SELECT id FROM definition where book_id={} and term = '{}'".format(book_id, word))
    row = cur.fetchone()
    if row is not None:
        result = "A definition for the word " + word + " already exists and was not replaced or added."
    else:
        cur.execute("INSERT INTO definition (book_id, term, definition) VALUES({}, '{}', '{}')".format(book_id, word, notes))
        conn.commit()
    cur.close()
    conn.close()
    return result


@app.route('/books/deleteDef/<book>', methods=['DELETE'])
def deleteDef(book):
    conn = psycopg2.connect(os.environ['DATABASE_URL'])
    cur = conn.cursor()
    # first get the id of the book
    cur.execute("SELECT id FROM book WHERE book_name='{}'".format(book))
    book_id = cur.fetchone()[0]
    # delete the entry
    cur.execute("DELETE from definition WHERE book_id = {} and term = '{}'".format(book_id, request.form['word']))
    conn.commit()
    cur.close()
    conn.close()
    return ''


@app.route('/books/editDef/<book>', methods=['POST'])
def editDef(book):
    conn = psycopg2.connect(os.environ['DATABASE_URL'])
    cur = conn.cursor()
    # first get the id of the book
    cur.execute("SELECT id FROM book WHERE book_name='{}'".format(book))
    book_id = cur.fetchone()[0]
    cur.execute("UPDATE definition SET definition = '{}' WHERE book_id = {} and term = '{}'".format(request.form['notes'], book_id, request.form['word']))
    conn.commit()
    cur.close()
    conn.close()
    return ''
