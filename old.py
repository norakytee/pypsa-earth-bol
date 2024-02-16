import pandas as pd

# Load monthly demand profiles
monthly_demand_path = 'C:/Users/noraky/Documents/Masteroppgave/pypsa-earth/monthly_demand_profiles.xlsx'
monthly_demand_profiles = pd.read_excel(monthly_demand_path)

# Load hourly demand profiles
hourly_demand_path = 'C:/Users/noraky/Documents/Masteroppgave/pypsa-earth/resources/demand_profiles.csv'
hourly_demand_profiles = pd.read_csv(hourly_demand_path)

# Display the first few rows of each dataframe for inspection
monthly_demand_profiles.head(), hourly_demand_profiles.head()

monthly_demand_profiles.columns = monthly_demand_profiles.columns.astype(str)

# Adjust the hourly loads based on the correct monthly sums
for node in monthly_demand_profiles.columns[1:]: # Skipping the 'time' column
    if node in hourly_demand_profiles.columns:
        for month in range(1, 13): # For each month
            # Find the total monthly demand for the node from monthly_demand_profiles
            monthly_total = monthly_demand_profiles.loc[monthly_demand_profiles['time'].dt.month == month, node].values[0]
            # Find the sum of hourly loads for the node in the same month from hourly_demand_profiles
            hourly_sum = hourly_sums.loc[month, node]
            # Calculate the adjustment factor
            if hourly_sum != 0: # Prevent division by zero
                adjustment_factor = monthly_total / hourly_sum
            else:
                adjustment_factor = 0
            
            # Apply the adjustment factor to each hourly value for the node in the month
            mask = (adjusted_hourly_profiles['time'].dt.month == month)
            adjusted_hourly_profiles.loc[mask, node] = hourly_demand_profiles.loc[mask, node] * adjustment_factor

# Fill NaN values with 0
adjusted_hourly_profiles.fillna(0, inplace=True)

# Save the adjusted_hourly_profiles DataFrame to a new CSV file
adjusted_hourly_profiles_path = 'C:/Users/noraky/Documents/Masteroppgave/pypsa-earth/custom_files/adjusted_demand_profiles.csv'
adjusted_hourly_profiles.to_csv(adjusted_hourly_profiles_path, index=False)

adjusted_hourly_profiles_path


import pandas as pd

# Load the datasets
monthly_demand_profiles = pd.read_excel('/path/to/monthly_demand_profiles.xlsx', skiprows=1)
demand_profiles = pd.read_csv('/path/to/demand_profiles.csv', header=None)

# Extract node names and correct the header for demand_profiles
node_names = demand_profiles.iloc[0]  # Assuming the first row contains node names
demand_profiles.columns = node_names  # Set node names as column headers
demand_profiles = demand_profiles.iloc[1:]  # Remove the row with node names
demand_profiles.reset_index(drop=True, inplace=True)

# Convert 'time' columns as needed (assuming necessary steps for datetime conversion are applied)

# Prepare monthly_demand_profiles by setting the first column as the index if it represents time
monthly_demand_profiles.set_index('Time_Column_Name', inplace=True)

# Calculate scaling factors and apply them
for node in node_names[1:]:  # Assuming the first column in demand_profiles is 'time'
    for index, row in monthly_demand_profiles.iterrows():
        month_year = pd.to_datetime(index).to_period('M')
        monthly_total = row[node]
        
        # Aggregate hourly data to monthly for this node
        hourly_data = demand_profiles[[node]]
        hourly_data['month_year'] = pd.to_datetime(demand_profiles['Time_Column']).dt.to_period('M')
        monthly_hourly_total = hourly_data[hourly_data['month_year'] == month_year][node].astype(float).sum()

        # Calculate scaling factor
        scaling_factor = monthly_total / monthly_hourly_total if monthly_hourly_total != 0 else 0
        
        # Apply scaling factor to adjust the hourly data
        mask = hourly_data['month_year'] == month_year
        demand_profiles.loc[mask, node] = demand_profiles.loc[mask, node].astype(float) * scaling_factor

# Drop the 'YearMonth' helper column from adjusted_demand_profiles before saving or further processing
demand_profiles_calc.drop('YearMonth', axis=1, inplace=True)
output_file_path = 'C:/Users/noraky/Documents/Masteroppgave/pypsa-earth/custom_files/adjusted_demand_profiles.csv'

# Save the DataFrame to a CSV file
demand_profiles_calc.to_csv(output_file_path, index=False)