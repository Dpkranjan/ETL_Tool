# Dynamic ETL Tool

## INTRODUCTION
The aim of the dynamic and configurable ETL framework would be to reduce the creation and modifications in an ETL job.
The proposed architecture is completely python based that has minimized the efforts of the continuous changes in an ETL process by making it configurable.

## BUSINESS REQUIREMENTS (IN BRIEF)
* Complete application on CentOS server.
* Extraction of required data from excel files *{Empirical , Regression and Data}*.
* Storing the data on a new excel file and also on a SQL server.
* Encrypt the data stored on the CentOS server.
* Create logs for each stage and exceptions faced during the entire process.
* Reduce the time complexity.

## CHALLENGES 
* Size of the excel files are very large.
* Reduce time complexity of the entire cycle which takes days for the customer currently.
* Handle the exceptions at each an every stage as the excel files are unstructured.
* Since the data is unstructred there is no fixed place to find the data. 

## FEATURES
*  Complete opensource tools used
*  Complete python based approach
*  Easy to configure
*  Log genration at every stage
*  Fast and robust
*  Ready for parallel extraction using containers

## HIGH LEVEL DESIGN
* > The complete application will be hosted on a CentOS instance on AWS cloud. 
* > An FTP server for loading data into the CentOS instance on AWS cloud
* > MariaDB will be used as a database for storing extracted data.
* > Jenkins for CI/CD of the application
* > Docker to containerize Stage 2 for parallel extraction rather serial extraction for effiency. :sparkles:

<img alt="HDL" src="https://github.com/srvk-99/ETL_Tool/blob/master/gifs/hdl%20update.png"/>

## HOW TO USE THE TOOL 
> git clone https://github.com/srvk-99/ETL_Tool.git 

* <strong>moduleCheckRun.py</strong> : This  python script ensures all required modules that are mentioned in *requirements.txt* 
> python3 moduleCheckRun.py
* <strong>db_initialisation.py</strong> : This python script ensures the tables *AnalystData* and *Data* are created in the SQL sever
> python3 db_initialisation.py
* <strong>envVarCheck.py</strong> : This python script ensures the environment variables related to AWS RDS are exported on the *.bashrc* file of the instance
> python3 envVarCheck.py
* <strong>datasets folder</strong> : Here all RAW datafiles are stored through a SFTP server.

* <strong>first.py</strong> : This python script runs to convert all the files into meta files (this is the key step to make the process faster)
> python3 first.py

* <strong>second.py</strong> : This python script runs which extracts all the required data, excel file is created and the *AnalystData* table is also filled on AWS RDS
> python3 second.py


* <strong>third.py</strong> : This python script runs which extracts all the data from *data sheets* of the excel file
> python3 second.py

* <strong>fourth.py</strong> : This python script runs which extracts all the required data, excel file is created and the *AnalystData* table is also filled on AWS RDS
> python3 second.py

## MVP RESULTS
### STAGE 2

> META EXTRACTION
<p align="center">
  <img width="1000" height="450" src="https://github.com/srvk-99/ETL_Tool/blob/master/gifs/first.gif">
</p>
The above result is the output of <strong>Stage2 {META EXTRACTION}</strong>  which takes around <strong>56 seconds to process 19 excel files of 1.1 GB</strong>.This time varies between <strong>50 to 60 seconds</strong> depending upon the current load on the system.
<br>
<br>

> DATA EXTRACTION

<p align="center">
  <img width="1000" height="450" src="https://github.com/srvk-99/ETL_Tool/blob/master/gifs/second.gif">
</p>
The above result is the output of data extracted from the excel files.
