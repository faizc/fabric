# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {}
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC CREATE TABLE Company
# MAGIC (
# MAGIC     company_id STRING,
# MAGIC     stock_symbol STRING,
# MAGIC     company_name STRING,
# MAGIC     sector_id STRING,
# MAGIC     market_cap_billion DOUBLE,
# MAGIC     headquarters STRING
# MAGIC );
# MAGIC 
# MAGIC INSERT INTO Company VALUES
# MAGIC ('C001','MSFT','Microsoft','S001',3800,'Redmond'),
# MAGIC ('C002','NVDA','NVIDIA','S001',3500,'Santa Clara'),
# MAGIC ('C003','TSLA','Tesla','S002',950,'Austin'),
# MAGIC ('C004','AMZN','Amazon','S003',2400,'Seattle'),
# MAGIC ('C005','GOOG','Google','S001',2300,'Mountain View');
# MAGIC 
# MAGIC %%sql
# MAGIC CREATE TABLE Sector
# MAGIC (
# MAGIC     sector_id STRING,
# MAGIC     sector_name STRING
# MAGIC );
# MAGIC 
# MAGIC INSERT INTO Sector VALUES
# MAGIC ('S001','Technology'),
# MAGIC ('S002','Automotive'),
# MAGIC ('S003','Retail & Cloud');
# MAGIC 
# MAGIC CREATE TABLE Investor
# MAGIC (
# MAGIC     investor_id STRING,
# MAGIC     investor_name STRING,
# MAGIC     investor_type STRING,
# MAGIC     risk_profile STRING
# MAGIC );
# MAGIC 
# MAGIC INSERT INTO Investor VALUES
# MAGIC ('I001','John Smith','Retail','Moderate'),
# MAGIC ('I002','Contoso Investments','Institutional','Aggressive'),
# MAGIC ('I003','Fabrikam Capital','Institutional','Balanced');
# MAGIC 
# MAGIC 
# MAGIC CREATE TABLE Portfolio
# MAGIC (
# MAGIC     portfolio_id STRING,
# MAGIC     investor_id STRING,
# MAGIC     portfolio_name STRING
# MAGIC );
# MAGIC 
# MAGIC INSERT INTO Portfolio VALUES
# MAGIC ('P001','I001','Retirement Portfolio'),
# MAGIC ('P002','I002','Growth Fund'),
# MAGIC ('P003','I003','Balanced Equity');
# MAGIC 
# MAGIC 
# MAGIC CREATE TABLE PortfolioHolding
# MAGIC (
# MAGIC     holding_id STRING,
# MAGIC     portfolio_id STRING,
# MAGIC     stock_symbol STRING,
# MAGIC     quantity INT,
# MAGIC     avg_purchase_price DOUBLE
# MAGIC );
# MAGIC 
# MAGIC INSERT INTO PortfolioHolding VALUES
# MAGIC ('H001','P001','MSFT',100,450),
# MAGIC ('H002','P001','GOOG',50,180),
# MAGIC ('H003','P002','NVDA',500,130),
# MAGIC ('H004','P002','TSLA',300,280),
# MAGIC ('H005','P003','AMZN',250,190);

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }
