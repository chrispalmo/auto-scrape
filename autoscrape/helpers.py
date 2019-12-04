def db_query_output_to_csv(query_output, columns_to_exclude):
	rows = query_output
	columns_to_exclude = set(columns_to_exclude)

	#create list of column names to write to csv
	column_names = [i for i in rows[0].__dict__]
	for column_name in columns_to_exclude:
		column_names.pop(column_names.index(column_name))

	#add column titles
	column_names.sort()
	csv = ", ".join(column_names) + "\n"

	#add data
	for row in rows:
		for column_name in column_names:
			if column_name not in columns_to_exclude:
				csv += str(row.__dict__[column_name]) + ","
		csv += "\n"

	return csv