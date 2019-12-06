def db_query_output_to_csv(query_output, columns_to_exclude):
	"""	Converts output from a SQLAlchemy query to a .csv string.

	Parameters:
		query_output (list of <class 'SQLAlchemy.Model'>): output from an SQLAlchemy query
		columns_to_exclude (list of str): names of columns to exclude

	Returns:
		csv (str): query_output represented in .csv format

	Example usage:
		users = db.Users.query.filter_by(user_id=123)
		csv = db_query_output_to_csv(users, ["id", "age", "address"]
	"""
	rows = query_output
	columns_to_exclude = set(columns_to_exclude)

	#create list of column names  
	column_names = [i for i in rows[0].__dict__]
	for column_name in columns_to_exclude:
		column_names.pop(column_names.index(column_name))

	#add column titles to csv
	column_names.sort()
	csv = ", ".join(column_names) + "\n"

	#add rows of data to csv
	for row in rows:
		for column_name in column_names:
			if column_name not in columns_to_exclude:
				data = str(row.__dict__[column_name])
				#Escape (") symbol by preceeding with another (")
				data.replace('"','""')
				#Enclose each datum in double quotes so commas within are not treated as separators
				csv += '"' + data + '"' + ","
		csv += "\n"

	return csv