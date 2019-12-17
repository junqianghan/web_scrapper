from services.service_base import ServiceBase


class ServiceMovieCheck(ServiceBase):
    def __init__(self,**kwargs):
        super(ServiceMovieCheck, self).__init__(**kwargs)

    def _query_now(self):
        return True

    def _query_data(self):
        return "hello"

    def _should_notify(self, cur_data):
        return True

    def _notify(self):
        print("notify")

    def _update_predata(self, cur_data=None):
        self.pre_data = cur_data
