#Paulina Marczak
#Jan 11 2021
#Purpose: Delete intermediary files in dike process
#Context: Classified1 and Classified both produced some dike and pertinence structures and we need to model the data to be standardized to BCGW.
#Context: Current dikes will be archived once the data cleanup is complete.
#Warnings: The script will fail if you have a field with an intial character length more than 30.
#Prerequisites: The data must be copied in the same directory as the script, in a folder named, "dikes_for_processing"
# There must be no coded-domain-to-text fields in the resultant line FC. 

import os
import time

print ("Starting at:", time.strftime('%a %H:%M:%S'))
print ("Importing modules.")
import arcpy

arcpy.env.overwriteOutput = True

#set workspace
#script dir=current working dir= where you saved this script
script_dir = os.path.dirname(os.path.realpath(__file__))

Out_workspace = os.path.join(script_dir, "Processed_dikes_operational.gdb")

#cleanup
# # #ONLY RUN IF YOU'RE CONFIDENT IN THE OUTPUT AND DONT HAVE TO RERUN ANYTHING
#Purpose: delete intermediate data
tables = arcpy.ListTables(Out_workspace)

for gdb, datasets, features in arcpy.da.Walk(Out_workspace, topdown= True):
	for feature in features:
		if not feature== "Flood_Protection_Works_Appurtenant_Structures" and not feature == "Flood_Protection_Works_Structural_Works" and not feature == "Flood_Protection_Works_Elevation_Points" and not feature == "Flood_Protection_Works_Appurtenance_Points" and not feature == "Flood_Protection_Works_Photo_Points": 
			feature_path = os.path.join(gdb, feature)
			try:
				arcpy.management.Delete(feature_path)
				print ("deleting intermediary feature", feature)
			except error:
				e = sys.exc_info()[1]
				print(e.args[0])
				print ("No file to delete")

