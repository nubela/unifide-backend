"""
This is a one-time run file that configures a brand (Creates the relevant models, etc) for the backend.
This file configures a brand.
"""
from base import items
from base.items.action import save_container_path
from base.items.mock import gen_model
from base.users.mock import gen_groups
from brand_cfg import CAMPAIGN_CHANNELS, USER_GROUPS, MODEL
from unifide_backend.action.brand.action import convert_campaign_channels
from unifide_backend.action.cp.action import put_new_menu, clear_menu


def create_item_containers(container_dic):
    for name, dic in container_dic.items():
        container_obj = items.container_from_path(items.container_path(dic["path_lis"]))
        if container_obj is None:
            save_container_path(dic["path_lis"], dic["description"])
        if "children" in dic:
            create_item_containers(dic["children"])


if __name__ == "__main__":
    print "Saving brand config"
    clear_menu()
    put_new_menu()
    print "Done!"

    print "Saving Campaign Channnel Config"
    config_obj = convert_campaign_channels(CAMPAIGN_CHANNELS)
    config_obj.save()
    print "Done!"

    print "Creating mock items and containers.."
    gen_model(MODEL)
    print "Done!"

    print "Creating user groups.."
    gen_groups(USER_GROUPS)
    print "Done!"