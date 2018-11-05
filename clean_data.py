# retieving data to be cleaned
raw_data  = pd.read_csv("yellow_tripdata_2018-01.csv")

# cleaning data:
# initial time equal final time
# distance <= 0
# total amount < 3.3 
# year not 2018
# month not current month (counter in loop) 
# price per mile > 25
data = raw_data.drop(raw_data[(raw_data.trip_distance >= 200) |(raw_data.trip_distance <= 0) | (raw_data.tpep_dropoff_datetime == raw_data.tpep_pickup_datetime) | (pd.DatetimeIndex(raw_data['tpep_pickup_datetime']).month != month) | (pd.DatetimeIndex(raw_data['tpep_pickup_datetime']).year != 2018) | (raw_data.total_amount < 3.3) | ((raw_data.total_amount / raw_data.trip_distance) > 25)].index) 

# free memory deleting the raw_data
del raw_data
