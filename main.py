from flask import Flask, render_template, request
import sqlite3 as sql

app = Flask(__name__)
conn = sql.connect('database.db')
print("Database opened sucessfully")

conn.execute('CREATE TABLE IF NOT EXISTS students (name TEXT, addr TEXT, city TEXT, pin TEXT)')
print("Table created sucessfully")
conn.close()


@app.route('/')
def home():
    return render_template('indexsql.html')


@app.route('/enternew')
def new_student():
    return render_template('student.html')


@app.route('/addrec', methods=['POST', 'GET'])
def addrec():
    msg = "msg"
    if request.method == 'POST':
        try:
            nm = request.form['nm']
            addr = request.form['addr']
            city = request.form['city']
            pin = request.form['pin']
            with sql.connect("database.db") as conn:
                cur = conn.cursor()
                cur.execute("INSERT INTO students(name, addr, city, pin) VALUES(?, ?, ?, ?)", (nm, addr, city, pin))
                conn.commit()
                msg = "Data added successfully"
        except:
            conn.rollback()
            msg = "error adding data"
        finally:
            return render_template("result.html", msg=msg)


@app.route('/list')
def list():
    conn = sql.connect("database.db")
    conn.row_factory = sql.Row
    cur = conn.cursor()
    cur.execute("select * from students")
    rows = cur.fetchall()
    return render_template("list.html", rows=rows)

if __name__ == "__main__":
    app.run(debug=True)