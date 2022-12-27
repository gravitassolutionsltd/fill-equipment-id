import pandas as pd
import time
import getpass

username = getpass.getuser()

file = open("../../bin/to_date.bin", "r")
check_date = file.read()
post_date = check_date.split("\n")[1].replace("/", "-")
file.close()

name = "WEEK 52 TOLLS (2022) AFP.xlsx"
masterfile = "amazon_lp_masterfile_12-22-22.xlsx"

# rawfiles_dir = "./raw_files/"
final_df = pd.read_excel(f"./raw_files/{name}")

lp_updated_mf = pd.read_excel(f"./master_files/{masterfile}",dtype=str)
lp_updated_mf_LP = pd.DataFrame(lp_updated_mf, columns=["LicenseplateID"])

# print(lp_updated_mf)

client_masterfile_amazon_TA = pd.read_excel(f"./master_files/{masterfile}",dtype=str, sheet_name="Transponder Assignments")
client_masterfile_amazon_PU = pd.read_excel(f"./master_files/{masterfile}",dtype=str, sheet_name="Power Units")
client_masterfile_amazon_REN = pd.read_excel(f"./master_files/{masterfile}",dtype=str, sheet_name="Rentals")

def value_not_okay(value):
    return (str(value).strip() == "-") or (str(value).strip() == "") or (str(value).strip() == "nan") or ("UNKNOWN" in str(value).strip()) or ("Unassigned" in str(value).strip())

start = time.time()
if not 'TRANSPONDER' in final_df.columns:
    final_df["TRANSPONDER"] = "-"
grouped_df = final_df.groupby(by=["LICENSE PLATE", "TRANSPONDER"])
df = pd.DataFrame()
print("Processing...................")
for group_name, group_df in grouped_df:
    lp = group_name[0]
    dnt = group_name[1]

    value = "-"
    if lp != "-":
        if len(lp_updated_mf[lp_updated_mf['License plate ID'].astype(str).str.contains(lp)]) > 0 and value_not_okay(value):
            value = lp_updated_mf[lp_updated_mf['License plate ID'].astype(str).str.contains(lp)]["Equipment ID"].iloc[0]
    if value_not_okay(value):   
        group_df["EquipmentID_LP_MF"] = "-"
    else:
        group_df["EquipmentID_LP_MF"] = value
    
    value = "-"
    if dnt != "-":
        if len(client_masterfile_amazon_TA[client_masterfile_amazon_TA["Transp. #"].astype(str).str.contains(str(dnt))]) > 0 and value_not_okay(value):
            value = client_masterfile_amazon_TA[client_masterfile_amazon_TA["Transp. #"].astype(str).str.contains(str(dnt))]["Equipment ID"].iloc[0]
    if lp != "-":
        if len(client_masterfile_amazon_TA[client_masterfile_amazon_TA["License plate ID"].astype(str).str.contains(str(lp))]) > 0 and value_not_okay(value):
            value = client_masterfile_amazon_TA[client_masterfile_amazon_TA["License plate ID"].astype(str).str.contains(str(lp))]["Equipment ID"].iloc[0]
    if value_not_okay(value):   
        group_df["EquipmentID_TA"] = "-"
    else:
        group_df["EquipmentID_TA"] = value

    value = "-"
    if lp != "-":
        if len(client_masterfile_amazon_PU[client_masterfile_amazon_PU["License plate ID"].astype(str).str.contains(str(lp))]) > 0 and value_not_okay(value):
            value = client_masterfile_amazon_PU[client_masterfile_amazon_PU["License plate ID"].astype(str).str.contains(str(lp))]["Equipment ID"].iloc[0]
    if value_not_okay(value):   
        group_df["EquipmentID_PU"] = "-"
    else:
        group_df["EquipmentID_PU"] = value

    value = "-"
    if lp != "-":
        if len(client_masterfile_amazon_REN[client_masterfile_amazon_REN["License plate ID"].astype(str).str.contains(str(lp))]) > 0 and value_not_okay(value):
            value = client_masterfile_amazon_REN[client_masterfile_amazon_REN["License plate ID"].astype(str).str.contains(str(lp))]["Equipment ID"].iloc[0]
    if value_not_okay(value):   
        group_df["EquipmentID_RENTALS"] = "-"
    else:
        group_df["EquipmentID_RENTALS"] = value

    df = pd.concat([df, group_df])

stop = time.time()
print(f"Time Taken: {stop - start}")
df.to_excel(f"./output_files/{name}", index=False)

