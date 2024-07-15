from flask import Flask, render_template
import sqlite3
from sqlite3 import Error


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
    # Define query and connection
    query = "SELECT * FROM books"
    con = create_connection(DATABASE)
    cur = con.cursor()

    # Query the database
    cur.execute(query)
    book_list = cur.fetchall()
    con.close()
    print(book_list)
    return render_template('index.html', books=book_list)
    


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)
