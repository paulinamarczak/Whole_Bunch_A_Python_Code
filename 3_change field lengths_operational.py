#3_change field lengths
#Paulina Marczak
#March 9 2021
#Purpose: Test changing float coded domain fields to text-based domain description fields
#Context: See convert_dikes_nocopy.py script

import os
import time

print ("Starting at:", time.strftime('%a %H:%M:%S'))
print ("Importing modules.")
import arcpy, os

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

# points_merged = os.path.join(Out_workspace, "Flood_Protection_Works_Appurtenant_Structures")

elev_merged = os.path.join(Out_workspace, "Flood_Protection_Works_Elevation_Points")
appt_merged = os.path.join(Out_workspace, "Flood_Protection_Works_Appurtenance_Points")
photos_merged = os.path.join(Out_workspace, "Flood_Protection_Works_Photo_Points")

points_merged = []

points_merged.append(elev_merged)
points_merged.append(appt_merged)
points_merged.append(photos_merged)


#domain fields that were floats, which are now text and length should be changed

field_list = [
					"WORKS_TYPE" ,
					"ACCESS_POINT_TYPE" ,
					"ACCESS_POINT_SIDE" ,
					"ARMOURED_BANK_TYPE",
					"ARMOURED_BANK_SIDE", #LEFTRIGHT in dikes_abk_point
					"CULVERT_MATERIAL" ,
					"CULVERT_END" ,
					"DROP_STRUCTURE_SIDE",
					"PROTECTION_POINT_END", #can also be STREAM domain #stream_2 in dike_photos
					"PROTECTION_POINT_TYPE", #fix names?
					"PROTECTION_POINT_CONDITION", #fix names?
					"FENCE_GATE_POINT_TYPE", #fix names?
					"FLOOD_BOX_CONCRETE_INLET_IND",
					"FLOOD_BOX_CONCRETE_OUTLET_IND",
					"FLOOD_BOX_TRASH_RACK_IND",
					"FLOOD_BOX_GATE_TYPE",
					"FLOOD_BOX_FUNCTIONAL_IND",  #fix names?
					"FOOT_BRIDGE_SIDE", #LEFTRIGHTMIDPOINT_1 #LEFTRIGHTMIDPOINTINT in Dike_APP_Point
					"FOOT_BRIDGE_MATERIAL",
					"GAUGE_TYPE",
					"GAUGE_READABILITY",
					"MANHOLE_TYPE",
					"PLATFORM_OBSTRUCTION_IND", #fix names?
					"OUTLET_POINT_CONCRETE_IND",
					"OUTLET_POINT_GATE_TYPE", #also OUTLET_POINT_GATE_TYPE
					"PUMP_HOUSE_BUILDING_MATERIAL",
					"PUMP_HOUSE_CORNER", #can also be DIRECTION #direction_2 in dike_photos
					"SIGN_MATERIAL", #can be WOOD_1
					"STAIRS_MATERIAL",
					"STAIRS_OBSTRUCTION_IND",
					"STRUCTURE_MATERIAL", #can be CONCRETE_12
					#"MONUMENT_MARKINGS",
					"MONUMENT_TYPE",
					"VEHICLE_BRIDGE_SIDE", #LEFTRIGHTMIDPOINT_1 #LEFTRIGHTMIDPOINTINT in Dike_APP_Point
					"VEHICLE_BRIDGE_END", #can be STREAM, STREAM_2
					"VEHICLE_BRIDGE_MATERIAL",
					"VEHICLE_BRIDGE_USAGE",
					"WEIR_SIDE",
					"WEIR_MATERIAL"]

for gdb, datasets, features in arcpy.da.Walk(Out_workspace, topdown= True, datatype= "FeatureClass"):

	for feature in features:
			item= (os.path.join(Out_workspace, feature))
			shapeType = arcpy.Describe(item).shapeType
			if feature == "Flood_Protection_Works_Elevation_Points" or feature == "Flood_Protection_Works_Appurtenance_Points" or feature == "Flood_Protection_Works_Photo_Points":
				for fieldName in [f.name for f in arcpy.ListFields(item) if not f.required]:
					#Delete excess fields, assign pattern to to other fields
					if fieldName in field_list: #and fieldName != "MONUMENT_MARKINGS":
						print ('altering field', fieldName)
						#add a way to identify the old fields, while giving it less than 30 character-limit length, so the fields can be copied over to the new fields easily
						arcpy.AlterField_management(item, fieldName, fieldName + "_")

						print ("Copying and altering length in field", fieldName, "in", item)

						arcpy.AddField_management(item, fieldName, "TEXT", "", "", 30)
					
					# if fieldName == "MONUMENT_MARKINGS":
					# 	print ("adding field", fieldName )
					# 	arcpy.AddField_management(item,"MONUMENT_MARKINGS_", "TEXT", "", "", 100) 



			for fieldName in [f.name for f in arcpy.ListFields(item) if not f.required]:
				
				if fieldName.endswith("_"):
					#basically building a mini-dictionary to ensure field attributes being transferred to correct output field.
					copyfield= fieldName[:-1]
					oldfield= "$feature." + fieldName
					print ("Copying features from", oldfield, "oldfield", "to", copyfield, "in", item)
					#it doesnt like calculate field
					#caution: it will make a field if theres no field, make sure AddField call is implemented above first- for proper domains, etc.
					arcpy.CalculateField_management(item, copyfield, oldfield, "ARCADE")
					arcpy.management.DeleteField(item, oldfield)

print ("Completed at:", time.strftime('%a %H:%M:%S'))
