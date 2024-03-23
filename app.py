import os
from os.path import join, dirname
from dotenv import load_dotenv
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME =  os.environ.get("DB_NAME")

client = MongoClient(MONGODB_URI)
db = client[DB_NAME]

app = Flask(__name__)

@app.route('/')
def home():
   return render_template('index.html')

@app.route("/bucket", methods=["POST"])
def bucket_post():
    bucket_receive = request.form["bucket_give"]
    count = db.bucket.count_documents({})
    current_time = datetime.now()
    num = count + 1
    doc = {
        'num':num,
        'bucket': bucket_receive,
        'done':0,
        'created_at': current_time,
        'updated_at': current_time
    }
    db.bucket.insert_one(doc)
    return jsonify({'msg':'Data Saved!'})

@app.route("/bucket/done", methods=["POST"])
def bucket_done():
    num_receive = request.form["num_give"]
    current_time = datetime.now()
    db.bucket.update_one(
        {'num': int(num_receive)},
        {'$set': {'done': 1, 'updated_at': current_time}}
    )
    return jsonify({'msg': 'Update Done!'})

@app.route("/bucket", methods=["GET"])
def bucket_get():
    buckets_list = list(db.bucket.find({},{'_id':False}))
    return jsonify({'buckets':buckets_list})

@app.route("/bucket/delete", methods=["POST"])
def bucket_delete():
    num_receive = request.form["num_give"]
    db.bucket.delete_one({'num': int(num_receive)})
    return jsonify({'msg': 'Data Deleted Duccessfully'})


if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)