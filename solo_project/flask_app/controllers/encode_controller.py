from flask import render_template, request, send_file
from flask_app import app
from flask_app.models.encode_model import encode_ducky

@app.route('/encode', methods=['GET', 'POST'])
def encode():
    if request.method == 'POST':
        ducky_script = request.form['ducky_script']
        encoded_script = encode_ducky(ducky_script)  # Implement the function to encode Ducky Script
        return encoded_script
    else:
        return render_template('encode_form.html')
