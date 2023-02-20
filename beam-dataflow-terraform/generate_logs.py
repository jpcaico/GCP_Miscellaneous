import random
import string
import time

def random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def random_timestamp():
    year = str(random.randint(2010, 2022))
    month = str(random.randint(1, 12)).zfill(2)
    day = str(random.randint(1, 28)).zfill(2)
    hour = str(random.randint(0, 23)).zfill(2)
    minute = str(random.randint(0, 59)).zfill(2)
    second = str(random.randint(0, 59)).zfill(2)
    return f"{year}-{month}-{day} {hour}:{minute}:{second}"

def random_log_entry():
    return {
        'timestamp': random_timestamp(),
        'log_level': random.choice(['ERROR', 'WARNING', 'INFO', 'DEBUG']),
        'message': random_string(20),
        'source': random_string(10),
        'user_id': random.randint(1000, 9999),
        'session_id': random_string(8)
    }
