import os
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, inspect, select
from flask import Flask, render_template, url_for, request, redirect, flash, session

UPLOAD_FOLDER = os.getcwd() + '/dbs/'
ALLOWED_EXTENSIONS = 'db'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "super secret key"


def file_check(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def rows_to_list(result, columns):
    listofrows = [[record[n] for n in range(len(columns))] for record in result]
    return listofrows



@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and file_check(file.filename):
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            #session['database'] = create_engine('sqlite:///dbs/' + file.filename, echo=True)
            return redirect(url_for('tables_list', filename=file.filename))
        else:
            flash('Wrong file!')
            return redirect(request.url)
    elif request.method == 'GET':
        return render_template('index.html')


@app.route('/<filename>/', methods=['GET', 'POST'])
def tables_list(filename):
    if request.method == 'GET':
        engine = create_engine('sqlite:///dbs/' + filename, echo=True)
        tables = inspect(engine).get_table_names()
        return render_template('tables.html', filename=filename, tables=tables)
    if request.method == 'POST':
        table = request.form.get('table')
        return redirect(url_for('display_table', filename=filename, table=table))


@app.route('/<filename>/<table>/', methods=['GET', 'POST'])
def display_table(filename, table):
    if request.method == 'GET':
        engine = create_engine('sqlite:///dbs/' + filename, echo=True)
        con = engine.connect()
        result = con.execute(f"SELECT * FROM {table}")
        columns = result.keys()
        wtable = Table(table, MetaData(), autoload_with=engine)
        query = select(wtable)
        result = engine.execute(query).fetchall()
        listofrows = rows_to_list(result, columns)
        return render_template('display_table.html', filename=filename, table=table, columns=columns, rows=listofrows)


if __name__ == '__main__':
    app.run(debug=True)
