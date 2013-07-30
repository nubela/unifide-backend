from flask import request, json, jsonify, redirect
from base import items, tags
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
        "description": container_obj.description if container_obj is not None else None,
        "items": [x.serialize(json_friendly=True) for x in all_items],
        "child_containers": [x.serialize(json_friendly=True) for x in all_child_containers]
    })


def put_container():
    """
    (PUT: container)
    """
    path_lis_json = request.form.get("path_lis")
    description = request.form.get("description", None)
    path_lis = json.loads(path_lis_json)
    container_obj = items.save_container_path(path_lis)
    container_obj.description = description
    items.save_container(container_obj)
    return jsonify({
        "status": "ok",
    })


def new_item(container_obj, custom_attr, custom_media, custom_tags, description, file_media_map, media_obj, name, price,
             quantity, status):
    item_obj = Item()
    item_obj.name = name
    item_obj.description = description
    item_obj.quantity = quantity
    item_obj.price = price
    item_obj.container_id = container_obj.obj_id()
    item_obj.status = status
    item_obj.custom_attr_lis = custom_attr
    item_obj.custom_media_lis = custom_media
    item_obj.media_id = media_obj.obj_id() if request.files.get("media_file").filename != "" else None
    for k, v in file_media_map.items():
        if k == "media_file": continue
        if hasattr(item_obj, k): continue
        setattr(item_obj, k, v.obj_id() if v is not None else None)
    for k in custom_attr:
        if hasattr(item_obj, k): continue
        setattr(item_obj, k, request.form.get(k, None))

    #save it
    item_obj._id = items.save(item_obj)

    #tag it
    for tag_name in custom_tags:
        tags.tag(item_obj, tag_name)


def update_item(custom_attr, custom_media, custom_tags, description, file_media_map, name, obj_id, price, quantity):
    item_obj = items.get(obj_id)
    item_obj.name = name
    item_obj.description = description
    item_obj.price = price
    item_obj.quantity = quantity
    item_obj.custom_attr_lis = custom_attr
    item_obj.custom_media_lis = custom_media
    if request.files.get("media_file").filename != "":
        item_obj.media_id = file_media_map["media_file"].obj_id()
    for k, v in file_media_map.items():
        if k == "media_file": continue
        if v is not None:
            setattr(item_obj, k, v.obj_id())
    for k in custom_attr:
        setattr(item_obj, k, request.form.get(k, None))
    items.save(item_obj)
    #remove all tags
    tags.clear(item_obj)
    #tag it
    print custom_tags
    for tag_name in custom_tags:
        tags.tag(item_obj, tag_name)


def put_item():
    """
    (PUT: item)
    """
    #attributes
    obj_id = request.form.get("id", None)
    path_lis_json = request.form.get("path_lis", None)
    path_lis = json.loads(path_lis_json) if path_lis_json is not None and path_lis_json != "" else None
    container_obj = container_from_path(container_path(path_lis))
    name = request.form.get("name")
    description = request.form.get("description")
    price = request.form.get("price", None)
    quantity = request.form.get("quantity", None)
    status = request.form.get("status", ItemStatus.VISIBLE)
    redirect_url = request.form.get("redirect_to", None)

    #extras
    custom_attr_json = request.form.get("custom_attr_lis", None)
    custom_attr = json.loads(custom_attr_json) if custom_attr_json is not None and custom_attr_json != "" else []
    tags_json = request.form.get("tags", None)
    custom_tags = json.loads(tags_json) if tags_json is not None else []
    custom_media_json = request.form.get("custom_media_lis", None)
    custom_media = json.loads(custom_media_json) if custom_media_json is not None else []

    #handle files
    file_media_map = {}
    files = ["media_file"] + custom_media
    for f in files:
        media_file = request.files.get(f)
        media_obj = None
        if media_file.filename != "":
            if media_file.mimetype in ["image/png", "image/gif", "image/jpeg", "image/jpg"]:
                media_obj = save_image(media_file, UPLOAD_METHOD)
            else:
                media_obj = save_media(media_file, UPLOAD_METHOD)
        file_media_map[f] = media_obj

    if obj_id is None or obj_id == "":
        new_item(container_obj, custom_attr, custom_media, custom_tags, description, file_media_map, media_obj, name,
                 price, quantity, status)
    else:
        update_item(custom_attr, custom_media, custom_tags, description, file_media_map, name, obj_id, price, quantity)

    if redirect_url is not None:
        return redirect(redirect_url)

    return jsonify({
        "status": "ok",
    })


def del_item():
    """
    (PUT: item)
    """
    item_id = request.args.get("item_id")
    items.remove(item_id)
    return jsonify({
        "status": "ok",
    })


def del_container():
    """
    (PUT: item)
    """
    container_id = request.args.get("container_id")
    items.remove_container(container_id)
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

    app.add_url_rule('/item/',
                     "del_item", del_item, methods=['DELETE'])

    app.add_url_rule('/container/',
                     "del_container", del_container, methods=['DELETE'])
