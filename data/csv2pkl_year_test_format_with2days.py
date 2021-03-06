# coding: utf-8

# MIT License
# 
# Copyright (c) 2018 Duong Nguyen
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# ==============================================================================

"""
A script to merge AIS messages into AIS tracks.
"""
import numpy as np
import matplotlib.pyplot as plt
import os
import sys
#sys.path.append("..")
#import utils
import pickle
import copy
import csv
from datetime import datetime
import time
from io import StringIO
from tqdm import tqdm as tqdm

## PARAMS
#======================================

## Bretagne dataset
# LAT_MIN = 46.5
# LAT_MAX = 50.5
# LON_MIN = -8.0
# LON_MAX = -3.0

# # Pkl filenames.
# pkl_filename = "bretagne_20170103_track.pkl"
# pkl_filename_train = "bretagne_20170103_10_20_train_track.pkl"
# pkl_filename_valid = "bretagne_20170103_10_20_valid_track.pkl"
# pkl_filename_test  = "bretagne_20170103_10_20_test_track.pkl"

# # Path to csv files.
# dataset_path = "./"
# l_csv_filename =["positions_bretagne_jan_mar_2017.csv"]


# # Training/validation/test/total period.
# t_train_min = time.mktime(time.strptime("01/01/2017 00:00:00", "%d/%m/%Y %H:%M:%S"))
# t_train_max = time.mktime(time.strptime("10/03/2017 23:59:59", "%d/%m/%Y %H:%M:%S"))
# t_valid_min = time.mktime(time.strptime("11/03/2017 00:00:00", "%d/%m/%Y %H:%M:%S"))
# t_valid_max = time.mktime(time.strptime("20/03/2017 23:59:59", "%d/%m/%Y %H:%M:%S"))
# t_test_min  = time.mktime(time.strptime("21/03/2017 00:00:00", "%d/%m/%Y %H:%M:%S"))
# t_test_max  = time.mktime(time.strptime("31/03/2017 23:59:59", "%d/%m/%Y %H:%M:%S"))
# t_min = time.mktime(time.strptime("01/01/2017 00:00:00", "%d/%m/%Y %H:%M:%S"))
# t_max = time.mktime(time.strptime("31/03/2017 23:59:59", "%d/%m/%Y %H:%M:%S"))

# cargo_tanker_filename = "bretagne_20170103_cargo_tanker.npy"

# ## Aruba
#LAT_MIN = 9.0
#LAT_MAX = 14.0
#LON_MIN = -71.0
#LON_MAX = -66.0

D2C_MIN = 2000 #meters


#===============
"""
dataset_path = "./"
l_csv_filename =["aruba_5x5deg_2017305_2018031.csv",
                 "aruba_5x5deg_2018305_2019031.csv",
                 "aruba_5x5deg_2019305_2020031.csv"]
l_csv_filename =["aruba_5x5deg_2017305_2018031.csv"]
pkl_filename = "aruba_20172020_track.pkl"
pkl_filename_train = "aruba_20172020_train_track.pkl"
pkl_filename_valid = "aruba_20172020_valid_track.pkl"
pkl_filename_test  = "aruba_20172020_test_track.pkl"

cargo_tanker_filename = "aruba_20172020_cargo_tanker.npy"

t_train_min = time.mktime(time.strptime("01/01/2017 00:00:00", "%d/%m/%Y %H:%M:%S"))
t_train_max = time.mktime(time.strptime("31/01/2019 23:59:59", "%d/%m/%Y %H:%M:%S"))
t_valid_min = time.mktime(time.strptime("01/11/2019 00:00:00", "%d/%m/%Y %H:%M:%S"))
t_valid_max = time.mktime(time.strptime("31/12/2019 23:59:59", "%d/%m/%Y %H:%M:%S"))
t_test_min  = time.mktime(time.strptime("01/01/2020 00:00:00", "%d/%m/%Y %H:%M:%S"))
t_test_max  = time.mktime(time.strptime("31/01/2020 23:59:59", "%d/%m/%Y %H:%M:%S"))
t_min = time.mktime(time.strptime("01/01/2017 00:00:00", "%d/%m/%Y %H:%M:%S"))
t_max = time.mktime(time.strptime("31/01/2020 23:59:59", "%d/%m/%Y %H:%M:%S"))

"""

#===============
"""
dataset_path = "./"
l_csv_filename =["aruba_zone1_5x5deg_2017121_2017244.csv",
                 "aruba_5x5deg_2018121_2018244.csv",
                 "aruba_zone1_5x5deg_2019121_2019244.csv"]
#l_csv_filename =["aruba_5x5deg_2018121_2018244.csv"]
pkl_filename = "aruba_20172020_summer_track.pkl"
pkl_filename_train = "aruba_20172020_summer_train_track.pkl"
pkl_filename_valid = "aruba_20172020_summer_valid_track.pkl"
pkl_filename_test  = "aruba_20172020_summer_test_track.pkl"

cargo_tanker_filename = "aruba_20172020_summer_cargo_tanker.npy"

t_train_min = time.mktime(time.strptime("01/01/2017 00:00:00", "%d/%m/%Y %H:%M:%S"))
t_train_max = time.mktime(time.strptime("31/08/2018 23:59:59", "%d/%m/%Y %H:%M:%S"))
t_valid_min = time.mktime(time.strptime("01/05/2019 00:00:00", "%d/%m/%Y %H:%M:%S"))
t_valid_max = time.mktime(time.strptime("31/07/2019 23:59:59", "%d/%m/%Y %H:%M:%S"))
t_test_min  = time.mktime(time.strptime("01/08/2019 00:00:00", "%d/%m/%Y %H:%M:%S"))
t_test_max  = time.mktime(time.strptime("31/08/2019 23:59:59", "%d/%m/%Y %H:%M:%S"))
t_min = time.mktime(time.strptime("01/01/2017 00:00:00", "%d/%m/%Y %H:%M:%S"))
t_max = time.mktime(time.strptime("31/01/2020 23:59:59", "%d/%m/%Y %H:%M:%S"))
"""

#===============
"""
dataset_path = "./"
l_csv_filename =["aruba_zone1_5x5deg_2017121_2017244.csv",
                 "aruba_5x5deg_2017305_2018031.csv",
                 "aruba_5x5deg_2018121_2018244.csv",
                 "Aruba_5x5deg_2018305_2019031.csv",
                 "aruba_zone1_5x5deg_2019121_2019244.csv"]
#l_csv_filename =["Aruba_5x5deg_2018305_2019031.csv"]
pkl_filename = "aruba_20172019_track.pkl"
pkl_filename_train = "aruba_20172019_all_train_track.pkl"
pkl_filename_valid = "aruba_20172019_all_valid_track.pkl"
pkl_filename_test  = "aruba_20172019_all_test_track.pkl"

cargo_tanker_filename = "aruba_20172019_all_cargo_tanker.npy"

t_train_min = time.mktime(time.strptime("01/01/2017 00:00:00", "%d/%m/%Y %H:%M:%S"))
t_train_max = time.mktime(time.strptime("31/01/2019 23:59:59", "%d/%m/%Y %H:%M:%S"))
t_valid_min = time.mktime(time.strptime("01/05/2019 00:00:00", "%d/%m/%Y %H:%M:%S"))
t_valid_max = time.mktime(time.strptime("31/07/2019 23:59:59", "%d/%m/%Y %H:%M:%S"))
t_test_min  = time.mktime(time.strptime("01/08/2019 00:00:00", "%d/%m/%Y %H:%M:%S"))
t_test_max  = time.mktime(time.strptime("31/08/2019 23:59:59", "%d/%m/%Y %H:%M:%S"))
t_min = time.mktime(time.strptime("01/01/2017 00:00:00", "%d/%m/%Y %H:%M:%S"))
t_max = time.mktime(time.strptime("31/01/2020 23:59:59", "%d/%m/%Y %H:%M:%S"))
"""

#===============
### ## Est Aruba
##LAT_MIN = 10.0
##LAT_MAX = 14.0
##LON_MIN = -66.0
##LON_MAX = -60.0
##
##dataset_path = "./"
##l_csv_filename =["Est-aruba_5x5deg_2018001_2018120.csv",
##                 "Est-aruba_5x5deg_2018001_2018180.csv",
##                "Est-aruba_5x5deg_2019240_2019365_.csv"]
###l_csv_filename =["Est-aruba_5x5deg_2018001_2018180.csv"]
##pkl_filename = "estaruba_20182019_track.pkl"
##pkl_filename_train = "estaruba_20182019_train_track.pkl"
##pkl_filename_valid = "estaruba_20182019_valid_track.pkl"
##pkl_filename_test  = "estaruba_20182019_test_track.pkl"
##
##cargo_tanker_filename = "estaruba_20182019_cargo_tanker.npy"
##
##t_train_min = time.mktime(time.strptime("01/01/2018 00:00:00", "%d/%m/%Y %H:%M:%S"))
##t_train_max = time.mktime(time.strptime("30/04/2019 23:59:59", "%d/%m/%Y %H:%M:%S"))
##t_valid_min = time.mktime(time.strptime("01/09/2019 00:00:00", "%d/%m/%Y %H:%M:%S"))
##t_valid_max = time.mktime(time.strptime("30/11/2019 23:59:59", "%d/%m/%Y %H:%M:%S"))
##t_test_min  = time.mktime(time.strptime("01/12/2019 00:00:00", "%d/%m/%Y %H:%M:%S"))
##t_test_max  = time.mktime(time.strptime("31/12/2019 23:59:59", "%d/%m/%Y %H:%M:%S"))
##t_min = time.mktime(time.strptime("01/01/2017 00:00:00", "%d/%m/%Y %H:%M:%S"))
##t_max = time.mktime(time.strptime("31/01/2020 23:59:59", "%d/%m/%Y %H:%M:%S"))
##
###========================================================================
##LAT_RANGE = LAT_MAX - LAT_MIN
##LON_RANGE = LON_MAX - LON_MIN
##SOG_MAX = 30.0  # the SOG is truncated to 30.0 knots max.
##
##EPOCH = datetime(1970, 1, 1)
##LAT, LON, SOG, COG, HEADING, ROT, NAV_STT, TIMESTAMP, MMSI, SHIPTYPE, D2C  = list(range(11))
##
##CARGO_TANKER_ONLY = True
##if  CARGO_TANKER_ONLY:
##    pkl_filename = "ct_"+pkl_filename
##    pkl_filename_train = "ct_"+pkl_filename_train
##    pkl_filename_valid = "ct_"+pkl_filename_valid
##    pkl_filename_test  = "ct_"+pkl_filename_test
##    
##print(pkl_filename_train)

###########################################################
# ## AIS New York Harbor
#[40.33, 40.77, -74.30, -73.50] # LAT(min, max), LON(min, max)

LAT_MIN = 40.33
LAT_MAX = 40.77
LON_MIN = -74.30
LON_MAX = -73.50

dataset_path = "./AIS_raw/"
l_csv_filename = ["AIS_2018_01_01.csv",
"AIS_2018_01_02.csv"] #,
'''
"AIS_2018_01_03.csv",
"AIS_2018_01_04.csv",
"AIS_2018_01_05.csv",
"AIS_2018_01_06.csv",
"AIS_2018_01_07.csv",
"AIS_2018_01_08.csv",
"AIS_2018_01_09.csv",
"AIS_2018_01_10.csv",
"AIS_2018_01_11.csv",
"AIS_2018_01_12.csv",
"AIS_2018_01_13.csv",
"AIS_2018_01_14.csv",
"AIS_2018_01_15.csv",
"AIS_2018_01_16.csv",
"AIS_2018_01_17.csv",
"AIS_2018_01_18.csv",
"AIS_2018_01_19.csv",
"AIS_2018_01_20.csv",
"AIS_2018_01_21.csv",
"AIS_2018_01_22.csv",
"AIS_2018_01_23.csv",
"AIS_2018_01_24.csv",
"AIS_2018_01_25.csv",
"AIS_2018_01_26.csv",
"AIS_2018_01_27.csv",
"AIS_2018_01_28.csv",
"AIS_2018_01_29.csv",
"AIS_2018_01_30.csv",
"AIS_2018_01_31.csv",
"AIS_2018_02_01.csv",
"AIS_2018_02_02.csv",
"AIS_2018_02_03.csv",
"AIS_2018_02_04.csv",
"AIS_2018_02_05.csv",
"AIS_2018_02_06.csv",
"AIS_2018_02_07.csv",
"AIS_2018_02_08.csv",
"AIS_2018_02_09.csv",
"AIS_2018_02_10.csv",
"AIS_2018_02_11.csv",
"AIS_2018_02_12.csv",
"AIS_2018_02_13.csv",
"AIS_2018_02_14.csv",
"AIS_2018_02_15.csv",
"AIS_2018_02_16.csv",
"AIS_2018_02_17.csv",
"AIS_2018_02_18.csv",
"AIS_2018_02_19.csv",
"AIS_2018_02_20.csv",
"AIS_2018_02_21.csv",
"AIS_2018_02_22.csv",
"AIS_2018_02_23.csv",
"AIS_2018_02_24.csv",
"AIS_2018_02_25.csv",
"AIS_2018_02_26.csv",
"AIS_2018_02_27.csv",
"AIS_2018_02_28.csv",
"AIS_2018_03_01.csv",
"AIS_2018_03_02.csv",
"AIS_2018_03_03.csv",
"AIS_2018_03_04.csv",
"AIS_2018_03_05.csv",
"AIS_2018_03_06.csv",
"AIS_2018_03_07.csv",
"AIS_2018_03_08.csv",
"AIS_2018_03_09.csv",
"AIS_2018_03_10.csv",
"AIS_2018_03_11.csv",
"AIS_2018_03_12.csv",
"AIS_2018_03_13.csv",
"AIS_2018_03_14.csv",
"AIS_2018_03_15.csv",
"AIS_2018_03_16.csv",
"AIS_2018_03_17.csv",
"AIS_2018_03_18.csv",
"AIS_2018_03_19.csv",
"AIS_2018_03_20.csv",
"AIS_2018_03_21.csv",
"AIS_2018_03_22.csv",
"AIS_2018_03_23.csv",
"AIS_2018_03_24.csv",
"AIS_2018_03_25.csv",
"AIS_2018_03_26.csv",
"AIS_2018_03_27.csv",
"AIS_2018_03_28.csv",
"AIS_2018_03_29.csv",
"AIS_2018_03_30.csv",
"AIS_2018_03_31.csv",
"AIS_2018_04_01.csv",
"AIS_2018_04_02.csv",
"AIS_2018_04_03.csv",
"AIS_2018_04_04.csv",
"AIS_2018_04_05.csv",
"AIS_2018_04_06.csv",
"AIS_2018_04_07.csv",
"AIS_2018_04_08.csv",
"AIS_2018_04_09.csv",
"AIS_2018_04_10.csv",
"AIS_2018_04_11.csv",
"AIS_2018_04_12.csv",
"AIS_2018_04_13.csv",
"AIS_2018_04_14.csv",
"AIS_2018_04_15.csv",
"AIS_2018_04_16.csv",
"AIS_2018_04_17.csv",
"AIS_2018_04_18.csv",
"AIS_2018_04_19.csv",
"AIS_2018_04_20.csv",
"AIS_2018_04_21.csv",
"AIS_2018_04_22.csv",
"AIS_2018_04_23.csv",
"AIS_2018_04_24.csv",
"AIS_2018_04_25.csv",
"AIS_2018_04_26.csv",
"AIS_2018_04_27.csv",
"AIS_2018_04_28.csv",
"AIS_2018_04_29.csv",
"AIS_2018_04_30.csv",
"AIS_2018_05_01.csv",
"AIS_2018_05_02.csv",
"AIS_2018_05_03.csv",
"AIS_2018_05_04.csv",
"AIS_2018_05_05.csv",
"AIS_2018_05_06.csv",
"AIS_2018_05_07.csv",
"AIS_2018_05_08.csv",
"AIS_2018_05_09.csv",
"AIS_2018_05_10.csv",
"AIS_2018_05_11.csv",
"AIS_2018_05_12.csv",
"AIS_2018_05_13.csv",
"AIS_2018_05_14.csv",
"AIS_2018_05_15.csv",
"AIS_2018_05_16.csv",
"AIS_2018_05_17.csv",
"AIS_2018_05_18.csv",
"AIS_2018_05_19.csv",
"AIS_2018_05_20.csv",
"AIS_2018_05_21.csv",
"AIS_2018_05_22.csv",
"AIS_2018_05_23.csv",
"AIS_2018_05_24.csv",
"AIS_2018_05_25.csv",
"AIS_2018_05_26.csv",
"AIS_2018_05_27.csv",
"AIS_2018_05_28.csv",
"AIS_2018_05_29.csv",
"AIS_2018_05_30.csv",
"AIS_2018_05_31.csv",
"AIS_2018_06_01.csv",
"AIS_2018_06_02.csv",
"AIS_2018_06_03.csv",
"AIS_2018_06_04.csv",
"AIS_2018_06_05.csv",
"AIS_2018_06_06.csv",
"AIS_2018_06_07.csv",
"AIS_2018_06_08.csv",
"AIS_2018_06_09.csv",
"AIS_2018_06_10.csv",
"AIS_2018_06_11.csv",
"AIS_2018_06_12.csv",
"AIS_2018_06_13.csv",
"AIS_2018_06_14.csv",
"AIS_2018_06_15.csv",
"AIS_2018_06_16.csv",
"AIS_2018_06_17.csv",
"AIS_2018_06_18.csv",
"AIS_2018_06_19.csv",
"AIS_2018_06_20.csv",
"AIS_2018_06_21.csv",
"AIS_2018_06_22.csv",
"AIS_2018_06_23.csv",
"AIS_2018_06_24.csv",
"AIS_2018_06_25.csv",
"AIS_2018_06_26.csv",
"AIS_2018_06_27.csv",
"AIS_2018_06_28.csv",
"AIS_2018_06_29.csv",
"AIS_2018_06_30.csv",
"AIS_2018_07_01.csv",
"AIS_2018_07_02.csv",
"AIS_2018_07_03.csv",
"AIS_2018_07_04.csv",
"AIS_2018_07_05.csv",
"AIS_2018_07_06.csv",
"AIS_2018_07_07.csv",
"AIS_2018_07_08.csv",
"AIS_2018_07_09.csv",
"AIS_2018_07_10.csv",
"AIS_2018_07_11.csv",
"AIS_2018_07_12.csv",
"AIS_2018_07_13.csv",
"AIS_2018_07_14.csv",
"AIS_2018_07_15.csv",
"AIS_2018_07_16.csv",
"AIS_2018_07_17.csv",
"AIS_2018_07_18.csv",
"AIS_2018_07_19.csv",
"AIS_2018_07_20.csv",
"AIS_2018_07_21.csv",
"AIS_2018_07_22.csv",
"AIS_2018_07_23.csv",
"AIS_2018_07_24.csv",
"AIS_2018_07_25.csv",
"AIS_2018_07_26.csv",
"AIS_2018_07_27.csv",
"AIS_2018_07_28.csv",
"AIS_2018_07_29.csv",
"AIS_2018_07_30.csv",
"AIS_2018_07_31.csv",
"AIS_2018_08_01.csv",
"AIS_2018_08_02.csv",
"AIS_2018_08_03.csv",
"AIS_2018_08_04.csv",
"AIS_2018_08_05.csv",
"AIS_2018_08_06.csv",
"AIS_2018_08_07.csv",
"AIS_2018_08_08.csv",
"AIS_2018_08_09.csv",
"AIS_2018_08_10.csv",
"AIS_2018_08_11.csv",
"AIS_2018_08_12.csv",
"AIS_2018_08_13.csv",
"AIS_2018_08_14.csv",
"AIS_2018_08_15.csv",
"AIS_2018_08_16.csv",
"AIS_2018_08_17.csv",
"AIS_2018_08_18.csv",
"AIS_2018_08_19.csv",
"AIS_2018_08_20.csv",
"AIS_2018_08_21.csv",
"AIS_2018_08_22.csv",
"AIS_2018_08_23.csv",
"AIS_2018_08_24.csv",
"AIS_2018_08_25.csv",
"AIS_2018_08_26.csv",
"AIS_2018_08_27.csv",
"AIS_2018_08_28.csv",
"AIS_2018_08_29.csv",
"AIS_2018_08_30.csv",
"AIS_2018_08_31.csv",
"AIS_2018_09_01.csv",
"AIS_2018_09_02.csv",
"AIS_2018_09_03.csv",
"AIS_2018_09_04.csv",
"AIS_2018_09_05.csv",
"AIS_2018_09_06.csv",
"AIS_2018_09_07.csv",
"AIS_2018_09_08.csv",
"AIS_2018_09_09.csv",
"AIS_2018_09_10.csv",
"AIS_2018_09_11.csv",
"AIS_2018_09_12.csv",
"AIS_2018_09_13.csv",
"AIS_2018_09_14.csv",
"AIS_2018_09_15.csv",
"AIS_2018_09_16.csv",
"AIS_2018_09_17.csv",
"AIS_2018_09_18.csv",
"AIS_2018_09_19.csv",
"AIS_2018_09_20.csv",
"AIS_2018_09_21.csv",
"AIS_2018_09_22.csv",
"AIS_2018_09_23.csv",
"AIS_2018_09_24.csv",
"AIS_2018_09_25.csv",
"AIS_2018_09_26.csv",
"AIS_2018_09_27.csv",
"AIS_2018_09_28.csv",
"AIS_2018_09_29.csv",
"AIS_2018_09_30.csv",
"AIS_2018_10_01.csv",
"AIS_2018_10_02.csv",
"AIS_2018_10_03.csv",
"AIS_2018_10_04.csv",
"AIS_2018_10_05.csv",
"AIS_2018_10_06.csv",
"AIS_2018_10_07.csv",
"AIS_2018_10_08.csv",
"AIS_2018_10_09.csv",
"AIS_2018_10_10.csv",
"AIS_2018_10_11.csv",
"AIS_2018_10_12.csv",
"AIS_2018_10_13.csv",
"AIS_2018_10_14.csv",
"AIS_2018_10_15.csv",
"AIS_2018_10_16.csv",
"AIS_2018_10_17.csv",
"AIS_2018_10_18.csv",
"AIS_2018_10_19.csv",
"AIS_2018_10_20.csv",
"AIS_2018_10_21.csv",
"AIS_2018_10_22.csv",
"AIS_2018_10_23.csv",
"AIS_2018_10_24.csv",
"AIS_2018_10_25.csv",
"AIS_2018_10_26.csv",
"AIS_2018_10_27.csv",
"AIS_2018_10_28.csv",
"AIS_2018_10_29.csv",
"AIS_2018_10_30.csv",
"AIS_2018_10_31.csv",
"AIS_2018_11_01.csv",
"AIS_2018_11_02.csv",
"AIS_2018_11_03.csv",
"AIS_2018_11_04.csv",
"AIS_2018_11_05.csv",
"AIS_2018_11_06.csv",
"AIS_2018_11_07.csv",
"AIS_2018_11_08.csv",
"AIS_2018_11_09.csv",
"AIS_2018_11_10.csv",
"AIS_2018_11_11.csv",
"AIS_2018_11_12.csv",
"AIS_2018_11_13.csv",
"AIS_2018_11_14.csv",
"AIS_2018_11_15.csv",
"AIS_2018_11_16.csv",
"AIS_2018_11_17.csv",
"AIS_2018_11_18.csv",
"AIS_2018_11_19.csv",
"AIS_2018_11_20.csv",
"AIS_2018_11_21.csv",
"AIS_2018_11_22.csv",
"AIS_2018_11_23.csv",
"AIS_2018_11_24.csv",
"AIS_2018_11_25.csv",
"AIS_2018_11_26.csv",
"AIS_2018_11_27.csv",
"AIS_2018_11_28.csv",
"AIS_2018_11_29.csv",
"AIS_2018_11_30.csv",
"AIS_2018_12_01.csv",
"AIS_2018_12_02.csv",
"AIS_2018_12_03.csv",
"AIS_2018_12_04.csv",
"AIS_2018_12_05.csv",
"AIS_2018_12_06.csv",
"AIS_2018_12_07.csv",
"AIS_2018_12_08.csv",
"AIS_2018_12_09.csv",
"AIS_2018_12_10.csv",
"AIS_2018_12_11.csv",
"AIS_2018_12_12.csv",
"AIS_2018_12_13.csv",
"AIS_2018_12_14.csv",
"AIS_2018_12_15.csv",
"AIS_2018_12_16.csv",
"AIS_2018_12_17.csv",
"AIS_2018_12_18.csv",
"AIS_2018_12_19.csv",
"AIS_2018_12_20.csv",
"AIS_2018_12_21.csv",
"AIS_2018_12_22.csv",
"AIS_2018_12_23.csv",
"AIS_2018_12_24.csv",
"AIS_2018_12_25.csv",
"AIS_2018_12_26.csv",
"AIS_2018_12_27.csv",
"AIS_2018_12_28.csv",
"AIS_2018_12_29.csv",
"AIS_2018_12_30.csv",
"AIS_2018_12_31.csv"  ]
'''
pkl_filename       = "AIS_20180101_track.pkl"
pkl_filename_train = "AIS_20180101_train_track.pkl"
pkl_filename_valid = "AIS_20180101_valid_track.pkl"
pkl_filename_test  = "AIS_20180101_test_track.pkl"

cargo_tanker_filename = "AIS_20180101_cargo_tanker.npy"

##t_train_min = time.mktime(time.strptime("01/01/2018 00:00:00", "%d/%m/%Y %H:%M:%S"))
##t_train_max = time.mktime(time.strptime("31/08/2018 23:59:59", "%d/%m/%Y %H:%M:%S"))
##t_valid_min = time.mktime(time.strptime("01/09/2018 00:00:00", "%d/%m/%Y %H:%M:%S"))
##t_valid_max = time.mktime(time.strptime("30/11/2018 23:59:59", "%d/%m/%Y %H:%M:%S"))
##t_test_min  = time.mktime(time.strptime("01/12/2018 00:00:00", "%d/%m/%Y %H:%M:%S"))
##t_test_max  = time.mktime(time.strptime("31/12/2018 23:59:59", "%d/%m/%Y %H:%M:%S"))


t_train_min = time.mktime(time.strptime("01/01/2018 00:00:00", "%d/%m/%Y %H:%M:%S"))
t_train_max = time.mktime(time.strptime("01/01/2018 10:59:59", "%d/%m/%Y %H:%M:%S"))
t_valid_min = time.mktime(time.strptime("01/01/2018 11:00:00", "%d/%m/%Y %H:%M:%S"))
t_valid_max = time.mktime(time.strptime("01/01/2018 23:59:59", "%d/%m/%Y %H:%M:%S"))
t_test_min  = time.mktime(time.strptime("01/01/2018 00:00:00", "%d/%m/%Y %H:%M:%S"))
t_test_max  = time.mktime(time.strptime("02/01/2018 23:59:59", "%d/%m/%Y %H:%M:%S"))

t_min = time.mktime(time.strptime("01/01/2018 00:00:00", "%d/%m/%Y %H:%M:%S"))
t_max = time.mktime(time.strptime("31/01/2020 23:59:59", "%d/%m/%Y %H:%M:%S"))

#========================================================================
LAT_RANGE = LAT_MAX - LAT_MIN
LON_RANGE = LON_MAX - LON_MIN
SOG_MAX = 30.0  # the SOG is truncated to 30.0 knots max.

EPOCH = datetime(1970, 1, 1)
#LAT, LON, SOG, COG, HEADING, ROT, NAV_STT, TIMESTAMP, MMSI, SHIPTYPE, D2C  = list(range(11))  #default format

#D2C = distance to coast
#https://github.com/CIA-Oceanix/GeoTrackNet/issues/7


#The format we get from AIS dataset
#MMSI, TIMESTAMP, LAT, LON, SOG, COG, HEADING, VESSELNAME, IMO, CALLSIGN,\
#SHIPTYPE, STATUS, LENGTH, WIDTH, DRAFT, CARGO, TRANSCEIVER_CLASS = list(range(17))



#THIS is the format we want to reformat into
#LAT, LON, SOG, COG, HEADING, ROT, NAV_STT, TIMESTAMP, MMSI


LAT, LON, SOG, COG, HEADING, ROT, NAV_STT, TIMESTAMP, MMSI, SHIPTYPE, D2C  = list(range(11))

CARGO_TANKER_ONLY = False #True
if  CARGO_TANKER_ONLY:
    pkl_filename = "ct_"+pkl_filename
    pkl_filename_train = "ct_"+pkl_filename_train
    pkl_filename_valid = "ct_"+pkl_filename_valid
    pkl_filename_test  = "ct_"+pkl_filename_test
    
print(pkl_filename_train)







## LOADING CSV FILES
#======================================
l_l_msg = [] # list of AIS messages, each row is a message (list of AIS attributes)
n_error = 0
for csv_filename in l_csv_filename:
    data_path = os.path.join(dataset_path,csv_filename)
    with open(data_path,"r") as f:
        print("Reading ", csv_filename, "...")
        csvReader = csv.reader(f)
        next(csvReader) # skip the legend row
        count = 1
        for row in csvReader:
#             utc_time = datetime.strptime(row[8], "%Y/%m/%d %H:%M:%S")
#             timestamp = (utc_time - EPOCH).total_seconds()
            print(count)
            count += 1


##            if count>200: break
##
##            if np.isnan(float(row[2])): continue
##            if np.isnan(float(row[3])): continue
##            if np.isnan(float(row[4])): continue
##            if np.isnan(float(row[5])): continue
            
                #original
##                
##                l_l_msg.append([float(row[5]),float(row[6]),
##                               float(row[7]),float(row[8]),
##                               int(row[9]),float(row[12]),
##                               int(row[11]),int(row[4]),
##                               int(float(row[1])),
##                               int(row[13]),
##                               float(row[14])])
                
                #LAT, LON, SOG, COG, HEADING, ROT, NAV_STT, TIMESTAMP, MMSI, SHIPTYPE, D2C
                #f    f     f   f    int      f    i        i          i     i         f
                
                #[float(row[5]),float(row[6]), float(row[7]),float(row[8]), int(row[9]),float(row[12]),
                # int(row[11]),int(row[4]), int(float(row[1])), int(row[13]), float(row[14])]

                #Hence
                #The format we get from AIS dataset
                #MMSI, TIMESTAMP, LAT, LON, SOG, COG, HEADING, VESSELNAME, IMO, CALLSIGN,
                #SHIPTYPE, STATUS, LENGTH, WIDTH, DRAFT, CARGO, TRANSCEIVER_CLASS = list(range(17))

                #become
                #MMSI, TIMESTAMP, LAT, LON, SOG, COG, HEADING, SHIPTYPE

                #THIS is the format we want to reformat into
                #LAT, LON, SOG, COG, HEADING, ROT, NAV_STT, TIMESTAMP, MMSI, SHIPTYPE, D2C = list(range(11))

   
            try:
                print(float(row[10]))
                test = int(float(row[10]))

                l_l_msg.append( [float(row[2]), float(row[3]), float(row[4]), float(row[5]), int(float(row[6])), 0 , 0, int(time.mktime(time.strptime(row[1], "%Y-%m-%dT%H:%M:%S"))),\
                                 int(row[0]), int(float(row[10])), 0 ] )
            
            
            except:

                
                try:
                    l_l_msg.append( [float(row[2]), float(row[3]), float(row[4]), float(row[5]), int(float(row[6])), 0 , 0, int(time.mktime(time.strptime(row[1], "%Y-%m-%dT%H:%M:%S"))),\
                                 int(row[0]), 0, 0 ] )
                
                except:
                    n_error += 1
                
                continue

m_msg = np.array(l_l_msg)
#del l_l_msg
print("Total number of AIS messages: ",m_msg.shape[0])

print("Lat min: ",np.min(m_msg[:,LAT]), "Lat max: ",np.max(m_msg[:,LAT]))
print("Lon min: ",np.min(m_msg[:,LON]), "Lon max: ",np.max(m_msg[:,LON]))
print("Ts min: ",np.min(m_msg[:,TIMESTAMP]), "Ts max: ",np.max(m_msg[:,TIMESTAMP]))

#if m_msg[0,TIMESTAMP] > 1584720228: 
#    m_msg[:,TIMESTAMP] = m_msg[:,TIMESTAMP]/1000 # Convert to suitable timestamp format

print("Time min: ",datetime.utcfromtimestamp(np.min(m_msg[:,TIMESTAMP])).strftime('%Y-%m-%d %H:%M:%SZ'))
print("Time max: ",datetime.utcfromtimestamp(np.max(m_msg[:,TIMESTAMP])).strftime('%Y-%m-%d %H:%M:%SZ'))


## Vessel Type    
#======================================
print("Selecting vessel type ...")
def sublist(lst1, lst2):
   ls1 = [element for element in lst1 if element in lst2]
   ls2 = [element for element in lst2 if element in lst1]
   return (len(ls1) != 0) and (ls1 == ls2)

VesselTypes = dict()
l_mmsi = []
n_error = 0
for v_msg in tqdm(m_msg):
    try:
        mmsi_ = v_msg[MMSI]
        type_ = v_msg[SHIPTYPE]
        if mmsi_ not in l_mmsi :
            VesselTypes[mmsi_] = [type_]
            l_mmsi.append(mmsi_)
        elif type_ not in VesselTypes[mmsi_]:
            VesselTypes[mmsi_].append(type_)
    except:
        n_error += 1
        continue
print(n_error)
for mmsi_ in tqdm(list(VesselTypes.keys())):
    VesselTypes[mmsi_] = np.sort(VesselTypes[mmsi_])
    
l_cargo_tanker = []
l_fishing = []


for mmsi_ in list(VesselTypes.keys()):
    print(VesselTypes[mmsi_])
    if sublist(VesselTypes[mmsi_], list(range(70,80))) or sublist(VesselTypes[mmsi_], list(range(80,90))):
        l_cargo_tanker.append(mmsi_)
    if sublist(VesselTypes[mmsi_], [30]):
        l_fishing.append(mmsi_)



print("ERROR ",n_error)

print("Total number of vessels: ",len(VesselTypes))
print("Total number of cargos/tankers: ",len(l_cargo_tanker))
print("Total number of fishing: ",len(l_fishing))

print("Saving vessels' type list to ", cargo_tanker_filename)
np.save(cargo_tanker_filename,l_cargo_tanker)
np.save(cargo_tanker_filename.replace("_cargo_tanker.npy","_fishing.npy"),l_fishing)


## FILTERING 
#======================================
# Selecting AIS messages in the ROI and in the period of interest.

## LAT LON
m_msg = m_msg[m_msg[:,LAT]>=LAT_MIN]
m_msg = m_msg[m_msg[:,LAT]<=LAT_MAX]
m_msg = m_msg[m_msg[:,LON]>=LON_MIN]
m_msg = m_msg[m_msg[:,LON]<=LON_MAX]
# SOG
m_msg = m_msg[m_msg[:,SOG]>=0]
m_msg = m_msg[m_msg[:,SOG]<=SOG_MAX]
# COG
m_msg = m_msg[m_msg[:,SOG]>=0]
m_msg = m_msg[m_msg[:,COG]<=360]
# D2C
##Bypassing Requirement of needing the distance to the nearest coastline to be larger than D2C_MIN (remove close to coast traj)
#m_msg = m_msg[m_msg[:,D2C]>=D2C_MIN]

# Remove ROT, NAV_STT since it is not used
m_msg[:,ROT]     = 0
m_msg[:,NAV_STT] = 0

# TIME
m_msg = m_msg[m_msg[:,TIMESTAMP]>=0]

m_msg = m_msg[m_msg[:,TIMESTAMP]>=t_min]
m_msg = m_msg[m_msg[:,TIMESTAMP]<=t_max]
m_msg_train = m_msg[m_msg[:,TIMESTAMP]>=t_train_min]
m_msg_train = m_msg_train[m_msg_train[:,TIMESTAMP]<=t_train_max]
m_msg_valid = m_msg[m_msg[:,TIMESTAMP]>=t_valid_min]
m_msg_valid = m_msg_valid[m_msg_valid[:,TIMESTAMP]<=t_valid_max]
m_msg_test  = m_msg[m_msg[:,TIMESTAMP]>=t_test_min]
m_msg_test  = m_msg_test[m_msg_test[:,TIMESTAMP]<=t_test_max]

print("Total msgs: ",len(m_msg))
print("Number of msgs in the training set: ",len(m_msg_train))
print("Number of msgs in the validation set: ",len(m_msg_valid))
print("Number of msgs in the test set: ",len(m_msg_test))


## MERGING INTO DICT
#======================================
# Creating AIS tracks from the list of AIS messages.
# Each AIS track is formatted by a dictionary.
print("Convert to dicts of vessel's tracks...")

# Training set
Vs_train = dict()
for v_msg in tqdm(m_msg_train):
    mmsi = int(v_msg[MMSI])
    if not (mmsi in list(Vs_train.keys())):
        Vs_train[mmsi] = np.empty((0,9))
    Vs_train[mmsi] = np.concatenate((Vs_train[mmsi], np.expand_dims(v_msg[:9],0)), axis = 0)
for key in tqdm(list(Vs_train.keys())):
    if CARGO_TANKER_ONLY and (not key in l_cargo_tanker):
        del Vs_train[key]
    else:
        Vs_train[key] = np.array(sorted(Vs_train[key], key=lambda m_entry: m_entry[TIMESTAMP]))

# Validation set
Vs_valid = dict()
for v_msg in tqdm(m_msg_valid):
    mmsi = int(v_msg[MMSI])
    if not (mmsi in list(Vs_valid.keys())):
        Vs_valid[mmsi] = np.empty((0,9))
    Vs_valid[mmsi] = np.concatenate((Vs_valid[mmsi], np.expand_dims(v_msg[:9],0)), axis = 0)
for key in tqdm(list(Vs_valid.keys())):
    if CARGO_TANKER_ONLY and (not key in l_cargo_tanker):
        del Vs_valid[key]
    else:
        Vs_valid[key] = np.array(sorted(Vs_valid[key], key=lambda m_entry: m_entry[TIMESTAMP]))

# Test set
Vs_test = dict()
for v_msg in tqdm(m_msg_test):
    mmsi = int(v_msg[MMSI])
    if not (mmsi in list(Vs_test.keys())):
        Vs_test[mmsi] = np.empty((0,9))
    Vs_test[mmsi] = np.concatenate((Vs_test[mmsi], np.expand_dims(v_msg[:9],0)), axis = 0)
for key in tqdm(list(Vs_test.keys())):
    if CARGO_TANKER_ONLY and (not key in l_cargo_tanker):
        del Vs_test[key]
    else:
        Vs_test[key] = np.array(sorted(Vs_test[key], key=lambda m_entry: m_entry[TIMESTAMP]))


## PICKLING
#======================================
for filename, filedict in zip([pkl_filename_train,pkl_filename_valid,pkl_filename_test],
                              [Vs_train,Vs_valid,Vs_test]
                             ):
    print("Writing to ", os.path.join(dataset_path,filename),"...")
    with open(os.path.join(dataset_path,filename),"wb") as f:
        pickle.dump(filedict,f)
    print("Total number of tracks: ", len(filedict))
