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


def connect_query(query):
    # Connect to and query database
    con = create_connection(DATABASE)
    cur = con.cursor()
    cur.execute(query)
    list = cur.fetchall()
    con.close()

    return list


def foreign_key(list1, list2):
    # Connect details from a second list to the foreign key in the first
    details = []
    for i in list1:
        for j in list2:
            if i[-1] == j[0]:
                details.append(j[1] + " " + j[2])

    return details


@app.route('/')
def render_index():
    # Define query
    book_query = "SELECT title, rating, genre, published, cover, author_id FROM books WHERE rating > 3"
    author_query = "SELECT author_id, first_name, last_name FROM authors"

    book_list = connect_query(book_query)
    author_list = connect_query(author_query)

    return render_template('index.html', books=book_list, authors=foreign_key(book_list, author_list))


@app.route('/books')
def render_books():
    # Define query
    book_query = "SELECT title, rating, genre, published, cover, author_id FROM books"
    author_query = "SELECT author_id, first_name, last_name FROM authors"

    book_list = connect_query(book_query)
    author_list = connect_query(author_query)

    return render_template('books.html', books=book_list, authors=foreign_key(book_list, author_list))


@app.route('/authors')
def render_authors():
    # Define query
    author_query = "SELECT author, first_name, last_name FROM authors"
    
    author_list = connect_query(author_query)

    return render_template('authors.html', authors=author_list)


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)
