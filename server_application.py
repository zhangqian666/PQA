# -*- coding: utf-8 -*-

"""
@author: zhangqian

@contact: 

@Created on: 2020-07-31 07:55
"""

from flask import Flask, render_template, request
from main import handle_question

app = Flask(__name__)


@app.route('/', methods=["GET"])
def index():
    return render_template("index.html")


@app.route('/question', methods=["POST", "GET"])
def get_question():
    question = request.values.get("message")
    result_answer = handle_question(question)
    result_data = {"data": "查询成功： {}".format(result_answer)}
    return result_data


if __name__ == '__main__':
    app.run(debug=True, port=8777)
