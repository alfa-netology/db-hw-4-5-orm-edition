from datetime import timedelta

def milliseconds_to_time(duration):
    # преобразование в часы, минуты и секунды
    seconds = int((duration/1000) % 60)
    minutes = int((duration / (1000 * 60)) % 60)
    hours = int((duration / (1000 * 60 * 60)) % 24)
    return f"{hours:02}:{minutes:02}:{seconds:02}"

def time_to_milliseconds(hours=0, minutes=0, seconds=0):
    # преобразование в милисекунды
    delta = timedelta(hours=hours, minutes=minutes, seconds=seconds)
    return int(delta.total_seconds()) * 1000