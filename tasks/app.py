from flask import Flask
from modelos import User, Task, db
from os import environ

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tutorial_canciones.db'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@flask_db:5432/flask_database'
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

if __name__ == '__main__':
    app.run(port=5001)
    
    

        
    
        
       