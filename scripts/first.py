import petl as etl 
from xlsx2csv import Xlsx2csv
from time import process_time 
import os

excel_files=os.listdir("/home/sourav/Desktop/WORK/Coss_internship/MAIN_PROJECT/datasets")
time=[]

def fileTicker(file):
    x=file.split("-")
    return(x[0])

def meta_extract(file):
    ticker=fileTicker(file)
    t1= process_time()
    Xlsx2csv("/home/sourav/Desktop/WORK/Coss_internship/MAIN_PROJECT/datasets/"+str(file), outputencoding="utf-8",include_sheet_pattern="^Empirical Model",).convert("META_FILES/"+str(ticker)+"/Emperical",sheetid=0)
    Xlsx2csv("/home/sourav/Desktop/WORK/Coss_internship/MAIN_PROJECT/datasets/"+str(file), outputencoding="utf-8",include_sheet_pattern="^Regression Model",).convert("META_FILES/"+str(ticker)+"/Regression",sheetid=0)
    #Xlsx2csv("ABT - EndNov2018_Send.xlsx", outputencoding="utf-8",include_sheet_pattern="^Data",).convert("test/Data",sheetid=0)
    t2= process_time()
    print("Done Meta Extraction !!")
    print("Time take by "+str(file)+" is : ",(t2-t1),"sec")
    time.append(t2-t1)
    print("******************************************************************************")

for file in excel_files:
    meta_extract(file)

print("Total time : ",sum(time)," sec")