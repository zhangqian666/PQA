# -*- coding: utf-8 -*-

"""
@author: zhangqian

@contact: 

@Created on: 2020-07-31 07:55
"""

from flask import Flask, render_template, request


app = Flask(__name__)


@app.route('/', methods=["GET"])
def index():
    return render_template("index.html")


@app.route('/question', methods=["POST", "GET"])
def get_question():
    question = request.values.get("message")
    # relationModel = RelationModel()
    # result_answer = relationModel.Other_simple_parse(question)
    result_data = {"data": "查询成功： {}".format(question)}
    return result_data


if __name__ == '__main__':
    app.run(debug=True, port=8777)