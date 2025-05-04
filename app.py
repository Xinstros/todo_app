from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/add', methods=['POST'])
def add_task():
    task = request.form['task']
    print(f"Task added: {task}")  # Will print to console; database later
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)