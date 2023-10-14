import calendar
from datetime import date

class DateUtilsException(Exception):
    pass


def days_to_expiration(year: int, month: int) -> int:
    """
    :param year: The expiration year (i.e. 2023)
    :param month: The expiration month (i.e. 10)
    :return: the days from today to the last business day of the month-year
    """
    expiration = expiration_date(year=year, month=month)
    days_to_expiration = (expiration - date.today()).days
    if days_to_expiration <= 0:
        raise DateUtilsException("Invalid input: Expiration date is in the past")
    return days_to_expiration


def expiration_date(year: int, month: int) -> date:
    """
    :param year: The expiration year (i.e. 2023)
    :param month: The expiration month (i.e. 10)
    :return: the date of the last business day of the month-year
    """
    last_business_day = last_business_day_in_month(year=year, month=month)
    expiration = date(day=last_business_day, month=month, year=year)
    return expiration


def last_business_day_in_month(year: int, month: int) -> int:
    """
    :param year: The year (i.e. 2023)
    :param month: the month (i.e. 10)
    :return: the last business day of the month
    """
    if not (1 <= month <= 12):
        raise DateUtilsException("Wrong month input")
    return max(calendar.monthcalendar(year, month)[-1][:5])
