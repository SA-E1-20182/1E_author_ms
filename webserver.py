from flask import Flask, jsonify, request
from flask_pymongo import PyMongo


app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'authors_db'
app.config['MONGO_URI'] = 'mongodb://lala:lalala123@ds141209.mlab.com:41209/authors_db'
#app.config['MONGO_URI'] = 'mongodb://192.168.99.101:27018/authors_db'

mongo = PyMongo(app)
db = mongo.db.authors_db

@app.route('/author/search/all', methods=['GET'])
def get_all_authors():
    output = []
    for q in db.find():
        output.append({'username' : q['username'], 'name' : q['name'], 'projects' : q['projects']})
    return jsonify({'result' : output})

@app.route('/author/<username>', methods=['GET'])
def get_author(username):
    q = db.find_one({'username' : username})
    if q:
        output = {'username' : q['username'], 'name' : q['name'], 'projects' : q['projects']}
    else:
        output = 'No results found'
    return jsonify({'result' : output})

@app.route('/author/create', methods=['POST'])
def create_author():
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
    output = db.delete_one({'username' : username}).acknowledged
    return jsonify({'result' : output})
    
@app.route('/author/<username>/addProject', methods=['PATCH'])
def add_project(username):
    project = request.json['project']
    output = db.update_one({'username': username}, {'$push': {'projects': project}}).acknowledged
    return jsonify({'result' : output})

@app.route('/author/<username>/removeProject', methods=['PATCH'])
def remove_project(username):
    project = request.json['project']
    output = db.update_one({'username': username}, {'$pull': {'projects': project}}).acknowledged
    return jsonify({'result' : output})



if __name__ == '__main__':
    ldap_server="35.247.37.179"
    username="jdnietov"
    password="contrasena"

    app.run(host='0.0.0.0', port=7999)
    app.run(debug=True)