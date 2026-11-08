# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "8a158871-7f78-4850-acd3-3052f5a5b916",
# META       "default_lakehouse_name": "lh_trucking",
# META       "default_lakehouse_workspace_id": "3f702ee1-4e25-4914-88c9-16edc01cd8ea",
# META       "known_lakehouses": [
# META         {
# META           "id": "8a158871-7f78-4850-acd3-3052f5a5b916"
# META         }
# META       ]
# META     }
# META   }
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

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

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

# CELL ********************

from pyspark.sql import SparkSession
from pyspark.sql.types import *
from datetime import datetime
import random
import time

spark = SparkSession.builder.getOrCreate()

# -----------------------------------------------------
# Stock Configuration
# -----------------------------------------------------
stocks = {
    "MSFT": {"current": 500.0, "min": 450.0, "max": 550.0},
    "NVDA": {"current": 160.0, "min": 130.0, "max": 220.0},
    "TSLA": {"current": 280.0, "min": 220.0, "max": 350.0},
    "AMZN": {"current": 210.0, "min": 180.0, "max": 260.0},
    "GOOG": {"current": 180.0, "min": 150.0, "max": 240.0}
}

# Maintain market trends
market_trends = {
    "MSFT": "BULLISH",
    "NVDA": "SIDEWAYS",
    "TSLA": "BEARISH",
    "AMZN": "SIDEWAYS",
    "GOOG": "BULLISH"
}

# Company IDs
company_ids = {
    "MSFT": "C001",
    "NVDA": "C002",
    "TSLA": "C003",
    "AMZN": "C004",
    "GOOG": "C005"
}


def generate_price(symbol, config):

    current = config["current"]
    lower = config["min"]
    upper = config["max"]

    trend = market_trends[symbol]
    companyId = company_ids[symbol]

    if trend == "BULLISH":
        delta = random.uniform(-1, 4)

    elif trend == "BEARISH":
        delta = random.uniform(-4, 1)

    else:
        delta = random.uniform(-2, 2)

    # occasional spike
    if random.random() < 0.03:
        delta += random.uniform(5, 15)

    # occasional crash
    elif random.random() < 0.03:
        delta -= random.uniform(5, 15)

    new_price = current + delta

    # bounce from boundaries
    if new_price > upper:
        new_price = upper - random.uniform(1, 5)

    if new_price < lower:
        new_price = lower + random.uniform(1, 5)

    config["current"] = round(new_price, 2)

    volume = random.randint(10000, 100000)

    return {
        "EventTime": datetime.utcnow(),
        "CompanyId": companyId,
        "StockSymbol": symbol,
        "Price": round(new_price, 2),
        "Volume": volume,
        "Trend": trend,
        "MarketStatus": "OPEN"
    }

schema = StructType([
    StructField("EventTime", TimestampType(), True),
    StructField("CompanyId", StringType(), True),
    StructField("StockSymbol", StringType(), True),
    StructField("Price", DoubleType(), True),
    StructField("Volume", LongType(), True),
    StructField("Trend", StringType(), True),
    StructField("MarketStatus", StringType(), True)
])

eventhouse_cluster_uri = "https://trd-c757kaycev6hss806u.z3.kusto.fabric.microsoft.com"
eventhouse_database = "stock_db"
access_token=mssparkutils.credentials.getToken(eventhouse_cluster_uri)

while True:

    events = []

    for symbol, config in stocks.items():
        events.append(generate_price(symbol, config))

    df = spark.createDataFrame(events, schema)

    display(df)

    df.write.format("com.microsoft.kusto.spark.synapse.datasource").option("kustoCluster",eventhouse_cluster_uri).option("kustoDatabase",eventhouse_database).option("kustoTable", 'StockPriceEvents').option("accessToken", access_token).option("tableCreateOptions", "CreateIfNotExist").mode("Append").save()  

    print(f"Written {len(events)} records at {datetime.utcnow()}")

    time.sleep(30)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
