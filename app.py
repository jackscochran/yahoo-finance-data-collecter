from Report import Report
from flask import Flask, render_template, request, send_file
import os
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        report = Report((int(date) for date in request.form.get('start').split("-")), (int(date) for date in request.form.get('start').split("-")))
        report.produce_excel(request.form.get('key'))
    except Exception as e:
        print(e)
        return{'success': False}

    return {'success': True}

@app.route('/download')
def download():
    return send_file(os.path.join('output', 'report.xlsx'), as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)

