from flask import Flask
from flask import request
from flask import json

from data.data import *
from modules.hierarchy_analyze.hierarchy_analyze import HierarchyAnalyze

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['CORS_HEADERS'] = 'Content-Type'


response = app.response_class(
    status=200,
    content_type='application/json; charset=utf8',
)
response.headers.add("Access-Control-Allow-Origin", "*")
response.headers.add('Access-Control-Allow-Headers', "*")
response.headers.add('Access-Control-Allow-Methods', "*")


@app.route('/<method>')
def get_result(method):
    body = HierarchyAnalyze.get_result(example, example_prefers_table, method)

    response.response = json.dumps(body)

    return response
    # return 'Hello world'


if __name__ == '__main__':
    app.run()
# if __name__ == '__main__':
#     print(HierarchyAnalyze.get_result(example, example_prefers_table))
