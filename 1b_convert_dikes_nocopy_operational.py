#Paulina Marczak
#april 2021
#Purpose: Convert dikes and auxiliary dike data to standardized format based on "overview of geodatabase fields"
#Part 1b of script to convert

import os
import time

print ("Starting script 1b at:", time.strftime('%a_%H:%M:%S'))
print ("Importing modules.")
import arcpy, os

from arcpy import env

import csv
import re
from re import search
import logging

arcpy.env.overwriteOutput = True

#set workspace
script_dir = os.path.dirname(os.path.realpath(__file__))

#check that you got the workspaces
print("script is located in", script_dir)

#Create new gdb to store results
#Define variable to link to new gdb
Out_workspace = os.path.join(script_dir, "Processed_dikes_operational.gdb")
backup_workspace = os.path.join(script_dir, "Processed_dikes_operational_1b_backup" + time.strftime('%d_%a_%H_%M') + ".gdb")
arcpy.management.CreateFileGDB(script_dir, "Processed_dikes_operational_1b_backup" + time.strftime('%d_%a_%H_%M') + ".gdb", "CURRENT")

temp_workspace = os.path.join(script_dir, "Processed_dikes_operational_1b_temp_outputs" + time.strftime('%d_%a_%H_%M') + ".gdb")
arcpy.management.CreateFileGDB(script_dir, "Processed_dikes_operational_1b_temp_outputs" + time.strftime('%d_%a_%H_%M') + ".gdb", "CURRENT")


for gdb, datasets, features in arcpy.da.Walk(Out_workspace, topdown= True, datatype= "FeatureClass"):
	for feature in features:
		if feature.endswith("backup"):
			arcpy.Delete_management(feature)
		else:
			arcpy.CopyFeatures_management(os.path.join(Out_workspace,feature),os.path.join(backup_workspace,feature)) 

arcpy.env.workspace = Out_workspace


#copy from script 1
field_list_lines = [
"REGION",
"DIKING_AUTHORITY",
"DIKE_NAME",
"DIKE_NUMBER",
"WATER_COURSE",
"WORKS_TYPE",
"WORKS_TYPE_ADDITIONAL_INFO",
"SEGMENT_ID",
"SEGMENT_LENGTH_M",
"CREST_SURVEY_DATE", #added underscore
"WAS_CREST_SURVEYED",
"LAST_DA_SURVEY_DATE",
"TOTAL_LENGTH_M",
"BANK_PROTECTION_LENGTH",
"OBJECT_ID",
"DIKE_CONSEQUENCE",
"DIKE_FAIL_LIKELIHOOD",
"DIKE_RISK",
"PRIVATE_INDIVIDUAL",
"DIKE_AUTH_MAILING_ADDRESS_1",
"DIKE_AUTH_MAILING_ADDRESS_2",
"DIKE_AUTH_MAILING_ADDRESS_3",
"DIKE_AUTH_CITY",
"DIKE_AUTH_PROVINCE",
"DIKE_AUTH_POSTAL",
"DIKE_AUTH_COUNTRY",
"PRINCIPAL_CONTACT_NAME",
"PRINCIPAL_DEFAULT_PHONE",
"PRINCIPAL_EMAIL",
"EPA_LOCAL_AUTHORITY",
"DMA_REGULATED",
"PRIVATE_DIKE",
"RIGHT_OF_WAY",
"RIGHT_OF_WAY_COMMENTS",
"DESIGN_RETURN_PERIOD",
"DIKING_AUTHORITY_TYPE",
"SERVICE_AREA",
"LAND_USE",
"INFRASTRUCTURE_PROTECTED",
"BUILDINGS_PROTECTED",
"FLOODPLAIN_MAP_LINK",
"FLOODPLAIN_MAP_DATE",
"DATA_SOURCE",
"COMMENTS", #CHANGED from comment
"DIKE_PROFILE_URL",
"DATA_LAYER_SOURCE"
]

field_list_points = [
"REGION",
"DIKING_AUTHORITY",
"DIKE_NAME",
"DIKE_NUMBER",
"WATER_COURSE",
"WORKS_TYPE",
"UTM_ZONE",
"CREST_EASTING_X",
"CREST_NORTHING_Y",
"CREST_CHAINAGE",
"CREST_ELEVATION_Z",
"CREST_SURVEY_DATE",
"FLOOD_PROFILE_EASTING_X",
"FLOOD_PROFILE_NORTHING_Y",
"FLOOD_PROFILE_CHAINAGE",
"FLOOD_PROFILE_ELEVATION_Z",
"FLOOD_PROFILE_MODEL_DATE",
"FLOOD_PROFILE_COMMENTS",
"APPURTENANT_STRUCTURE_NUMBER", #slight change, added STRUCTURE instead of STRUCT
"COMMENTS",
"DATA_SOURCE",
"OBJECT_ID",
"ACCESS_POINT_TYPE",
"ACCESS_POINT_SIDE",
"ACCESS_POINT_NAME",
"ARMOURED_BANK_TYPE",
"ARMOURED_BANK_SIDE",
"CULVERT_MATERIAL",
"CULVERT_END",
"CULVERT_SIZE",
"DROP_STRUCTURE_SIDE",
"PROTECTION_POINT_END",
"PROTECTION_POINT_TYPE",
"PROTECTION_POINT_CONDITION",
"FENCE_GATE_POINT_TYPE",
"LOCK_IDENTIFICATION_FEATURE",
"FLOOD_BOX_CONCRETE_INLET_IND",
"FLOOD_BOX_CONCRETE_OUTLET_IND",
"FLOOD_BOX_TRASH_RACK_IND",
"FLOOD_BOX_GATE_TYPE",
"FLOOD_BOX_FUNCTIONAL_IND",
"FLOOD_BOX_NUMBER_OF_PIPES",
"FOOT_BRIDGE_SIDE",
"FOOT_BRIDGE_MATERIAL",
"GAUGE_TYPE",
"GAUGE_READABILITY",
"GROYNE_END",
"GROYNE_MATERIAL",
"GROYNE_WIDTH",
"MANHOLE_TYPE",
"MANHOLE_SIZE",
"CROSS_SECTION_IDENTIFIER",
"PLATFORM_OBSTRUCTION_IND",
"OUTLET_POINT_CONCRETE_IND",
"OUTLET_POINT_GATE_TYPE",
"OUTLET_POINT_NUMBER_OF_PIPES",
"PUMP_HOUSE_BUILDING_MATERIAL",
"PUMP_HOUSE_CORNER",
"PUMP_HOUSE_DIMENSIONS",
"SIGN_MATERIAL",
"SIGN_TEXT",
"STAIRS_MATERIAL",
"STAIRS_OBSTRUCTION_IND",
"STRUCTURE_MATERIAL",
"MONUMENT_MARKINGS",
"MONUMENT_TYPE",
"VEHICLE_BRIDGE_SIDE",
"VEHICLE_BRIDGE_END",
"VEHICLE_BRIDGE_MATERIAL",
"VEHICLE_BRIDGE_USAGE",
"VEHICLE_BRIDGE_NAME",
"WEIR_SIDE",
"WEIR_MATERIAL",
"PHOTO_ID",
"PHOTO_URL",
"PHOTO_FILENAME",
"AZIMUTH",
"PHOTO_COMMENTS",
"x",
"y",
"DATA_LAYER_SOURCE"
]
#save features to be merged in empty lists
PointList_alignment_elevation = []
PointList_appurtenances = []
PointList_photos = []

store_point_list = []

store_point_list.append(PointList_alignment_elevation)
store_point_list.append(PointList_appurtenances)
store_point_list.append(PointList_photos)


LineList = []

#For QC
count_list_poly = []
count_list_point = []

for gdb, datasets, features in arcpy.da.Walk(Out_workspace, topdown= True, datatype= "FeatureClass"):

	for feature in features:
		item= (os.path.join(Out_workspace, feature))
		print (feature)
		shapeType = arcpy.Describe(item).shapeType
		if shapeType == "Polyline":
			for fieldName in [f.name for f in arcpy.ListFields(item) if not f.required]:
				#Delete excess fields, assign pattern to to other fields
				if fieldName in field_list_lines and not fieldName.endswith("_"):
					print ('altering field', fieldName)
					#add a way to identify the old fields, while giving it less than 30 character-limit length, so the fields can be copied over to the new fields easily
					arcpy.AlterField_management(item, fieldName, fieldName+"_")
				else:
					print ("Deleting excess field", fieldName)
					arcpy.management.DeleteField(item, fieldName)
			
			#adding new fields which will replace the old fields
			print ("Adding fields and assigning domains to", item)
			arcpy.AddField_management(item, "REGION", "TEXT", "","", 30)
			arcpy.AddField_management(item, "DIKING_AUTHORITY", "TEXT", "","", 150)
			arcpy.AddField_management(item, "DIKE_NAME", "TEXT", "","", 80)
			arcpy.AddField_management(item, "DIKE_NUMBER", "LONG", 7) #domain
			#arcpy.AssignDomainToField_management(item, "EXISTING_GPS", "DOMAIN_7")
			arcpy.AddField_management(item, "WATER_COURSE", "TEXT", "","",250)
			arcpy.AddField_management(item, "WORKS_TYPE", "TEXT", "","",30)
			arcpy.AddField_management(item, "WORKS_TYPE_ADDITIONAL_INFO", "TEXT", "","",250)
			arcpy.AddField_management(item, "SEGMENT_ID", "TEXT", "","", 50)
			arcpy.AddField_management(item, "SEGMENT_LENGTH_M", "FLOAT") #NO domain; FLOAT
			arcpy.AddField_management(item, "CREST_SURVEY_DATE", "DATE")
			arcpy.AddField_management(item, "WAS_CREST_SURVEYED", "TEXT", "","",10)
			arcpy.AddField_management(item, "LAST_DA_SURVEY_DATE", "DATE")
			arcpy.AddField_management(item, "TOTAL_LENGTH_M", "LONG", 8)  #domain
			arcpy.AddField_management(item, "BANK_PROTECTION_LENGTH", "TEXT", "","",5)
			arcpy.AddField_management(item, "OBJECT_ID", "TEXT", "","", 50)
			arcpy.AddField_management(item, "DIKE_CONSEQUENCE", "DOUBLE", 50)  #domain
			arcpy.AddField_management(item, "DIKE_FAIL_LIKELIHOOD", "DOUBLE", 50)  #domain
			arcpy.AddField_management(item, "DIKE_RISK", "DOUBLE", 50)  #domain
			arcpy.AddField_management(item, "PRIVATE_INDIVIDUAL", "TEXT", "","",1)
			arcpy.AddField_management(item, "DIKE_AUTH_MAILING_ADDRESS_1", "TEXT", "","",250)
			arcpy.AddField_management(item, "DIKE_AUTH_MAILING_ADDRESS_2", "TEXT", "","",250)
			arcpy.AddField_management(item, "DIKE_AUTH_MAILING_ADDRESS_3", "TEXT", "","",250)
			arcpy.AddField_management(item, "DIKE_AUTH_CITY", "TEXT", "","",100)
			arcpy.AddField_management(item, "DIKE_AUTH_PROVINCE", "TEXT", "","", 2)
			arcpy.AddField_management(item, "DIKE_AUTH_POSTAL", "TEXT","","", 10)		
			arcpy.AddField_management(item, "DIKE_AUTH_COUNTRY", "TEXT","","", 100)
			arcpy.AddField_management(item, "PRINCIPAL_CONTACT_NAME", "TEXT", "","",100)
			arcpy.AddField_management(item, "PRINCIPAL_DEFAULT_PHONE", "TEXT","","", 30)
			arcpy.AddField_management(item, "PRINCIPAL_EMAIL", "TEXT", "","",100)
			arcpy.AddField_management(item, "EPA_LOCAL_AUTHORITY", "TEXT", "","",250)
			arcpy.AddField_management(item, "DMA_REGULATED", "TEXT", "","",5)
			arcpy.AddField_management(item, "PRIVATE_DIKE", "TEXT", "","",5)
			arcpy.AddField_management(item, "RIGHT_OF_WAY", "TEXT", "","",50)
			arcpy.AddField_management(item, "RIGHT_OF_WAY_COMMENTS", "TEXT", "","",2500)
			arcpy.AddField_management(item, "DESIGN_RETURN_PERIOD", "TEXT", "","",50)
			arcpy.AddField_management(item, "DIKING_AUTHORITY_TYPE", "TEXT", "","",50)
			arcpy.AddField_management(item, "SERVICE_AREA", "TEXT", "","",8)
			arcpy.AddField_management(item, "LAND_USE", "TEXT", "","",250)
			arcpy.AddField_management(item, "INFRASTRUCTURE_PROTECTED", "TEXT", "","",250)
			arcpy.AddField_management(item, "BUILDINGS_PROTECTED", "DOUBLE", 250)  #domain
			#arcpy.AssignDomainToField_management(item, "BUILDINGS_PROTECTED", "DOMAIN_250")
			arcpy.AddField_management(item, "FLOODPLAIN_MAP_LINK", "TEXT","","", 500)
			arcpy.AddField_management(item, "FLOODPLAIN_MAP_DATE", "DATE")
			arcpy.AddField_management(item, "DATA_SOURCE", "TEXT", "","",100) 
			arcpy.AddField_management(item, "COMMENTS", "TEXT","","", 500)
			arcpy.AddField_management(item, "DIKE_PROFILE_URL", "TEXT","","", 100)
			arcpy.AddField_management(item,"DATA_LAYER_SOURCE", "TEXT", "","", 100)

			print("Done creating fields for", item)

		else: #points fields
			print ("Adding fields and assigning domains to", item)
			#modify input fields so its easy to delete later
			for fieldName in [f.name for f in arcpy.ListFields(item) if not f.required]:
				#Delete excess fields, assign pattern to to other fields
				# if fieldName in field_list_points:
				# 	print ('altering field', fieldName)
				# 	#add a way to identify the old fields, while giving it less than 30 character-limit length, so the fields can be copied over to the new fields easily
				# 	arcpy.AlterField_management(item, fieldName, fieldName+"_")
				if fieldName in field_list_points and not fieldName.endswith("_"):
					print ('altering field', fieldName)
					#add a way to identify the old fields, while giving it less than 30 character-limit length, so the fields can be copied over to the new fields easily
					arcpy.AlterField_management(item, fieldName, fieldName+"_")
				else:
					print ("Deleting excess field", fieldName)
					arcpy.management.DeleteField(item, fieldName)
			

	# # 	#add new fields to copy old fields into
	# 		#for points, https://gis.stackexchange.com/questions/92545/transfer-domain-descriptions-from-coded-values-to-string-text-at-a-new-field
			#fields with coded domains are firstly added as FLOAT fields, in script 3 theyre changed to text fields with field limits
			arcpy.AddField_management(item,"REGION", "TEXT", "","",30)
			arcpy.AddField_management(item,"DIKING_AUTHORITY", "TEXT", "","", 150)
			arcpy.AddField_management(item,"DIKE_NAME", "TEXT", "","",80)
			arcpy.AddField_management(item, "DIKE_NUMBER", "LONG", 7) #domain #changed to LONG
			arcpy.AddField_management(item,"WATER_COURSE","TEXT","","",250)
			arcpy.AddField_management(item,"WORKS_TYPE", "FLOAT")
			arcpy.AddField_management(item,"UTM_ZONE", "TEXT", "","", 30)
			arcpy.AddField_management(item,"CREST_EASTING_X", "DOUBLE") #domain
			arcpy.AddField_management(item,"CREST_NORTHING_Y", "DOUBLE") #domain
			arcpy.AddField_management(item,"CREST_CHAINAGE", "FLOAT")
			arcpy.AddField_management(item,"CREST_ELEVATION_Z", "FLOAT")
			arcpy.AddField_management(item,"CREST_SURVEY_DATE", "DATE")
			arcpy.AddField_management(item,"FLOOD_PROFILE_EASTING_X", "DOUBLE", 10) #domain
			arcpy.AddField_management(item,"FLOOD_PROFILE_NORTHING_Y", "DOUBLE", 10) #domain
			arcpy.AddField_management(item,"FLOOD_PROFILE_CHAINAGE", "FLOAT")
			arcpy.AddField_management(item,"FLOOD_PROFILE_ELEVATION_Z", "FLOAT")
			arcpy.AddField_management(item,"FLOOD_PROFILE_MODEL_DATE", "DATE")
			arcpy.AddField_management(item,"FLOOD_PROFILE_COMMENTS", "TEXT", "","", 250)
			arcpy.AddField_management(item,"APPURTENANT_STRUCTURE_NUMBER", "TEXT", "","", 30)
			arcpy.AddField_management(item,"COMMENTS", "TEXT", "","",500)
			arcpy.AddField_management(item,"DATA_SOURCE", "TEXT", "","", 200)
			arcpy.AddField_management(item,"OBJECT_ID", "TEXT","","", 50)
			arcpy.AddField_management(item,"ACCESS_POINT_TYPE", "FLOAT")
			arcpy.AddField_management(item,"ACCESS_POINT_SIDE", "FLOAT")
			arcpy.AddField_management(item,"ACCESS_POINT_NAME", "TEXT", "","",100)
			arcpy.AddField_management(item,"ARMOURED_BANK_TYPE", "FLOAT")
			arcpy.AddField_management(item,"ARMOURED_BANK_SIDE", "FLOAT")
			arcpy.AddField_management(item,"CULVERT_MATERIAL", "FLOAT")
			arcpy.AddField_management(item,"CULVERT_END", "FLOAT")
			arcpy.AddField_management(item,"CULVERT_SIZE", "FLOAT")
			arcpy.AddField_management(item,"DROP_STRUCTURE_SIDE", "FLOAT")
			arcpy.AddField_management(item,"PROTECTION_POINT_END", "FLOAT")
			arcpy.AddField_management(item,"PROTECTION_POINT_TYPE", "FLOAT")
			arcpy.AddField_management(item,"PROTECTION_POINT_CONDITION", "FLOAT")
			arcpy.AddField_management(item,"FENCE_GATE_POINT_TYPE", "FLOAT")
			arcpy.AddField_management(item,"LOCK_IDENTIFICATION_FEATURE", "TEXT", "","",30)
			arcpy.AddField_management(item,"FLOOD_BOX_CONCRETE_INLET_IND", "FLOAT")
			arcpy.AddField_management(item,"FLOOD_BOX_CONCRETE_OUTLET_IND", "FLOAT")
			arcpy.AddField_management(item,"FLOOD_BOX_TRASH_RACK_IND", "FLOAT")
			arcpy.AddField_management(item,"FLOOD_BOX_GATE_TYPE", "FLOAT")
			arcpy.AddField_management(item,"FLOOD_BOX_FUNCTIONAL_IND", "FLOAT")
			arcpy.AddField_management(item,"FLOOD_BOX_NUMBER_OF_PIPES", "SHORT")
			arcpy.AddField_management(item,"FOOT_BRIDGE_SIDE", "FLOAT")
			arcpy.AddField_management(item,"FOOT_BRIDGE_MATERIAL", "FLOAT")
			arcpy.AddField_management(item,"GAUGE_TYPE", "FLOAT")
			arcpy.AddField_management(item,"GAUGE_READABILITY", "FLOAT")
			arcpy.AddField_management(item,"GROYNE_END", "TEXT", "","",5)
			arcpy.AddField_management(item,"GROYNE_MATERIAL", "TEXT", "","",10)
			arcpy.AddField_management(item,"GROYNE_WIDTH", "FLOAT")
			arcpy.AddField_management(item,"MANHOLE_TYPE", "FLOAT")
			arcpy.AddField_management(item,"MANHOLE_SIZE", "FLOAT")
			arcpy.AddField_management(item,"CROSS_SECTION_IDENTIFIER", "TEXT", "","",30)
			arcpy.AddField_management(item,"PLATFORM_OBSTRUCTION_IND", "FLOAT")
			arcpy.AddField_management(item,"OUTLET_POINT_CONCRETE_IND", "FLOAT")
			arcpy.AddField_management(item,"OUTLET_POINT_GATE_TYPE", "FLOAT")
			arcpy.AddField_management(item,"OUTLET_POINT_NUMBER_OF_PIPES", "LONG") #just says integer
			arcpy.AddField_management(item,"PUMP_HOUSE_BUILDING_MATERIAL", "FLOAT")
			arcpy.AddField_management(item,"PUMP_HOUSE_CORNER", "FLOAT")
			arcpy.AddField_management(item,"PUMP_HOUSE_DIMENSIONS", "TEXT", "","",100)
			arcpy.AddField_management(item,"SIGN_MATERIAL", "FLOAT")
			arcpy.AddField_management(item,"SIGN_TEXT", "TEXT", "","",100)
			arcpy.AddField_management(item,"STAIRS_MATERIAL", "FLOAT")
			arcpy.AddField_management(item,"STAIRS_OBSTRUCTION_IND", "FLOAT")
			arcpy.AddField_management(item,"STRUCTURE_MATERIAL", "FLOAT")
			#RUDY WANTED MONUMENT MARKINGS AS FLOAT BUT THEY ARE TEXT FIELDS, THEREFORE CHANGED TO TEXT and length 100
			arcpy.AddField_management(item,"MONUMENT_MARKINGS", "TEXT", "", "", 100)
			arcpy.AddField_management(item,"MONUMENT_TYPE", "FLOAT")
			arcpy.AddField_management(item,"VEHICLE_BRIDGE_SIDE", "FLOAT")
			arcpy.AddField_management(item,"VEHICLE_BRIDGE_END", "FLOAT")
			arcpy.AddField_management(item,"VEHICLE_BRIDGE_MATERIAL", "FLOAT")
			arcpy.AddField_management(item,"VEHICLE_BRIDGE_USAGE", "FLOAT")
			arcpy.AddField_management(item,"VEHICLE_BRIDGE_NAME", "TEXT", "","", 100)
			arcpy.AddField_management(item,"WEIR_SIDE", "FLOAT")
			arcpy.AddField_management(item,"WEIR_MATERIAL", "FLOAT")
			arcpy.AddField_management(item,"PHOTO_ID", "TEXT", "","",30)
			arcpy.AddField_management(item,"PHOTO_URL", "TEXT","","",300)
			arcpy.AddField_management(item,"PHOTO_FILENAME", "TEXT", "","", 100)
			arcpy.AddField_management(item,"AZIMUTH", "SHORT", 3) #domain
			arcpy.AddField_management(item,"PHOTO_COMMENTS", "TEXT", "","", 100)
			arcpy.AddField_management(item,"DATA_LAYER_SOURCE", "TEXT", "","", 100)

		# after fields are added, copy over the old field to the new field for all features (i.e., item)

		#if classified2 list
		classified2_list = [
					"Dike_ABK_Line",
					"Dike_APP_Point",
					"Dike_DCL_Line",
					"Dike_Photos",
					"Dikes_ABK_Point",
					"Dikes_DCL_Point"
				]

		#if classified1 list
		classified1_list = [
					"Dikes",
					"Dikes_Appert",
					"Protection",
					"Riprap",
					"Dikes_ABK_Point_classified1",
					"Dikes_ABK_Point_for_dike_119"
					"Photos_Survey"
				]

		flood_works_list = [
		"Flood_Profiles_Points_ABK",
		"Flood_Profiles_Points_DCL"
		]

		classified_list = [
			"classified_centrelines",
			"classified_points"
		]

		orphan_dike_list = [
		"selected_dikes"]

		bcgw_list = ["FPW_AS_SVW_point_selected_for_merging"
					"FPW_FPWKLN_line_selected_for_merging"]

		for fieldName in [f.name for f in arcpy.ListFields(item) if not f.required]:
			
			if fieldName.endswith("_") and not fieldName.startswith("DATA_SOURCE") and not fieldName.startswith("DATA_LAYER_SOURCE"):
				#basically building a mini-dictionary to ensure field attributes being transferred to correct output field.
				copyfield= fieldName[:-1]
				oldfield= "$feature." + fieldName
				print ("Copying features from", oldfield, "oldfield", "to", copyfield, "in", item)
				#it doesnt like calculate field
				#caution: it will make a field if theres no field, make sure AddField call is implemented above first- for proper domains, etc.
				arcpy.CalculateField_management(item, copyfield, oldfield, "ARCADE")
				arcpy.management.DeleteField(item, oldfield)
			
			#rewrite DATA_SOURCE according to either classified1 or classified2
			elif fieldName.endswith("_") and fieldName.startswith("DATA_SOURCE") and feature.startswith(tuple(classified1_list)):
				#only do this for classified1 features; those feature names correspond with classified1.
				copyfield= fieldName[:-1]
				oldfield= "$feature." + fieldName
				expression= "'Based on 2019/2020 survey from classified1'" + ";"
				print ("Calculating expression for", copyfield, "in", item)
				arcpy.CalculateField_management(item, copyfield, expression, "ARCADE")
				arcpy.management.DeleteField(item, oldfield)
			
			#if classified2 do...
			elif fieldName.endswith("_") and fieldName.startswith("DATA_SOURCE") and feature.startswith(tuple(classified2_list)):
				copyfield= fieldName[:-1]
				oldfield= "$feature." + fieldName
				expression= "'Based on 2019/2020 survey from classified2'" + ";"
				print ("Calculating expression for", copyfield, "in", item)
				arcpy.CalculateField_management(item, copyfield, expression, "ARCADE")
				arcpy.management.DeleteField(item, oldfield)

			#if flood do...
			elif fieldName.endswith("_") and fieldName.startswith("DATA_SOURCE") and feature.startswith(tuple(flood_works_list)):
				copyfield= fieldName[:-1]
				oldfield= "$feature." + fieldName
				expression= "'Based on 2019/2020 work from Golder, using 2014 Lower Fraser River design flood profile'" + ";"
				print ("Calculating expression for", copyfield, "in", item)
				arcpy.CalculateField_management(item, copyfield, expression, "ARCADE")
				arcpy.management.DeleteField(item, oldfield)

			#if classified, bcgw, or orphan dikes: copy content within fields as they are
			elif fieldName.endswith("_") and fieldName.startswith("DATA_SOURCE"):
				copyfield= fieldName[:-1]
				oldfield= "$feature." + fieldName
				print ("Copying features from", oldfield, "oldfield", "to", copyfield, "in", item)
				#caution: it will make a field if theres no field, make sure AddField call is implemented above first
				arcpy.CalculateField_management(item, copyfield, oldfield, "ARCADE")
				arcpy.management.DeleteField(item, oldfield)

			# field to identify original data source and layer name
			# cant use calculate field because python3 link is broken within tool; arcade isnt flexible enough; must use cursor
			elif fieldName.startswith("DATA_LAYER_SOURCE") and feature.startswith(tuple(classified1_list)): 
				with arcpy.da.UpdateCursor(item, "DATA_LAYER_SOURCE") as cursor:
					for row in cursor:
						year=  feature.split("_copy")[0] + " from classified1"
						row[0] =  year
						print ("Calculating expression for", fieldName, "in", item)
						cursor.updateRow(row)

			elif fieldName.startswith("DATA_LAYER_SOURCE") and feature.startswith(tuple(classified2_list)): 
				with arcpy.da.UpdateCursor(item, "DATA_LAYER_SOURCE") as cursor:
					for row in cursor:
						year=  feature.split("_copy")[0] + " from classified2"
						row[0] =  year
						print ("Calculating expression for", fieldName, "in", item)
						cursor.updateRow(row)

			elif fieldName.startswith("DATA_LAYER_SOURCE") and feature.startswith(tuple(classified_list)): 
				with arcpy.da.UpdateCursor(item, "DATA_LAYER_SOURCE") as cursor:
					for row in cursor:
						year=  feature.split("_copy")[0] + " from classified"
						row[0] =  year
						print ("Calculating expression for", fieldName, "in", item)
						cursor.updateRow(row)

			elif fieldName.startswith("DATA_LAYER_SOURCE") and feature.startswith(tuple(flood_works_list)): 
				with arcpy.da.UpdateCursor(item, "DATA_LAYER_SOURCE") as cursor:
					for row in cursor:
						year=  feature.split("_copy")[0] + " From Flood Profile"
						row[0] =  year
						print ("Calculating expression for", fieldName, "in", item)
						cursor.updateRow(row)

			elif fieldName.startswith("DATA_LAYER_SOURCE") and feature.startswith(tuple(orphan_dike_list)):
				with arcpy.da.UpdateCursor(item, "DATA_LAYER_SOURCE") as cursor:
					for row in cursor:
						year=  feature.split("_copy")[0] + " From Orphan Dike Files"
						row[0] =  year
						print ("Calculating expression for", fieldName, "in", item)
						cursor.updateRow(row)

			elif fieldName.startswith("DATA_LAYER_SOURCE") and feature.startswith(tuple(bcgw_list)):
				with arcpy.da.UpdateCursor(item, "DATA_LAYER_SOURCE") as cursor:
					for row in cursor:
						year=  feature.split("_copy")[0] + " From BCGW"
						row[0] =  year
						print ("Calculating expression for", fieldName, "in", item)
						cursor.updateRow(row)

		#copy feautre when done
		arcpy.CopyFeatures_management(item,os.path.join(temp_workspace,feature))

		print("Done creating and calculating fields for", item)


print ("Completed at:", time.strftime('%a %H:%M:%S'))
