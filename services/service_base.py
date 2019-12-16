# coding=utf-8
import os
import config
import logging
from scrapy_exception import NotImplementedError
from email_client import EmailClient


class ServiceBase(object):
    def __init__(self, service_name=None, query_delay=None,
                 local_conf_file=None, global_conf_data=None):
        self.service_name = service_name

        self.global_conf_data = global_conf_data
        self.local_conf_data = config.get_conf_json(local_conf_file)
        self.conf_data = config.merge_conf_data(self.global_conf_data,
                                                self.local_conf_data)

        self.query_delay = query_delay or self.conf_data.get('query_delay', 10)

        self.logger = self._get_logger_client()

        mail_sender = self.conf_data.get("email", None)
        self.mail_client = EmailClient(mail_sender)

        self.pre_data = None

    def _get_logger_client(self):
        logger = logging.getLogger(self.service_name)

        log_file = os.path.abspath(self.conf_data.get("log_file"))
        log_level = config.log_levels_map[self.conf_data.get("log_level")]
        f_handler = logging.FileHandler(log_file)
        f_handler.setLevel(log_level)
        logger.addHandler(f_handler)
        return logger

    def _query_now(self):
        raise NotImplementedError()

    def _query_data(self):
        raise NotImplementedError()

    def _should_notify(self, cur_data):
        raise NotImplementedError()

    def _notify(self):
        raise NotImplementedError()

    def _update_predata(self, cur_data=None):
        raise NotImplementedError()

    def execute(self):
        if not self._query_now():
            return

        cur_data = self._query_data()
        if self._should_notify(cur_data):
            self._notify()
            self.logger.info("nofity success")
            self._update_predata(cur_data)
        self.logger.info("execute success.")
