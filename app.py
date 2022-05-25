
from errno import ESTALE
from logging import root
import random
from flask import Flask, redirect, session, url_for,flash
from flask import render_template, request
from flask import Response
from flaskext.mysql import MySQL
from datetime import datetime
import cv2
from numpy import number 

app = Flask(__name__)
#importacion de la data para el reconocimiento facial
cap =cv2.VideoCapture(1,cv2.CAP_DSHOW)
#haarcascade_frontalface_defaul.xml
naranja=cv2.CascadeClassifier('cascade.xml')


app.secret_key="proyecto python"
mysql = MySQL()
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'inteligencia_artificial'
mysql.init_app(app)


led=0
mot=0

#serialArduino = serial.Serial("COM6",9600) 


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

#ruta para lsitar los reportes de frutas
@app.route('/reports')
def reports():
   
    sql = "SELECT * FROM `reporte`;"
    conn = mysql.connect();
    Cursor = conn.cursor();
    Cursor.execute(sql);
    reporte = Cursor.fetchall();
    conn.commit();
    return render_template('reportes/reportes.html',reporte = reporte);

#ruta del api para insertar los registros del reconocimiento de naranjas
@app.route('/insertar-reconocimiento-fruta',methods=['POST'])
def insert_fruta():
    request_data=request.get_json()
    est=request_data['estado']
    prob=request_data['probabilidad']
    res=est+prob
    #datos para los reportes
    fecha = datetime.today().strftime('%Y/%m/%d');
    hora = datetime.today().strftime('%H:%M:%S');
    estado = est;
    descripcion='naranja';
    
    #movimiento del led cuando se detecte una naranja en mal estado
    print("Estado: "+est+" Porbabilidad: "+prob+" " );

    if est=='Naranja en Mal estado':
        #led=1
        #mot=180
        #cad = str(led) + ","+ str(mot)
        #serialArduino.write(cad.encode('ascii'))
        print("naranja mala");
        sql = "INSERT INTO `reporte` (`id_reporte`, `fecha`,`hora`, `estado`,`descripcion`,`porcentaje_aceptacion`) VALUES (NULL, %s,%s, %s,%s,%s);";
        datos = (fecha,hora,estado,descripcion,prob)
        conn = mysql.connect()
        Cursor = conn.cursor()
        Cursor.execute(sql,datos)
        conn.commit()

    elif est=='Naranja en Buen estado':
        sql = "INSERT INTO `reporte` (`id_reporte`, `fecha`,`hora`, `estado`,`descripcion`,`porcentaje_aceptacion`) VALUES (NULL, %s,%s, %s,%s,%s);";
        datos = (fecha,hora,estado,descripcion,prob)
        conn = mysql.connect()
        Cursor = conn.cursor()
        Cursor.execute(sql,datos)
        conn.commit()
        #
        

    return res+'led encendido'     
    
#ruta para renderizar la vista lista empleados
@app.route('/list')
def list():
    sql = "SELECT * FROM `empleado` where estado='A';"
    conn = mysql.connect();
    Cursor = conn.cursor();
    Cursor.execute(sql);
    empleados = Cursor.fetchall();
    print(empleados);
    conn.commit();
    return render_template('empleados/list.html', empleados=empleados );

#ruta para activar la camara del sistema
@app.route('/camera')
def camera():
    return render_template('empleados/camera.html')

#metodo para validad los datos de entrada del login
@app.route('/ingresar', methods=['POST', 'GET'])
def ingresar():
   
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
            flash('!Error. Usuario o contraseña incorrectos')
    return render_template('login/login.html')

#metodo para cerrar sesion
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
    estado = 'A';
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
    flash('!Error. Usuario o contraseña incorrectos')
    return render_template('empleados/index.html')

# funcion para Actualizar un usuario    
@app.route('/edit/<int:id>')
def editarEmpleado(id):
    conn = mysql.connect();
    Cursor = conn.cursor();
    Cursor.execute("SELECT * FROM EMPLEADO WHERE id_emp=%s",(id));
    empleado = Cursor.fetchall();
    print(empleado);
    return render_template('empleados/edit.html',empleado=empleado);
#funcion para eliminar un usuario
@app.route("/delete/<int:id>")
def eliminarUsuario(id):
    conn = mysql.connect();
    Cursor = conn.cursor();
    Cursor.execute("UPDATE empleado SET estado ='I' WHERE id_emp=%s",(id));
    empleado = Cursor.fetchall();
    conn.commit();
    return redirect('/list');

#metodo para confirmar la edicion de un numero
@app.route('/edit', methods=['POST'])
def editarEmpleados(): 
    _id = request.form['txtId'];
    nombre = request.form['txtNombre'];
    correo= request.form['txtCorreo'];
    foto = request.files['txtFoto'];
    user_name = request.form['txtUserName'];
    contrasenia= request.form['password'];
    estado = request.form['txtEstado'];
    now = datetime.now();
    tiempo = now.strftime("%Y%H%M%S");
    if foto.filename!= '':
        nuevoNombreF=tiempo+foto.filename
        foto.save("uploads/"+nuevoNombreF);  
    sql = "UPDATE EMPLEADO SET nombre=%s, correo=%s , foto=%s , user_name=%s, contrasenia=%s,estado=%s  where id_emp=%s"
    datos = (nombre,correo,nuevoNombreF,user_name,contrasenia,estado ,_id);
    conn = mysql.connect();
    Cursor = conn.cursor();
    Cursor.execute(sql,datos);
    conn.commit();
    flash('!Error. Usuario o contraseña incorrectos');
    return redirect('/list');

#funcion para generar la estrucutra del reconocimiento facial
def generate():
    while True:
        ret, frame = cap.read()
        if ret:
            gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            #faces=face_detector.detectMultiScale(gray,scaleFactor=8,minNeighbors=100,minSize=(80,80))
            objeto=naranja.detectMultiScale(gray,scaleFactor=8,minNeighbors=120,minSize=(100,100))
            
            for(x,y,w,h) in objeto:
                
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
                cv2.putText(frame,'Naranja',(x,y-20),2,0.7,(0,255,0),2,cv2.LINE_AA)
            (flag,encodedImage)=cv2.imencode(".jpg",frame)
            if not flag:
                continue
            yield(b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n'+bytearray(encodedImage)+b'\r\n')

           
#ruta para iniciar la ventana de la camara con reconocimiento
@app.route('/reconocimiento')
def reconocimiento():
   return Response(generate(),mimetype="multipart/x-mixed-replace; boundary=frame")


 # enlace para instalar open cv https://pypi.org/project/opencv-contrib-python/
 


if '__main__':
    app.run(debug=False)
    cap.release()
  
