
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

#ruta para renderizar la vista del login
@app.route('/')
def login():
    return render_template('login/login.html');

#ruta para renderizar la vista crear empleados
@app.route('/create')
def create():
    return render_template('empleados/create.html');

#ruta para renderizar la vista lista empleados
@app.route('/list')
def list():
    return render_template('empleados/list.html');

#ruta para activar la camara del sistema
@app.route('/camara')
def camara():
    return render_template('empleados/camara');

#metodo para validad los datos de entrada del login
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

#metodo para 
@app.route('/logout')
def logout():
    session.pop('loggedin',None)
    session.pop('username',None)
    return redirect(url_for('login'))


#fucniona para crear un nuevo usuario
@app.route('/store', methods=['POST'])
def storage():
    nombre = request.form['txtNombre'];
    correo= request.form['txtCorreo'];
    foto = request.files['txtFoto'];
    user_name = request.form['txtUserName'];
    password = request.form['password'];
    estado = 'activo';

    now = datetime.now();
    tiempo = now.strftime("%Y%H%M%S");
    if foto.filename!= '':
        nuevoNombreF=tiempo+foto.filename
        foto.save("uploads/"+nuevoNombreF); 
        
    sql = "INSERT INTO `empleado` (`id_emp`, `nombre`, `correo`, `foto`, `user_name`, `contrasenia`, `estado`) VALUES (NULL, %s, %s, %s,%s,%s,%s);"
    datos = (nombre,correo,nuevoNombreF,user_name,password,estado)
    conn = mysql.connect()
    Cursor = conn.cursor()
    Cursor.execute(sql,datos)
    conn.commit()
    return render_template('empleados/index.html')

# funcion para Actualizar un usuario    

@app.route('/edit/<int:id>')
def editarEmpleado(id):
    conn = mysql.connect();
    Cursor = conn.cursor();
    Cursor.execute("SELECT * FROM EMPLEADOS WHERE id=%s",(id));
    empleado = Cursor.fetchall();
    print(empleado);
    return render_template('empleados/edit.html',empleado=empleado);




if '__main__':
    app.run(debug=True)
