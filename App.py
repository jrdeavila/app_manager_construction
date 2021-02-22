from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

# config mysql connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'devcodehacker777'
app.config['MYSQL_PASSWORD'] = 'jose1003'
app.config['MYSQL_DB'] = 'managerconstruction'

# settings
app.secret_key = 'mykey'

mysql = MySQL(app)



@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.callproc('get_quotations', [])
    data = cur.fetchall()
    cur.nextset()
    if len(data) == 1:
        if len(data[0]) == 1:
            flash(data[0][0])
            return render_template('index.html', quotations = ())
        else:
            return render_template('index.html', quotations = data)
    else:
        return render_template('index.html', quotations = data)

@app.route('/new-quotation')
def name_quotation():
    return render_template('new_quotation.html')

@app.route('/create-quotation', methods=['POST'])
def create_quotation():
    if request.method == 'POST':
        quotation_name = request.form['name_quotation']
        cur = mysql.connection.cursor()
        cur.callproc('add_quotation', [quotation_name, ])
        message = cur.fetchall()
        cur.nextset();
        mysql.connection.commit()
        flash(message[0][0])
        return redirect(url_for('Index'))

@app.route('/edit/<string:id>')
def edit_quotation(id):
    cur = mysql.connection.cursor()
    cur.callproc('get_services_quotation', [id, ])
    data = cur.fetchall()
    cur.nextset()
    if len(data) == 1:
        if len(data[0]) == 1:
            return render_template('edit.html', services = (), quotation_id = id)
        else:
            return render_template('edit.html', services = data, quotation_id = id)
    else:
        return render_template('edit.html', services = data, quotation_id = id)
@app.route('/add_services/<string:id>', methods=['POST'])
def add_services(id):
    if request.method == 'POST':
        amount = int(request.form['amount'])
        unit_value = int(request.form['unit_value'])
        total_value = amount * unit_value
        cur = mysql.connection.cursor()
        cur.callproc('add_services_quotation', [
            id,
            request.form['service_name'],
            request.form['unit'],
            amount,
            unit_value,
            total_value
        ])
        message = cur.fetchall()
        cur.nextset()
        mysql.connection.commit()
        flash(message[0][0])
        return redirect(url_for('edit_quotation', id = id))


@app.route('/delete/<string:id>')
def delete_quotation(id):
    cur = mysql.connection.cursor()
    cur.callproc('remove_quotation', [id, ])
    message = cur.fetchall()
    cur.nextset();
    mysql.connection.commit()
    flash(message[0][0])
    return redirect(url_for('Index'))

@app.route('/delete-service/<string:id>')
def delete_service(id):
    cur = mysql.connect.cursor()
    cur.callproc('remove_service_quotation', [id, ])
    message = cur.fetchall()
    cur.nextset()
    flash(message[0][0])
    return redirect(url_for('edit_quotation', id = id))


@app.route('/edit-service/<string:id>/<string:quotation_id>')
def edit_service(id, quotation_id):
    cur = mysql.connect.cursor()
    cur.callproc('get_service', [id, ])
    data = cur.fetchall()
    return render_template('edit_service.html', service = data[0])

@app.route('/update-service/<string:id>/<string:quotation_id>', methods=['POST'])
def update_service(id, quotation_id):
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        total = int(request.form['amount']) * int(request.form['unit_value'])
        cur.callproc('update_service_quotation',[
            id,
            request.form['service_name'],
            request.form['unit'],
            request.form['amount'],
            request.form['unit_value'],
            total
        ])
        message = cur.fetchall()
        cur.nextset()
        mysql.connection.commit()
        flash(message[0][0])
        return redirect(url_for('edit_quotation', id = quotation_id))

@app.route('/build-quotation_pdf/<string:id>')
def build_quotation_pdf(id):
    return "this is a pdf of quotation {}".format(id)



if __name__ == '__main__':
    app.run(port = 3000, debug=True)
