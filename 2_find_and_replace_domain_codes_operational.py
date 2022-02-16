#Paulina Marczak
#Jan 11 2021
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
input_workspace = os.path.join(script_dir, "dikes_for_processing_operational")

Out_workspace = os.path.join(script_dir, "Processed_dikes_operational.gdb")

# copy backup
backup_workspace = os.path.join(script_dir, "Processed_dikes_operational_1a_b_c_backup" + time.strftime('%a_%H_%M') + ".gdb")
arcpy.management.CreateFileGDB(script_dir, "Processed_dikes_operational_1a_b_c_backup" + time.strftime('%a_%H_%M') + ".gdb", "CURRENT")

for gdb, datasets, features in arcpy.da.Walk(Out_workspace, topdown= True, datatype= "FeatureClass"):
	for feature in features:
		if feature.endswith("backup"):
			arcpy.Delete_management(feature)
			print("deleted", feature)
		else:
			arcpy.CopyFeatures_management(os.path.join(Out_workspace,feature),os.path.join(backup_workspace,feature)) 
			print ("backed up step 1b output", feature)


#onlym merge with points
# points_merged = os.path.join(Out_workspace, "Flood_Protection_Works_Appurtenant_Structures")

elev_merged = os.path.join(Out_workspace, "Flood_Protection_Works_Elevation_Points")
appt_merged = os.path.join(Out_workspace, "Flood_Protection_Works_Appurtenance_Points")
photos_merged = os.path.join(Out_workspace, "Flood_Protection_Works_Photo_Points")

points_merged = []

points_merged.append(elev_merged)
points_merged.append(appt_merged)
points_merged.append(photos_merged)


lines_merged = os.path.join(Out_workspace, "Flood_Protection_Works_Structural_Works")

#We need to have aliases/names without underscores for the Flood Portal popups
for point_file in points_merged:
	for fieldName in [f.name for f in arcpy.ListFields(point_file)]:
		alias_name =fieldName.replace("_", " ")
		print ("Adding alias by replacing underscores to spaces from", fieldName, "to", alias_name)
		arcpy.AlterField_management(point_file, fieldName, fieldName, alias_name)

for fieldName1 in [f.name for f in arcpy.ListFields(lines_merged)]:
	try:
		alias_name1 =fieldName1.replace("_", " ")
		print ("Adding alias by replacing underscores to spaces from", fieldName1, "to", alias_name1)
		arcpy.AlterField_management(lines_merged, fieldName1, fieldName1, alias_name1)
	except:
		e = sys.exc_info()[1]
		print(e.args[0] , "this error passes because the field actually does exist, and it does actually change the alias, checked manually")


#make field mapping between what field to join on 

#first make dictionary to match the infields with the join fields
#still change fields to text if no domains available
#are all fields named the same? it will delete fields not nameed exactly as in list
#its okay if there are multiple domains, theyre duplicates, just use the first one
#just make sure table exists in both gdbs
#just save domain tables in output gdb folder. that way all of the domains are together with the point file

join_dict = {
					"WORKS_TYPE" : "WORKS_TYPE",
					"ACCESS_POINT_TYPE" : "ACCESS_TYPE",
					"ACCESS_POINT_SIDE" : "CROSSING",
					"ARMOURED_BANK_TYPE": "BANK_TYPE",
					"ARMOURED_BANK_SIDE" : "LEFT", #LEFTRIGHT in dikes_abk_point
					"CULVERT_MATERIAL" : "CULVERT_MAT",
					"CULVERT_END" : "CULVERT_END",
					"DROP_STRUCTURE_SIDE": "LEFT",
					"PROTECTION_POINT_END": "STREAM_1", #can also be STREAM domain #stream_2 in dike_photos
					"PROTECTION_POINT_TYPE": "PROTECTION_POINT_TYPE", #fix names?
					"PROTECTION_POINT_CONDITION": "CONDITION", #fix names?
					"FENCE_GATE_POINT_TYPE": "FENCE_GATE_POINT_TYPE", #fix names?
					"FLOOD_BOX_CONCRETE_INLET_IND": "YES_NO",
					"FLOOD_BOX_CONCRETE_OUTLET_IND": "YES_NO",
					"FLOOD_BOX_TRASH_RACK_IND": "YES_NO",
					"FLOOD_BOX_GATE_TYPE": "FLOOD_BOX_GATE_TYPE",
					"FLOOD_BOX_FUNCTIONAL_IND": "YES_NO_OTHER",  #fix names?
					"FOOT_BRIDGE_SIDE": "LEFT_1", #LEFTRIGHTMIDPOINT_1 #LEFTRIGHTMIDPOINTINT in Dike_APP_Point
					"FOOT_BRIDGE_MATERIAL": "CONCRETE",
					"GAUGE_TYPE": "GAUGE_TYPE",
					"GAUGE_READABILITY": "GAUGE_READABILITY",
					"MANHOLE_TYPE": "MANHOLE_TYPE",
					"PLATFORM_OBSTRUCTION_IND": "YES_NO", #fix names?
					"OUTLET_POINT_CONCRETE_IND": "YES_NO",
					"OUTLET_POINT_GATE_TYPE": "GATE_TYPE_1", #also OUTLET_POINT_GATE_TYPE
					"PUMP_HOUSE_BUILDING_MATERIAL": "CONCRETE",
					"PUMP_HOUSE_CORNER": "DIRECTION_1", #can also be DIRECTION #direction_2 in dike_photos
					"SIGN_MATERIAL": "WOOD", #can be WOOD_1
					"STAIRS_MATERIAL": "CONCRETE",
					"STAIRS_OBSTRUCTION_IND": "YES_NO",
					"STRUCTURE_MATERIAL": "CONCRETE", #can be CONCRETE_12
					#"MONUMENT_MARKINGS": "CONCRETE",
					"MONUMENT_TYPE": "MONUMENT_TYPE",
					"VEHICLE_BRIDGE_SIDE": "LEFT_1", #LEFTRIGHTMIDPOINT_1 #LEFTRIGHTMIDPOINTINT in Dike_APP_Point
					"VEHICLE_BRIDGE_END": "STREAM_1", #can be STREAM, STREAM_2
					"VEHICLE_BRIDGE_MATERIAL": "CONCRETE",
					"VEHICLE_BRIDGE_USAGE": "VEHICLE_USAGE",
					"WEIR_SIDE": "LEFT",
					"WEIR_MATERIAL": "CONCRETE"

}

#make sure nothing else is named with a .gdb extension. Change the name of the parent folder of BCGW_Dike_Survey_Region_2.gdb otherwise it will result in errors.
for gdb, datasets, features in arcpy.da.Walk(input_workspace, topdown= True):
	if gdb.endswith(".gdb"):
		print(gdb)

		domains = arcpy.da.ListDomains(gdb)

		for domain in domains:
			print('Domain name: {0}'.format(domain.name))
			if domain.domainType == 'CodedValue':
				domname= domain.name
				if " " in domname:
					domname_new= domname.replace(" ", "_")
					print ("Fixing domain", domname, "to", domname_new)
					arcpy.management.AlterDomain(gdb, domname, domname_new)
					# #step one move domain descriptions to table for each domain
					out_table = os.path.join(Out_workspace, domname_new)
					join_field = domname_new + "_code"
					description_field = domname_new + "_description"
					domname_new_path= os.path.join(Out_workspace, domname_new)
					print ("exporting", domname_new,  "to a domain table for replacement field")
					arcpy.management.Delete(domname_new_path)
					arcpy.management.DomainToTable(gdb, domname_new, out_table, join_field, description_field)

				else:
					out_table = os.path.join(Out_workspace, domname)
					join_field = domname + "_code"
					description_field = domname + "_description"
					domname_path= os.path.join(Out_workspace, domname)
					print ("exporting", domname,  "to a domain table for replacement field")
					arcpy.management.Delete(domname_path)
					arcpy.management.DomainToTable(gdb, domname, out_table, join_field, description_field)


for in_field, domain_name in join_dict.items():
	
	
	# print ("point item is", point_item)
	#the domain table (which is the table being joined) will have the same name as the domain that was originally assigned to the input gdbs.
	join_table = domain_name
	#print (join_table)
	join_field = domain_name + "_code"
	description_field = domain_name + "_description"
	join_table_path = os.path.join(Out_workspace, join_table)
	#if the field [in_field] in the merged points file  is the same name as the input field i extracted the domain from [which i then used to name the domain table],thereby having the same domain:
	# print (f"Attaching data to table {point_item} with input field {in_field} from domain table {join_table} using its join field {join_field}")
	#for rerunning, delete the joined fields first before proceeding
	[(arcpy.management.DeleteField(x, description_field)) for x in points_merged]
	# arcpy.management.DeleteField(point_item, description_field)
	[(arcpy.management.DeleteField(x, join_field)) for x in points_merged]
	#perform table join
	[(arcpy.JoinField_management(x, in_field, join_table_path, join_field))  for x in points_merged]
	# then delete the join_field and in_field, leaving only the domain description field
	print (f"Deleting extra fields from output file, {in_field} and {join_field}")
	[(arcpy.management.DeleteField(x, in_field)) for x in points_merged]
	[(arcpy.management.DeleteField(x, join_field)) for x in points_merged]
	#then rename the domain description field to be what the original in_field was
	print(f"Renaming domain description field {description_field} to {in_field}")
	rename_field = str(in_field)
	#rename the description of the domain to reflect the original field the domain was constraining, along with its alias
	[(arcpy.AlterField_management(x, description_field, rename_field, rename_field)) for x in points_merged]
	
print ("Completed at:", time.strftime('%a %H:%M:%S'))
