import math

from flask import Flask, jsonify

from db import get_user_feed, get_user_feed_count, get_users_detail, get_user_detail, get_repo_detail

app = Flask(__name__)


@app.route('/api/my_feed/<user_id>/<page>')
def my_feed(user_id=None, page=None):
    if user_id is None or page is None:
        return jsonify({
            'code': -1,
            'msg': 'invali user id or page'
        })

    user_id = int(user_id)
    page = int(page)
    count = get_user_feed_count(user_id)
    limit = 1
    max_page = math.ceil(count / limit)
    if page > max_page:
        page = max_page
    offset = (page - 1) * limit

    user_feeds = get_user_feed(user_id, offset, limit)
    user_ids = list(set(uf['user_id'] for uf in user_feeds))
    users_detail_tmp = get_users_detail(user_ids)
    user_detail = {v['id']: v['name'] for v in users_detail_tmp}

    result = []
    for user_feed in user_feeds:
        uid = user_feed['user_id']
        if uid not in user_detail:
            continue

        rs = {'create_time': user_feed['create_time'],
              'user_id': uid,
              'user_name': user_detail[uid],
              'action': user_feed['action']}
        if user_feed['action'] == 'following':
            user = get_user_detail(user_feed['object_id'])
            if user is None:
                continue
            rs['event_content'] = {'following_name': user['name'], 'following_uid': user['id']}
        elif user_feed['action'] == 'fork_repo':
            repo = get_repo_detail(user_feed['object_id'])
            if repo is None:
                continue
            fork_from = repo['fork_from']
            fork_from_repo = get_repo_detail(fork_from)
            if fork_from_repo is None:
                continue
            rs['event_content'] = {'repo_name': repo['name'],
                                   'fork_from_id': fork_from_repo['id'],
                                   'fork_from_repo_name': fork_from_repo['name']}
        elif user_feed['action'] == 'create_repo':
            repo = get_repo_detail(user_feed['object_id'])
            if repo is None:
                continue
            rs['event_content'] = {'repo_name': repo['name']}
        result.append(rs)

    return jsonify({
        'code': 0,
        'msg': 'success',
        'data': result,
    })
