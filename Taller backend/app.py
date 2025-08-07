#Importar flask
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

#creamos la instalacion del flask
app = Flask(__name__)

#Configurar nuestra aplicacion para crear nuestro modelo de db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tareas.db'

app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

db = SQLAlchemy(app)

class Tarea(db.Model):
    #columna identificador unico
    id = db.Column (db.Integer, primary_key = True)
    #columna de titulo
    titulo = db.Column(db.String(100), nullable = True)
    #columna de prioridad
    prioridad = db.Column(db.String(100), nullable = True)
    #columna para las fechas
    fecha_inicio = db.Column(db.String(100), nullable = True)
    fecha_fin = db.Column(db.String(100), nullable = True)
    #columna para el estado
    estado = db.Column(db.String(100), nullable = True)

with app.app_context():
    db.create_all()#crear todas las tablas definidas


@app.route('/', methods=['GET'])
def home():
    #consultar la base de datos
    tareas = Tarea.query.all()
    return render_template('index.html', tarea=tareas)

@app.route('/tarea', methods=['POST'])
def manejar_tarea():

    accion = request.form.get('accion')
    tarea_id = request.form.get('id')

    if accion == 'agregar':
        nueva = Tarea(
            titulo= request.form.get('titulo'),
            descripcion= request.form.get('descripcion'),
            fecha_inicio= request.form.get('fecha_inicio'),
            fecha_limite= request.form.get('fecha_limite'),
        )
        db.session.add(nueva)
        db.session.commit()

        #si la operacion es editar
    elif accion == 'editar' and tarea_id:
        #buscar la tarea poe su id en la base de datos
        tarea = Tarea.query.get(tarea_id)

        tareas = Tarea.query.all()

        return render_template('index.html', tarea = tareas, tarea_editando=tarea)
    
    elif accion == 'actualizar' and tarea_id:

        tarea = Tarea.query.get(tarea_id)

        #si la tarea existe actualizamos con nuevos datos

        if tarea:
            tarea.titulo = request.form.get('titulo')
            tarea.descripcion = request.form.get('descripcion')
            tarea.prioridad = request.form.get('prioridad')
            tarea.fecha_inicio = request.form.get('fecha_inicio')
            tarea.fecha_limite = request.form.get('fecha_limite')
            tarea.estado = request.form.get('estado')

            db.session.commit()

            #si la opcion es eliminar
        elif accion == 'eliminar' and tarea_id:

            #buscar la tarea que queremos borrar
            tarea = Tarea.query.get(tarea_id)

            #si la tarea ya existe, marcar para borrar
            if tarea:
                db.session.delete(tarea)

                #confirmar para eliminar de la base de datos
                db.session.commit()
                

if __name__== "__main__":
    app.run()
