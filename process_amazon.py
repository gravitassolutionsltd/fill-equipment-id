import pandas as pd
import time
import os
import re
import getpass
from datetime import timedelta, datetime
from py_console import console

username = getpass.getuser()

file = open("../../bin/to_date.bin", "r")
check_date = file.read()
post_date = check_date.split("\n")[1].replace("/", "-")
file.close()

name = "WEEK 51 TOLLS (2022) TRAILERS.xlsx"
masterfile = "amazon_lp_masterfile_12-22-22.xlsx"

# rawfiles_dir = "./raw_files/"
final_df = pd.read_excel(f"./raw_files/{name}")
if not 'TRANSPONDER' in final_df.columns:
    final_df["TRANSPONDER"] = "-"

lp_updated_mf = pd.read_excel(f"./master_files/{masterfile}",dtype=str)
lp_updated_mf_LP = pd.DataFrame(lp_updated_mf, columns=["LicenseplateID"])

# print(lp_updated_mf)

client_masterfile_amazon_TA = pd.read_excel(f"./master_files/{masterfile}",dtype=str, sheet_name="Transponder Assignments")
client_masterfile_amazon_PU = pd.read_excel(f"./master_files/{masterfile}",dtype=str, sheet_name="Power Units")
client_masterfile_amazon_REN = pd.read_excel(f"./master_files/{masterfile}",dtype=str, sheet_name="Rentals")


print("Updating Equipment ID from LP Masterfile")
def add_eqid(lp):
    # dnt = str(dnt).replace("DNT.", "").replace("DFW.", "").strip()
    lp = str(lp).strip()
    value = "-"
    def value_not_okay(value):
        return (str(value).strip() == "-") or (str(value).strip() == "") or (str(value).strip() == "nan") or ("UNKNOWN" in str(value).strip()) or ("Unassigned" in str(value).strip())

    # if dnt != "-":
    #     if len(lp_updated_mf[lp_updated_mf['DNT'].astype(str).str.contains(dnt)]) > 0 and value_not_okay(value):
    #         value = lp_updated_mf[lp_updated_mf['DNT'].astype(str).str.contains(dnt)]["Unit #"].iloc[0]
    if lp != "-":
        if len(lp_updated_mf[lp_updated_mf['License plate ID'].astype(str).str.contains(lp)]) > 0 and value_not_okay(value):
            value = lp_updated_mf[lp_updated_mf['License plate ID'].astype(str).str.contains(lp)]["Equipment ID"].iloc[0]
    if value_not_okay(value):   
        return "-"
    else:
        return value
final_df["EquipmentID_LP_MF"] = list(map(add_eqid, final_df["LICENSE PLATE"]))


print("Updating Equipment ID from Client MF Transponder Assignment Sheet ")
def add_eqid(dnt, lp):
    dnt = str(dnt).replace("DNT.", "").replace("DFW.", "").strip()
    lp = str(lp).strip()
    lp2 = dnt
    value = "-"
    def value_not_okay(value):
        return (str(value).strip() == "-") or (str(value).strip() == "") or (str(value).strip() == "nan") or ("UNKNOWN" in str(value).strip()) or ("Unassigned" in str(value).strip())
        
    if dnt != "-":
        if len(client_masterfile_amazon_TA[client_masterfile_amazon_TA["Transp. #"].astype(str).str.contains(str(dnt))]) > 0 and value_not_okay(value):
            value = client_masterfile_amazon_TA[client_masterfile_amazon_TA["Transp. #"].astype(str).str.contains(str(dnt))]["Equipment ID"].iloc[0]
        # if len(client_masterfile_amazon_TA[client_masterfile_amazon_TA["Transp. #"].astype(str).str.contains(str(dnt))]) > 0 and value_not_okay(value):
        #     value = client_masterfile_amazon_TA[client_masterfile_amazon_TA["Transp. #"].astype(str).str.contains(str(dnt))]["Equip ID"].iloc[0]

    if lp != "-":
        if len(client_masterfile_amazon_TA[client_masterfile_amazon_TA["License plate ID"].astype(str).str.contains(str(lp))]) > 0 and value_not_okay(value):
            value = client_masterfile_amazon_TA[client_masterfile_amazon_TA["License plate ID"].astype(str).str.contains(str(lp))]["Equipment ID"].iloc[0]
        # if len(client_masterfile_amazon_TA[client_masterfile_amazon_TA["License plate ID"].astype(str).str.contains(str(lp))]) > 0 and value_not_okay(value):
        #     value = client_masterfile_amazon_TA[client_masterfile_amazon_TA["License plate ID"].astype(str).str.contains(str(lp))]["Equip ID"].iloc[0]
    if lp2 != "-":
        if len(client_masterfile_amazon_TA[client_masterfile_amazon_TA["Transp. #"].astype(str).str.contains(str(lp2))]) > 0 and value_not_okay(value):
            value = client_masterfile_amazon_TA[client_masterfile_amazon_TA["Transp. #"].astype(str).str.contains(str(lp2))]["Equipment ID"].iloc[0]

    if value_not_okay(value):   
        return "-"
    else:
        return value  
final_df["EquipmentID_TA"] = list(map(add_eqid, final_df["TRANSPONDER"], final_df["LICENSE PLATE"]))


print("Updating Equip ID from Client MF Transponder Assignment Sheet ")
def add_eqid(dnt, lp):
    dnt = str(dnt).replace("DNT.", "").replace("DFW.", "").strip()
    lp = str(lp).strip()
    lp2 = dnt
    value = "-"
    def value_not_okay(value):
        return (str(value).strip() == "-") or (str(value).strip() == "") or (str(value).strip() == "nan") or ("UNKNOWN" in str(value).strip()) or ("Unassigned" in str(value).strip())
        
    if dnt != "-":
        if len(client_masterfile_amazon_TA[client_masterfile_amazon_TA["Transp. #"].astype(str).str.contains(str(dnt))]) > 0 and value_not_okay(value):
            value = client_masterfile_amazon_TA[client_masterfile_amazon_TA["Transp. #"].astype(str).str.contains(str(dnt))]["Equip ID"].iloc[0]

    if lp != "-":
        if len(client_masterfile_amazon_TA[client_masterfile_amazon_TA["License plate ID"].astype(str).str.contains(str(lp))]) > 0 and value_not_okay(value):
            value = client_masterfile_amazon_TA[client_masterfile_amazon_TA["License plate ID"].astype(str).str.contains(str(lp))]["Equip ID"].iloc[0]

    if lp2 != "-":
        if len(client_masterfile_amazon_TA[client_masterfile_amazon_TA["Transp. #"].astype(str).str.contains(str(lp2))]) > 0 and value_not_okay(value):
            value = client_masterfile_amazon_TA[client_masterfile_amazon_TA["Transp. #"].astype(str).str.contains(str(lp2))]["Equip ID"].iloc[0]

    if value_not_okay(value):   
        return "-"
    else:
        return value  
final_df["Equip ID_TA"] = list(map(add_eqid, final_df["TRANSPONDER"], final_df["LICENSE PLATE"]))


# check_unit = final_df[(final_df["TRANSPONDER"] == "-") | (~final_df["TRANSPONDER"].notnull())]
# final_df = final_df.drop(index=check_unit.index)

print("Updating Equipment ID from Client MF Power Unit Sheet")
def add_eqid(lp):
    # dnt = str(dnt).replace("DNT.", "").replace("DFW.", "").strip()
    lp = str(lp).strip()
    value = "-"
    def value_not_okay(value):
        return (str(value).strip() == "-") or (str(value).strip() == "") or (str(value).strip() == "nan") or ("UNKNOWN" in str(value).strip()) or ("Unassigned" in str(value).strip())
        
    # if dnt != "-":
    #     if len(client_masterfile_amazon[client_masterfile_amazon["Transp. #"].astype(str).str.contains(str(dnt))]) > 0 and value_not_okay(value):
    #         value = client_masterfile_amazon[client_masterfile_amazon["Transp. #"].astype(str).str.contains(str(dnt))]["Equipment ID"].iloc[0]

    if lp != "-":
        if len(client_masterfile_amazon_PU[client_masterfile_amazon_PU["License plate ID"].astype(str).str.contains(str(lp))]) > 0 and value_not_okay(value):
            value = client_masterfile_amazon_PU[client_masterfile_amazon_PU["License plate ID"].astype(str).str.contains(str(lp))]["Equipment ID"].iloc[0]

    if value_not_okay(value):   
        return "-"
    else:
        return value  
final_df["EquipmentID_PU"] = list(map(add_eqid, final_df["LICENSE PLATE"]))

print("Updating Equipment ID from Client MF Rentals Sheet")
def add_eqid(lp):
    # dnt = str(dnt).replace("DNT.", "").replace("DFW.", "").strip()
    lp = str(lp).strip()
    value = "-"
    def value_not_okay(value):
        return (str(value).strip() == "-") or (str(value).strip() == "") or (str(value).strip() == "nan") or ("UNKNOWN" in str(value).strip()) or ("Unassigned" in str(value).strip())
        
    # if dnt != "-":
    #     if len(client_masterfile_amazon[client_masterfile_amazon["Transp. #"].astype(str).str.contains(str(dnt))]) > 0 and value_not_okay(value):
    #         value = client_masterfile_amazon[client_masterfile_amazon["Transp. #"].astype(str).str.contains(str(dnt))]["Equipment ID"].iloc[0]

    if lp != "-":
        if len(client_masterfile_amazon_REN[client_masterfile_amazon_REN["License plate ID"].astype(str).str.contains(str(lp))]) > 0 and value_not_okay(value):
            value = client_masterfile_amazon_REN[client_masterfile_amazon_REN["License plate ID"].astype(str).str.contains(str(lp))]["Equipment ID"].iloc[0]

    if value_not_okay(value):   
        return "-"
    else:
        return value  
final_df["EquipmentID_RENTALS"] = list(map(add_eqid, final_df["LICENSE PLATE"]))


final_df.to_excel(f"./output_files/{name}", index=False)

