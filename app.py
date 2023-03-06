from flask import Flask, render_template, request, flash
from converter.currencies import Currency
from converter.convertion import Convert
from converter.config import secret_key

app = Flask(__name__)
app.config['SECRET_KEY'] = secret_key

@app.route('/')
def get_index():
    return render_template('index.html', currencies=Currency)

@app.route('/history')
def get_history():
    curr = Convert('USD')
    transactions = curr.get_transactions()
    return render_template('history.html', result=transactions)

@app.route('/convert', methods=['POST'])
def convert():
    if request.form:
        rf = request.form
        curr = Convert(rf['base-curr'])
        result = curr.exchange(float(rf['amount']),rf['to-curr'],2)
        send = {'rf':rf,'result':result}
        print(curr.get_db_rate(rf['to-curr']))
        return render_template('convert.html',currency=send)
    else:
        flash('Please fill all the fields', 'red')
        return render_template('index.html', currencies=Currency)

app.run(debug=True, host='127.0.0.1', port=3000)