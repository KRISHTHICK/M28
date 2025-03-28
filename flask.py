from flask import Flask, request, jsonify, render_template
import sqlite3
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect('carbon_emissions.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS emissions (product TEXT, emission REAL)''')
    conn.commit()
    conn.close()

# Function to get carbon emission from the database
def get_carbon_emission(product):
    conn = sqlite3.connect('carbon_emissions.db')
    c = conn.cursor()
    c.execute('SELECT emission FROM emissions WHERE product=?', (product,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Upload route
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        # Here you would call your image recognition API
        # For this example, let's assume a function recognize_product(image_path)
        product = recognize_product(file_path)
        emission = get_carbon_emission(product)
        if emission:
            return jsonify({'product': product, 'emission': emission})
        else:
            return jsonify({'error': 'Product not found in database'})

# Dummy image recognition function
def recognize_product(image_path):
    # Implement your image recognition logic here
    # For this example, let's assume it always recognizes 'laptop'
    return 'laptop'

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
