from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///licenses.db'
db = SQLAlchemy(app)
admin = Admin(app, name='License Admin', template_mode='bootstrap3')

# Model definition for licenses
class License(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    license_key = db.Column(db.String(80))
    status = db.Column(db.String(20))

db.create_all()
admin.add_view(ModelView(License, db.session))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
