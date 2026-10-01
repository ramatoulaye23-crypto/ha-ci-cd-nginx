from flask import Flask, render_template, request, redirect, url_for, session
from functools import wraps

app = Flask(__name__)
app.secret_key = 'cle-secrete-projet-ha'

USERS = {"admin": "admin123"}
emplois_du_temps = []
next_id = 1

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if USERS.get(username) == password:
            session['user'] = username
            return redirect(url_for('dashboard'))
        error = 'Identifiants invalides'
    return render_template('login.html', error=error)

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    global next_id
    if request.method == 'POST':
        cours = {'id': next_id, 'matiere': request.form.get('matiere'), 'jour': request.form.get('jour'), 'heure': request.form.get('heure')}
        emplois_du_temps.append(cours)
        next_id += 1
    return render_template('dashboard.html', emplois=emplois_du_temps, user=session['user'])

@app.route('/supprimer/<int:id>')
@login_required
def supprimer(id):
    global emplois_du_temps
    emplois_du_temps = [c for c in emplois_du_temps if c['id'] != id]
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
