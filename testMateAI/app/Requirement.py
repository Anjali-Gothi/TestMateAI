from app import mysql


class Req:
    def __init__(self,rqid, summary, description):
        self.rqid = rqid
        self.summary = summary
        self.description = description

    def __init__(self, summary, description):
        self.summary = summary
        self.description = description

    def save(self):
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO requirement (summary, description) VALUES (%s, %s)',
                    (self.summary, self.description))
        mysql.connection.commit()
        cur.close()

    @staticmethod
    def get_all():
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM Requirement')
        result = cur.fetchall()
        cur.close()
        requirements = [Requirement(row[0], row[1], row[2]) for row in result]
        return requirements

    @staticmethod
    def get_by_id(req_id):
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM requirement WHERE id = %s', [req_id])
        result = cur.fetchone()
        cur.close()
        if result:
            book = Requirement(result[0], result[1], result[2])
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
