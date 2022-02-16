#1c merge the resulting altered feature classes with ease

import os
import time

print ("Starting at:", time.strftime('%a_%H:%M:%S'))
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
backup_workspace = os.path.join(script_dir, "Processed_dikes_operational_1b_backup" + time.strftime('%a_%H_%M') + ".gdb")
arcpy.management.CreateFileGDB(script_dir, "Processed_dikes_operational_1b_backup" + time.strftime('%a_%H_%M') + ".gdb", "CURRENT")

for gdb, datasets, features in arcpy.da.Walk(Out_workspace, topdown= True, datatype= "FeatureClass"):
	for feature in features:
		if feature.endswith("backup"):
			arcpy.Delete_management(feature)
			print("deleted", feature)
		else:
			arcpy.CopyFeatures_management(os.path.join(Out_workspace,feature),os.path.join(backup_workspace,feature)) 
			print ("backed up step 1b output", feature)

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
		shapeType = arcpy.Describe(item).shapeType
		# Since all features have identical fields, no field mapping 
		# is required
		#gather all the output generated files, and merge Flood_Protection_Works_Structural_Works and points, respectively.
		
		if shapeType == "Polyline" and not feature == "Flood_Protection_Works_Structural_Works": 
			LineList.append(item)
			print ("added", feature, "to merge list for Flood_Protection_Works_Structural_Works")
			counting_in_poly = arcpy.management.GetCount(item)
			counting_in_poly = int(counting_in_poly.getOutput(0))
			count_list_poly.append(counting_in_poly)

		#First is non-appurtenance, non-photo points, so add classified here
		if feature.startswith("Dikes_ABK_Point") or feature.startswith("Dikes_DCL_Point") or feature.startswith("classified_points") or feature.startswith("Flood_Profiles"):
			PointList_alignment_elevation.append(item)
			print ("added", feature, "to merge list for elevation points")
			counting_in_point_elev = arcpy.management.GetCount(item)
			counting_in_point_elev = int(counting_in_point_elev.getOutput(0))
			count_list_point.append(counting_in_point_elev)

		#second is appurtenant
		elif feature.startswith("Dikes_Appert") or feature.startswith("Dike_APP_Point") or feature.startswith("Riprap") or feature.startswith("FPW_AS_SVW_point_selected_for_merging"):
			PointList_appurtenances.append(item)
			print ("added", feature, "to merge list for appurtenances points")
			counting_in_point_appurtenances = arcpy.management.GetCount(item)
			counting_in_point_appurtenances = int(counting_in_point_appurtenances.getOutput(0))
			count_list_point.append(counting_in_point_appurtenances)

		#third is photos
		elif shapeType == "Point" and feature.startswith("Photos_Survey") or feature.startswith("Dike_Photos"):
			PointList_photos.append(item)
			print ("added", feature, "to merge list for photos points")
			counting_in_point_photos = arcpy.management.GetCount(item)
			counting_in_point_photos = int(counting_in_point_photos.getOutput(0))
			count_list_point.append(counting_in_point_photos)


lines_merged = os.path.join(Out_workspace, "Flood_Protection_Works_Structural_Works")

points_merged = os.path.join(Out_workspace, "Flood_Protection_Works_Appurtenant_Structures")

elev_merged = os.path.join(Out_workspace, "Flood_Protection_Works_Elevation_Points")
appt_merged = os.path.join(Out_workspace, "Flood_Protection_Works_Appurtenance_Points")
photos_merged = os.path.join(Out_workspace, "Flood_Protection_Works_Photo_Points")

store_point_merged = []
store_point_merged.append(elev_merged)
store_point_merged.append(appt_merged)
store_point_merged.append(photos_merged)


point_dict = zip(store_point_list, store_point_merged)

count_list_poly_merge = []

count_list_point_merge = []

# count_list_point_merge_elev = []
# count_list_point_merge_appurtenance = []
# count_list_point_merge_photos = []

# count_list_point_merge.append(count_list_point_merge_elev)
# count_list_point_merge.append(count_list_point_merge_appurtenance)
# count_list_point_merge.append(count_list_point_merge_photos)

#merge
#if there are features to merge
if len(LineList) > 1:
	print ("merging lines to", lines_merged)
	print (LineList)
	#sometimes the FC doesnt like being deleted, if it fails on this line, delete the merged feature class manually in ArcMap/Pro before continuing with Merge. 
	try:
		arcpy.management.Delete(lines_merged)
	except error:
		e = sys.exc_info()[1]
		print(e.args[0])
		print ("No file to delete")
	merged_poly = arcpy.Merge_management(LineList, lines_merged)

	print ("Successfully merged all dike line data to", lines_merged)

	#extract row count from a string output
	counting_out_poly = arcpy.management.GetCount(merged_poly)
	counting_out_poly = int(counting_out_poly.getOutput(0))
	count_list_poly_merge.append(counting_out_poly)

#merge if there are more than 1 features to merge
#point list is i, point merged is v
for i,v in point_dict:
	print ("merging points to", v)
	print (i)
	##sometimes the FC doesnt like being deleted, if it fails on this line, delete the merged feature class manually in ArcMap/Pro before continuing with Merge. 
	try:
		arcpy.management.Delete(v)
	except error:
		e = sys.exc_info()[1]
		print(e.args[0])
		print ("No file to delete")
	try:
		merged_points = arcpy.Merge_management(i, v)
	except error:
		e = sys.exc_info()[1]
		print(e.args[0])
		print ("Not enough files to merge")
	
	print ("Successfully merged all dike point data to", v)

	##extract row count from a string output and add to list to sum the number of rows
	counting_out_point = arcpy.management.GetCount(v)
	counting_out_point = int(counting_out_point.getOutput(0))
	#still have just one list to sum points outputs
	count_list_point_merge.append(counting_out_point)


#quick QC check
#number of rows comparison
print ("Validation Time!...")
print ('...For Flood_Protection_Works_Structural_Works, the input rows of all input features sum to {} and the output rows sum to {}.'.format(sum(count_list_poly), sum(count_list_poly_merge)))
print ('...For points, the input rows of all input features sum to {} and the output rows sum to {}.'.format(sum(count_list_point), sum(count_list_point_merge)))
print ("If the numbers match, success, if they don't match, please double-check any commented out lines of code, check the field names, and check the original data and rerun code, make sure all the FCs are there, and that there are no duplicates")
print("Make sure to manually inspect the data in ArcPro before using as production")


print ("Completed at:", time.strftime('%a %H:%M:%S'))
