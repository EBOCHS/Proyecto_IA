from flask import Flask
from flask import render_template,request
from flaskext.mysql import MySQL
from datetime import datetime

app = Flask(__name__)

mysql=MySQL()
app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_DB']='sistema'
mysql.init_app(app)

@app.route('/')
def index():
    return render_template('empleados/index.html')

@app.route('/create')
def create():
    return render_template('empleados/create.html')

@app.route('/store', methods=['POST'])
def storage():
    _nombre=request.form['txtNombre']
    _correo=request.form['txtCorreo']
    _foto=request.files['txtFoto']
    now=datetime.now()
    tiempo=now.strftime("%Y%H%M%S")
    if _foto.filename!='':
        nuevoNombre=tiempo+_foto.filename
        _foto.save("uploads/"+nuevoNombre)

    sql="INSERT INTO `empleado` (`id`, `nombre`, `correo`, `foto`) VALUES (NULL,%s,%s,%s);"
    datos=(_nombre,_correo,nuevoNombre)
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql,datos)
    conn.commit()  
    return render_template('empleados/index.html')

if '__main__':
    app.run(debug=True)

