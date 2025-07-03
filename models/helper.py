from datetime import datetime, date


# Handle date time conversion
def handle_date_time(date_time_value):
    if isinstance(date_time_value, str):
        try:
            handled_date = datetime.strptime(date_time_value, "%Y-%m-%d %H:%M:%S")
        except (ValueError, TypeError):
            handled_date = None
    elif isinstance(date_time_value, datetime):
        handled_date = date_time_value
    else:
        handled_date = None
    return handled_date


# Handle date conversion
def handle_date(date_value):
    if isinstance(date_value, str):
        try:
            handled_date = datetime.strptime(date_value, "%Y-%m-%d").date()
        except (ValueError, TypeError):
            handled_date = None
    elif isinstance(date_value, datetime):
        handled_date = date_value.date()
    elif isinstance(date_value, date):
        handled_date = date_value
    else:
        handled_date = None
    return handled_date
