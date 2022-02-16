#fill in more fields like contact info for dike portal
#sept 20 2021
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
LUT = pd.read_csv(os.path.join(script_dir, "LUT2.csv"), encoding='cp1252')
#print (LUT)
LUT.columns = [
"DIKE_NUMBER",
"WORKS_TYPE_ADDITIONAL_INFO",
"TOTAL_LENGTH_M",
"BANK_PROTECTION_LENGTH",
"OBJECT_ID",
"DIKE_CONSEQUENCE",
"DIKE_RISK",
"PRIVATE_INDIVIDUAL",
"DIKE_AUTH_MAILING_ADDRESS_1",
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
"DIKE_NAME",
"DIKE_AUTH_MAILING_ADDRESS_2",
"DIKE_AUTH_MAILING_ADDRESS_3"
] #rename list


column_names = LUT.columns

LUT = LUT.reindex(columns=column_names)

LUT = LUT.to_dict('records')

fields = column_names


feature_list = LUT #updated to spreadsheet dictionary


for gdb, datasets, features in arcpy.da.Walk(Out_workspace, topdown= True, datatype= "FeatureClass"):

	for feature in features:
		item= (os.path.join(Out_workspace,gdb, feature))
		# if feature == "dike_14_test": # test on one feature
		if feature == "Flood_Protection_Works_Structural_Works": # test on one feature
			for dictionary in feature_list:
				with arcpy.da.UpdateCursor(item, fields) as cursor:
					print(fields)
					for row in cursor:
						#Change some fields to private individual if owned by private owner
						if row[0]== 56 or row[0]==272 or row[0]==273 or row[0]==274 or row[0]==275 or row[0]==88 or row[0]==299:
							print (row, dictionary["DIKE_NUMBER"])
							for i in row:
								row[1] = dictionary["WORKS_TYPE_ADDITIONAL_INFO"] #["DIKE_NUMBER"]
								row[2] = dictionary["TOTAL_LENGTH_M"]
								row[3] = dictionary["BANK_PROTECTION_LENGTH"]
								row[4] = dictionary["OBJECT_ID"]
								row[5] = dictionary["DIKE_CONSEQUENCE"]
								row[6] = dictionary["DIKE_RISK"]
								row[7] = dictionary["PRIVATE_INDIVIDUAL"]
								row[8] = "Private Individual"
								row[9] = dictionary["DIKE_AUTH_CITY"]
								row[10] = dictionary["DIKE_AUTH_PROVINCE"]
								row[11] = "Private Individual"
								row[12] = dictionary["DIKE_AUTH_COUNTRY"]
								row[13] = "Private Individual"
								row[14] = "Private Individual"
								row[15] = "Private Individual"
								row[16] = dictionary["EPA_LOCAL_AUTHORITY"]
								row[17] = dictionary["DMA_REGULATED"]
								row[18] = dictionary["PRIVATE_DIKE"]
								row[19] = dictionary["RIGHT_OF_WAY"]
								row[20] = dictionary["RIGHT_OF_WAY_COMMENTS"]
								row[21] = dictionary["DESIGN_RETURN_PERIOD"]
								row[22] = dictionary["DIKING_AUTHORITY_TYPE"]
								row[23] = dictionary["SERVICE_AREA"]
								row[24] = dictionary["LAND_USE"]
								row[25] = dictionary["INFRASTRUCTURE_PROTECTED"]
								row[26] = dictionary["BUILDINGS_PROTECTED"]
								row[27] = "Private Individual"
								row[28] = "Private Individual"
								row[29] = "Private Individual"
								print ("dike", row[0], row[2], row[13], row[14], row[15], "match found for missing data in row", dictionary["DIKE_NUMBER"], "in", feature, "using", dictionary)
								cursor.updateRow(row)
						elif row[0]==dictionary["DIKE_NUMBER"]: #change fields for ALL rows
							print (row, dictionary["DIKE_NUMBER"])
							for i in row:
								row[1] = dictionary["WORKS_TYPE_ADDITIONAL_INFO"] #["DIKE_NUMBER"]
								row[2] = dictionary["TOTAL_LENGTH_M"]
								row[3] = dictionary["BANK_PROTECTION_LENGTH"]
								row[4] = dictionary["OBJECT_ID"]
								row[5] = dictionary["DIKE_CONSEQUENCE"]
								row[6] = dictionary["DIKE_RISK"]
								row[7] = dictionary["PRIVATE_INDIVIDUAL"]
								row[8] = dictionary["DIKE_AUTH_MAILING_ADDRESS_1"]
								row[9] = dictionary["DIKE_AUTH_CITY"]
								row[10] = dictionary["DIKE_AUTH_PROVINCE"]
								row[11] = dictionary["DIKE_AUTH_POSTAL"]
								row[12] = dictionary["DIKE_AUTH_COUNTRY"]
								row[13] = dictionary["PRINCIPAL_CONTACT_NAME"]
								row[14] = dictionary["PRINCIPAL_DEFAULT_PHONE"]
								row[15] = dictionary["PRINCIPAL_EMAIL"]
								row[16] = dictionary["EPA_LOCAL_AUTHORITY"]
								row[17] = dictionary["DMA_REGULATED"]
								row[18] = dictionary["PRIVATE_DIKE"]
								row[19] = dictionary["RIGHT_OF_WAY"]
								row[20] = dictionary["RIGHT_OF_WAY_COMMENTS"]
								row[21] = dictionary["DESIGN_RETURN_PERIOD"]
								row[22] = dictionary["DIKING_AUTHORITY_TYPE"]
								row[23] = dictionary["SERVICE_AREA"]
								row[24] = dictionary["LAND_USE"]
								row[25] = dictionary["INFRASTRUCTURE_PROTECTED"]
								row[26] = dictionary["BUILDINGS_PROTECTED"]
								print ("dike", row[0], row[2], row[13], row[14], row[15], "match found for missing data in row", dictionary["DIKE_NUMBER"], "in", feature, "using", dictionary)
								cursor.updateRow(row)
							else:
								continue
