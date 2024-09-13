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
    """Connect to and query database"""
 
    con = create_connection(DATABASE)
    cur = con.cursor()
    cur.execute(query)
    result = cur.fetchall()
    con.close()

    return result


def sort(default):
    """Sorts the database"""

    sort = request.args.get('sort', default)
    order = request.args.get('order', 'asc')
    if order == 'asc':
        new_order = 'desc'
    else:
        new_order = 'asc'

    return sort, order, new_order


@app.route('/')
def render_index():
    """
    Finds all top rated books in the database
    :returns a rendered page
    """

    # Define and execute query
    book_query = "SELECT books.title, books.rating, books.genre, books.cover, authors.name, books.url FROM books, authors WHERE books.author_id = authors.author_id AND rating > 3"
    book_list = connect_query(book_query)

    return render_template('index.html', books=book_list)


@app.route('/books')
def render_books():
    """
    Finds all books in the database
    :returns a rendered page
    """

    # Define sort, query and execute query
    sorting = sort('book_id')
    book_query = "SELECT books.title, books.rating, books.genre, books.cover, authors.name, books.url FROM books, authors WHERE books.author_id = authors.author_id ORDER BY " + sorting[0] +" "+ sorting[1]
    book_list = connect_query(book_query)

    return render_template('books.html', books=book_list, order=sorting[2])


@app.route('/authors')
def render_authors():
    """
    Finds all authors in the database
    :returns a rendered page
    """

    # Define sort, query and execute query
    sorting = sort('author_id')
    author_query = "SELECT author_id, name, age, country FROM authors ORDER BY " + sorting[0] +" "+ sorting[1]
    author_list = connect_query(author_query)

    return render_template('authors.html', authors=author_list, order=sorting[2])


@app.route('/search', methods=['GET', 'POST'])
def render_search():
    """
    Find all records which contain the search item
    :POST contains the search value
    :returns a rendered page"""

    # Define search and queries
    search = request.form['search']
    book_query = "SELECT books.title, books.rating, books.genre, books.cover, authors.name, books.url FROM books, authors WHERE books.author_id = authors.author_id AND (books.title LIKE ? OR books.rating LIKE ? OR books.genre LIKE ? OR authors.name LIKE ?)"
    author_query = "SELECT author, name, age, country FROM authors WHERE name LIKE ? OR age LIKE ? OR country LIKE ?"
    
    # Connect to database
    con = create_connection(DATABASE)
    cur = con.cursor()

    # Query for books and authors with search term
    cur.execute(book_query, ("%"+search+"%", "%"+search+"%", "%"+search+"%", "%"+search+"%"))
    book_list = cur.fetchall()
    cur.execute(author_query, ("%"+search+"%", "%"+search+"%", "%"+search+"%"))
    author_list = cur.fetchall()
    con.close()

    return render_template('search.html', books=book_list, authors=author_list)


@app.route('/book/<url>')
def render_book(url):
    
    # Define and execute query
    book_query = "SELECT books.title, books.rating, books.genre, books.published, books.cover, authors.name, books.quote, books.adaptation, books.pages, books.url FROM books, authors WHERE books.author_id = authors.author_id AND books.url = '" + url + "'"
    book_list = connect_query(book_query)

    return render_template("book.html", books=book_list)


@app.route('/author/<name>')
def render_author(name):
    
    # Define and execute queries
    author_query = "SELECT authors.author, authors.name, authors.age, authors.country FROM authors WHERE authors.name = '" + name + "'"
    books_query = "SELECT books.title, books.cover, books.url FROM authors, books WHERE books.author_id = authors.author_id AND authors.name = '" + name + "'"
    author_list = connect_query(author_query)
    authors_books = connect_query(books_query)

    return render_template("author.html", authors=author_list, books=authors_books)


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)
