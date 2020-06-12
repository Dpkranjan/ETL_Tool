# Dynamic ETL Tool

## INTRODUCTION
The aim of the dynamic and configurable ETL framework would be to reduce the creation and modifications in an ETL job.
The proposed architecture is completely python based that has minimized the efforts of the continuous changes in an ETL process by making it configurable.

## FEATURES
*  Complete opensource tools used
*  Complete python based approach
*  Reduced 
*  Easy to configure
*  Log genration at every stage

## HIGH LEVEL DESIGN
* > The complete application will be hosted on a CentOS instance on AWS cloud. 
* > MariaDB will be used as a database for storing extracted data.
* > An FTP server for loading data into the CentOS instance on AWS cloud
* > Jenkins for CI/CD of the application
* > Docker to containerize Stage 2 for parallel extraction rather serial extraction for effiency 

<img alt="HDL" src="https://github.com/srvk-99/ETL_Tool/blob/master/images/HDL.png"/>
