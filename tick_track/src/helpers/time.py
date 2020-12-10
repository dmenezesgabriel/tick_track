import datetime
import pytz


def now():
    """
    Returns UTC timestamp with time zone
    """
    return pytz.UTC.localize(datetime.datetime.utcnow())


def now_br():
    """
    Returns America - São Paulo timestamp with time zone
    """
    return now().astimezone(pytz.timezone("America/Sao_Paulo"))


def timestamptz_to_unix(timestamptz):
    """
    Converts timestamp with time zone to epoch
    """
    return timestamptz.timestamp()


def unix_to_timestamp_utc(unix):
    """
    Converts epoch to timestamp with time zone
    """
    return datetime.datetime.utcfromtimestamp(unix)


def timestamptz_to_text(timestamptz):
    """
    Converts timestamp with time zone to string
    """
    return datetime.datetime.strftime(timestamptz, "%Y-%m-%d %H:%M:%S.%f%z")


def timestamptz_text_to_date(text):
    """
    Converts string date to date object
    """
    return datetime.datetime.strptime(text, "%Y-%m-%d %H:%M:%S.%f%z")


def date_trunc_day(timestamptz):
    """
    Trunc timestamp at day
    """
    return timestamptz.replace(hour=0, minute=0, second=0, microsecond=0)