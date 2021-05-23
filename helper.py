import datetime
import time

FORMAT = '%Y-%m-%d %H:%M:%S'


class DateTimeHelper(object):
    @staticmethod
    def epoch_now():
        """
        Will return 13 digit epoch time
        :return:
        """
        return int(time.time() * 1000)

    @staticmethod
    def epoch_to_date_time(epoch: int):
        """
        Expecting 13 digit epoch time
        :param epoch:
        :return:
        """
        return time.strftime(FORMAT, time.localtime(epoch / 1000))

    @staticmethod
    def now():
        return datetime.datetime.now().strftime(FORMAT)

    @staticmethod
    def utc_now(format__=None):
        __format = format__ if format__ else FORMAT
        return datetime.datetime.utcnow().strftime(__format)

    @staticmethod
    def str_to_date(date_time: str, format__=None) -> datetime:
        __format = format__ if format__ else FORMAT
        return datetime.datetime.strptime(date_time, __format)
