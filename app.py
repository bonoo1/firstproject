from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from flask import redirect

client = MongoClient('mongodb+srv://test:sparta@cluster0.7tst7.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta

app = Flask(__name__)


@app.route('/')
def main():
    return render_template('main.html')


@app.route('/create')
def create():
    return render_template('create.html')


@app.route("/reviews", methods=["POST"])
def reviews_create():
    name_receive = request.form['name_give']
    comment_receive = request.form['comment_give']
    vaccine_receive = request.form['vaccine_give']
    number_receive = request.form['number_give']

    doc = {
        'name': name_receive,
        'comment': comment_receive,
        'vaccine': vaccine_receive,
        'number': number_receive
    }
    db.vaccines.insert_one(doc)

    return jsonify({'msg': '저장 완료!'})


@app.route("/reviews", methods=["GET"])
def reviews():
    vaccine_list = list(db.vaccines.find({}, {'_id': False}))
    return jsonify({'list': vaccine_list})

@app.route("/reviews")
def board_create():
    return render_template('create.html')

@app.route("/")
def board_cancle():
    return render_template('main.html')



if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
