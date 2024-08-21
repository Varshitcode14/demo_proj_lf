from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Dummy data
lost_items = []
found_items = []

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/lost', methods=['GET', 'POST'])
def lost():
    if request.method == 'POST':
        item = request.form.get('item')
        location = request.form.get('location')
        description = request.form.get('description')
        lost_items.append(f"{item} at {location}: {description}")
        return redirect(url_for('lostitems'))
    return render_template('lost.html')

@app.route('/found', methods=['GET', 'POST'])
def found():
    if request.method == 'POST':
        item = request.form.get('item')
        location = request.form.get('location')
        description = request.form.get('description')
        found_items.append(f"{item} at {location}: {description}")
        return redirect(url_for('founditems'))
    return render_template('found.html')

@app.route('/lostitems')
def lostitems():
    return render_template('lostitems.html', items=lost_items)

@app.route('/founditems')
def founditems():
    return render_template('founditems.html', items=found_items)

if __name__ == '__main__':
    app.run(debug=True)
