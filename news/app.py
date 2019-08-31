from flask import Flask, render_template, abort
import os
import json
from flask_sqlalchemy import SQLAlchemy
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)
app.config['TEMPLATE_AUTO_RELOAD'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/louweb'
db = SQLAlchemy(app)
client = MongoClient('127.0.0.1', 27017)
mgdb = client.shiyanlou

class File(db.Model):
    __tablename__ = 'file'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    created_time = db.Column(db.DateTime, nullable=False, default=datetime.now)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.relationship('Category', 
               backref=db.backref('file', lazy=True))
    
    def __init__(self, title, created_time, category, content):
        self.title = title
        self.created_time = created_time
        self.category = category
        self.content = content

    def add_tag(self, tag_name):
        mytag = mgdb.tag.find_one({'id': self.id})
        if mytag:
            if tag_name not in mytag['tag']:
                mytags = mytag['tag']
                mytags.append(tag_name)
                mgdb.tag.update({'id': self.id}, {'$set': {'tag': mytags}})
        else:
            mgdb.tag.insert_one({'id': self.id, 'tag': [tag_name]})
    
    def remove_tag(self, tag_name):
        mytag = mgdb.tag.find_one({'id': self.id})
        if mytag:
            if tag_name in mytag['tag']:
                mytags = mytag['tag']
                mytags.pop(tag_name)
                mgdb.tag.update({'id': self.id}, {'$set': {'tag': mytags}})

    @property
    def tags(self):
        mytag = mgdb.tag.find_one({'id': self.id})
        return mytag['tag']

    def __repr__(self):
        return '<File(title={})>'.format(self.title)
class Category(db.Model):
    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Category(name={})>'.format(self.name)

def inset_data():
    java = Category('Java')
    python = Category('Python')
    file1 = File('Hello Java', datetime.utcnow(), java, 'File Content - Java is cool!')
    file2 = File('Hello Python', datetime.utcnow(), python, 'File Content - Python is cool!')
    db.session.add(java)
    db.session.add(python)
    db.session.add(file1)
    db.session.add(file2)
    db.session.commit()

    file1.add_tag('tech')
    file1.add_tag('java')
    file1.add_tag('linux')
    file2.add_tag('tech')
    file2.add_tag('python')

@app.route('/')
def index():
    file_list = db.engine.execute('select id, title from file').fetchall()
    tagdb = mgdb.tag
    return render_template('index.html', file_list=file_list, tagdb=tagdb)

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
