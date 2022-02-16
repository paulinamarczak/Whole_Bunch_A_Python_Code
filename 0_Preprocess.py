# 0 preprocess old BCGW  in preparation for merging with survey files
#Paulina Marczak
#March 17 2021
#Purpose: Classified
#After this script is run, copy over to dikes for processing folder.

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

# Additions from FPW (Context: Classified)
FPW = os.path.join(script_dir, "structural_works_from_bcgw", "structural_works_from_bcgw.gdb", "FPW_FPWKLN_line")

item1 = os.path.join(FPW, FPW + "_selected_for_merging")
arcpy.Delete_management(item1)
arcpy.CopyFeatures_management(FPW, item1) 
print (item1)

#ADD NEW COLULMN DATA_SOURCE
fieldName = "DATA_SOURCE"
arcpy.management.DeleteField(item1, fieldName)
arcpy.AddField_management(item1, fieldName, "TEXT", "","",100) 

#copy and paste workstype field to new field and lengthen field
fieldName = "DATA_SOURCE"
arcpy.management.DeleteField(item1, fieldName)
arcpy.AddField_management(item1, fieldName, "TEXT", "","",100) 

# delete from FPW line unless:
fields = ["FLDPRTCTNW","FLDPRTCTNS", "Shape_Length", "DATA_SOURCE", "WORKS_TYPE"]

with arcpy.da.UpdateCursor(item1, fields) as cursor:
	for row in cursor:

		# Filter through dikes from FPW_FPWKLN_line file
		#Sometimes the lines were manually split in ArcGIS Pro, but then still populating/adding the data_source field here

		# dike number = 8
		if row[0] == 6890458 and str(row[2]).startswith("81.670693"): #good
			row[3] = "Based on 2004 survey"

		elif row[0] == 6890459 and str(row[2]).startswith("119.154545"): #good
			row[3] = "Based on 2004 survey"

		# dike number = 14
		elif row[0] == 6890476 and str(row[2]).startswith("30.84744"): #good
			row[3] = "Based on 2004 survey"

		elif row[0] == 6890476 and str(row[2]).startswith("172.739827"): #good
			row[3] = "Based on 2004 survey"

		elif row[0] == 6890476 and str(row[2]).startswith("195.3356"): #good
			row[3] = "Based on 2004 survey"

		elif row[0] == 6890475 and str(row[2]).startswith("43.20935"): #good
			row[3]= "Based on 2004 survey"

		elif row[0] == 6890475 and str(row[2]).startswith("199.98707"): #good
			row[3]= "Based on 2004 survey"

		elif row[0] == 6890475 and str(row[2]).startswith("88.13686"): #good
			row[3]= "Based on 2004 survey"

		elif row[0] == 6890475 and str(row[2]).startswith("35.9009"): #good
			row[3]= "Based on 2004 survey"

		elif row[0] == 6890476 and str(row[2]).startswith("92.547855"): #good
			row[3]= "Based on 2004 survey"

		elif row[0] == 6887793 and str(row[2]).startswith("88.148433"): #good
			row[3]= "Based on 2004 survey"

		elif row[0] == 6890475 and str(row[2]).startswith("34.34334"): #good
			row[3]= "Based on 2004 survey"

		elif row[0] == 6890475 and str(row[2]).startswith("45.82257"): #good
			row[3]= "Based on 2004 survey"

		#dike number 16
		elif row[0] == 6889603 and str(row[2]).startswith("71.52924"): #good
			row[3]= "Based on 2004 survey"

		# dike number 44
		elif row[0] == 6890687 and str(row[2]).startswith("214.1175"): #good
			cursor.deleteRow()
			continue

		# dike number 44- ADDITION
		elif row[0] == None and str(row[2]).startswith("69.43878"): 
			row[3]= "Assumed from air photo 2021"

		elif row[0] == None and str(row[2]).startswith("163.00874"):
			row[3]= "Assumed from air photo 2021"

		# dike number 56
		elif row[0] == 6887901 and str(row[2]).startswith("230.35778"): #works
			row[3]= "Based on 2004 survey"

		elif row[0] == 6887904 and str(row[2]).startswith("132.466092"): #works
			row[3]= "Based on 2004 survey"

		#dike 107
		elif row[0] == 6889850 and str(row[2]).startswith("1688.7617"): 
			row[3]= "Based on 2004 survey"
			
		# dike number 119
		elif row[0] == 6889448 and str(row[2]).startswith("373.01797"): #good
			row[3]= "Based on 2004 survey"

		elif row[0] == 6889449 and str(row[2]).startswith("79.3734"): #good
			row[3]= "Based on 2004 survey"

		elif row[0] == 6889450 and str(row[2]).startswith("139.47114"): #good
			row[3]= "Based on 2004 survey"

		elif row[0] == 6889454 and str(row[2]).startswith("507.80109"): #good
			row[3]= "Based on 2004 survey"

		# dike number 121
		elif row[0] == 6888382 and str(row[2]).startswith("278.03292"): #good
			row[3]= "Based on 2004 survey"

		elif row[0] == 6888380 and str(row[2]).startswith("229.765263"): #works
			row[3]= "Based on 2004 survey"
		
		# dike number 122 all
		elif row[1] == 122:
			row[3]= "Based on 2004 survey"

		# dike number 123
		elif row[0] == 6890502 and str(row[2]).startswith("226.78976"): #works
			row[3]= "Based on 2004 survey"

		# dike number 124
		elif row[0] == 6890515 and str(row[2]).startswith("169.81832"): #works
			row[3]= "Based on 2004 survey"

		elif row[0] == 6890514 and str(row[2]).startswith("14.6680"): #works
			row[3]= "Based on 2004 survey"

		elif row[0] == 6890514 and str(row[2]).startswith("141.37227"): #works
			row[3]= "Based on 2004 survey"

		elif row[0] == 6890510 and str(row[2]).startswith("10.14831"): #works
			row[3]= "Based on 2004 survey"

		elif row[0] == 6890509 and str(row[2]).startswith("96.49076"): #works
			row[3]= "Based on 2004 survey"

		elif row[0] == 6890508 and str(row[2]).startswith("743.1091"): #works
			row[3]= "Based on 2004 survey"

		elif row[0] == 6890508 and str(row[2]).startswith("64.0774"): #works
			row[3]= "Based on 2004 survey"

		elif row[0] == 6890508 and str(row[2]).startswith("54.84619"):#works
			row[3]= "Based on 2004 survey"

		elif row[0] == 6890508 and str(row[2]).startswith("12.52577"): #works
			row[3]= "Based on 2004 survey"

		elif row[0] == 6890508 and str(row[2]).startswith("201.28437"): #works
			row[3]= "Based on 2004 survey"

		elif row[0] == 6890506 and str(row[2]).startswith("11.74268"): #works
			row[3]= "Based on 2004 survey"

		elif row[0] == 6890504 and str(row[2]).startswith("104.70764"): #works
			row[3]= "Based on 2004 survey"

		elif row[0] == 6890504 and str(row[2]).startswith("56.35094"): #works
			row[3]= "Based on 2004 survey"

		elif row[0] == 6890503 and str(row[2]).startswith("340.83643"): #works
			row[3]= "Based on 2004 survey"

		elif row[0] == 6890505 and str(row[2]).startswith("13.00540"): #works
			row[3]= "Based on 2004 survey"

		elif row[0] == 6890511 and str(row[2]).startswith("250.0631"): #works
			row[3]= "Based on 2004 survey"

		elif row[0] == 6890511 and str(row[2]).startswith("832.6938"):  #works
			row[3]= "Based on 2004 survey"

		elif row[0] == 6890512 and str(row[2]).startswith("9.62520"): #works
			row[3]= "Based on 2004 survey"

		elif row[0] == 6890513 and str(row[2]).startswith("3.7091"): #works
			row[3]= "Based on 2004 survey"

		# dike number 128
		elif row[0] == 6889424 and str(row[2]).startswith("211.8897"): #works
			row[3]= "Based on 2004 survey"

		# dike number 134
		elif row[0] == 6890031 and str(row[2]).startswith("222.7431"): #works
			row[3]= "Based on 2004 survey"

		#
		elif row[0] == 6888611 and str(row[2]).startswith("36.2832"): #works
			row[3]= "Based on 2004 survey"

		#dike number 231
		elif row[0] == 6890644 and str(row[2]).startswith("224.26763"): #works
			row[3]= "Based on 2004 survey"

		# dike number 324
		elif row[0] == 6890726 and str(row[2]).startswith("95.6676"): #works
			row[3]= "Based on 2004 survey"

		# dike number 281
		elif row[0] == 6890648 and str(row[2]).startswith("147.9254"):
			row[3]= "Based on 2004 survey"

		elif row[0] ==6888210	and str(row[2]).startswith("35.006889"):
			row[3]= "Based on 2004 survey"

		cursor.updateRow(row)

	#delete the rows which we didnt specify as going into merged file
	with arcpy.da.UpdateCursor(item1, 'DATA_SOURCE', 'DATA_SOURCE is NULL') as cursor:
		for row in cursor:
			cursor.deleteRow()
			#should result in 55 values plus the air photo ones

#copy shape length field to new SEGMENT_LENGTH_M FIELD
#ADD NEW COLULMN DATA_SOURCE
fieldName = "SEGMENT_LENGTH_M"
oldfield= "$feature." + "Shape_Length"
arcpy.management.DeleteField(item1, fieldName)
arcpy.AddField_management(item1, "SEGMENT_LENGTH_M", "FLOAT")
arcpy.CalculateField_management(item1, "SEGMENT_LENGTH_M", oldfield, "ARCADE")

# 2004 bcgw points to add
# only adding if the points are not equal to PHOTOPT or ALIGNMENT "POINT_TYPE"

FPW_points_old = os.path.join(script_dir, "structural_works_from_bcgw", "structural_works_from_bcgw.gdb", "FPW_AS_SVW_point")

FPW_points = arcpy.CopyFeatures_management(FPW_points_old, FPW_points_old + "_selected_for_merging") 

print(FPW_points)

#ADD NEW COLULMN DATA_SOURCE
fieldName = "DATA_SOURCE"
arcpy.management.DeleteField(FPW_points, fieldName)
arcpy.AddField_management(FPW_points, fieldName, "TEXT", "","",100) 

# delete from FPW line unless:
fields = ["FLDPRTCTNS", "POINT_TYPE", "DATA_SOURCE"]

with arcpy.da.UpdateCursor(FPW_points, fields) as cursor:

	# add appurtenance points as Classified
	# also see email Classified
	for row in cursor:

		if row[1]== "PHOTOPT":
			cursor.deleteRow()
			continue

		elif row[1]== "ALIGNMENT":
			cursor.deleteRow()
			continue

		elif row[0] == 56:
			row[2]= "Based on 2004 survey"

		elif row[0] == 107:
			row[2]= "Based on 2004 survey"
		
		elif row[0] == 121:
			row[2]= "Based on 2004 survey" 

		elif row[0] == 122:
			row[2]= "Based on 2004 survey"

		#add classified
		elif row[0] == 57:
			row[2]= "Based on 2004 survey"

		elif row[0] == 58:
			row[2]= "Based on 2004 survey"

		elif row[0] == 60:
			row[2]= "Based on 2004 survey"

		elif row[0] == 61:
			row[2]= "Based on 2004 survey"

		elif row[0] == 164:
			row[2]= "Based on 2004 survey"

		elif row[0] == 356:
			row[2]= "Based on 2004 survey"

		elif row[0] == 357:
			row[2]= "Based on 2004 survey"

		elif row[0] == 359:
			row[2]= "Based on 2004 survey"

		elif row[0] == 360:
			row[2]= "Based on 2004 survey"

		cursor.updateRow(row)

	#delete the rows which we didnt specify as going into merged file
with arcpy.da.UpdateCursor(FPW_points, 'DATA_SOURCE', 'DATA_SOURCE is NULL') as cursor:
		for row in cursor:
			cursor.deleteRow()


print("Completed at:", time.strftime('%a %H:%M:%S'))