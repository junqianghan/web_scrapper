# coding=utf8
import logging

LOG = logging.getLogger(__name__)


class ScrapyException(Exception):
    msg_fmt = "An unknown exception occurred."
    safe = False

    def __init__(self, message=None, **kwargs):
        self._kwargs = kwargs

        if not message:
            try:
                message = self.msg_fmt.format(**self._kwargs)
            except AttributeError:
                self._log_exception()
                message = self.msg_fmt

        self.message = message
        super(ScrapyException, self).__init__(message)

    def _log_exception(self):
        LOG.exception("Exception in string format operation")
        for name, value in self._kwargs:
            LOG.error("%s : %s" % (name, value))