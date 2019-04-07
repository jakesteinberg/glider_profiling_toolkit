
import numpy as np
import glob
import pickle
import matplotlib.pyplot as plt
from dive_processing_and_velocity_estimation import Glider
from tools import plot_pro

# ----------------------------------------------------------------------------------------------------------------------
# DIVE SELECTION (point to path of .nc files)
# -----------------------------------------------------------------------------------------
#        SG NUMBER,  DIVE NUMBERS,                DIVE FILE PATH
# -----------------------------------------------------------------------------------------
# --- DG BATS 2015
x = Glider(35, np.arange(101, 104), '/Users/jake/Documents/baroclinic_modes/DG/BATS_2015/sg035')

# ----------------------------------------------------------------------------------------------------------------------
# --- define vertical grid
bin_depth = np.concatenate((np.arange(0, 300, 5), np.arange(300, 1000, 10), np.arange(1000, 4600, 20)))  # 36N

# --- vertical bin averaging separation of dive-climb cycle into two profiles (extractions from nc files)
Binned = x.make_bin(bin_depth)
d_time = Binned['time']
lon = Binned['lon']
lat = Binned['lat']
ref_lat = np.nanmean(lat)
t = Binned['temp']
s = Binned['sal']
dac_u = Binned['dac_u']
dac_v = Binned['dac_v']
profile_tags = Binned['profs']
if 'o2' in Binned.keys():
    o2 = Binned['o2']

# ----------------------------------------------------------------------------------------------------------------------
# --- compute of absolute salinity, conservative temperature, and potential density anomaly
sa, ct, theta, sig0, sig2, N2 = x.density(bin_depth, ref_lat, t, s, lon, lat)
# ----------------------------------------------------------------------------------------------------------------------
# --- compute velocity profiles using M/W sections and compute velocity
# --- density levels to estimate the depth of and plot and in plot_cross_section
sigth_levels = np.concatenate(
    [np.arange(23, 25.4, 0.4), np.arange(26.2, 27.2, 0.2),
     np.arange(27.2, 27.8, 0.2), np.arange(27.72, 27.8, 0.02), np.arange(27.8, 27.9, 0.01)])

# --- choice between single transect (_0) and all dives (_1, will separate into transects)
# toggle comment/uncomment
# --- for combined set of transects
# ds, dist, avg_ct_per_dep_0, avg_sa_per_dep_0, avg_sig0_per_dep_0, v_g, vbt, \
# isopycdep, isopycx, mwe_lon, mwe_lat, DACe_MW, DACn_MW, profile_tags_per, shear, v_g_east, v_g_north = \
#     x.transect_cross_section_1(bin_depth, sig0, ct, sa, lon, lat, dac_u, dac_v, profile_tags, sigth_levels, 1)

# --- for single transects (last value = choose to include(1)/exclude(0) partial M/W profiles)
ds, dist, avg_ct_per_dep_0, avg_sa_per_dep_0, avg_sig0_per_dep_0, v_g, vbt, \
isopycdep, isopycx, mwe_lon, mwe_lat, DACe_MW, DACn_MW, profile_tags_per, shear, v_g_east, v_g_north= \
    x.transect_cross_section_0(bin_depth, sig0, ct, sa, lon, lat, dac_u, dac_v, profile_tags, sigth_levels, 1)

# --- MAIN output (key)
# ds = distance along transect of velocity profiles
# dist = distance along transect of each grided measurement
# avg_ct_per_dep_0 = avg conservative temperature profile computed using the same profiles contributing to velocity est.
# avg_sa_per_dep_0 = same as above for absolute salinity
# avg_sig0_per_dep_0 = same as above for potential density referenced to the surface
# v_g = cross-track geostrophic velocity profiles
# vbt = cross-track barotropic depth avg current (DAC)
# isopycdep = depth of specficied isopycnals along profile path
# isopycx = distance along transec of specified isopycnals
# mwe_lon = longitude of velocity profiles and avg ca, sa, sig profiles
# mwe_lat = latitude of velocity profiles and avg ca, sa, sig profiles
# DACe_MW = Eastward component of DAC
# DACn_MW = Northward component of DAC
# profile_tags_per = profiles contributing to each transect
# shear = along-track density gradient ~ vertical shear of the cross-track velocity
# v_g_east = Eastward component of v_g
# v_g_north = Northward component of v_g
# ----------------------------------------------------------------------------------------------------------------------
# --- PLOT cross section
# define velocity contours
u_levels = np.arange(-0.4, 0.4, .04)
# --- plot single transect from set (use if ran transect_cross_section_1)
# transect_no = 3
# fig0 = x.plot_cross_section(bin_depth, ds[transect_no], v_g[transect_no], dist[transect_no],
#                             profile_tags_per[transect_no], isopycdep[transect_no], isopycx[transect_no],
#                             sigth_levels, d_time, u_levels)
# --- plot single transect from single transect input (use if ran transect_cross_section_0)
fig0 = x.plot_cross_section(bin_depth, ds, v_g, dist, profile_tags_per, isopycdep, isopycx,
                            sigth_levels, d_time, u_levels)

# --- save option
# fig0.savefig("/Users/jake/Documents/Conferences/USCLIVAR_19/eddy_cross.jpeg", dpi=450)
# ----------------------------------------------------------------------------------------------------------------------
# --- PLOT plan view
# load in bathymetry and lat/lon plotting bounds
# BATS
bathy_path = '/Users/jake/Desktop/bats/bats_bathymetry/GEBCO_2014_2D_-67.7_29.8_-59.9_34.8.nc'
plan_window = [-66, -63, 31, 33]  # lon/lat plotting boundaries

# --- for combined set of transects ---
# x.plot_plan_view(lon, lat, mwe_lon[transect_no], mwe_lat[transect_no],
#                  DACe_MW[transect_no], DACn_MW[transect_no],
#                  ref_lat, profile_tags_per[transect_no], d_time, plan_window, bathy_path)
# --- for single transect ---
x.plot_plan_view(lon, lat, mwe_lon, mwe_lat, DACe_MW, DACn_MW,
                 ref_lat, profile_tags_per, d_time, plan_window, bathy_path)
# ----------------------------------------------------------------------------------------------------------------------
# --- PLOT absolute salinity vs. conservative temp
x.plot_t_s(ct, sa, d_time)
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# --- PLOT Velocity Profiles
# --- for combined set of transects ---
# x.plot_v(bin_depth, v_g[transect_no], d_time, profile_tags, np.arange(-0.25, 0.25, .02))
# --- for single transect ---
x.plot_v(bin_depth, v_g, d_time, profile_tags, np.arange(-0.25, 0.25, .02))
# ----------------------------------------------------------------------------------------------------------------------
# TESTING OF TRANSECT SEPARATION AND GROUPING
# def group_consecutives(vals, step=1):
#     """Return list of consecutive lists of numbers from vals (number list)."""
#     run = []
#     result = [run]
#     expect = None
#     for v in vals:
#         if (v == expect) or (expect is None):
#             run.append(v)
#         else:
#             run = [v]
#             result.append(run)
#         expect = v + step
#     return result
#
# # separate dives into unique transects
# target_test = 1000000 * x.target[:, 0] + np.round(x.target[:, 1], 3)
# unique_targets = np.unique(target_test)
# transects = []
# for m in range(len(unique_targets)):
#     indices = np.where(target_test == unique_targets[m])[0]
#     if len(indices) > 1:
#         transects.append(group_consecutives(indices, step=1))

# ds_out = []
# dist_out = []
# v_g_out = []
# vbt_out = []
# isopycdep_out = []
# isopycx_out = []
# mwe_lon_out = []
# mwe_lat_out = []
# DACe_MW_out = []
# DACn_MW_out = []
# profile_tags_out = []
# for n in range(len(transects)):  # loop over all transect segments
#     for o in range(len(transects[n])):  # loop over all times a glider executed that segment
#         this_transect = transects[n][o]
#         index_start = 2 * this_transect[0]
#         index_end = 2 * (this_transect[-1] + 1)
#         order_set = np.arange(0, 2 * len(this_transect), 2)
#         sig0_t = sig0[:, index_start:index_end]
#         lon_t = lon[:, index_start:index_end]
#         lat_t = lat[:, index_start:index_end]
#         dac_u_t = dac_u[index_start:index_end]
#         dac_v_t = dac_v[index_start:index_end]
#         profile_tags_t = profile_tags[index_start:index_end]

# _____________________________________________________________________________________________________________________
# vehicle pitch: 'eng_pitchAng'
# DAC_u: 'depth_avg_curr_east'
# DAC_v: 'depth_avg_curr_north'
