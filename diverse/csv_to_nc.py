import pandas as pd
import xarray as xr

# Step 1: Load the CSV data
csv_file_path = 'corrected_new_plant_inflow.csv'
df = pd.read_csv(csv_file_path)

# Step 2: Prepare the data (assuming 'Hour' is your time column)
df['time'] = pd.to_datetime(df['time'])
df['plant'] = df['plant'].astype('U3')

# Convert the DataFrame to an Xarray Dataset
# Assuming 'Hour' is set as index if your data is time series
ds = df.set_index('time').to_xarray()

# Step 4: Create the NetCDF file
nc_file_path = 'new_profiles_hydro.nc'
ds.to_netcdf(nc_file_path)