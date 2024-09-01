import sqlite3
from sqlite3 import Error

from flask import Flask, render_template, request


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
    # Connect match from a second list to the foreign key in the first
    match = []
    full_list = []
    for i in list1:
        for j in list2:
            if i[-1] == j[0]:
                match.append(j[1] + " " + j[2])

    for i in list1:
        main = list(i)
        foreign = match[list1.index(i)]
        main[-1] = foreign
        full_list.append(main)

    return full_list


@app.route('/')
def render_index():
    # Define query
    book_query = "SELECT title, rating, genre, published, cover, author_id FROM books WHERE rating > 3"
    author_query = "SELECT author_id, first_name, last_name FROM authors"

    book_list = connect_query(book_query)
    author_list = connect_query(author_query)

    return render_template('index.html', books=foreign_key(book_list, author_list))


@app.route('/books')
def render_books():
    # Define query
    book_query = "SELECT title, rating, genre, published, cover, author_id FROM books"
    author_query = "SELECT author_id, first_name, last_name FROM authors"

    book_list = connect_query(book_query)
    author_list = connect_query(author_query)

    return render_template('books.html', books=foreign_key(book_list, author_list))


@app.route('/authors')
def render_authors():
    # Define query
    author_query = "SELECT author, first_name, last_name FROM authors"
    
    author_list = connect_query(author_query)

    return render_template('authors.html', authors=author_list)


@app.route('/search', methods=['GET', 'POST'])
def render_search():
    """
    Find all records which contain the search item
    :POST contains the search value
    :returns a rendered page"""

    # Define search
    search = request.form['search']

    # Define queries
    book_query = "SELECT title, rating, genre, published, cover, author_id FROM books"
    author_query = "SELECT first_name, last_name, author FROM authors WHERE first_name LIKE ? OR last_name LIKE ?"
    all_authors_query = "SELECT author_id, first_name, last_name FROM authors"
    
    # Connect releavent author to each book 
    all_authors = connect_query(all_authors_query)
    books = connect_query(book_query)
    full_books = foreign_key(books, all_authors)
    
    #Search books 
    filtered_books = []
    for book in full_books:
        for b in book:
            if search.lower() in str(b).lower():
                filtered_books.append(book)
                break
    
    # Connect and query database for authors
    con = create_connection(DATABASE)
    cur = con.cursor()
    cur.execute(author_query, ("%"+search+"%", "%"+search+"%"))
    author_list = cur.fetchall()
    con.close()

    return render_template('search.html', books=filtered_books, authors=author_list)


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)
