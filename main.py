# coding=utf-8
import os
import config
import logging


global_conf_file = os.path.abspath("etc/scrapper_conf.json")
global_conf_data = None


def initial_basic_logging(service_name=None):
    log_dir = global_conf_data.get("log_dir")
    log_file = os.path.abspath(log_dir + "%s.log" % service_name)
    log_level = config.log_levels_map[global_conf_data.get("log_level")]
    log_format = "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
    logging.basicConfig(level=log_level,
                        filename=log_file,
                        format=log_format)


def main():
    global global_conf_data
    global_conf_data = config.get_conf_json(global_conf_file)
    print(global_conf_data)
    service_name = "movie_check"
    initial_basic_logging(service_name)



if __name__ == '__main__':
    main()