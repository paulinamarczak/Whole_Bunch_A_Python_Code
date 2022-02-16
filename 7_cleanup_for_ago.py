#cleanup underscores in alias for AGO popup purposes
#May 17 2021
#Paulina Marczak
#Warnings: Any acronyms that should remain fully capitalized must be manually changed back after script has run, such as URL, ID, UTM, etc.


import os
import time

print ("Starting at:", time.strftime('%a %H:%M:%S'))
print ("Importing modules.")
import arcpy, os

from arcpy import env
import re

arcpy.env.overwriteOutput = True

#set workspace
script_dir = os.path.dirname(os.path.realpath(__file__))

#define workspace
Out_workspace = os.path.join(script_dir, "Processed_dikes_operational.gdb")

space_dictionary = {"_":" "}

#from python docs for .title()
def titlecase(s):
	return re.sub(r"[A-Za-z]+('[A-Za-z]+)?",
		lambda mo: mo.group(0).capitalize(),
		s)


for gdb, datasets, features in arcpy.da.Walk(Out_workspace, topdown= True, datatype= "FeatureClass"):

	for feature in features:
		item= (os.path.join(Out_workspace, feature))
		alias_dict = {f.aliasName: f.name for f in arcpy.ListFields(item) if not f.required}
		print (alias_dict)

		#replace underscores in field alias names and change all caps to sentence case
		for alias,fieldname in alias_dict.items():
			for underscore,space in space_dictionary.items():
				new_alias_name= re.sub(underscore, space, alias)
				new_alias_name_sentence_case = titlecase(new_alias_name)
				if alias != new_alias_name_sentence_case:
					print ("Replacing alias", alias, 'with', new_alias_name_sentence_case, "in", feature)
					#only change alias
					#you must change it to something completely different first, else the case change will not register
					#see https://support.esri.com/en/bugs/nimbus/TklNMTAxODEw
					arcpy.AlterField_management(item, fieldname, fieldname, "ESRI_bug_NIM101810")
					arcpy.AlterField_management(item, fieldname, fieldname, new_alias_name_sentence_case)

