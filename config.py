# coding=utf-8

import json
import logging
import os
import copy

LOG = logging.getLogger(__name__)
log_levels_map = {
        "info":logging.INFO,
        "debug":logging.DEBUG,
        "warning":logging.WARNING,
        "error":logging.ERROR
    }

def get_json_file(fn, keys=None):
    """
    Get data from json file
    :param fn: filename
    :param keys: interested keys
    :return: dict formatted data
    """
    if not fn or not os.path.exists(fn):
        LOG.debug("get data from json but filename is none.")
        return None

    try:
        with open(fn, encoding='utf-8') as f:
            jsobj = json.load(f)
    except Exception as e:
        LOG.exception("get data from json error, filename:%s" % fn)
        raise e
    if not keys:
        return jsobj

    retDict = {}
    for key in keys:
        retDict[key] = jsobj[key]
    return retDict


def save_json_file(fn,json_data):
    """
    save json data to file.
    :param fn: filename
    :param json_data: data
    :return: None
    """
    json_str = json.dumps(json_data, indent=4,
                          ensure_ascii=False, sort_keys=False)
    with open(fn, 'w') as f:
        f.write(json_str)


def get_conf_json(conf_file = None):
    """Return json format from json file.

    :param conf_file:
    :return: json config
    """
    if not conf_file:
        return None
    if not os.path.exists(conf_file):
        return None

    try:
        with open(conf_file, encoding='utf-8') as f:
            jsobj = json.load(f)
    except Exception as e:
        LOG.exception("Get config data from conf_file error.")
        raise e
    return jsobj


def merge_conf_data(global_conf, local_conf):
    if not local_conf:
        return global_conf

    # conf = local_conf
    # for item in global_conf.keys():
    #     if item not in conf:
    #         conf[item] = global_conf[item]
    conf = copy.deepcopy(global_conf)
    conf.update(local_conf)
    return conf


def check_and_build_directory(abs_path=None):
    """
    check if abs_path exists, if not mkdir.

    :param abs_path: absolute path
    :return: None
    """
    if not abs_path:
        return

    if not os.path.exists(abs_path):
        os.makedirs(abs_path)