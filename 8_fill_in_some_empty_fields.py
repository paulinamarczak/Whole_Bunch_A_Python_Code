#fill in missing region, diking authority, dike name, and water course
#May 19 2021
#Paulina Marczak


import os
import time

print ("Starting at:", time.strftime('%a %H:%M:%S'))
print ("Importing modules.")
import arcpy, os

from arcpy import env
import re
import pandas as pd

arcpy.env.overwriteOutput = True

#set workspace
script_dir = os.path.dirname(os.path.realpath(__file__))

#define workspace
Out_workspace = os.path.join(script_dir, "Processed_dikes_operational.gdb")

#lokoup table with all dike numbers and names from Rudy
LUT = pd.read_csv(os.path.join(script_dir, "LUT.csv"), encoding='cp1252')
#print (LUT)
LUT.columns = ['DIKE_NUMBER', "REGION", "DIKE_NAME", "WATER_COURSE", "DIKING_AUTHORITY"] #rename list

column_names = ["DIKE_NUMBER", "REGION", "DIKING_AUTHORITY", "DIKE_NAME", "WATER_COURSE"] #reorder list

LUT = LUT.reindex(columns=column_names)


LUT = LUT.to_dict('records')
#print (LUT)

fields = ["DIKE_NUMBER", "REGION","DIKING_AUTHORITY","DIKE_NAME", "WATER_COURSE", "ObjectID"]

#get a list of values that correspond to each dike number? so like unique list of values that arent null then populate the empty rows with it?

a=[1,2,4,5,1,3,5,6]

feature_list = LUT #updated to spreadsheet dictionary

for gdb, datasets, features in arcpy.da.Walk(Out_workspace, topdown= True, datatype= "FeatureClass"):

	for feature in features:
		item= (os.path.join(Out_workspace,gdb, feature))
		# if feature == "dike_14_test": # test on one feature
		#if feature == "Flood_Protection_Works_Structural_Works": # test on one feature
		for dictionary in feature_list:
			# with arcpy.da.UpdateCursor(item, fields, sql_clause=(None,'ORDER BY DIKE_NUMBER')) as cursor:
			with arcpy.da.UpdateCursor(item, fields) as cursor:
				for row in cursor:			
				#if the null dike number matches the dictionary dike number, then fill in with dictionary dike number
					if row[0]==dictionary["DIKE_NUMBER"]: #change fields for ALL rows
						print (row, dictionary["DIKE_NUMBER"])
						row[1] = dictionary["REGION"] #["DIKE_NUMBER"]
						row[2] = dictionary["DIKING_AUTHORITY"]
						row[3] = dictionary["DIKE_NAME"]
						row[4] = dictionary["WATER_COURSE"]
						print ("dike", row[0], row[1], row[2], row[3], row[4], "match found for missing data in row", dictionary["DIKE_NUMBER"], "in", feature, "using", dictionary)
						cursor.updateRow(row)
					else:
						continue

