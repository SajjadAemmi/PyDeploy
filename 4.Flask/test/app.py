from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    x = request.form['number']
    return redirect(url_for('result', number=x))

@app.route('/result')
def result():
    number = request.args.get('number')
    return render_template('result.html', number=number)

if __name__ == '__main__':
    app.run(debug=True)
