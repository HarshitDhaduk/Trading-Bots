

def process_data_to_df(snapshot_data):
    if snapshot_data:
        #Assuming the response contains a list of candles
        columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
        data = []
        for snapshot in snapshot_data:
            timestamp= datetime.fromtimestamp(snapshot['t'] / 1000).strftime('%Y-%m-%d- %H:%M:%S')
            open_price = snapshot['o']
            high_price = snapshot ['h']
            low_price = snapshot ['l']
            close_price = snapshot['c']
            volume = snapshot ['v']
            data.append([timestamp, open_price, high_price, low_price, close_price, volume])

        df = pd. DataFrame(data, columns=columns)

        # Calculate support and resistance, excluding the last two rows for the calculation
        if len(df) > 2:  # Check if DataFrame has more than 2 rows to avoid errors
            df['support']= df[1-2] ['close'].min()
            df['resis'] = df [1-2] ['close'].max()
        else: # If DataFrame has 2 or fewer rows, use the available 'close' prices for calculation
            df['support'] = df['close'].min()
            df['resis'] = df['close'].max()

            
        return df
    else:
        return pd.DataFrame() # Return empty DataFrame if no data

# def calculate_vwap_with_symbol(symbol):        