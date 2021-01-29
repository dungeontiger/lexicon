from flask import Flask, jsonify, request
from os import listdir
from os.path import isfile, join
import os
import json
from collections import OrderedDict


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
        f.write("{}")
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


@app.route('/books/<book>')
def getBook(book):
    with open(join('books', '{}.json'.format(book)), 'r') as f:
        defs = json.load(f)
        ordered = {}
        for k in sorted(defs.keys()):
            ordered[k] = defs[k]
    return jsonify(ordered)


@app.route('/books/addDef/<book>', methods=['POST'])
def addDef(book):
    # read in the book
    with open(join('books', '{}.json'.format(book)), 'r') as f:
        defs = json.load(f)
    word = request.form['word']
    notes = request.form['notes']
    # add the definition (if it does not exist)
    if word in defs:
        return "A definition for the word " + word + " already exists and was not replaced or added."
    # write out the book
    defs[word] = notes
    with open(join('books', '{}.json'.format(book)), 'w') as f:
        json.dump(defs, f)
    return ''


@app.route('/books/deleteDef/<book>', methods=['DELETE'])
def deleteDef(book):
    # read in the book
    with open(join('books', '{}.json'.format(book)), 'r') as f:
        defs = json.load(f)
    del defs[request.form['word']]
    with open(join('books', '{}.json'.format(book)), 'w') as f:
        json.dump(defs, f)
    return ''


@app.route('/books/editDef/<book>', methods=['POST'])
def editDef(book):
    # read in the book
    with open(join('books', '{}.json'.format(book)), 'r') as f:
        defs = json.load(f)
    defs[request.form['word']] = request.form['notes']
    with open(join('books', '{}.json'.format(book)), 'w') as f:
        json.dump(defs, f)
    return ''
