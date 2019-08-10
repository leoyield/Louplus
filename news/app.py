from flask import Flask, render_template, abort
import os
import json

app = Flask(__name__)
app.config['TEMPLATE_AUTO_RELOAD'] = True

@app.route('/')
def index():
    dir_path = os.path.abspath('../files')
    dir_list = os.listdir('../files')
    file_list = []
    for i in dir_list:
        if os.path.isfile(os.path.join(dir_path, i)):
            file_list.append(os.path.splitext(i)[0])
            print(file_list)
    return render_template('index.html', file_list=file_list)

@app.route('/files/<filename>')
def file(filename):
    dir_path = os.path.abspath('../files')
    dir_list = os.listdir(dir_path)
    filename = filename + '.json'
    if filename in dir_list:
        with open(os.path.join(dir_path, filename)) as f:
            data = json.load(f)
        return render_template('file.html', data=data)
    else:
        abort(404)
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404
