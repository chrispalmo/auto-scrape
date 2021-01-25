from math import floor

def to_filename(s, substitute_char='-', lower=True):
	"""Converts a string containing characters unsuitable for a folder or filename to one that is suitable.

	Parameters:
		s (string): the string to be converted.
		substitute_char (string): character to replace unsuitable characters with
		lower (bool): should the final string be converted to all lowercase?

	Returns:
		(string): the converted string.

	Example usage:
		>>> bad_filename = '~/filename/WITH/slashes\/and.\/BackSlashes.NOT.an.extension'
		>>> good_filename = to_filename(bad_filename)
		'--filename-with-slashes--and---backslashes-not-an-extension'
	"""
	# create list of unsuitable characters
	bad_chars = []
	for char in s:
		if not char.isalnum():
			bad_chars.append(char)

	# replace bad chars
	for bad_char in bad_chars:
		s = s.replace(bad_char, substitute_char)

	# to lowercase
	if lower:
		s = s.lower()

	return s
