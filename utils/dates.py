from datetime import datetime, timedelta


def get_days_count_in_month(dt: datetime):
    return (dt.replace(month = dt.month % 12 +1, day = 1)-timedelta(days=1)).day

