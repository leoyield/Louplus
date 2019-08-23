from flask import Flask, render_template, abort
import os
import json
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['TEMPLATE_AUTO_RELOAD'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/louweb'
db = SQLAlchemy(app)

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    created_time = db.Column(db.DateTime, nullable=False, default=datetime.now)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.relationship('Category', 
               backref=db.backref('file', lazy=True))

    def __repr__(self):
        return '<File(title={})>'.format(self.title)
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    def __repr__(self):
        return '<Category(name={})>'.format(self.name)

@app.route('/')
def index():
    file_list = db.engine.execute('select id, title from file').fetchall()
    return render_template('index.html', file_list=file_list)

@app.route('/files/<file_id>')
def file(file_id):
    file_id = (int(file_id),)
    all_id = db.engine.execute('select id from file').fetchall()
    print('all_id:',all_id)
    print('file_id:',file_id)
    if file_id in all_id:
        data = db.engine.execute('select * from file where id = {}'.format(file_id[0])).fetchall()
        name = db.engine.execute(
                'select name from category where id = {}'.format(
                    data[0][3])).fetchall()[0]
        return render_template('file.html', data=data, name=name)
    else:
        abort(404)
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404
