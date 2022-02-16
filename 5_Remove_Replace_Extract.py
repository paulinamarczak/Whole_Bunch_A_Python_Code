#5_change UTM zones for consistency
#Other changes in deleting excess rows, excess appuretnances
#Paulina Marczak
#March 17 2021
#Purpose: The UTM Zones are inconsistently formatted so they need to be standardized
#Purpose: Any additional small field changes Client wants, such as changing dike number from 396 to 400 for existing data.
#Context: See convert_dikes_nocopy.py script
#Let it run, it takes a while (field calculator and python3 are broken, cant do in arcade)
#add field calculator to change dike numbers

#Once this operation is done, you may have to re-merge the orphan dikes and modify the features in the output polyline file processed_dikes_operational/Flood_Protection_Works_Structural_Works
#So manually deleted objectID 5391 from processed operational dataset to replace with orphan dike 188
#manual editing of dike 211 to delete feature (see orphan and missing dike line check sheet 211)
#Classified manual conversion of dike crest elevations was performed, transformation model was 2002, or 1997 or 2010- double check with Client

import os
import time

import os.path
from os import path

print ("Starting at:", time.strftime('%a %H:%M:%S'))
print ("Importing modules.")
import arcpy

from arcpy import env
try:
	import pandas as pd
except ImportError:
	print ("No pandas found- must install from pip")
import csv
try:
	import re
except Import:
	print ("re not imported")

arcpy.env.overwriteOutput = True

#set workspace
#script dir=current working dir= where you saved this script
script_dir = os.path.dirname(os.path.realpath(__file__))


Out_workspace = os.path.join(script_dir, "Processed_dikes_operational.gdb")
Out_workspace1 = os.path.join(script_dir, "Processed_dikes.gdb")

workspace_list = [Out_workspace  , Out_workspace1]

field_dictionary= {
	
	"9" : "9N",
	"10": "10N",
	"11" : "11N",
	"NAD_1983_UTM_Zone_9N" : "9N", 
	"NAD_1983_UTM_Zone_10N" : "10N",
	"NAD_1983_UTM_Zone_11N" : "11N",

}

# first, modify output structural works

field_list_replace = ["UTM_ZONE"]
fields = ["DIKE_NAME", "DIKE_NUMBER", "DATA_SOURCE", "SEGMENT_LENGTH_M", "Shape_Length", "WORKS_TYPE", "WATER_COURSE"]

for i in workspace_list:

	if path.exists(i):
		process_list= []
		#points_merged = os.path.join(i, "Flood_Protection_Works_Appurtenant_Structures")
		lines_merged = os.path.join(i, "Flood_Protection_Works_Structural_Works")
		# elev_merged = os.path.join(Out_workspace, "Flood_Protection_Works_Elevation_Points")
		# appt_merged = os.path.join(Out_workspace, "Flood_Protection_Works_Appurtenance_Points")
		# photos_merged = os.path.join(Out_workspace, "Flood_Protection_Works_Photo_Points")

		# points_merged = []

		# process_list.append(elev_merged)
		# process_list.append(appt_merged)
		# process_list.append(photos_merged)

		#process_list.append(points_merged)
		process_list.append(lines_merged)
		print ("List of items to be processed is", process_list)

		#Replace UTM formatting in points only
		# for k,v in field_dictionary.items():
		# 	for x in process_list:
		# 		if not x.endswith("Flood_Protection_Works_Structural_Works"):
		# 			with arcpy.da.UpdateCursor(x, field_list_replace) as cursor:
		# 				for row in cursor:
		# 					if row[0] == k:
		# 						row[0] = v
		# 					cursor.updateRow(row)
		# 				print ("updated field from", k, "to", v)

		#replace things in points and lines
		
		for item in process_list:
			for fieldName in [f.name for f in arcpy.ListFields(item) if not f.required]:
				print (fieldName)
			with arcpy.da.UpdateCursor(item, fields) as cursor:
				print ("the fields being processed are", fields, "in", item)

				for row in cursor:

					# add some conditions to change merged outputs from Orphan and Missing Dike line Check mar 19 2021

					# modify works type
					if row[5] == "PROTECTN":
						row[5]= "EROSION PROTECTION"

					# add replacing line field dike number
					if row[0] == "Rail Bridge to Allenby South Side":
						row[1] =  "400"
						print ("Calculating new expression for", row, "in", item)

					elif row[0] == "Upstream of Allenby North Side":
						row[1] =  "401"
						print ("Calculating new expression for", row, "in", item)

					# delete WSP and replace with orphan dike in merge, so this is removing the duplicate
					## bern at cnr bridge dike 
					#ok dont need this anymore because the segment was deleted manually
					# elif row[1] == 354 and str(row[4]).startswith(""): 
					# 	print ("Deleting", row, "in", item)
					# 	cursor.deleteRow()
					# 	continue

					#delete wsp from missing dikes spreadsheet
					elif row[0] == "Diversion Works" and row[1] == 107:  #works
						print ("Deleting", row, "in", item)
						cursor.deleteRow()
						continue

					# delete part of dike 14
					elif row[1] == 14 and str(row[4]).startswith("88.148"): 
						print ("Deleting", row, "in", item)
						cursor.deleteRow()
						continue

					# delete erosion protection from dike 135
					elif row[0] == "Silverdale" and row[5] == "EROSION PROTECTION": #works
						print ("Deleting", row, "in", item)
						cursor.deleteRow()
						continue

					# delete part of dike 134
					elif row[1] == 134 and str(row[4]).startswith("30.4322"): 
						print ("Deleting", row, "in", item)
						cursor.deleteRow()
						continue

					# delete part of dike 323
					elif row[0] == "Treatment Plant Berm" and str(row[4]).startswith("54.292341"): #works
						print ("Deleting", row, "in", item)
						cursor.deleteRow()
						continue

					#remove part of dike 95
					elif row[0] == "Campbell Creek Industrial Park" and str(row[4]).startswith("106.6972"): #works
						print ("Deleting", row, "in", item)
						cursor.deleteRow()
						continue

					#remove part of dike 99
					elif row[0] == "Thrupp St to McArthur Park Causeway" and str(row[4]).startswith("30.47"): #works
						print ("Deleting", row, "in", item)
						cursor.deleteRow()
						continue

					#rename dike 261
					elif row[0] == "Dragons Creek":
						print ("Calculating new expression for", row, "in", item)
						row[1] =  "262"

					#rename part of dike 302
					#did this in original dikes from axiom, so when rerun this will show up
					elif row[0] == "Bartlett Flood Protection" and str(row[4]).startswith("140.294091"):
						print ("Calculating new expression for", row, "in", item)
						row[1] =  "303"
						row[0] == "Cottonwood Flood Protection"

					#same , just did it twice
					#did this in original dikes from axiom, so when rerun this will show up
					elif row[0] == "Bartlett Flood Protection" and str(row[4]).startswith("140.063757"):
						print ("Calculating new expression for", row, "in", item)
						row[1] =  "303"

					elif row[0] == "Zeballos River Training Berm" and str(row[4]).startswith("495.825768"):
						print ("Calculating new expression for", row, "in", item)
						row[5] =  "EROSION PROTECTION"

					# replace 369 number
					elif row[1] == 369:
						print ("Calculating new expression for", row, "in", item)
						row[1] =  "368"
					
					# next set
					elif row[1] == 222 or row[1] == 275:
						print ("Calculating new expression for", row, "in", item)
						row[2] = "Based on 2004 survey"

					elif row[1] == 308 and str(row[3]).startswith("4728.45"):
						print ("Calculating new expression for", row, "in", item)
						row[2] = "Based on 2004 survey"

					elif row[1] == 311 and str(row[3]).startswith("251.437"):
						print ("Calculating new expression for", row, "in", item)
						row[2] = "Based on 2004 survey"

					elif row[1] == 311 and str(row[3]).startswith("110.00"):
						print ("Calculating new expression for", row, "in", item)
						row[2] = "Based on 2004 survey"

					elif row[1] == 354:
						print ("Calculating new expression for", row, "in", item)
						row[2] = "Based on 2004 survey"

					elif row[1] == 188:
						print ("Calculating new expression for", row, "in", item)
						row[2] = "Based on 2004 survey"

					elif row[1] == 368:
						print ("Calculating new expression for", row, "in", item)
						row[0] = "Baker Trails (Guy Creek and Tank Creek)"
						row[6] = "Guy Creek, Tank Creek"


					cursor.updateRow(row)
						
				# except:
				# 	e = sys.exc_info()[1]
				# 	print(e.args[0], ", this error passes because its a point file with no line length")

UTM_field = ["UTM_ZONE"]
fields = ["DIKE_NAME", "DIKE_NUMBER", "DATA_SOURCE", "WORKS_TYPE"]

#for associated appurtenance structures

for i in workspace_list:

	if path.exists(i):
		process_list= []
		#points_merged = os.path.join(i, "Flood_Protection_Works_Appurtenant_Structures")
		elev_merged = os.path.join(Out_workspace, "Flood_Protection_Works_Elevation_Points")
		appt_merged = os.path.join(Out_workspace, "Flood_Protection_Works_Appurtenance_Points")
		photos_merged = os.path.join(Out_workspace, "Flood_Protection_Works_Photo_Points")

		process_list.append(elev_merged)
		process_list.append(appt_merged)
		process_list.append(photos_merged)
		# points_merged = os.path.join(i, "Flood_Protection_Works_Appurtenant_Structures")
		# process_list.append(points_merged)
		print ("List of items to be processed is", process_list)
		#Replace UTM formatting
		for k,v in field_dictionary.items():
			for x in process_list:
				#with arcpy.da.UpdateCursor(points_merged, UTM_field) as cursor:
				with arcpy.da.UpdateCursor(x, UTM_field) as cursor:
					for row in cursor:
						if row[0] == k:
							row[0] = v
						cursor.updateRow(row)
					print ("updated UTM zone field from", k, "to", v)

		for item in process_list:
			for fieldName in [f.name for f in arcpy.ListFields(item) if not f.required]:
				print (fieldName)
			with arcpy.da.UpdateCursor(item, fields) as cursor:
				print ("the fields being processed are", fields)

				for row in cursor:

					# add some conditions to change merged outputs from Orphan and Missing Dike line Check mar 19 2021

					# add replacing line field dike number
					if row[0] == "Rail Bridge to Allenby South Side":
						row[1] =  "400"
						print ("Calculating new expression for", row, "in", item) #works

					elif row[0] == "Upstream of Allenby North Side":
						row[1] =  "401"
						print ("Calculating new expression for", row, "in", item) #works

					# delete WSP and replace with orphan dike in merge, so this is removing the duplicate
					## bern at cnr bridge dike
					elif row[1] == 354: #works
						print ("Deleting", row, "in", item) #works
						cursor.deleteRow()
						continue

					#delete wsp from missing dikes spreadsheet
					elif row[0] == "Diversion Works" and row[1] == 107:  #works
						print ("Deleting", row, "in", item)
						cursor.deleteRow()
						continue

					# delete erosion protection from dike 135
					elif row[0] == "Silverdale" and row[3] == "EROSION PROTECTION": #works
						print ("Deleting", row, "in", item)
						cursor.deleteRow()
						continue

					# replace 369 number
					elif row[1] == 369:
						print ("Calculating new expression for", row, "in", item) #works
						row[1] =  "368"
					
					# # next set #RIGHT now dont change appurtenance structures data source- ask Client
					# elif row[1] == 222 or row[1] == 275:
					# 	print ("Calculating new expression for", row, "in", item)
					# 	row[2] = "Based on 2004 survey"


					cursor.updateRow(row)


print("Completed at:", time.strftime('%a %H:%M:%S'))
