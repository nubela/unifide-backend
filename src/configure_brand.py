"""
This is a one-time run file that configures a brand (Creates the relevant models, etc) for the backend.
This file configures a brand.
"""
from base import items
from base.items.action import save_container_path
from brand_cfg import RESERVED_ITEM_CONTAINERS, CAMPAIGN_CHANNELS
from unifide_backend.action import brand
from unifide_backend.action.brand.action import convert_campaign_channels


def create_item_containers(container_dic):
    for name, dic in container_dic.items():
        container_obj = items.container_from_path(items.container_path(dic["path_lis"]))
        if container_obj is None:
            save_container_path(dic["path_lis"], dic["description"])
        if "children" in dic:
            create_item_containers(dic["children"])


if __name__ == "__main__":
    print "Creating reserved item containers.."
    config_obj = convert_campaign_channels(CAMPAIGN_CHANNELS)
    brand.save(config_obj)
    print "Done!"

    print "Creating reserved item containers.."
    create_item_containers(RESERVED_ITEM_CONTAINERS)
    print "Done!"