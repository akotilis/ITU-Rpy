# -*- coding: utf-8 -*-
""" This example shows how to compute the rainfall-rate (mm/hr) exceeded
for 0.01 % of the time of the average year over a large region of the Earth.

This image is similar to the one plotted in page 5 of Recommendation
ITU-R P.837-7.
"""
import itur
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import numpy as np
from astropy import units as u
# Set Recommendation ITU-R P.837 to version 7
itur.models.itu837.change_version(7)
itur.models.itu1814.change_version(1)

# Generate a regular grid of latitude and longitudes with 0.1 degree resolution
# for the region of interest.
#lat, lon = itur.utils.regular_lat_lon_grid(resolution_lat=1, resolution_lon=1, lon_start_0=False,
 #                        lat_min=-90, lat_max=90, lon_min=-180, lon_max=180):
lat, lon = itur.utils.regular_lat_lon_grid(resolution_lat=.1,
                                            resolution_lon=.1)
#europe
#lat, lon = itur.utils.regular_lat_lon_grid(resolution_lat=1,
#                                           resolution_lon=1,lat_min=35, lat_max=72, lon_min=-25, lon_max =65)

# Compute the rainfall rate exceeded for 0.01 % of the time.
p = 1
path_length =  5.0 * itur.u.km#km
R001 = itur.models.itu837.rainfall_rate(lat, lon, p)
dsd_shape_param = 0

#calculate the attenutation due to this rain
itu1814_model = itur.models.itu1814.__ITU1814__(version=1)
#attenuation_rain = itu1814_model.specific_attenuation_due_to_rain(
#    rain_rate=R001,  # Rain rate in mm/hr
#    dsd_shape_param=0  # DSD shape parameter (0 for typical)
#)

# Create an empty matrix to store the results
print("done with calculating rain rate")
attenuation_rain = np.empty(R001.shape, dtype=object)

# Iterate over the matrix and calculate attenuation for each element
for i in range(0,R001.shape[0]):

    for j in range(0,R001.shape[1]):
        print("still working on row ", i, " and column ",j)
        attenuation_rain[i, j] = itu1814_model. path_attentuation_due_to_rain(R001[i, j], dsd_shape_param, path_length)

        #print(type(attenuation_rain[i,j]))
# Display the results in a map
#attenuation_rain_float = np.array([[val.value for val in row] for row in attenuation_rain], dtype=float)

#    attenuation_rain_float = np.array([
#        [val.value if val is not None else np.nan for val in row]
#        for row in attenuation_rain
#    ], dtype=float)
# attenuation_rain = u.Quantity(attenuation_rain)
# #attenuation_rain = itu1814_model.specific_attenuation_due_to_rain(rain_rate=R001, dsd_shape_param=0)
# fig = plt.figure(figsize=(16, 8))
# ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
# m = itur.plotting.plot_in_map(
#     R001, lat, lon, cmap='jet', vmin=0, vmax=90, ax=ax,
#     cbar_text='Rainfall rate exceeded for 0.01% of an average year [mm/hr]')

attenuation_rain_float = np.array(
    [[val.value if val is not None else np.nan for val in row] for row in attenuation_rain],
    dtype=float
)

# Plot the attenuation map
fig = plt.figure(figsize=(16, 8))
ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
m = itur.plotting.plot_in_map(
    attenuation_rain_float, lat, lon, cmap='jet', vmin=0, vmax=np.nanmax(attenuation_rain_float), ax=ax,
    cbar_text=f'Specific attenuation due to rain exceeded by {p}% of time for link of {path_length} [dB]'
)
plt.show()