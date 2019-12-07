from math import floor

def time_breakdown(ms):
	"""Converts an integer representing number of milliseconds into days, hours, minutes, seconds and milliseconds. Output numbers are rounded down to the nearest whole number.

	Parameters:
		ms (integer): number of milliseconds

	Returns:
		(dictionary): breakdown of total days, hours, minutes, seconds and milliseconds

	Example useage:
		time_breakdown = time_breakdown(12345) 
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

def time_breakdown_string(ms):
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
		time_string += " " + str(time["min"]) + " minutes"
		if time["min"] != 1:
			time_string += "s"
	if time["sec"] != 0:
		time_string += " " + str(time["sec"]) + " second"
		if time["sec"] != 1:
			time_string += "s"	

	return time_string.strip()
