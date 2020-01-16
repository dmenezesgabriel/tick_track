import datetime
import pytz


def now():
    return pytz.UTC.localize(datetime.datetime.utcnow())


def now_br():
    return now().astimezone(pytz.timezone("America/Sao_Paulo"))


def timestamptz_to_unix(timestamptz):
    return timestamptz.timestamp()


def unix_to_timestamp_utc(unix):
    return datetime.datetime.utcfromtimestamp(value)


def timestamptz_to_text(timestamptz):
    return datetime.datetime.strftime(timestamptz, "%Y-%m-%d %H:%M:%S.%f%z")


def timestamptz_text_to_date(text):
    text
    return datetime.datetime.strptime(text, "%Y-%m-%d %H:%M:%S.%f%z")


def date_trunc_day(timestamptz):
    return timestamptz.replace(hour=0, minute=0, second=0, microsecond=0)
