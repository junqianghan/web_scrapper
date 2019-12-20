from services.service_base import ServiceBase
import datetime
import logging
from urllib.request import urlopen
from bs4 import BeautifulSoup
LOG = logging.getLogger(__name__)


class ServiceMovieCheck(ServiceBase):
    def __init__(self,**kwargs):
        super(ServiceMovieCheck, self).__init__(**kwargs)
        self.query_delay = self.conf_data["query_delay"]
        self.check_time = self.conf_data["check_time"]

    def _query_now(self):
        local_date_time = datetime.datetime.now()
        if int(local_date_time.hour) in self.check_time:
            return True
        else:
            return False

    def _get_movie_list(self):
        LOG.debug("get movie list")
        url = self.conf_data["index_url"]
        LOG.debug("check url %s" % url)
        html = urlopen(url).read().decode('gbk')

        bsObj = BeautifulSoup(html, 'lxml')
        head = bsObj.head
        cont = bsObj.find("div", {"class": "co_content8"})

    def _query_data(self):
        LOG.debug("query_data...")
        self._get_movie_list()
        return "hello"

    def _should_notify(self, cur_data):
        return True

    def _notify(self):
        print("notify")

    def _update_predata(self, cur_data=None):
        self.pre_data = cur_data
