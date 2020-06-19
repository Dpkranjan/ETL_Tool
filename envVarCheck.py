import os
try:
    RDS_HOST=os.environ['RDS_HOST']
    DATABASE=os.environ['DATABASE']
    USER =os.environ['RDS_USER']
    PASSWORD=os.environ['RDS_PASS']
    print("RDS_HOST-->",RDS_HOST)
    print("DATABASE-->",DATABASE)
    print("USER------>",USER)
    print("PASSWORD-->",PASSWORD)
except:
    print("Set the environment variables!")
