from unifide_backend.action.cp.model import CPMenu, CPMenuItem
from unifide_backend.action.admin.user.model import User


BASE_MENU = [
            {"order": 0,
             "name": "OVERVIEW",
             "sub-menu":
                  [
                      {"name": "View All", "link": "/", "order": "0"},
                      {"name": "divider", "link": "", "order": "1"},
                      {"name": "Facebook", "link": "/facebook/page/activity", "order": "2"},
                      {"name": "Twitter", "link": "/twitter/activity", "order": "3"},
                      {"name": "Foursquare", "link": "/foursquare/venue/activity", "order": "4"},
                      {"name": "Brand Mention", "link": "/brand-mention", "order": "5"},
                      {"name": "divider", "link": "", "order": "6"},
                      {"name": "Web / Mobile", "link": "/web", "order": "7"}
                   ]},
            {"order": 1,
             "name": "CAMPAIGN",
             "sub-menu":
                  [
                      {"name": "New Promotion", "link": "/campaign/promo/new", "order": "0"},
                      {"name": "New Event", "link": "/campaign/event/new", "order": "1"},
                      {"name": "divider", "link": "", "order": "2"},
                      {"name": "Manage", "link": "/campaign", "order": "3"}
                  ]},
            {"order": 2,
             "name": "MODULES",
             "sub-menu":
                  [
                      {"name": "Business Info", "link": "/bizinfo", "order": "0"},
                      {"name": "Blog", "link": "/blog", "order": "1"},
                      {"name": "Orders", "link": "/order", "order": "2"},
                      {"name": "divider", "link": "", "order": "3"},
                      {"name": "Items", "link": "/items", "order": "4"}
                  ]}
            ]


def init_cp_menu():
    dic_list = User.collection().find() if User.collection().find() is not None else []

    for dic in dic_list:
        user = User.unserialize(dic)

        if CPMenu.collection().find_one({"uid": user._id}) is None:
            for item in BASE_MENU:
                menu = CPMenu()
                menu.uid = user._id
                menu.order = item["order"]
                menu.first_lvl = item["name"]

                for val in item["sub-menu"]:
                    sub_menu = CPMenuItem()
                    sub_menu.name = val["name"]
                    sub_menu.link = val["link"]
                    sub_menu.order = val["order"]
                    menu.second_lvl.append(sub_menu.serialize())

                menu._id = CPMenu.collection().insert(menu.serialize())


def put_new_user_menu(user_id):
    for item in BASE_MENU:
        menu = CPMenu()
        menu.uid = user_id
        menu.order = item["order"]
        menu.first_lvl = item["name"]

        for val in item["sub-menu"]:
            sub_menu = CPMenuItem()
            sub_menu.name = val["name"]
            sub_menu.link = val["link"]
            sub_menu.order = val["order"]
            menu.second_lvl.append(sub_menu.serialize())

        menu._id = CPMenu.collection().insert(menu.serialize())

    return menu