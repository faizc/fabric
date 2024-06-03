
## JDBC connectivity to the Fabric Warehouse

Connecting to the Fabric Warehouse using JDBC requires few libraries and the connection related properties. 

Follow the steps below to make JDBC connection using the JMeter tool. 


## Load the Jars files to the JMeter tool 

- Open the JMeter tool and click the on the Test Plan to all the required JAR files.
- Click on the 'Browse' button and load all the jar files

Note - The JAR versions are good as of 3rd June 2024 but in future the same version may not work, so you may need to use the latest versions. 

Check the following image for reference. 

![Alt text](snaps/1.png?raw=true)


## Update the JDBC connection properties 

In the JDBC Connection config, update the following properies,
- JDBC URL - jdbc:sqlserver://<CONNECTION_STRING_FABRIC_WAREHOUSE>:1433;databaseName=<DATABASE_NAME>;encrypt=true;loginTimeout=30;authentication=ActiveDirectoryInteractive 

- Driver class - com.microsoft.sqlserver.jdbc.SQLServerDriver

- Username - <AD_USER_NAME>

- Password - <AD_PASSWORD>

Run the experiments to check the connectivity. Check the following image for reference. 
![Alt text](snaps/2.png?raw=true)
