from flask import Flask, request, render_template, redirect, Response
from flask_sqlalchemy import SQLAlchemy
import io
import csv

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)


class Items(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float(precision=2), nullable=False)
    unit = db.Column(db.String(10), nullable=True)


@app.route('/', methods=['POST', 'GET'])
def homepage():
    if request.method == 'POST':
        category = request.form.get('category')
        name = request.form.get('name')
        price = request.form.get('price')
        unit = request.form.get('unit')
        new_item = Items(category=category, name=name,
                         price=price, unit=unit)
        try:
            db.session.add(new_item)
            db.session.commit()
            return redirect('/')
        except:
            return "cannot add your item"

    else:
        items = Items.query.all()
        return render_template('index.html', items=items)


@app.route('/delete/<int:id>')
def delete_item(id):
    item = Items.query.get_or_404(id)

    try:
        db.session.delete(item)
        db.session.commit()
        return redirect('/')
    except:
        return "Cannot delete this item"


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_item(id):
    item = Items.query.get_or_404(id)
    if request.method == 'POST':
        item.category = request.form.get('category')
        item.name = request.form.get('name')
        item.price = request.form.get('price')
        item.unit = request.form.get('unit')
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "Cannot update this item"

    else:
        return render_template('update.html', item=item)


@app.route('/download')
def download():
    items = Items.query.all()
    output = io.StringIO()
    writer = csv.writer(output)
    fields = ['ID', 'Category', 'Name', 'Price', 'Unit']
    rows = []
    for row in items:
        rows.append([str(row.id), row.category, row.name, str(row.price), row.unit])

    writer.writerow(fields)
    writer.writerows(rows)
    output.seek(0)
    return Response(output, mimetype="text/csv",
                    headers={"Content-Disposition": "attachment; filename=inventory.csv"})


app.run(port=5000, debug=True)
