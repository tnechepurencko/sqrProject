from flask import Flask, redirect, url_for, request

app = Flask(__name__)


@app.route('/success/<name>')
def name_check(name):
    return 'welcome %s' % name


@app.route('/success/<name>/<pwd>')
def name_pwd_check(name, pwd):
    return 'welcome %s %s' % (name, pwd)


@app.route('/login', methods=['GET'])
def login():
    user = request.args.get('uname')
    pwd = request.args.get('pwd')
    return redirect(url_for('name_pwd_check', name=user, pwd=pwd))


@app.route('/logout', methods=['GET'])
def logout():
    user = request.args.get('uname')
    return redirect(url_for('name_check', name=user))


@app.route('/registration', methods=['POST'])
def registration():
    user = request.args.get('uname')
    pwd = request.args.get('pwd')
    return redirect(url_for('name_pwd_check', name=user, pwd=pwd))


if __name__ == '__main__':
    app.run(debug=True)
