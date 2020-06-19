import multiprocessing
from xlsx2csv import Xlsx2csv
import time 
from time import process_time
import os

start=time.perf_counter()
excel_files=os.listdir("datasets")
processes=[]

def fileTicker(file):
    x=file.split("-")
    return(x[0])

def meta_extract(file):
    ticker=fileTicker(file)
    t1= process_time()
    Xlsx2csv("datasets/"+str(file), outputencoding="utf-8",include_sheet_pattern="^Data",).convert("META_FILES1/Data/"+str(ticker),sheetid=0)
    t2= process_time()
    print("Done Meta Extraction !!")
    print("Time take by "+str(file)+" is : ",(t2-t1),"sec")
    print("******************************************************************************")

for i in range(len(excel_files)):
    p=multiprocessing.Process(target=meta_extract,args=[excel_files[i]])
    p.start()
    processes.append(p)
for process in processes:
    process.join()

finish=time.perf_counter()
print("************* DONE EXTRACTING DATA SHEETS *************")
print("*******************************************************")
print("Total time for Stage III: "+str((finish-start)/60)+" minutes")
print("*******************************************************")
