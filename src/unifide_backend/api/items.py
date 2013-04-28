from flask import request, json, jsonify
from base import items


def get_containers_and_items():
    """
    (GET: container+item)

    Fetches the immediate child containers of a path, as well as the items in the specified container.
    """
    path_lis_json_str = request.args.get("path_lis")
    path_lis = json.loads(path_lis_json_str) if path_lis_json_str is not None else None
    container_obj = items.container_from_path(path_lis)
    all_items = items.get_all(container_obj)
    all_child_containers = items.child_containers(container_obj)
    return jsonify({
        "status": "ok",
        "items": [x.serialize(json_friendly=True) for x in all_items],
        "child_containers": [x.serialize(json_friendly=True) for x in all_child_containers]
    })


def put_container():
    """
    (PUT: container)
    """
    path_lis_json = request.form.get("path_lis")
    path_lis = json.loads(path_lis_json)
    items.save_container_path(path_lis)
    return jsonify({
        "status": "ok",
    })


def _register_api(app):
    """
    interface method so the app can register the API (routing) calls.
    """

    app.add_url_rule('/container+item/',
                     "get_containers_and_items", get_containers_and_items, methods=['GET'])

    app.add_url_rule('/container/',
                     "put_container", put_container, methods=['PUT'])