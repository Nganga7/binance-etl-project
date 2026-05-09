# Extracting Account Info from Binance

This batch ETL is designed to extract real-time metrics from Binance and load the data to a database. Database chosen here is a local Postgres instance

## Description

The ETL fetches account information data from the Binance API and loads it into a Postgres local database. It does this via the Binance client installed and using the api key & api secret generated. The raw data is saved as json before transformation.

Data fetched is rendered as a nested dictionary, hence we need to slice the data to get the required columns. Columns needed for our pipeline are: asset, free & locked. Once sliced, we then convert the data into a DataFrame which will allow us to load into the database.

Following the transformations above, we then create a database called api_data on the database. Once created, we test the connection details. We then create a table on the public schema named, "src_binance_info".

The table src_binance_info should have columns that match the data transformed. Additionally, a column for load_date is added so as to know which day / time the data for Binance account information was collected.


## Getting Started

### Dependencies

* Libraries required:
    - pandas 
    - requests 
    - psycopg2
    - sql 
    - extras
	- binance.client
	- os
    - dotenv

### Installing

* The ETL pipeline can be downloaded from the GitHub repository: https://github.com/Nganga7/LuxDev_Assignments/binance/extract_binance.ipynb
* Users can then setup their own virtual environment using uv and use ```uv sync``` to install the required dependencies
* Users can modify the database connection details to their own database connection

### Executing program

* Since the program is saved as a ipynb file, you can run it with any IDE of your choice
