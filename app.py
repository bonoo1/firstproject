from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from flask import redirect
from datetime import datetime

client = MongoClient('mongodb+srv://test:sparta@cluster0.7tst7.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta

app = Flask(__name__)


@app.route('/')
def main():
    return render_template('index.html')


@app.route('/new-review')
def create():
    return render_template('new_review.html')


@app.route("/new-reviews", methods=["POST"])
def reviews_create():

    name_receive = request.form['name_give']
    comment_receive = request.form['comment_give']
    vaccine_receive = request.form['vaccine_give']
    number_receive = request.form['number_give']
    time_receive = request.form['time_give']

    doc = {
        'name': name_receive,
        'comment': comment_receive,
        'vaccine': vaccine_receive,
        'number': number_receive,
        'time': time_receive

    }
    db.vaccines.insert_one(doc)

    return jsonify({'msg': '작성완료'})


@app.route('/api/reviews', methods=['GET'])
def index():
    vaccine = request.args.get('vaccine', "")
    degree = request.args.get('degree', "")
    page = int(request.args.get('page', 1))

    options = {}

    if len(vaccine) > 0 and len(degree) > 0:
        options['vaccine'] = vaccine
        options['degree'] = degree
    elif len(vaccine) > 0:
        options['vaccine'] = vaccine
    elif len(degree) > 0:
        options['degree'] = degree

    review_list = list(db.vaccines.find(options).limit(9).skip((page - 1) * 9).sort('date', -1))

    results = []

    for document in review_list:
        results.append(document)

    return jsonify({'reviews': results})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

