from datetime import datetime, time

from dateutil.relativedelta import relativedelta


def first_day_of_month(dt: datetime) -> datetime:
    return datetime.combine(dt + relativedelta(day=1), time(0))
