# OHS Acadec Website Repo

Current Functions:


scoreImport


- csvimport(inputFile, database, dateOverride, ignore, addSuffix)

  -inputFile: CSV to import in string format
	
  -database: Json to save to in string format
	
  -dateOverride: a date to write over all test dates within a CSV, useful for competitions. Optional.
	
  -ignore: a list, [stuff, things, yeah], of strings which will be ignored columns within the imported CSV. Optional. Still doesn't work sometimes idk why.
	
  -addSuffix: automatically adds an additional string onto each test imported. Optional.
	
  -All optional items can be passed over with either no input or a blank definition such as "" or [].
	
