# Dynamic ETL Tool

## INTRODUCTION
The aim of the dynamic and configurable ETL framework would be to reduce the creation and modifications in an ETL job.
The proposed architecture is completely python based that has minimized the efforts of the continuous changes in an ETL process by making it configurable.

## BUSINESS REQUIREMENTS (IN BRIEF)
* Complete application on CentOS server.
* Extraction of required data from excel files.
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
*  Reduced 
*  Easy to configure
*  Log genration at every stage

## HIGH LEVEL DESIGN
* > The complete application will be hosted on a CentOS instance on AWS cloud. 
* > An FTP server for loading data into the CentOS instance on AWS cloud
* > MariaDB will be used as a database for storing extracted data.
* > Jenkins for CI/CD of the application
* > Docker to containerize Stage 2 for parallel extraction rather serial extraction for effiency 

<img alt="HDL" src="https://github.com/srvk-99/ETL_Tool/blob/master/images/HDL.png"/>

## MVP RESULTS
### STAGE 2

> META EXTRACTION
<img alt="first" src="https://github.com/srvk-99/ETL_Tool/blob/master/gifs/first.gif"/>

> DATA EXTRACTION
<img alt="second" src="https://github.com/srvk-99/ETL_Tool/blob/master/gifs/second.gif"/>




