from flask import render_template, request, redirect, url_for
from app import app
from app.models import Book

from TestMateAI.testMateAI.app import generatetc
from TestMateAI.testMateAI.app.Requirement import Req


@app.route('/')
def index():
    books = Book.get_all()
    return render_template('index.html', books=books)

@app.route('/books/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        summary = request.form['summary']
        description = request.form['description']
        requirement = Req(summary, description)
        requirement.save()
        print(generatetc.generatetc(description))
        return redirect(url_for('index'))
    return render_template('create.html')

@app.route('/books/edit/<int:book_id>', methods=['GET', 'POST'])
def edit(book_id):
    book = Book.get_by_id(book_id)
    if not book:
        return redirect(url_for('index'))
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        book.title = title
        book.author = author
        book.update(book_id)
        return redirect(url_for('index'))
    return render_template('edit.html', book=book)

@app.route('/books/delete/<int:book_id>', methods=['POST'])
def delete(book_id):
    Book.delete(book_id)
    return redirect(url_for('index'))