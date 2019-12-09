from math import floor

def time_breakdown(ms):
	"""Converts an integer representing number of milliseconds into a dictionary representing days, hours, minutes, seconds and milliseconds. Output numbers are rounded down to the nearest whole number.

	Parameters:
		ms (integer): number of milliseconds.

	Returns:
		(dictionary): breakdown of total days, hours, minutes, seconds and milliseconds.

	Example usage:
		>>> time_breakdown = time_breakdown(123456789)
		{'day': 1, 'hr': 10, 'min': 17, 'sec': 36, 'ms': 789} 
	"""

	ms_out = ms % 1000;
	sec = floor((ms % (1000 * 60)) / 1000)
	min = floor((ms % (1000 * 60 * 60)) / 1000 / 60)
	hr = floor((ms % (1000 * 60 * 60 * 24)) / 1000 / 60 / 60)
	day = floor(
		(ms % (1000 * 60 * 60 * 24 * 365)) / 1000 / 60 / 60 / 24
	)

	return {
		"day": day,
		"hr": hr,
		"min": min,
		"sec": sec,
		"ms": ms_out
	}

def time_breakdown_string(ms, granularity=5):
	"""Converts an integer representing number of milliseconds into a string that uses natural language to represent the time quantity.

	Parameters:
		ms (integer): number of milliseconds.
		granularity (integer): the level of detail required.

	Returns:
		(string): string that uses natural language to represent the time quantity.

	Example usage:
		>>> time_breakdown_string(123456789)
		
		'1 day 10 hours 17 minutes 36 seconds 789 milliseconds'

		>>>time_breakdown_string(
		123456789,
		granularity=3)
		
		'1 day 10 hours 17 minutes'
	"""

	time = time_breakdown(ms)
	time_string = ""

	if time["day"] != 0:
		time_string += str(time["day"]) + " day"
		if time["day"] != 1:
			time_string += "s"

	if time["hr"] != 0:
		time_string += " " + str(time["hr"]) + " hour"
		if time["hr"] != 1:
			time_string += "s"

	if time["min"] != 0:
		time_string += " " + str(time["min"]) + " minute"
		if time["min"] != 1:
			time_string += "s"

	if time["sec"] != 0:
		time_string += " " + str(time["sec"]) + " second"
		if time["sec"] != 1:
			time_string += "s"	

	if time["ms"] != 0:
		time_string += " " + str(time["ms"]) + " millisecond"
		if time["ms"] != 1:
			time_string += "s"	

	#filter to specified granularity
	time_string = time_string.strip().split(" ")[:2*granularity]

	return " ".join(time_string)


