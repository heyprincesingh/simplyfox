from datetime import datetime, timedelta

def convert_date_to_unix(date_str):
    date_format = "%Y-%m-%d"
    final_date = datetime.strptime(date_str, date_format)
    return int(final_date.timestamp())

def convert_unix_to_date(timestamp):
    timestamp = datetime.fromtimestamp(float(timestamp))
    return timestamp.strftime('%Y-%m-%d %H:%M:%S.%f') 

def valid_start_end_date(start_date, end_date):
    if start_date and end_date:
        start_date_dt = datetime.strptime(start_date, "%Y-%m-%d")
        end_date_dt = datetime.strptime(end_date, "%Y-%m-%d")

        if start_date_dt <= end_date_dt:
            return True
        print("Error: Start date cannot exceed end date.")
        return False