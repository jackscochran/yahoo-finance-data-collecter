from Company import Company
from Report import generate_ticker_list, save_sheet
from flask import Flask, render_template, request, send_file
import os
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():

    tickers = generate_ticker_list((int(date) for date in request.form.get('start').split("-")), (int(date) for date in request.form.get('start').split("-")))
    
    return {'tickers': tickers, 'key': request.form.get('key')}


@app.route('/save-ticker', methods=['POST'])
def save_ticker():
    if request.method == 'POST':
        save_sheet(request.form.get('ticker'), request.form.get('key'))
        return {'success': True}

@app.route('/download')
def download():
    return send_file(os.path.join('output', 'report.xlsx'), as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)

