from flask import Flask, make_response, current_app, request, jsonify

from geoseeq.plotting.plot_editor import _make_highcharts_config

from geoseeq import Knex
from geoseeq.cli.shared_params.config import load_profile
from geoseeq.blob_constructors import project_from_uuid

app = Flask(__name__)


@app.route("/<proj_uuid>/<col_x>", methods=['GET'])
def hello_world(proj_uuid, col_x):
    endpoint, token = load_profile('dev')
    knex = Knex(endpoint)
    knex.add_api_token(token)
    proj = project_from_uuid(knex, proj_uuid)
    col_y = request.args.get('col_y', None)
    col_color = request.args.get('col_color', None)
    config = _make_highcharts_config(
        proj.get_sample_metadata(),
        col_x,
        col_y=col_y,
        col_color=col_color
    ).to_dict()
    out = {
        'config': config,
    }
    print(out)
    response = jsonify(out)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
