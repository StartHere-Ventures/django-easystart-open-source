from django.conf import settings
from pytz import timezone

DATE_FORMATS = {
    "DD-MM-YYYY": "DD-MM-YYYY   ---  (24-12-2021)",
    "DD/MM/YYYY": "DD/MM/YYYY  ---  (24/12/2021)",
    "MM-DD-YYYY": "MM-DD-YYYY  ---  (12-24-2021)",
    "MM/DD/YYYY": "MM/DD/YYYY  ---  (12/24/2021)",
    "DD-MM-YY": "DD-MM-YY  ---  (24-12-21)",
    "DD/MM/YY": "DD/MM/YY  ---  (24/12/21)",
    "MM-DD-YY": "MM-DD-YY  ---  (12-24-21)",
    "MM/DD/YY": "MM/DD/YY  ---  (12/24/21)",
}

TIMEZONE_FORMAT = {
    "DD-MM-YYYY": "%d-%m-%Y",
    "DD/MM/YYYY": "%d/%m/%Y",
    "MM-DD-YYYY": "%m-%d-%Y",
    "MM/DD/YYYY": "%m/%d/%Y",
    "DD-MM-YY": "%d-%m-%y",
    "DD/MM/YY": "%d/%m/%y",
    "MM-DD-YY": "%m-%d-%y",
    "MM/DD/YY": "%m/%d/%y",
}


def change_utc_date(date):
    date_utc = date.astimezone(timezone(settings.TIME_ZONE))
    return date_utc
