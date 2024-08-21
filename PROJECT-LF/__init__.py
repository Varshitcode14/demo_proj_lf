from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///items.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class LostItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=True)

class FoundItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=True)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/lost', methods=['GET', 'POST'])
def lost():
    if request.method == 'POST':
        item = request.form.get('item')
        location = request.form.get('location')
        description = request.form.get('description')
        new_lost_item = LostItem(item=item, location=location, description=description)
        db.session.add(new_lost_item)
        db.session.commit()
        return redirect(url_for('lostitems'))
    return render_template('lost.html')

@app.route('/found', methods=['GET', 'POST'])
def found():
    if request.method == 'POST':
        item = request.form.get('item')
        location = request.form.get('location')
        description = request.form.get('description')
        new_found_item = FoundItem(item=item, location=location, description=description)
        db.session.add(new_found_item)
        db.session.commit()
        return redirect(url_for('founditems'))
    return render_template('found.html')

@app.route('/lostitems')
def lostitems():
    items = LostItem.query.all()
    return render_template('lostitems.html', items=items)

@app.route('/founditems')
def founditems():
    items = FoundItem.query.all()
    return render_template('founditems.html', items=items)

@app.route('/delete_lost/<int:id>')
def delete_lost(id):
    item_to_delete = LostItem.query.get_or_404(id)
    db.session.delete(item_to_delete)
    db.session.commit()
    return redirect(url_for('lostitems'))

@app.route('/delete_found/<int:id>')
def delete_found(id):
    item_to_delete = FoundItem.query.get_or_404(id)
    db.session.delete(item_to_delete)
    db.session.commit()
    return redirect(url_for('founditems'))

if __name__ == '__main__':
    app.run(debug=True)
