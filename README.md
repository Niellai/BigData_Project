BigData_Project

Things to do:
1. Transfer data to hdfs
2. ETL process, listen to twitter and write to hdfs (batches)
 - kafka consumer for extracting required information from raw tweets
 - kafka consumer do data cleaning before storing back to hdfs
 - kafka producer sending data clean completed to analytics to refresh 
3. Analytic process (Spark processes - pyspark) -- Not sure --
 - kafka consumer listen to clean complete and start analytic process 
 - Analytic result is store as RDD
 - UI backend interact with spark 



