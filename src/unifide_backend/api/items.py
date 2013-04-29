from flask import request, json, jsonify, redirect
from base import items
from base.items import ItemStatus, Item, container_path
from base.items.action import container_from_path
from base.media.action import save_image, save_media
from cfg import UPLOAD_METHOD


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


def put_item():
    """
    (PUT: item)
    """
    #attributes
    path_lis_json = request.form.get("path_lis", None)
    path_lis = json.loads(path_lis_json) if path_lis_json is not None else None
    container_obj = container_from_path(container_path(path_lis))
    name = request.form.get("name")
    description = request.form.get("description")
    price = request.form.get("price", None)
    quantity = request.form.get("quantity", None)
    status = request.form.get("status", ItemStatus.VISIBLE)
    extra_json = request.form.get("extra_attributes", None)
    extra_attr = json.loads(extra_json) if extra_json is not None else None

    #files
    media_file = request.files.get("media_file")

    #others
    redirect_url = request.form.get("redirect_to", None)

    #save media
    if request.files.get("media_file").mimetype in ["image/png", "image/gif", "image/jpeg", "image/jpg"]:
        media_obj = save_image(media_file, UPLOAD_METHOD)
    else:
        media_obj = save_media(media_file, UPLOAD_METHOD)

    #create item obj
    item_obj = Item()
    item_obj.name = name
    item_obj.description = description
    item_obj.quantity = quantity
    item_obj.price = price
    item_obj.container_id = container_obj.obj_id()
    item_obj.status = status
    item_obj.media_id = media_obj.obj_id()
    if extra_attr is not None:
        for k, v in extra_attr.items():
            setattr(item_obj, k, v)

    #save it
    Item.collection().save(item_obj.serialize())

    if redirect_url is not None:
        return redirect(redirect_url)
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

    app.add_url_rule('/item/',
                     "put_item", put_item, methods=['PUT', 'POST'])