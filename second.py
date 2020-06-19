import mysql.connector
import schedule
from mysql.connector import Error
import os
import pandas as pd
import re
from datetime import datetime
from time import process_time 
import copy
from pyexcelerate import Workbook

time1= process_time()
META_FILES=os.listdir("META_FILES1")

RDS_HOST=os.environ['RDS_HOST']
DATABASE=os.environ['DATABASE']
USER =os.environ['RDS_USER']
PASSWORD=os.environ['RDS_PASS']

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
    pos=absPosEmp("META_FILES1/"+str(meta)+"/"+sheet,[4],"^Max")
    if (pos[1]==1):
        pos=int(pos[0])
        table=pd.read_csv("META_FILES1/"+str(meta)+"/"+sheet,usecols=[3,8],dtype="a")
        table=pd.DataFrame(table)
        table1=table.iloc[pos-1:pos+2,1:2]
        l=table1.values.tolist()
        table2=table.iloc[pos-1:pos,0:1]
        l1=table2.values.tolist()
        l.append(l1[0])
        return (l)
    else:
        pos=int(pos[0])
        table=pd.read_csv("META_FILES1/"+str(meta)+"/"+sheet,usecols=[3,5],dtype="a")
        table=pd.DataFrame(table)
        table1=table.iloc[pos-1:pos+2,1:2]
        table2=table.iloc[pos-1:pos,0:1]
        l1=table2.values.tolist()
        l=table1.values.tolist()
        l.append(l1[0])
        return (l)


def get_data_reg(sheet,meta):
    table=pd.read_csv("META_FILES1/"+str(meta)+"/"+sheet,usecols=[2,17])
    table=pd.DataFrame(table)
    pos=absPosReg("META_FILES1/"+str(meta)+"/"+sheet,[16],"^Max")
    table1=table.iloc[pos-1:pos,0:1]
    l1=table1.values.tolist()
    table2=table.iloc[pos-1:pos+2,1:2]
    l2=table2.values.tolist()
    l2.append(l1[0])
    return (l2)


excel_data=[]
header=["DATE","TICKER","TYPE","QUARTER","YEAR","ESTIMATED TOTAL SOLD","ESTIMATED MAX SOLD","ESTIMATED MIN SOLD","FORECAST W/O SA ACTUAL","FORECAST W/O SA MAX","FORECAST W/O SA MIN"]
excel_data.append(header)
single_files=[]
multiple_files=[]

for meta in META_FILES:
    files=os.listdir("META_FILES1/"+str(meta))
    files.sort()
    if(len(files)==2):
        holder=[]
        holder.append([meta])
        holder.append(files)
        single_files.append(holder)
for meta in META_FILES:
    files=os.listdir("META_FILES1/"+str(meta))
    files.sort()
    if(len(files)>2):
        holder=[]
        holder.append([meta])
        holder.append(files)
        multiple_files.append(holder)


def typeFind(file):
    x=file.split("-")
    if(len(x)<=1):
        return("Null")
    else:
        return(x)

def typeMullFind(file):
    x=file.split("-")
    if(len(x)<=1):
        return("Null")
    else:
        return(x[-1][:-4])

def fileChecker_Reg(file):
    if(file=="l"):
        return(".csv")
    elif (file[0]==" "):
        return(file)
    else:
        return(" "+str(file))

def fileChecker_Emp(file):
    if(file=="l"):
        return(".csv")
    elif (file[0]!=" "):
        return(file)
    else:
        return(str(file[1:]))

Emp_list=[]
Reg_list=[]

for i in multiple_files:
    count=0
    #print(i[0])
    h=[]
    for j in i[1]:
        m = re.match("^Emp",j)
        if m:
            count+=1
    h.append(i[0])
    h.append(i[1][0:count])     
    Emp_list.append(h)


for i in multiple_files:
    count=0
    #print(i[0])
    h=[]
    if(len(i[1])%2==0):
        for j in i[1]:
            m = re.match("^Reg",j)
            if m:
                count+=1
        h.append(i[0])
        h.append(i[1][count:])     
        Reg_list.append(h)
    else:
        for j in i[1]:
            m = re.match("^Reg",j)
            if m:
                count+=1
        h.append(i[0])
        h.append(i[1][count-1:])     
        Reg_list.append(h)


copy_Reg=copy.deepcopy(Reg_list)
multiple_pair_files=[]      
emp_left_files=[]
reg_left_files=[]
for i in range(len(Emp_list)):
    for j in range(len(Emp_list[i][1])):
        hold=[]
        s0="Regression Model - "+fileChecker_Emp(typeFind(Emp_list[i][1][j])[-1])
        s1="Regression Model-"+fileChecker_Emp((typeFind(Emp_list[i][1][j])[-1]))
        s2="Regression Model -"+fileChecker_Emp((typeFind(Emp_list[i][1][j])[-1]))
        s3="Regression Model- "+fileChecker_Emp((typeFind(Emp_list[i][1][j])[-1]))
        s4="Regression Model"+fileChecker_Emp((typeFind(Emp_list[i][1][j])[-1]))
        s5="Regression Model - "+str(fileChecker_Emp((typeFind(Emp_list[i][1][j])[-1]))[:-5]+".csv")
        if (s0 in Reg_list[i][1]):
            hold.append(Emp_list[i][0])
            hold1=[]
            hold1.append(Emp_list[i][1][j])
            hold1.append(s0)
            hold.append(hold1)
            multiple_pair_files.append(hold)
            copy_Reg[i][1].remove(s0)
            
        elif(s1 in Reg_list[i][1]):
            hold.append(Emp_list[i][0])
            hold1=[]
            hold1.append(Emp_list[i][1][j])
            hold1.append(s1)
            hold.append(hold1)
            multiple_pair_files.append(hold)
            copy_Reg[i][1].remove(s1)
            
        elif(s2 in Reg_list[i][1]):
            hold.append(Emp_list[i][0])
            hold1=[]
            hold1.append(Emp_list[i][1][j])
            hold1.append(s2)
            hold.append(hold1)
            multiple_pair_files.append(hold)
            copy_Reg[i][1].remove(s2)
            
        elif(s3 in Reg_list[i][1]):
            hold.append(Emp_list[i][0])
            hold1=[]
            hold1.append(Emp_list[i][1][j])
            hold1.append(s3)
            hold.append(hold1)
            multiple_pair_files.append(hold)
            copy_Reg[i][1].remove(s3)
        
        elif(s4 in Reg_list[i][1]):
            hold.append(Emp_list[i][0])
            hold1=[]
            hold1.append(Emp_list[i][1][j])
            hold1.append(s4)
            hold.append(hold1)
            multiple_pair_files.append(hold)
            copy_Reg[i][1].remove(s4)
        
        elif(s5 in Reg_list[i][1]):
            hold.append(Emp_list[i][0])
            hold1=[]
            hold1.append(Emp_list[i][1][j])
            hold1.append(s5)
            hold.append(hold1)
            multiple_pair_files.append(hold)
            copy_Reg[i][1].remove(s5)
            
        else:
            hold.append(Emp_list[i][0])
            hold1=[]
            hold1.append(Emp_list[i][1][j])
            hold.append(hold1)
            emp_left_files.append(hold)
            
for i in copy_Reg:
    if(len(i[1])>0):
        hold2=[]
        hold2.append(i[0])
        hold2.append(i[1])
        reg_left_files.append(hold2)

for i in range(len(single_files)):
    data=[]
    ticker=single_files[i][0][0]
    type_data="Null"
    data_emp=get_data_emp(str(single_files[i][1][0]),str(ticker))
    current_time = datetime.now()
    data_reg=get_data_reg(str(single_files[i][1][1]),str(ticker))
    QY=data_reg[3][0]
    data.append(current_time.strftime('%d/%m/%Y'))
    data.append(ticker)
    data.append(type_data)
    data.append(QY[0:2])
    data.append(QY[2:4])
    data.append(data_emp[0][0])
    data.append(data_emp[1][0])
    data.append(data_emp[2][0])
    data.append(data_reg[0][0])
    data.append(data_reg[1][0])
    data.append(data_reg[2][0])
    excel_data.append(data)


for i in range(len(multiple_pair_files)):
    data=[]
    ticker=multiple_pair_files[i][0][0]
    type_data=typeMullFind(multiple_pair_files[i][1][0])
    data_emp=get_data_emp(str(multiple_pair_files[i][1][0]),str(ticker))
    current_time = datetime.now()
    data_reg=get_data_reg(str(multiple_pair_files[i][1][1]),str(ticker))
    QY=data_reg[3][0]
    data.append(current_time.strftime('%d/%m/%Y'))
    data.append(ticker)
    data.append(type_data)
    data.append(QY[0:2])
    data.append(QY[2:4])
    data.append(data_emp[0][0])
    data.append(data_emp[1][0])
    data.append(data_emp[2][0])
    data.append(data_reg[0][0])
    data.append(data_reg[1][0])
    data.append(data_reg[2][0])
    excel_data.append(data)


for i in range(len(emp_left_files)):
    data=[]
    ticker=emp_left_files[i][0][0]
    type_data=typeMullFind(emp_left_files[i][1][0])
    data_emp=get_data_emp(str(emp_left_files[i][1][0]),str(ticker))
    current_time = datetime.now()
    QY=data_emp[3][0].split("in ")[-1]
    data.append(current_time.strftime('%d/%m/%Y'))
    data.append(ticker)
    data.append(type_data)
    data.append(QY[0:2])
    data.append(QY[2:4])
    data.append(data_emp[0][0])
    data.append(data_emp[1][0])
    data.append(data_emp[2][0])
    data.append("Null")
    data.append("Null")
    data.append("Null")
    excel_data.append(data)
    print("--> Only "+str(emp_left_files[i][1][0])+" sheet found! Could not find corresponding Regression sheet")


for i in range(len(reg_left_files)):
    data=[]
    ticker=reg_left_files[i][0][0]
    type_data=typeMullFind(reg_left_files[i][1][0])
    current_time = datetime.now()
    data_reg=get_data_reg(str(reg_left_files[i][1][0]),str(ticker))
    QY=data_reg[3][0]
    data.append(current_time.strftime('%d/%m/%Y'))
    data.append(ticker)
    data.append(type_data)
    data.append(QY[0:2])
    data.append(QY[2:4])
    data.append("Null")
    data.append("Null")
    data.append("Null")
    data.append(data_reg[0][0])
    data.append(data_reg[1][0])
    data.append(data_reg[2][0])
    excel_data.append(data)
    print("--> Only "+str(reg_left_files[i][1][0])+" sheet found! Could not find corresponding Empirical sheet")

os.chdir("/opt/output")
os.system("rm -rf model_"+str(current_time.strftime('%d%m%Y'))+str(".xlsx"))
wb = Workbook()
current_time = datetime.now()
wb.new_sheet("Analyst data", data=excel_data)
wb.save("/opt/output/model_"+str(current_time.strftime('%d%m%Y'))+str(".xlsx"))
print("******************************************************")
print("Excel file generated : "+str(current_time.strftime('%d%m%Y'))+str(".xlsx"))
print("******************************************************")
dataset = pd.read_excel("/opt/output/model_"+str(current_time.strftime('%d%m%Y'))+str(".xlsx"))

x=dataset.iloc[:]
tuples = [tuple(x) for x in dataset.to_numpy()]

mydb = mysql.connector.connect(host=RDS_HOST,
                                         database=DATABASE,
                                          user=USER,
                                         password=PASSWORD)
cur=mydb.cursor()
s="""INSERT INTO AnalystData (DATE ,TICKER ,TYPE ,QUARTER ,YEAR ,`ESTIMATED TOTAL SOLD` ,`ESTIMATED MAX SOLD` ,`ESTIMATED MIN SOLD`,`FORECAST_W/O_SA_ACTUAL` ,`FORECAST W/O SA MAX` ,`FORECAST W/O SA MIN` ) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
cur.executemany(s,tuples)
mydb.commit()
mydb.close
print("Data transfered to AWS RDS DB!")

time2= process_time()
print("*******************************************************")
print("Total time for Step II : "+ str(time2-time1)+" seconds")
print("*******************************************************")
