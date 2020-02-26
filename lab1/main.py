from flask import Flask
from flask import request
from flask import json

from lab1.modules.shifted_ideal_method import *
from lab1.modules.permutations_method import *
from lab1.data import *


app = Flask(__name__)


@app.route('/shifted_ideal')
def shifted_ideal():
    body = ShiftedIdeal.get_result(example)

    response = app.response_class(
        response=json.dumps(body),
        status=200,
        content_type='application/json; charset=utf8'
    )

    return response


@app.route('/permutations')
def permutations():
    body = Permutations.get_result(example)

    response = app.response_class(
        response=json.dumps(body),
        status=200,
        content_type='application/json; charset=utf8'
    )

    return response


if __name__ == '__main__':
    app.run()