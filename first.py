import multiprocessing
from xlsx2csv import Xlsx2csv
import time 
import os

start=time.perf_counter()
excel_files=os.listdir("datasets")
processes=[]

def fileTicker(file):
    x=file.split("-")
    return(x[0])

def meta_extract(file):
    ticker=fileTicker(file)
    Xlsx2csv("datasets/"+str(file), outputencoding="utf-8",include_sheet_pattern="^Empirical Model",).convert("META_FILES1/"+str(ticker),sheetid=0)
    Xlsx2csv("datasets/"+str(file), outputencoding="utf-8",include_sheet_pattern="^Emperical Model",).convert("META_FILES1/"+str(ticker),sheetid=0)
    Xlsx2csv("datasets/"+str(file), outputencoding="utf-8",include_sheet_pattern="^Regression Model",).convert("META_FILES1/"+str(ticker),sheetid=0)
        
for i in range(len(excel_files)):
    p=multiprocessing.Process(target=meta_extract,args=[excel_files[i]])
    p.start()
    processes.append(p)

for process in processes:
    process.join()

finish=time.perf_counter()


print("************************************************************")
print("Total time taken for Step I : "+str(finish-start)+" seconds")
print("************************************************************")
