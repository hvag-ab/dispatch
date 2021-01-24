import logging
import datetime
import json
from logging.handlers import RotatingFileHandler

class JSONFormatter(logging.Formatter):
    REMOVE_ATTR = ["module", "exc_text", "stack_info", "created", "msecs", "relativeCreated", "exc_info",
                   "msg", "thread", "threadName", "processName", "process",'args']

    def format(self, record):
        extra = self.build_record(record)
        self.set_format_time(extra)  # set time
        extra['message'] = record.msg  # set message
        if record.exc_info:
            extra['exc_info'] = self.formatException(record.exc_info)
        if self._fmt == 'pretty':
            return json.dumps(extra, indent=1, ensure_ascii=False)
        else:
            return json.dumps(extra, ensure_ascii=False)

    @classmethod
    def build_record(cls, record):
        return {
            attr_name: record.__dict__[attr_name]
            for attr_name in record.__dict__
            if attr_name not in cls.REMOVE_ATTR
        }

    @classmethod
    def set_format_time(cls, extra):
        now = datetime.datetime.utcnow()
        format_time = now.strftime("%Y-%m-%dT%H:%M:%S" + ".%03d" % (now.microsecond / 1000) + "Z")
        extra['@timestamp'] = format_time
        return format_time


class JsonRotatingFileHandler(RotatingFileHandler):


    def __init__(self, filename, mode='a', maxBytes=0, backupCount=0, encoding=None, delay=False):
        super().__init__(filename, mode, maxBytes, backupCount, encoding, delay)
        # 实例化自定义的日志格式化对象
        json_format = JSONFormatter()
        self.setFormatter(json_format)