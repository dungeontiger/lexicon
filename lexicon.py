from flask import Flask, jsonify, request
from os import listdir
from os.path import isfile, join
import os
app = Flask(__name__)


@app.route('/')
def index():
    with open('index.html', 'r') as f:
        return f.read()


@app.route('/books')
def books():
    books = [f[:-5] for f in listdir('books') if isfile(join('books', f))]
    books.sort()
    return jsonify(books)


@app.route('/books/newBook', methods=['POST'])
def newBook():
    # check to see if a book with this name exists already
    if isfile(join('books', '{}.json'.format(request.form['name']))):
        return 'A book with the name {} already exists. No new book was created.'.format(request.form['name'])
    # create the book file
    with open(join('books', '{}.json'.format(request.form['name'])), 'w') as f:
        f.write("[]")
    return ''


@app.route('/books/delete/<book>', methods=['DELETE'])
def deleteBook(book):
    filename = join('books', '{}.json'.format(book))
    os.remove(filename)
    return ''


@app.route('/books/rename/<book>', methods=['POST'])
def renameBook(book):
    # check to see if the new name exists, if it does fail
    if isfile(join('books', '{}.json'.format(request.form['name']))):
        return 'A book with the name {} already exists. No book has been renamed.'.format(request.form['name'])
    os.rename(join('books', '{}.json'.format(book)), join('books', '{}.json'.format(request.form['name'])))
    return ''
