from flask import Flask, jsonify, request
from flask_pymongo import PyMongo


app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'author_db'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/author_db'

mongo = PyMongo(app)

@app.route('/author/search/all', methods=['GET'])
def get_all_authors():
    db = mongo.db.author_db
    output = []
    for q in db.find():
        output.append({'username' : q['username'], 'name' : q['name'], 'projects' : q['projects']})
    return jsonify({'result' : output})

@app.route('/author/<username>', methods=['GET'])
def get_author(username):
    db = mongo.db.author_db
    q = db.find_one({'username' : username})
    if q:
        output = {'username' : q['username'], 'name' : q['name'], 'projects' : q['projects']}
    else:
        output = 'No results found'
    return jsonify({'result' : output})

@app.route('/author/create', methods=['POST'])
def create_author():
    db = mongo.db.author_db 
    username = request.json['username']
    name = request.json['name']
    projects = request.json['projects']
    q = db.find_one({'username' : username})
    if q:
        output = 'Author already exists'
    else:    
        author_id = db.insert_one({'username' : username, 'name' : name, 'projects' : projects}).inserted_id
        new_author = db.find_one({'_id' : author_id})
        output = {'username' : new_author['username'], 'name' : new_author['name'],  'projects' : new_author['projects']}
        return jsonify({'result' : output})

@app.route('/author/<username>', methods=['DELETE'])
def delete_author(username):
    db = mongo.db.author_db
    output = db.delete_one({'username' : username}).acknowledged
    return jsonify({'result' : output})
    
@app.route('/author/<username>/addProject', methods=['PATCH'])
def add_project(username):
    db = mongo.db.author_db
    project = request.json['project']
    output = db.update_one({'username': username}, {'$push': {'projects': project}}).acknowledged
    return jsonify({'result' : output})

@app.route('/author/<username>/removeProject', methods=['PATCH'])
def add_project(username):
    db = mongo.db.author_db
    project = request.json['project']
    output = db.update_one({'username': username}, {'$pull': {'projects': project}}).acknowledged
    return jsonify({'result' : output})


    
if __name__ == '__main__':
    app.run(debug=True)