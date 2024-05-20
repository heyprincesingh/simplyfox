from datetime import datetime, timedelta

def convert_date_to_unix(day):
    timestamp_format = "%A, %B %d, %Y %I:%M:%S.%f %p GMT%z"
    finalDate = datetime.now() - timedelta(days=int(day))
    finalDate.strftime(timestamp_format)
    return finalDate.timestamp()

def convert_unix_to_date(timestamp):
    timestamp = datetime.fromtimestamp(float(timestamp))
    return timestamp.strftime('%Y-%m-%d %H:%M:%S.%f') 