import os
import pandas as pd
import re
from datetime import datetime

META_FILES=os.listdir("/home/sourav/Desktop/WORK/Coss_internship/MAIN_PROJECT/META_FILES")
META_FILES.sort()

def absPosEmp(path,posx,keyword):
    find=pd.read_csv(path,usecols=posx,dtype="a")
    #find=find.iloc[:,posx:posy]
    find=find.values.tolist()
    pos=-1
    for i in range(len(find)):
        m = re.match(keyword,str(find[i][0]))
        pos+=1
        if m:
            r=list()
            r.append(pos)
            r.append(0)
            return(r)
    pos=-1
    if(pos==-1):
        find=pd.read_csv(path,usecols=[7],dtype="a")
        find=find.values.tolist()
        pos=-1
        for i in range(len(find)):
            m = re.match("^Max",str(find[i][0]))
            pos+=1
            if m:
                r=list()
                r.append(pos)
                r.append(1)
                return(r)

def absPosReg(path,posx,keyword):
    find=pd.read_csv(path,usecols=posx,dtype="a")
    #find=find.iloc[:,posx:posy]
    find=find.values.tolist()
    pos=-1
    for i in range(len(find)):
        m = re.match(keyword,str(find[i][0]))
        pos+=1
        if m:
            return(pos)
    pos=-1
    if(pos==-1):
        find=pd.read_csv(path,usecols=[7],dtype="a")
        find=find.values.tolist()
        pos=-1
        for i in range(len(find)):
            m = re.match("^Max",str(find[i][0]))
            pos+=1
            if m:
                return(pos)

def get_data_emp(sheet,meta):
    pos=absPosEmp("/home/sourav/Desktop/WORK/Coss_internship/MAIN_PROJECT/META_FILES/"+str(meta)+"/Emperical/"+sheet,[4],"^Max")
    if (pos[1]==1):
        pos=int(pos[0])
        table=pd.read_csv("/home/sourav/Desktop/WORK/Coss_internship/MAIN_PROJECT/META_FILES/"+str(meta)+"/Emperical/"+sheet,usecols=[8],dtype="a")
        table=pd.DataFrame(table)
        table=table.iloc[pos-1:pos+2,0:1]
        l=table.values.tolist()
        return (l)
    else:
        pos=int(pos[0])
        table=pd.read_csv("/home/sourav/Desktop/WORK/Coss_internship/MAIN_PROJECT/META_FILES/"+str(meta)+"/Emperical/"+sheet,usecols=[5],dtype="a")
        table=pd.DataFrame(table)
        table=table.iloc[pos-1:pos+2,0:1]
        l=table.values.tolist()
        return (l)


def get_data_reg(sheet,meta):
    table=pd.read_csv("/home/sourav/Desktop/WORK/Coss_internship/MAIN_PROJECT/META_FILES/"+str(meta)+"/Regression/"+sheet,usecols=[2,17])
    table=pd.DataFrame(table)
    pos=absPosReg("/home/sourav/Desktop/WORK/Coss_internship/MAIN_PROJECT/META_FILES/"+str(meta)+"/Regression/"+sheet,[16],"^Max")
    table1=table.iloc[pos-1:pos,0:1]
    l1=table1.values.tolist()
    table2=table.iloc[pos-1:pos+2,1:2]
    l2=table2.values.tolist()
    l2.append(l1[0])
    return (l2)

def typeFind(file):
    x=file.split("-")
    if(len(x)<=1):
        return("Null")
    else:
        return(x[-1][:-4])

for meta in META_FILES:
    Empfiles=os.listdir("/home/sourav/Desktop/WORK/Coss_internship/MAIN_PROJECT/META_FILES/"+str(meta)+"/Emperical")
    Regfiles=os.listdir("/home/sourav/Desktop/WORK/Coss_internship/MAIN_PROJECT/META_FILES/"+str(meta)+"/Regression")
    Empfiles.sort()
    Regfiles.sort()
    print("############################################# "+str(meta)+"#########################################################")
    for file in Empfiles:
        data=[]
        ticker=meta
        type_data=typeFind(file)
        data=get_data_emp(file,meta)
        current_time = datetime.now()
        print("******************************************")
        print("Sheet: ",file)
        print("Estimated Total Sold--> ",data[0][0])
        print("Estimated Max Sold--> ",data[1][0])
        print("Estimated Min Sold--> ",data[2][0])
        print("Type-->",type_data)
        print("Date-->",current_time.strftime('%d/%m/%Y'))
        print("Ticker-->",ticker)
        print("******************************************")

    for file in Regfiles:
        data=[]
        data=get_data_reg(file,meta)
        print("******************************************")
        print("Sheet: ",file)
        print("Forecast w/o SA Actual--> ",data[0][0])
        print("Forecast w/o SA Max--> ",data[1][0])
        print("Forecast w/o SA Min--> ",data[2][0])
        QY=data[3][0]
        print("Quarter-->",QY[0:2])
        print("Year-->",QY[2:4])
        print("******************************************")
    print("############################################################################################################")