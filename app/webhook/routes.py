from flask import Blueprint, request, render_template
from datetime import datetime
from .. import extensions
import json

webhook = Blueprint('Webhook', __name__, url_prefix='/webhook')


@webhook.route('/')
def userview():
    data = extensions.get_main()
    return render_template('ui.html', data=extensions.format_data(data))


@webhook.route('/api', methods=['POST'])
def cur_api():
    timestamp = request.json['timestamp']
    datalist = extensions.get_after_time(timestamp)
    data = extensions.format_data(datalist)
    return json.dumps(data)


@webhook.route('/push', methods=["POST"])
def push():
    info = request.json
    if len(info['commits']) > 1:
        print("This is a Merge Push")
        return {}, 200
    data = {
        'request_id': info['head_commit']['id'],
        'timestamp': datetime.fromisoformat(info['head_commit']['timestamp']),
        'author': info['head_commit']['author']['username'],
        'from_branch': None,
        'to_branch': info['ref'].split('/', 2)[2],
        'action': "PUSH"
    }
    extensions.store_data(data)
    return {}, 200


@webhook.route('/pull', methods=["POST"])
def pull_request():
    info = request.json
    if info['action'] == 'opened':
        data = {
            'request_id': str(info['pull_request']['id']),
            'timestamp': datetime.fromisoformat(info['pull_request']['created_at'][:-1]),
            'author': info['sender']['login'],
            'from_branch': info['pull_request']['head']['ref'],
            'to_branch': info['pull_request']['base']['ref'],
            'action': "PULL_REQUEST",
        }
        extensions.store_data(data)
        return {}, 200
    elif info['action'] == 'closed' and info['pull_request']['merged'] == True:
        data = {
            'request_id': info['pull_request']['merge_commit_sha'],
            'timestamp': datetime.fromisoformat(info['pull_request']['merged_at'][:-1]),
            'author': info['pull_request']['merged_by']['login'],
            'from_branch': info['pull_request']['head']['ref'],
            'to_branch': info['pull_request']['base']['ref'],
            'action': "MERGE",
        }
        extensions.store_data(data)
        return {}, 200
    else:
        return {}, 200
