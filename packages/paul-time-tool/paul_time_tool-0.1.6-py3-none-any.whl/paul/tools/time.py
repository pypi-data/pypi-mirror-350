from datetime import datetime

def get_current_datetime():
    """Returns the current naive datetime (no timezone)."""
    return datetime.now()

def print_date():
    """Prints the current date."""
    now = get_current_datetime()
    print(f"Date: {now.strftime('%Y-%m-%d')}")

def print_local_time():
    """Prints the current local time."""
    now = get_current_datetime()
    print(f"Time: {now.strftime('%H:%M:%S')}")

def print_time_info():
    """Prints both date and local time together."""
    now = get_current_datetime()
    print(f"Date & Time: {now.strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    print_date()
    print_local_time()