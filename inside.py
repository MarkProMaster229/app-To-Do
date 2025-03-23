from flask import Flask, render_template, request
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    test = None

    test = request.form.get('inputField')

    return render_template('index.html', post=test)

if __name__ == '__main__':
    app.run(debug=True)
