import flask
from flask import request, jsonify
import psycopg2

app = flask.Flask(__name__)
app.config["DEBUG"] = True


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


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
    print(query)
    records = write_db(query)
    print(records)
    return '{"published": "%s", "author": "%s", "sentence": "%s"}' % (published, author, sentence)


def read_db():
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="mysecretpassword",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="books")

        cursor = connection.cursor()
        # Print PostgreSQL Connection properties
        print(connection.get_dsn_parameters(), "\n")

        # Print PostgreSQL version
        cursor.execute("SELECT * FROM books;")
        records = cursor.fetchall()

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        # closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
    return records


def write_db(query):

    try:
        connection = psycopg2.connect(user="postgres",
                                      password="mysecretpassword",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="books")

        cursor = connection.cursor()
        # Print PostgreSQL Connection properties
        print(connection.get_dsn_parameters(), "\n")

        # Print PostgreSQL version
        cursor.execute(query)
        connection.commit()

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        # closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


app.run()
