import pandas as pd
import numpy as np
import datetime
import requests
import xarray as xr
import os



lev=[1000.0, 975.0, 950.0, 925.0, 900.0, 850.0, 800.0, 
     750.0, 700.0, 650.0, 600.0, 550.0, 500.0, 450.0, 400.0, 350.0, 300.0, 
     250.0, 200.0, 150.0, 100.0, 70.0, 50.0, 40.0, 30.0, 20.0]

lev = np.array(lev)


def round_to_grid(value, res=0.25):
    return round(value / res) * res
    

#for multiple forecatsing hour and if the variable is pressure level

def get_data_preprocess(date,utc,ft,var,pvar='yes',lon_range=None, lat_range=None):
    if isinstance(date, str):
        date = datetime.datetime.strptime(date, "%Y-%m-%d")
    elif isinstance(date, datetime.date):
        date = datetime.datetime.combine(date, datetime.time.min)

    yy, mm, dd = date.year, date.month, date.day
    
    if lon_range is None:
        lon_range = (60, 100)
    if lat_range is None:
        lat_range = (0, 40)

    # Calculate start and end indices
  # Ensure resolution alignment (GFS 0.25° grid)


    # Snap inputs to nearest valid grid points
    lon_start_val = round_to_grid(lon_range[0])
    lon_end_val   = round_to_grid(lon_range[1])
    lat_start_val = round_to_grid(lat_range[0])
    lat_end_val   = round_to_grid(lat_range[1])

    # Calculate index positions based on grid starting at 0°
    lon_start_idx = int((lon_start_val - 0) / 0.25)
    lon_end_idx   = int((lon_end_val - 0) / 0.25)

    lat_start_idx = int(((lat_start_val - 0)+90) / 0.25)
    lat_end_idx   = int(((lat_end_val - 0)+90)    / 0.25)

    # Create coordinate arrays
    lon_coords = np.arange(lon_start_val, lon_end_val + 0.25, 0.25)
    lat_coords = np.arange(lat_start_val, lat_end_val + 0.25, 0.25)
    

    n1=(np.shape(lon_coords)[0])
    n2=(np.shape(lat_coords)[0])
    
    print(lat_end_idx,lon_end_idx)
    
    

    start_date = datetime.datetime(yy, mm, dd, tzinfo=datetime.timezone.utc)
    dt_index = pd.date_range(start=start_date, periods=ft+1, freq='h')

    if pvar=='yes':
        url=f'https://nomads.ncep.noaa.gov/dods/gfs_0p25/gfs{yy}{mm:02d}{dd}/gfs_0p25_{utc:02d}z.ascii?{var}%5B0:{ft:02d}%5D%5B0:25%5D%5B{lat_start_idx}:{lat_end_idx}%5D%5B{lon_start_idx}:{lon_end_idx}%5D'
        try:
            # Send a GET request to fetch data from the URL
            response = requests.get(url)
            # Raise an HTTPError if the HTTP request returned an unsuccessful status code
            response.raise_for_status()
            filename = f'station.csv'
            with open(filename, 'w') as f:
                f.write(response.text)

            df=pd.read_csv('station.csv',skiprows=1,header=None,low_memory=False)
            df1=df.iloc[:-8,1:].astype(float)
            df1=df1.dropna(axis=1,how='all')

            df11=df1.values.reshape(ft+1,26, n2, n1)
            dt_index_naive = dt_index.tz_convert(None)


            ds= xr.Dataset(
                {
                    f"{var}": (("time","levels","lon", "lat"), np.array(df11.astype(float)))
                },
                coords={
                     "time": dt_index_naive,
                    "levels": lev,
                    "lat": lat_coords,
                    "lon": lon_coords
                }
            )
            ds1=ds.transpose('time','level',"lat","lon")

        except requests.exceptions.RequestException as e:
                print(f"An error occurred: {e}")
    else:
        url=f'https://nomads.ncep.noaa.gov/dods/gfs_0p25/gfs{yy}{mm:02d}{dd}/gfs_0p25_{utc:02d}z.ascii?{var}%5B0:{ft:01d}%5D%5B{lat_start_idx}:{lat_end_idx}%5D%5B{lon_start_idx}:{lon_end_idx}%5D'
        try:
            # Send a GET request to fetch data from the URL
            response = requests.get(url)
            # Raise an HTTPError if the HTTP request returned an unsuccessful status code
            response.raise_for_status()
            filename = f'station.csv'
            lines = response.text.splitlines()

            lines_to_save = lines[:-6]

            text_to_save = "\n".join(lines_to_save)
            
            with open(filename, 'w') as f:
                f.write(text_to_save)
            # print(f"Data successfully written to {filename}")
            df=pd.read_csv('station.csv',skiprows=1,header=None,low_memory=False)
            df1=df.iloc[:,1:]
            df11=df1.values.reshape(ft+1, n2, n1)
            dt_index_naive = dt_index.tz_convert(None)

            ds= xr.Dataset(
                {
                    f"{var}": (("time","lat", "lon"), np.array(df11.astype(float)))
                },
                coords={
                    "time": dt_index_naive,
                    "lat": lat_coords,"lon": lon_coords,
                    
                }
            )

            ds1=ds.transpose('time',"lat","lon")
        except requests.exceptions.RequestException as e:
                print(f"An error occurred: {e}")
    
    # print(url)
    os.remove('station.csv')

    return ds1



#for a single forecast hour
def get_data_preprocess_s(date,utc,ft,var,pvar='yes',lon_range=None,lat_range=None):
    if isinstance(date, str):
        date = datetime.datetime.strptime(date, "%Y-%m-%d")
    elif isinstance(date, datetime.date):
        date = datetime.datetime.combine(date, datetime.time.min)

    yy, mm, dd = date.year, date.month, date.day
    
    if lon_range is None:
        lon_range = (0, 100)
    if lat_range is None:
        lat_range = (0, 40)



    # Snap inputs to nearest valid grid points
    lon_start_val = round_to_grid(lon_range[0])
    lon_end_val   = round_to_grid(lon_range[1])
    lat_start_val = round_to_grid(lat_range[0])
    lat_end_val   = round_to_grid(lat_range[1])

    # Calculate index positions based on grid starting at 0°
    lon_start_idx = int((lon_start_val - 0) / 0.25)
    lon_end_idx   = int((lon_end_val - 0) / 0.25)

    lat_start_idx = int(((lat_start_val - 0)+90) / 0.25)
    lat_end_idx   = int(((lat_end_val - 0)+90)    / 0.25)

    # Create coordinate arrays
    lon_coords = np.arange(lon_start_val, lon_end_val + 0.25, 0.25)
    lat_coords = np.arange(lat_start_val, lat_end_val + 0.25, 0.25)


    n1=(np.shape(lon_coords)[0])
    n2=(np.shape(lat_coords)[0])
    
    
    
    start_date = datetime.datetime(yy, mm, dd, tzinfo=datetime.timezone.utc)
    ss = start_date+ + datetime.timedelta(hours=ft)
    dt_index = pd.DatetimeIndex([ss]).tz_convert(None)


    if pvar=='yes':
        url=f'https://nomads.ncep.noaa.gov/dods/gfs_0p25/gfs{yy}{mm:02d}{dd}/gfs_0p25_{utc:02d}z.ascii?{var}%5B{ft:02d}%5D%5B0:25%5D%5B{lat_start_idx}:{lat_end_idx}%5D%5B{lon_start_idx}:{lon_end_idx}%5D'
        try:
            # Send a GET request to fetch data from the URL
            response = requests.get(url)
            # Raise an HTTPError if the HTTP request returned an unsuccessful status code
            response.raise_for_status()
            filename = f'station.csv'
            with open(filename, 'w') as f:
                f.write(response.text)

            df=pd.read_csv('station.csv',skiprows=1,header=None,low_memory=False)
            df1=df.iloc[:-8,1:].astype(float)
            df1=df1.dropna(axis=1,how='all')
            
            df11=df1.values.reshape(1,26, n2, n1)

            ds= xr.Dataset(
                {
                    f"{var}": (("time","lat", "lon"), np.array(df11.astype(float)))
                },
                coords={
                    "time":dt_index,
                    "lat": lat_coords,
                    "lon": lon_coords
                }
            )
            
           
            
            ds1=ds.transpose('time','level',"lat","lon")

        except requests.exceptions.RequestException as e:
                print(f"An error occurred: {e}")
    else:
        url=f'https://nomads.ncep.noaa.gov/dods/gfs_0p25/gfs{yy}{mm:02d}{dd}/gfs_0p25_{utc:02d}z.ascii?{var}%5B{ft:02d}%5D%5B{lat_start_idx}:{lat_end_idx}%5D%5B{lon_start_idx}:{lon_end_idx}%5D'
        try:
            # Send a GET request to fetch data from the URL
            response = requests.get(url)
            # Raise an HTTPError if the HTTP request returned an unsuccessful status code
            response.raise_for_status()
            filename = f'station.csv'
            lines = response.text.splitlines()

            lines_to_save = lines[:-6]

            text_to_save = "\n".join(lines_to_save)


            with open(filename, 'w') as f:
                f.write(text_to_save)
            # print(f"Data successfully written to {filename}")
            df=pd.read_csv('station.csv',skiprows=1,header=None,low_memory=False)
            df1=df.iloc[:,1:]
            df1=df1.dropna(axis=1,how='all')
            
            df11=df1.values.reshape(1, n2, n1)
                        
            ds= xr.Dataset(
                {
                    f"{var}": (("time","lat", "lon"), np.array(df11.astype(float)))
                },
                coords={
                    "time": dt_index,
                    "lat": lat_coords,"lon": lon_coords,
                    
                }
            )
            ds1=ds.transpose('time',"lat","lon")

        except requests.exceptions.RequestException as e:
                print(f"An error occurred: {e}")
    
    # print(url)
    os.remove('station.csv')
    
    return ds1