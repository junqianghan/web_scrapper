# coding=utf-8
import os
import config
import logging
from scrapy_exception import NotImplementedError
from email_client import EmailClient
LOG = logging.getLogger(__name__)


class ServiceBase(object):
    def __init__(self, service_name=None, query_delay=None,
                 local_conf_file=None, global_conf_data=None):
        self.service_name = service_name

        self.global_conf_data = global_conf_data
        self.local_conf_data = config.get_conf_json(local_conf_file)
        self.conf_data = config.merge_conf_data(self.global_conf_data,
                                                self.local_conf_data)

        self.query_delay = query_delay or self.conf_data.get('query_delay', 10)

        mail_sender = self.conf_data.get("email", None)
        self.mail_client = EmailClient(mail_sender)

        self.pre_data = None

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
            LOG.info("nofity success")
            self._update_predata(cur_data)
        LOG.info("execute success.")
