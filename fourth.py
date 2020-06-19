import mysql.connector
import schedule
from mysql.connector import Error
import os
import pandas as pd
import re
from datetime import datetime
import time 

start=time.perf_counter()

RDS_HOST=os.environ['RDS_HOST']
DATABASE=os.environ['DATABASE']
USER =os.environ['RDS_USER']
PASSWORD=os.environ['RDS_PASS']

def data_extractor(folder,file,count,pos):
    reqd_header={'Date', 'FacilityType', 'BedSize', 'Region', 'Manufacturer', 'Ticker', 'Group', 'Therapy', 'Anatomy','SubAnatomy', 'ProductCategory', 'Quantity', 'AvgPrice', 'TotalSpend'}
    dataset = pd.read_csv("/home/sourav/Desktop/WORK/Coss_internship/MAIN_PROJECT/META_FILES1/Data/"+str(folder)+"/"+str(file),low_memory=False,nrows=1, warn_bad_lines=False).columns
    header=dataset.values.tolist()
    headers=set(header)
    y=reqd_header.intersection(headers)
    heads=[]
    if(len(y)==14):
        heads=list(y)
        dataset1 = pd.read_csv("/home/sourav/Desktop/WORK/Coss_internship/MAIN_PROJECT/META_FILES1/Data/"+str(folder)+"/"+str(file),low_memory=False,usecols=heads, warn_bad_lines=False)
        l=dataset1.iloc[count-pos:count,:]
        l=l[list(reqd_header)]
        l.fillna("NA",inplace=True)
        tuples = [tuple(x) for x in l.to_numpy()]
        return(tuples)
    else:
        na_column=["NA"]*pos
        left_columns=tuple(reqd_header-y)
        heads=list(y)
        dataset1 = pd.read_csv("/home/sourav/Desktop/WORK/Coss_internship/MAIN_PROJECT/META_FILES1/Data/"+str(folder)+"/"+str(file),low_memory=False,usecols=heads, warn_bad_lines=False)
        l=dataset1.iloc[count-pos:count,:]
        for column in left_columns:
            l.loc[:,column]=na_column
            print("Column "+str(column)+" not present in "+str(file))
        l=l[list(reqd_header)]
        l.fillna("NA",inplace=True)
        tuples = [tuple(x) for x in l.to_numpy()]
        return(tuples)

def DataPos(file,folder):
    path="/home/sourav/Desktop/WORK/Coss_internship/MAIN_PROJECT/META_FILES1/Data/"+str(folder)+"/"+str(file)
    dataset = pd.read_csv(path,low_memory=False, usecols=[0],warn_bad_lines=False)
    dataset=dataset.values.tolist()
    count=0
    
    for i in range(len(dataset)):
        if(len(str(dataset[i][0]))>3):
            count+=1
    dataset[count-1]
    pos=0
    for j in range(len(dataset)):
        m = re.match("^"+str(dataset[count-1][0]),str(dataset[j][0]))
        if m:
            pos+=1
    return(data_extractor(folder,file,count,pos))
    

mydb = mysql.connector.connect(host=RDS_HOST,database=DATABASE,user=USER,password=PASSWORD)
cur=mydb.cursor()
s="""INSERT INTO Data (Date , FacilityType , BedSize , Region , Manufacturer , Ticker , `Group` , Therapy , Anatomy ,SubAnatomy , ProductCategory , Quantity , AvgPrice , TotalSpend) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

META_FOLDERS=os.listdir("/home/sourav/Desktop/WORK/Coss_internship/MAIN_PROJECT/META_FILES1/Data")
for folder in META_FOLDERS:
    all_files=os.listdir("/home/sourav/Desktop/WORK/Coss_internship/MAIN_PROJECT/META_FILES1/Data/"+str(folder))
    print("############ "+str(folder)+"############")
    for i in range(len(all_files)):
        print("** "+str(all_files[i])+" **")
        table=DataPos(all_files[i],folder)
        cur.executemany(s,table)
        mydb.commit()
        print("Done transfering "+str(all_files[i])+" data to AWS RDS DB!")
        print("     ")
    print("*********************************************************")

mydb.close
finish=time.perf_counter()
print("*******************************************************")
print("Total time for Stage IV : "+str(finish-start)+" seconds")
print("*******************************************************")
print("<-------------------CYCLE COMPLETE-------------------->")




