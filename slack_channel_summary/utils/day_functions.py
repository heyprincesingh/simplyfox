from datetime import datetime, timedelta
import pytz

# Set the timezone to Indian Standard Time (GMT+5:30)
ist = pytz.timezone('Asia/Kolkata')

def convert_date_to_unix(date_str):
    date_format = "%Y-%m-%d"
    final_date = datetime.strptime(date_str, date_format)
    final_date = ist.localize(final_date)
    return int(final_date.astimezone(pytz.utc).timestamp())

def convert_unix_to_date(timestamp):
    utc_timestamp = datetime.fromtimestamp(float(timestamp), tz=pytz.utc)
    ist_timestamp = utc_timestamp.astimezone(ist)
    return ist_timestamp.strftime('%Y-%m-%d %H:%M:%S.%f')

def convert_date_string_to_unix(date_str):
    date_format = "%d%b%Y"
    date_obj = datetime.strptime(date_str, date_format)
    date_obj = ist.localize(date_obj)
    return int(date_obj.astimezone(pytz.utc).timestamp())

def validate_date_format(date_str):
    try:
        datetime.strptime(date_str, '%d%b%Y')
        return True
    except ValueError:
        return False

def valid_start_end_date(start_date, end_date):
    if start_date and end_date:
        start_date_dt = datetime.strptime(start_date, "%Y-%m-%d")
        end_date_dt = datetime.strptime(end_date, "%Y-%m-%d")
        start_date_dt = ist.localize(start_date_dt)
        end_date_dt = ist.localize(end_date_dt)
        return start_date_dt <= end_date_dt

def adjust_unix_date_to_today(unix_timestamp, is_start_date=True):
    utc_date = datetime.fromtimestamp(float(unix_timestamp), tz=pytz.utc) + timedelta(days=1) 
    ist = pytz.timezone('Asia/Kolkata') 
    if is_start_date:
        adjusted_date = utc_date.replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=ist)
    else: 
        adjusted_date = utc_date.replace(hour=23, minute=59, second=59, microsecond=0, tzinfo=ist)
    return int(adjusted_date.astimezone(pytz.utc).timestamp())