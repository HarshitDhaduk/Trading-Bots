import pandas as pd
import nice_funcs as n

# Define symbol, timeframe, and the total limit you want to fetch
symbol = 'WIF'
timeframe = '1h'
total_limit = 5000  # Total records you want to fetch

# Maximum records per call allowed by the API
max_call_limit = 5000

# Calculate the number of iterations needed
iterations = -(-total_limit // max_call_limit) + 1  # Ceiling division to ensure we cover all records

# Initialize an empty DataFrame to append fetched data
all_data = pd.DataFrame()

# Loop to fetch and append data
for i in range(iterations):
    print(f'Fetching data for iteration {i + 1}/{iterations}')
    
    # Calculate the limit for this iteration
    iteration_limit = min(max_call_limit, total_limit - (i * max_call_limit))
    
    # Fetch the OHLCV data
    snapshot_data = n.get_ohlcv2(symbol, timeframe, iteration_limit)
    df = n.process_data_to_df(snapshot_data)

    # Append the fetched data to the all_data DataFrame
    all_data = pd.concat([all_data, df], ignore_index=True)

# Construct the file path using symbol, timeframe and total_limit
file_path = f'data/{symbol}_{timeframe}_{total_limit}.csv'    