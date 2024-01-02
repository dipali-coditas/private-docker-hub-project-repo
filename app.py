from pymongo import MongoClient
import datetime
from bson import ObjectId
from flask import Flask, jsonify, request, redirect, render_template

uri = 'mongodb+srv://bbt0987:BBT0987@cluster0.jcazi2w.mongodb.net/?retryWrites=true&w=majority'
client = MongoClient(uri)

db = client.get_database('userdb')
table = db.get_collection('Todo')

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        data = {
            "title": request.form['title'],
            "desc": request.form['desc'],
            "created_date": datetime.datetime.now().strftime("%d-%m-%Y %I:%M:%S"),
        }
        table.insert_one(data)
        return redirect('/')
    else:
        all_data = list(table.find())
        return render_template('index.html', all_data=all_data)

@app.route('/delete', methods=['POST'])
def delete_data():
    try:
        data_id = request.form['data_id']
        table.delete_one({"_id": ObjectId(data_id)})
        return redirect('/')
    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True, port=8000)
