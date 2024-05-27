from datetime import date
from babel.dates import format_date
from babel import Locale


def get_month_name_br(month):
    locale = Locale("pt", "BR")
    date_obj = date(date.today().year, month, 1)
    month_name = format_date(
        date_obj,
        format="MMMM",
        locale=locale,
    )
    return f"{month:02d}-{month_name.upper()}"
