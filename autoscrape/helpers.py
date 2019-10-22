from random import randint

def random_string_of_numbers(length):
	return "".join([str(randint(0,9)) for i in range (length)])

from datetime import datetime

def timestamp_string():
    datetime.now().strftime("%Y%m%d %H:%M:%S")