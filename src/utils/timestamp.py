import time

def timestamp(signed_time: time.struct_time | None = None) -> str:
    return time.strftime("%Y-%m-%d %H:%M:%S UTC", signed_time or time.gmtime())
