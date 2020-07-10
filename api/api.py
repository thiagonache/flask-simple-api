import flask
from flask import request, jsonify
import psycopg2
import os

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return '''<h1>Distant Reading Archive</h1>
<p>A prototype API for distant reading of science fiction novels.</p>'''


@app.route('/api/v1/resources/books/all', methods=['GET'])
def api_all():
    all_books = read_db()

    return jsonify(all_books)


@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


@app.route('/api/v1/resources/books/new', methods=['POST'])
def api_new():
    payload = request.json
    published = payload.get("published")
    author = payload["author"]
    title = payload["title"]
    sentence = payload["sentence"]

    query = "INSERT INTO books VALUES(NULL,%s,'%s','%s','%s')" % (
        published, author, title, sentence)
    write_db(query)
    return '{"published": "%s", "author": "%s", "sentence": "%s"}' % (published, author, sentence)


def connect_db():
    try:
        connection = psycopg2.connect(user=os.getenv("DB_USER", "postgres"),
                                      password=os.getenv(
                                          "DB_PASS", "postgres"),
                                      host=os.getenv("DB_HOST", "127.0.0.1"),
                                      port=os.getenv("DB_PORT", 5432),
                                      database=os.getenv("DB_SCHEMA", "books"))
    except (Exception, psycopg2.Error) as error:
        raise(Exception("Error while connecting to PostgreSQL", error))

    return connection


def read_db():
    connection = connect_db()
    cursor = connection.cursor()
    # Print PostgreSQL Connection properties
    print(connection.get_dsn_parameters(), "\n")

    try:
        cursor.execute("SELECT * FROM books;")
        records = cursor.fetchall()
    except (Exception, psycopg2.Error) as error:
        print("Error while reading database data", error)
    finally:
        # closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
    return records


def write_db(query):
    connection = connect_db()
    cursor = connection.cursor()
    # Print PostgreSQL Connection properties
    print(connection.get_dsn_parameters(), "\n")

    try:
        cursor.execute(query)
        connection.commit()
    except (Exception, psycopg2.Error) as error:
        print("Error to insert data on PostgreSQL", error)
    finally:
        # closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


app.run()
