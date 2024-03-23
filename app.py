from datetime import datetime
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

client = MongoClient('mongodb+srv://ricolaa02:fg6swfzg7m@cluster0.cysbprr.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client.dbbucketrico

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