
import datetime


def check_date(start_date,end_date):
    today = datetime.date.today().strftime('%Y%m%d')
    if end_date is None or end_date > today:
        end_date = today
    start_date = start_date.replace('-', '')
    end_date = end_date.replace('-', '')
    if start_date > today:
        return "start_date大于现在时间"
    if start_date > end_date:
        return "start_date大于end_date"
    return start_date,end_date