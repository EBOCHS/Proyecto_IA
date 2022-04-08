
from flask import Flask, redirect, session, url_for
from flask import render_template, request
from flaskext.mysql import MySQL
from datetime import datetime


app = Flask(__name__)
app.secret_key="proyecto python"
mysql = MySQL()
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'inteligencia_artificial'
mysql.init_app(app)


@app.route('/dashboard')
def dash():
    return render_template('empleados/index.html',username=session['username'])


@app.route('/')
def login():
    return render_template('login/login.html')


@app.route('/create')
def create():
    return render_template('empleados/create.html')

@app.route('/list')
def list():
    return render_template('empleados/list.html')



@app.route('/store', methods=['POST'])
def storage():
    _nombre = request.form['txtNombre']
    _correo = request.form['txtCorreo']
    _foto = request.files['txtFoto']
    now = datetime.now()
    tiempo = now.strftime("%Y%H%M%S")
    if _foto.filename != '':
        nuevoNombre = tiempo+_foto.filename
        _foto.save("uploads/"+nuevoNombre)

    sql = "INSERT INTO `empleado` (`id`, `nombre`, `correo`, `foto`) VALUES (NULL,%s,%s,%s);"
    datos = (_nombre, _correo, nuevoNombre)
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, datos)
    conn.commit()
    return render_template('empleados/index.html')


@app.route('/ingresar', methods=['POST', 'GET'])
def ingresar():
    msg = ''

    if request.method == 'POST':
        user = request.form['txtUsuario']
        password = request.form['txtPass']
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM empleado where user_name=%s AND contrasenia=%s', (user, password))
        record = cursor.fetchone()
        if record:
            session['loggedin'] = True
            session['username'] = record[1]
            return redirect(url_for('dash'))
        else:
            msg = '¡Contraseña/Usuario Incorrecto, Intente de Nuevo!'
    return render_template('login/login.html', msg=msg )

@app.route('/logout')
def logout():
    session.pop('loggedin',None)
    session.pop('username',None)
    return redirect(url_for('login'))

if '__main__':
    app.run(debug=True)
