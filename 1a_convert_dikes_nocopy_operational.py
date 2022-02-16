#Paulina Marczak
#Jan 11 2021
#Purpose: Convert dikes and auxiliary dike data to standardized format based on "overview of geodatabase fields"
#Context: Classified
#Context: Classified
#Warnings: The script will fail if you have a field with an initial character length more than 30.
#Warnings: None of the input fields should already have the special character "_", if they do, change lines 403/472 to "/" or some other special character
#Warnings: WORKS_TYPE IS TEXT IN THE RAW POLYLINE DATA BUT FLOAT IN THE POINT DATA!!!! That is why they are different in the AddField function
#Prerequisites: The data must be copied in the same directory as the script, in a folder named, "dikes_for_processing"
#Prerequisites: Classified WORKS_TYPE was originally a text field, it was manually changed to a float field with the same WORKS_TYPE domain as Classified before running this script
#Prerequisites: Classified REGION and DIKING_AUTHORITY columns were populated manually. Please use Classified gdb from "F:" to copy and paste the data into the dikes_for_processing_operational folder when initializing the script
#Prerequisites: Must calculate Classified's easting and northing fields manually
# There must be no coded-domain-to-text fields in the resultant line FC. 
# There should be a WORKS_TYPE field calculated for Classified for the lines and point FCs, either 'DIKE' or 'Erosion Protection'
#For Classified, a manual X and Y column was calculated based on the UTM coordinates, with more significant digits than EASTING_X and NORTHING_Y. This was done using Calculate Geometry based on UTM Zone 9, 10, or 11 in ArcMap 
#Check the field "UTM" to determine which UTM zone to calculate the X and Y columns on. 
#Some manual editing occurred after step 5, that is some orphan dike merge into the final product, and some manual "add missing sections" which means
# "typically when I say these it's because the Classified "


import os
import time

print ("Starting script 1a at:", time.strftime('%a %H:%M:%S'))
print ("Importing modules.")
import arcpy, os

from arcpy import env
try:
	import pandas as pd
except ImportError:
	print ("No pandas found- must install from pip")
import csv
import re
from re import search
import logging

arcpy.env.overwriteOutput = True

#set workspace
script_dir = os.path.dirname(os.path.realpath(__file__))
#preprocessing workspace
input_workspace = os.path.join(script_dir, "dikes_for_processing_operational")

Out_workspace = os.path.join(script_dir, "Processed_dikes_operational.gdb")
arcpy.Delete_management(Out_workspace)
arcpy.management.CreateFileGDB(script_dir, "Processed_dikes_operational.gdb", "CURRENT")

# #check that you got the workspaces
# print("script is located in", script_dir)

# #Create new gdb to store results
# #Define variable to link to new gdb

#Save backup on if needed

for gdb, datasets, features in arcpy.da.Walk(Out_workspace, topdown= True, datatype= "FeatureClass"):
	for feature in features:
		if feature.endswith("backup"):
			arcpy.Delete_management(feature)
			print("deleted", feature)
		else:
			arcpy.CopyFeatures_management(os.path.join(Out_workspace,feature),os.path.join(backup_workspace,feature)) 
			print ("backed up step 1 output", feature)

arcpy.env.workspace = Out_workspace

#Wanted field list
#Purpose: To programatically exclude all other fields from the final merged dataset, that may be in the incoming datasets.
#Having these lists will delete the excess fields. Any field not listed in 
#these two lists will not be present in the resultant merged datasets.
#Q: How does that work with the addField functions later in the script? 
#A: If a field is in the addField command, but not in these initial lists, then
# the fields will be added, but they will be empty.
#Therefore, if you want to add a field to keep which is already present in the data, 
#make sure you add it in both the lists here, and the addField calls. 
#If adding a field not already present in the original input data, then just use an addField command 
#and use CalculateField with whatever new dataset its coming from.

#First, process Flood Data, rename fields, add new flood profile model date column
flood_dict = {
"EASTING_X" : "FLOOD_PROFILE_EASTING_X",
"NORTHING_Y": "FLOOD_PROFILE_NORTHING_Y",
"COMMENT" : "FLOOD_PROFILE_COMMENTS",
"COMMENTS" : "FLOOD_PROFILE_COMMENTS",
"DIKE_NO" : "DIKE_NUMBER",
"CHAINAGE" : "FLOOD_PROFILE_CHAINAGE",
"ELEVATION" : "FLOOD_PROFILE_ELEVATION_Z"
}

for gdb, datasets, features in arcpy.da.Walk(input_workspace, topdown= True):
	if gdb.endswith("FloodProfilesPoints_20210126.gdb"):
		for feature in features:
			item= (os.path.join(input_workspace,gdb, feature))
			for fieldName in [f.name for f in arcpy.ListFields(item) if not f.required]:
				for k,v in flood_dict.items():
					#find if its a standalone word (e.g., to replace whole names)
					flood_name= re.search('^' + k + '$', fieldName)

					if flood_name:
						try:
							new_flood_name= re.sub(k , v, fieldName)
							print ("Replacing field", fieldName, 'with', new_flood_name, "in", feature, "using replaced_name2 pattern")
							#add a way to identify the old fields, while giving it less than 30 character-limit length, so the fields can be copied over to the new fields easily
							arcpy.AlterField_management(item, fieldName, new_flood_name, new_flood_name)
						except:
							e = sys.exc_info()[1]
							print(e.args[0] , "this error passes because the Regex is run twice")

			#add one new field
			print ("Adding and calculating flood profile model date")
			fieldName= "FLOOD_PROFILE_MODEL_DATE"
			arcpy.management.DeleteField(item, "FLOOD_PROFILE_MODEL_DATE")
			#02 = 3rd month = march
			arcpy.AddField_management(item,fieldName, "DATE")
			arcpy.CalculateField_management(item, fieldName, "Date(2014,02,01)" , "ARCADE" )

#LINES
#to get this list, simply paste transpose the polyline excel fields in a new sheet, and cleanup any "name changes"
# copy to a blank sublime session, and highlight the whole list with your cursor, then CTRL+SHIFT+L to get your cursor on the end of each list item, then press right arrow to remove the highlight.
# add a comma, then unselect all. Delete the comma after the last item, and then paste into this list.
#additionally, dont copy over the fields that are coloured grey, theyre not being used.
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

#POINTS
#to get this list, simply paste transpose the point excel fields in a new sheet, and cleanup any "name changes"
# copy to a blank sublime session, and highlight the whole list with your cursor, then CTRL+SHIFT+L to get your cursor on the end of each list item, then press right arrow to remove the highlight.
# add a comma, then unselect all. Delete the comma after the last item, and then paste into this list.
#additionally, dont copy over the fields that are coloured grey, theyre not being used.
#then add DATA_LAYER_SOURCE, which is not in the spreadsheet.

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

#Add regex conversions to match_dict if they occur as partial words within the field name.
match_dict = {
"PT":"POINT",
"MAT": "MATERIAL",
"COND": "CONDITION",
"FUNCT": "FUNCTIONAL",
"OBS": "OBSTRUCTION",
"STRUCT": "STRUCTURE",
"NUM" : "NUMBER",
"DIMENTIONS" : "DIMENSIONS",
}


#Must use a separate regex loop for entire-field renaming operations, add those to match_dict_2. 
#There is a known bug in arcpy with changing field case, so be careful to make sure its converted properly
#Region and Dike_Name are susceptible to the bug, so change these fields manually before starting script
match_dict_2 = {
"FLOOD_BOX_CONCRETE_OUTLET" : "FLOOD_BOX_CONCRETE_OUTLET_IND",
"EXISTING_GPS" : "DIKE_NUMBER",
"EASTING_X" :"CREST_EASTING_X",
"NORTHING_Y": "CREST_NORTHING_Y",
"CHAINAGE": "CREST_CHAINAGE",
"SURVEY_DATE" : "CREST_SURVEY_DATE", #yes, survey date is crest survey date
"LENGTH_M" : "SEGMENT_LENGTH_M",
"x" :"CREST_EASTING_X",
"y": "CREST_NORTHING_Y",
"COMMENT" : "COMMENTS",
"APPURTENANT_STRUCT_NUM": "APPURTENANT_STRUCTURE_NUMBER",
"H2013_2002" : "CREST_ELEVATION_Z", #FOR Classified POINTS- the original elevation column was converted from 1928 datum to 2013 datum using 2002 epoch based on Classified's surveying.
"Dike_GPS_N" : "DIKE_NUMBER", #FOR ORPHAN DIKE LINES FIELD NAME RENAMING
"Dike_Name" : "DIKE_NAME",  #FOR ORPHAN DIKE LINES FIELD NAME RENAMING
"Watercours" : "WATER_COURSE",  #FOR ORPHAN DIKE LINES FIELD NAME RENAMING
"Descriptio" : "COMMENTS", #FOR ORPHAN DIKE LINES FIELD NAME RENAMING
"SHAPE_Leng" : "SEGMENT_LENGTH_M", #FOR ORPHAN DIKE LINES FIELD NAME RENAMING
"Region" : "REGION", #FOR ORPHAN DIKE LINES FIELD NAME RENAMING
"Local_Gove" : "DIKING_AUTHORITY", #FOR ORPHAN DIKE LINES FIELD NAME RENAMING
#"OnPrivateL" : "" #not included because its "the private individual was supposed to identify a diking authority that is a person, so doesn't apply to orphan dike.  And private dike is not defined only by the dike being on private land"
"FLDPRTCTNS" : "DIKE_NUMBER",
#"POINT_TYPE" : "WORKS_TYPE", #just use works_type field that was manually generated
"ELEVATION_Z" : "CREST_ELEVATION_Z",
# "CREST_ELEVATION" : "CREST_ELEVATION_Z"
#CREST ELEVATION ARE SUPPOSED TO BE DELETED IN DIKE LINES - REMINDER.
}

Classified_layers= ['Dikes_Appert',
				'Riprap']

direction_layers = ['EASTING_X',
					'NORTHING_Y']

#copy all to one gdb in order to set domains properly, etc.
#add regex to keep all names consistent if names have shortform
for gdb, datasets, features in arcpy.da.Walk(input_workspace, topdown= True, datatype= "FeatureClass"):
	for feature in features:
		item= (os.path.join(input_workspace,gdb, feature))
		for fieldName in [f.name for f in arcpy.ListFields(item) if not f.required]:

			#Deleting the less precise easting and northing for Classified here
			#generated manually a new x and y field for Classified layers with more precise UTM in ArcMap
			#( Calculate Geometry using UTM zone 10 or 11 depending on UTM zone of feature class)
			
			#could it be looped better? yes. but it does the job
			for i in Classified_layers:
				for j in direction_layers: 
					if fieldName.startswith(j):
						print ("Deleting imprecise duplicate fields", fieldName, "in", feature)
						arcpy.management.DeleteField(item, fieldName)

	for feature in features:
		item= (os.path.join(input_workspace,gdb, feature))
		for fieldName in [f.name for f in arcpy.ListFields(item) if not f.required]:

			#Run a separate regex for whole-field substitutions, given that neither dictionaries contain within them the same words
			for k,v in match_dict_2.items():
				#find if its a standalone word (e.g., to replace whole names)
				replaced_name2= re.search('^' + k + '$', fieldName)

				if replaced_name2:
					try:
						replacement_name= re.sub(k , v, fieldName)
						print ("Replacing field", fieldName, 'with', replacement_name, "in", feature, "using replaced_name2 pattern")
						#add a way to identify the old fields, while giving it less than 30 character-limit length, so the fields can be copied over to the new fields easily
						arcpy.AlterField_management(item, fieldName, replacement_name, replacement_name)
					except:
						e = sys.exc_info()[1]
						print(e.args[0] , "this error passes because the Regex is run twice")


			#alter the field if the field contains the shortform 
			for k,v in match_dict.items():
				#find when its the last word (e..g,  PUMP_HOUSE_BUILDING_MAT)
				replaced_name1 = re.search('[_]' + k + "$", fieldName)
				replaced_name_ = re.search('[_]' + k + '[_]', fieldName)

				if replaced_name1:
					try:
						#only match if k is not at the beginning of the phrase
						replacement_name= re.sub('_' + k , '_' + v, fieldName)
						print ("Replacing field", fieldName, 'with', replacement_name, "in", feature, "using replaced_name/1 pattern")
						#add a way to identify the old fields, while giving it less than 30 character-limit length, so the fields can be copied over to the new fields easily
						arcpy.AlterField_management(item, fieldName, replacement_name, replacement_name)

						for k,v in match_dict.items():
							#now do regex search in updated field to change second componenet of string
							replaced_name_ = re.search('[_]' + k + '[_]', replacement_name)

							if replaced_name_:
								#twice
								replacement_name_= re.sub('_' + k , '_' + v, replacement_name)
								print ("Replacing field", replacement_name, 'with', replacement_name_, "in", feature, "using replaced_name/1 pattern twice")
								arcpy.AlterField_management(item, replacement_name, replacement_name_, replacement_name_)
					except:
						e = sys.exc_info()[1]
						print(e.args[0], "this error passes because the Regex is run twice or the field was just deleted")

				if replaced_name_:
					try:
						#only match if k is not at the beginning of the phrase
						replacement_name= re.sub('_' + k, '_' + v, fieldName)
						print ("Replacing field", fieldName, 'with', replacement_name, "in", feature, "using replaced_name_/2 pattern")
						#add a way to identify the old fields, while giving it less than 30 character-limit length, so the fields can be copied over to the new fields easily
						arcpy.AlterField_management(item, fieldName, replacement_name, replacement_name)

						for k,v in match_dict.items():
							#now do regex search in updated field to change second componenet of string
							replaced_name_ = re.search('[_]' + k + '$', replacement_name)

							if replaced_name_:
								#twice
								replacement_name_= re.sub('_' + k , '_' + v, replacement_name)
								print ("Replacing field", replacement_name, 'with', replacement_name_, "in", feature, "using replaced_name_/2 pattern twice")
								arcpy.AlterField_management(item, replacement_name, replacement_name_, replacement_name_)

							for k,v in match_dict.items():
								#now do regex search in updated field to change second componenet of string
								replaced_name_ = re.search('[_]' + k + '_', replacement_name)

								if replaced_name_:
									#twice
									replacement_name_= re.sub('_' + k , '_' + v, replacement_name)
									print ("Replacing field", replacement_name, 'with', replacement_name_, "in", feature, "using replaced_name_/2 pattern twice")
									arcpy.AlterField_management(item, replacement_name, replacement_name_, replacement_name_)
					except:
						e = sys.exc_info()[1]
						print(e.args[0], "this error passes because the Regex is run twice or the field was just deleted")


			
		save = os.path.join(Out_workspace, feature + "_copy")
		arcpy.management.Delete(save)
		arcpy.CopyFeatures_management(os.path.join(gdb,feature),os.path.join(Out_workspace,save)) 
		print ("copied feature class", feature, "to", Out_workspace)

print ("Completed at:", time.strftime('%a %H:%M:%S'))
