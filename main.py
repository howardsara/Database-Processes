import sqlite3
from sqlite3 import Error

from flask import Flask, render_template


app = Flask(__name__)
DATABASE = "books.db"


def create_connection(db_file):
    """
    Creates connection to the database
    :parameter    db_file - name of the file 
    :returns    connection - connection to the database"""
    
    try:
        connection = sqlite3.connect(db_file)
        return connection

    except Error as e:
        print(e)
        return None


@app.route('/')
def render_index():

    return render_template('index.html')


@app.route('/books')
def render_books():
    # Define query and connection
    query = "SELECT title, rating, genre, published, cover, author_id FROM books"
    author_query = "SELECT author_id, first_name, last_name FROM authors"
    con = create_connection(DATABASE)
    cur = con.cursor()

    # Query the database
    cur.execute(query)
    book_list = cur.fetchall()
    cur.execute(author_query)
    author_list = cur.fetchall()
    con.close()
    print(book_list, author_list)

    # Make an ordered list of authors in relation to each book
    book_author = []
    for book in book_list:
        for author in author_list:
            if book[-1] == author[0]:
                book_author.append(author[1] + " " + author[2])

    
    return render_template('books.html', books=book_list, authors=book_author)


@app.route('/authors')
def render_authors():
    # Define query and connection
    query = "SELECT * FROM authors"
    con = create_connection(DATABASE)
    cur = con.cursor()

    # Query the database
    cur.execute(query)
    author_list = cur.fetchall()
    con.close()
    print(author_list)
    return render_template('authors.html', authors=author_list)


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)
