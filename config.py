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