import sqlite3
from flask import Flask, render_template, redirect, url_for
from werkzeug.exceptions import abort

def get_item(item_id):
    conn = get_db_connection()
    item = conn.execute('SELECT * FROM items WHERE id = ?',
                        (item_id,)).fetchone()
    positions = conn.execute('SELECT * FROM positions WHERE item_id = ?',
                             (item_id,)).fetchall()
    conn.close()
    if item is None:
        abort(404)
    return item, positions

app = Flask(__name__)

@app.route('/create_item', methods=['GET', 'POST'])
def create_item():
    if request.method == 'POST':
        title = request.form['title']
        company = request.form['company']
        date = request.form['date']
        positions = []
        for i in range(1, 6):
            name = request.form.get(f'name_{i}')
            unit = request.form.get(f'unit_{i}')
            quantity = request.form.get(f'quantity_{i}')
            if name and unit and quantity:
                positions.append((name, unit, quantity))

        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("INSERT INTO items (title, company, status, time) VALUES (?, ?, ?, ?)", (title, company, 'не выдан', date))
        item_id = c.lastrowid
        for name, unit, quantity in positions:
            c.execute("INSERT INTO positions (item_id, name, unit, quantity) VALUES (?, ?, ?, ?)", (item_id, name, unit, quantity))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('create_item.html')

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    items = conn.execute('SELECT * FROM items').fetchall()
    conn.close()
    return render_template('index.html', items=items)

@app.route('/<int:item_id>')
def item(item_id):
    item, positions = get_item(item_id)
    return render_template('item.html', item=item, positions=positions)

@app.route('/<int:item_id>', methods=['POST'])
def issue_item(item_id):
    conn = get_db_connection()
    conn.execute('UPDATE items SET status = ?, time = CURRENT_TIMESTAMP WHERE id = ?',
                 ('выдан', item_id))
    conn.commit()
    conn.close()
    return redirect(url_for('item', item_id=item_id))

from flask import request

@app.route('/<int:item_id>/add_position', methods=['POST'])
def add_position(item_id):
    name = request.form['name']
    unit = request.form['unit']
    quantity = request.form['quantity']

    conn = get_db_connection()
    conn.execute('INSERT INTO positions (item_id, name, unit, quantity) VALUES (?, ?, ?, ?)',
                 (item_id, name, unit, quantity))
    conn.commit()
    conn.close()
    return redirect(url_for('item', item_id=item_id))

if __name__ == '__main__':
    app.run()
