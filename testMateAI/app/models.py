from app import mysql

class Book:
    def __init__(self, id, title, author):
        self.id = id
        self.title = title
        self.author = author

    def save(self):
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO books (title, author) VALUES (%s, %s)', (self.title, self.author))
        mysql.connection.commit()
        cur.close()

    @staticmethod
    def get_all():
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM books')
        result = cur.fetchall()
        cur.close()
        books = [Book(row[0], row[1], row[2]) for row in result]
        return books

    @staticmethod
    def get_by_id(book_id):
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM books WHERE id = %s', [book_id])
        result = cur.fetchone()
        cur.close()
        if result:
            book = Book(result[0], result[1], result[2])
            return book
        return None

    def update(self, book_id):
        cur = mysql.connection.cursor()
        cur.execute('UPDATE books SET title = %s, author = %s WHERE id = %s',
                    (self.title, self.author, book_id))
        mysql.connection.commit()
        cur.close()

    @staticmethod
    def delete(book_id):
        cur = mysql.connection.cursor()
        cur.execute('DELETE FROM books WHERE id = %s', [book_id])
        mysql.connection.commit()
        cur.close()