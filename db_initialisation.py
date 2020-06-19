import mysql.connector
from mysql.connector import Error
try:
    connection = mysql.connector.connect(host='rdsdbuser.caxoy3n3x5ka.us-east-1.rds.amazonaws.com',
                                            database='rdsdbuser',
                                            user='rdsdbuser',
                                            password='rdsdbuser')

    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = connection.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)
        cursor.execute("""CREATE TABLE AnalystData (DATE text,TICKER text,TYPE text,QUARTER text,YEAR text,`ESTIMATED TOTAL SOLD` text,`ESTIMATED MAX SOLD` text,`ESTIMATED MIN SOLD` text,`FORECAST_W/O_SA_ACTUAL` text,`FORECAST W/O SA MAX` text,`FORECAST W/O SA MIN` text)""")
        cursor.execute("""CREATE TABLE Data (Date text, FacilityType text, BedSize text, Region text, Manufacturer text, Ticker text, `Group` text, Therapy text, Anatomy text,SubAnatomy text, ProductCategory text, Quantity text, AvgPrice text, TotalSpend text)""")

except Error as e:
    print("Error while connecting to MySQL", e)
finally:
    if (connection.is_connected()):
        cursor.close()
        connection.close()
        print("MySQL connection is closed and tables AnalystData and Data are sucessfully created!")
    
