# coding=utf-8
import os
import config
import logging
import argparse


global_conf_file = os.path.abspath("etc/scrapper_conf.json")
global_conf_data = None

services_map = {
    "movie_check":"services.service_movie_check.ServiceMovieCheck"
}

def initial_basic_logging(service_name=None):
    log_dir = global_conf_data.get("log_dir")
    log_file = os.path.abspath(log_dir + "%s.log" % service_name)
    log_level = config.log_levels_map[global_conf_data.get("log_level")]
    log_format = "%(asctime)s %(levelname)s %(message)s %(funcName)s:%(lineno)d"
    logging.basicConfig(level=log_level,
                        filename=log_file,
                        format=log_format)


def main():
    global global_conf_data
    global_conf_data = config.get_conf_json(global_conf_file)

    parse = argparse.ArgumentParser(description="web scrappy framework.")
    parse.add_argument("service", help="service name", choices=services_map.keys())
    args = parse.parse_args()

    service_name = args.service
    initial_basic_logging(service_name)




if __name__ == '__main__':
    main()