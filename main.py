from flask import Flask, redirect, url_for, request

app = Flask(__name__)


@app.route('/success/<p1>')
def one_param_check(p1):
    return '%s' % p1


@app.route('/success/<p1>/<p2>')
def two_param_check(p1, p2):
    return '%s %s' % (p1, p2)


@app.route('/login', methods=['GET'])
def login():
    user = request.args.get('uname')
    pwd = request.args.get('pwd')
    return redirect(url_for('two_param_check', p1=user, p2=pwd))


@app.route('/logout', methods=['GET'])
def logout():
    user = request.args.get('uname')
    return redirect(url_for('one_param_check', p1=user))


@app.route('/registration', methods=['POST'])
def registration():
    user = request.args.get('uname')
    pwd = request.args.get('pwd')
    return redirect(url_for('two_param_check', p1=user, p2=pwd))


@app.route('/create_store', methods=['POST'])
def create_store():
    user = request.args.get('uname')
    store = request.args.get('sname')
    return redirect(url_for('two_param_check', p1=user, p2=store))


@app.route('/remove_store', methods=['POST'])
def remove_store():
    user = request.args.get('uname')
    store = request.args.get('sname')
    return redirect(url_for('two_param_check', p1=user, p2=store))


@app.route('/track_store', methods=['POST'])
def track_store():
    store = request.args.get('sname')
    return redirect(url_for('one_param_check', p1=store))


if __name__ == '__main__':
    app.run(debug=True)
