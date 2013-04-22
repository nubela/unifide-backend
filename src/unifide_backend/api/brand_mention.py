from flask import request, jsonify
from unifide_backend.action.social.brand_mention import register, del_keyword


def put_keyword():
    """
    (PUT: brand_mention/keyword)
    """
    kw = request.form.get("keyword")
    register(kw)
    return jsonify({
        "status": "ok"
    })


def httpdel_keyword():
    """
    (DELETE: brand_mention/keyword)
    """
    kw = request.args.get("keyword")
    del_keyword(kw)
    return jsonify({
        "status": "ok"
    })


def _register_api(app):
    """
    interface method so the app can register the API (routing) calls.
    """

    app.add_url_rule('/brand_mention/keyword/',
                     "put_keyword", put_keyword, methods=['PUT'])

    app.add_url_rule('/brand_mention/keyword/',
                     "del_keyword", httpdel_keyword, methods=['DELETE'])