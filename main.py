from flask import Flask, render_template, jsonify, request
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_cors import CORS
from models import db, Todo
import json

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['DEBUG'] = True 
app.config['ENV'] = 'development'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' 
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:picachu2171@localhost:3306/todolistft9' 
db.init_app(app)
Migrate(app, db)
CORS(app)
manager = Manager(app)
manager.add_command("db", MigrateCommand)

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/todos/username/<username>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def todos(username):
    if request.method == 'GET':
            todo = Todo.query.filter_by(username=username)
            todo = list(map(lambda todo: todo.serialize(), todo))
          
            return jsonify(todo), 200


    if request.method == 'POST':

        #Agarro la TABLA
        body = request.get_json()
        #Creo algo por DEFAULT
        body.append({"label": "defecto algo", "done": "false"})

        todo = Todo()
        todo.username = username
        #Lo transformo de PYTHON A JSON
        todo.tasks = json.dumps(body)
        todo.save()

        return jsonify({"result": "ok"}), 201  
        
    if request.method == 'PUT':
        todo = Todo.query.filter_by(username=username)
        body = request.get_json()
       
        if todo:
            todo = Todo()
            todo.tasks = json.dumps(body)
            todo.update()
            return jsonify({"result": "a list with " + str(len(body)) + " todos was successfully saved"}), 200
        else:
            return jsonify({"msg": "User not found"}), 404    

        return jsonify(), 201 
        
    if request.method == 'DELETE':
        todo = Todo.query.filter_by(username=username).first()
        todo.delete()
        return jsonify({"success": "Deleted Complete"}),200
        if not todo:
            return jsonify({"msg": "user not found"}), 404

if __name__ == '__main__':
    manager.run()