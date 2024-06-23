import pandas as pd
import xarray as xr

df = pd.read_excel('resources/renewable_profiles/inflows.xlsx')

# Assuming df is your DataFrame after reading the Excel file
# Replace 'Hour_Column_Name' with the actual name of your Hour column
df_long = pd.melt(df, id_vars=['BUSS'], var_name='plant', value_name='inflow')

# Convert the 'Hour' column to datetime if it's not already
df_long['BUSS'] = pd.to_datetime(df_long['BUSS'])

# Rename the columns to 'Hour', 'Plant', and 'Inflow'
df_long.rename(columns={'BUSS': 'time'}, inplace=True)

df_long = df_long[['plant', 'time', 'inflow']]

unique_plants = df_long['plant'].unique()
unique_hours = df_long['time'].unique()

# List of plants to add
plants_to_add = [0, 10, 100, 12, 14, 17, 19, 2, 21, 23, 25, 27, 29, 31, 33, 34, 35, 36, 37, 38, 39, 4, 40, 41, 42, 43, 44, 45, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 6, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 8, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99]
plants_original = plants_to_add.copy()

for plant in unique_plants:
    if plant in plants_to_add:
        plants_to_add.remove(plant)
        
# Step 3: Create a new DataFrame for the missing plants
rows = []
for hour in unique_hours:
    for plant in plants_to_add:
        rows.append({'plant': plant, 'time': hour, 'inflow': 0})
        
df_new_plants = pd.DataFrame(rows)
df_new_plants.sort_values(by=['plant', 'time'], inplace=True)

# Step 4: Append the new DataFrame to the original one
df_combined = pd.concat([df_long, df_new_plants])

df_combined['plant'] = pd.Categorical(df_combined['plant'], categories=plants_original, ordered=True)
df_combined.sort_values(by=['plant', 'time'], inplace=True)

# Make sure the plant column is of type 'U3' (string with max length 3)
df_combined['plant'] = df_combined['plant'].astype('U3')

df_combined['time'] = pd.to_datetime(df_combined['time']).dt.tz_localize(None)

df_combined.set_index(['plant', 'time'], inplace=True)

df_combined.to_csv('resources/renewable_profiles/inflows_long.csv', index=True)

# Step 3: Convert the DataFrame to an xarray Dataset
ds = xr.Dataset.from_dataframe(df_combined)

# Step 4: Save the Dataset as a NetCDF file
output_nc_file = 'resources/renewable_profiles/profile_hydro.nc'
ds.to_netcdf(output_nc_file)


## COMPARE NETCDF FILES (the new one and the old one)

# # Load the NetCDF files
# inflows_nc = xr.open_dataset('resources/renewable_profiles/profile_hydro.nc')
# profile_hydro_nc_old = xr.open_dataset('resources/renewable_profiles/profile_hydro_pypsa.nc')

# # Compare dimensions
# dimensions_equal = inflows_nc.dims == profile_hydro_nc_old.dims

# # Compare variables
# variables_equal = inflows_nc.data_vars.keys() == profile_hydro_nc_old.data_vars.keys()

# # Compare variable attributes
# variable_attributes_equal = all(inflows_nc[var].attrs == profile_hydro_nc_old[var].attrs for var in inflows_nc.variables)

# # Compare global attributes
# global_attributes_equal = inflows_nc.attrs == profile_hydro_nc_old.attrs

# # Print comparison results
# print(f"Dimensions equal: {dimensions_equal}")
# print(f"Variables equal: {variables_equal}")
# print(f"Variable attributes equal: {variable_attributes_equal}")
# print(f"Global attributes equal: {global_attributes_equal}")
