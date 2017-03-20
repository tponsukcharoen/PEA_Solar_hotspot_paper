
# coding: utf-8

# The goal of this notebook is to decipher the code ```PEA_SAM_all.py``` and its components for further use and communication.
# 
# Here is [a notebook example](https://nsrdb.nrel.gov/api-instructions).

# **IMPORTANT**: Make sure that you put this code and the Shift+F5 core Python output from GUI SAM in the SDK folder. Also make sure that the Python and SAM version are correct.

# In[19]:

import sys
print (sys.version)


# In[20]:

SDKdir = r"C:/Users/Admin/Downloads/sam-sdk-2016-3-14-r3/languages/python/"


# In[76]:

#Import necessary Python libraries
import site
site.addsitedir(SDKdir)
from PySSC import PySSC

import csv
import os
import numpy
import pandas as pd

#Specify data directories
DataDir = r'C:/Users/Admin/Dropbox/Solar NEM (ERI)/Data manipulation/'
OutputDir = r'C:/Users/Admin/Desktop/ERI_w_PArm/'


# In[86]:

#write headers for the result file
filename = OutputDir + 'test.csv'
f = open(filename,'w')
writer = csv.writer(f)
writer.writerow(['Customer type','Scheme', 'Sensitivity','NEM sales rate', 'Region', 'Annual energy', 	'Capacity factor', 	'Energy yield', 	'LCOE (nominal)', 	'LCOE (real)', 	'Bill without system', 	'Bill with system', 	'Net saving with system', 	'NPV', 	'Payback period', 	'IRR', 	'Net capital cost', 	'File name'])


# In[81]:

# #----------------define inputs for each customer and scheme-----------------------------#

# filename2 = 'Results/SAM_results'+ '_monthly'  + '.csv'
# f2 = csv.writer(open(filename2,'w', encoding = 'utf-8'))
# f2.writerow(['Customer type','Scheme', 'Sensitivity', 'Region', \
# 	'Month', 'Hour','Energy', 'Load', \
# 	'Energy_to_grid', 'Energy_from_grid', 'Energy_system_to_load'])


# In[82]:

system_sizes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
Customers = ['Res','Res_TOU','SGS','SGS_TOU','MGS','LGS', 'LGS_BOI']
Schemes = [1, 2, 3] #1. Pilot, 2. Net Metering/ NEM, 3. Net billing/ real-time buyback
Sensitivities = [1, 2, 3] #1 = below retail/ wholesale, 2 = retail/central case, 3 = above retail/ percent add-on
 
weather_filenames = os.listdir(DataDir + b'SAM/' + b'THA_weather_data/') #This corresponding to all provinces
#remove filenames we don't want 
weather_filenames.remove('.Rhistory')
weather_filenames.remove('THA_BANGKOK_484550_IW2')
weather_filenames.remove('THA_DON-MUANG_484560_IW2')
weather_filenames.remove('THA_KO-LANTA_485660_IW2')
weather_filenames.remove('THA_KO-SAMUI_485500_IW2')
weather_filenames.remove('THA_KO-SICHANG_484600_IW2')
weather_filenames.remove('THA_PHITSANULOK_483780_IW2')
weather_filenames.remove('THA_PHRAE_483300_IW2')
weather_filenames.remove('THA_SAKON-NAKHON_483560_IW2')


# Define the simulate function here (from the previous notebook).

# In[38]:

def simulate(Customer, Scheme, Sensitivity, weather_file, Region, system_size):
    ###############################################################################################################
    #Basic buyback rate
    if Customer in ["Res","SGS"] :
        block1 = 0.083
        block2 = 0.111
        block3 = 0.117
        block_average = (block1 + block2 + block3)/3 #Not using it after all?

    if Customer in ["Res_TOU","SGS_TOU"] :
        TOU_retail_1 = 0.066
        TOU_retail_2 = 0.156
        TOU_retail_average = (TOU_retail_1 + TOU_retail_2)/2

        TOU_wholesale_1 = 0.057823
        TOU_wholesale_2 = 0.111183
        TOU_wholesale_average = (TOU_wholesale_1 + TOU_wholesale_2)/2

    elif Customer in ["MGS","LGS", "LGS_BOI"]:
        TOU_retail_1 = 0.066
        TOU_retail_2 = 0.111
        TOU_retail_average = (TOU_retail_1 + TOU_retail_2)/2

        TOU_wholesale_1 = 0.057106
        TOU_wholesale_2 = 0.087409
        TOU_wholesale_average = (TOU_wholesale_1 + TOU_wholesale_2)/2
    #################################################################################################################
    #Buyback rate for different customers and sensitivies (Sensitivity: 1 = below retail, 2 = retail, 3 = above retail)
    if Customer in ["Res","SGS"] :
        buyback_block_values = [0,                  1/35,               2/35,                    3/35]
    if Customer in ["Res_TOU","SGS_TOU","MGS","LGS", "LGS_BOI"]:
        buyback_TOU_net_metering_values = [0, TOU_wholesale_average, TOU_retail_average, TOU_retail_average*1.05]
        buyback_TOU_net_billing_offpeak_values = [0,               1/35,               2/35,               3/35] 
        buyback_TOU_net_billing_peak_values = [0,                1/35,               2/35,                 3/35]
    ##################################################################################################################
    #Set load profile based on Customer Type
    if Customer in ["Res", "Res_TOU"]:
        Customer_type = b'11'
    elif Customer in ["SGS", "SGS_TOU"]:
        Customer_type = b'20'
    elif Customer == "MGS":
        Customer_type = b'30'
    elif Customer in ["LGS", "LGS_BOI"]:
        Customer_type = b'40' 

    load_file = DataDir + '/2015/load profile/DATA' + str(Region).encode('utf-8') + '_' + Customer_type + '.csv'
    #################################################################################################################
    #Fill in necessary values
    if Customer in ["Res","SGS"] :
        install_cost = 1.93*1000*system_size 
        discount_rate = 2.67

        ur_ec_sched_weekday = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]*12
        ur_ec_sched_weekend = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]*12

        if Scheme == 1: #pilot
            ur_ec_tou_mat = [None]*3
            ur_ec_tou_mat[0] = [ 1,   1,   150,         0,   block1,   0 ]
            ur_ec_tou_mat[1] = [ 1,   2,   400,         0,   block2,   0 ]
            ur_ec_tou_mat[2] = [ 1,   3,   300000000,   0,   block3,   0 ]
            metering = 2
            NEM_sale_rate = 0

        elif Scheme == 2: #net-metering
            ur_ec_tou_mat = [None]*3
            ur_ec_tou_mat[0] = [ 1,   1,   150,         0,   block1,   0 ]
            ur_ec_tou_mat[1] = [ 1,   2,   400,         0,   block2,   0 ]
            ur_ec_tou_mat[2] = [ 1,   3,   300000000,   0,   block3,   0 ]
            metering = 0
            NEM_sale_rate = buyback_block_values[Sensitivity]

        elif Scheme == 3: #net-billing
            ur_ec_tou_mat = [None]*3
            ur_ec_tou_mat[0] = [ 1,   1,   150,         0,   block1,   buyback_block_values[Sensitivity] ]
            ur_ec_tou_mat[1] = [ 1,   2,   400,         0,   block2,   buyback_block_values[Sensitivity] ]
            ur_ec_tou_mat[2] = [ 1,   3,   300000000,   0,   block3,   buyback_block_values[Sensitivity] ]
            metering = 2
            NEM_sale_rate = 0

        fixed_charge = 1.0920000076293945
        ur_dc_sched_weekday = ur_ec_sched_weekday
        ur_dc_sched_weekend = ur_dc_sched_weekday
        ur_dc_flat_mat = [None]*12
        ur_dc_flat_mat[0] = [ 0,   1,   168.69999694824219,   3.7980000972747803 ]
        ur_dc_flat_mat[1] = [ 1,   1,   200,                  3.7980000972747803 ]
        ur_dc_flat_mat[2] = [ 2,   1,   178.60000610351562,   3.7980000972747803 ]
        ur_dc_flat_mat[3] = [ 3,   1,   193.1300048828125,    3.7980000972747803 ]
        ur_dc_flat_mat[4] = [ 4,   1,   189.92999267578125,   3.7980000972747803 ]
        ur_dc_flat_mat[5] = [ 5,   1,   184.92999267578125,   3.7980000972747803 ]
        ur_dc_flat_mat[6] = [ 6,   1,   176.6199951171875,    3.7980000972747803 ]
        ur_dc_flat_mat[7] = [ 7,   1,   168.80000305175781,   3.7980000972747803 ]
        ur_dc_flat_mat[8] = [ 8,   1,   177.66000366210938,   3.7980000972747803 ]
        ur_dc_flat_mat[9] = [ 9,   1,   171.44000244140625,   3.7980000972747803 ]
        ur_dc_flat_mat[10] = [ 10,   1,   189.21000671386719,  3.7980000972747803 ]
        ur_dc_flat_mat[11] = [ 11,   1,   177.3800048828125,   3.7980000972747803 ]
        ur_dc_tou_mat = [[ 1,   1,   9e+37,   0 ]]
        dc_enable = 0

    elif Customer in ["Res_TOU","SGS_TOU"] :
        install_cost = 1.93*1000*system_size 
        discount_rate = 2.67
        ur_ec_sched_weekday = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1]]*12
        ur_ec_sched_weekend = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]*12
        if Scheme == 1:
            ur_ec_tou_mat = [None]*2
            ur_ec_tou_mat[0] = [ 1,   1,   9e+37,   0,   TOU_retail_1,   0 ]
            ur_ec_tou_mat[1] = [ 2,   1,   9e+37,   0,   TOU_retail_2,   0 ]
            metering = 2
            NEM_sale_rate = 0
        elif Scheme == 2:
            ur_ec_tou_mat = [None]*2
            ur_ec_tou_mat[0] = [ 1,   1,   9e+37,   0,   TOU_retail_1,   0 ]
            ur_ec_tou_mat[1] = [ 2,   1,   9e+37,   0,   TOU_retail_2,   0 ]
            metering = 0
            NEM_sale_rate = buyback_TOU_net_metering_values[Sensitivity]
        elif Scheme == 3:
            ur_ec_tou_mat = [None]*2
            ur_ec_tou_mat[0] = [ 1,   1,   9e+37,   0,   TOU_retail_1,  buyback_TOU_net_billing_offpeak_values[Sensitivity] ]
            ur_ec_tou_mat[1] = [ 2,   1,   9e+37,   0,   TOU_retail_2,  buyback_TOU_net_billing_peak_values[Sensitivity] ]
            metering = 2
            NEM_sale_rate = 0

        fixed_charge = 1.0920000076293945
        ur_dc_sched_weekday = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]*12
        ur_dc_sched_weekend = ur_dc_sched_weekday 
        ur_dc_flat_mat = [None]*12
        ur_dc_flat_mat[0] = [ 0,   1,   168.69999694824219,   3.7980000972747803 ]
        ur_dc_flat_mat[1] = [ 1,   1,   200,                  3.7980000972747803 ]
        ur_dc_flat_mat[2] = [ 2,   1,   178.60000610351562,   3.7980000972747803 ]
        ur_dc_flat_mat[3] = [ 3,   1,   193.1300048828125,    3.7980000972747803 ]
        ur_dc_flat_mat[4] = [ 4,   1,   189.92999267578125,   3.7980000972747803 ]
        ur_dc_flat_mat[5] = [ 5,   1,   184.92999267578125,   3.7980000972747803 ]
        ur_dc_flat_mat[6] = [ 6,   1,   176.6199951171875,    3.7980000972747803 ] 
        ur_dc_flat_mat[7] = [ 7,   1,   168.80000305175781,   3.7980000972747803 ]
        ur_dc_flat_mat[8] = [ 8,   1,   177.66000366210938,   3.7980000972747803 ]
        ur_dc_flat_mat[9] = [ 9,   1,   171.44000244140625,   3.7980000972747803 ]
        ur_dc_flat_mat[10] = [ 10,   1,   189.21000671386719,  3.7980000972747803 ]
        ur_dc_flat_mat[11] = [ 11,   1,   177.3800048828125,   3.7980000972747803 ]
        ur_dc_tou_mat = [[ 1,   1,   9e+37,   0 ]]
        dc_enable = 0

    elif Customer in ["MGS"]:
        install_cost = 1.29*1000*system_size 
        discount_rate = 6.62

        ur_ec_sched_weekday = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1]]*12
        ur_ec_sched_weekend = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]*12
        if Scheme == 1:
            ur_ec_tou_mat = [None]*2
            ur_ec_tou_mat[0] = [ 1,   1,   9e+37,   0,   TOU_retail_1,   0 ]
            ur_ec_tou_mat[1] = [ 2,   1,   9e+37,   0,   TOU_retail_2,   0 ]
            metering = 2
            NEM_sale_rate = 0
        elif Scheme == 2:
            ur_ec_tou_mat = [None]*2
            ur_ec_tou_mat[0] = [ 1,   1,   9e+37,   0,   TOU_retail_1,   0 ]
            ur_ec_tou_mat[1] = [ 2,   1,   9e+37,   0,   TOU_retail_2,   0 ]
            metering = 0
            NEM_sale_rate = buyback_TOU_net_metering_values[Sensitivity]
        elif Scheme == 3:
            ur_ec_tou_mat = [None]*2
            ur_ec_tou_mat[0] = [ 1,   1,   9e+37,   0,   TOU_retail_1,   buyback_TOU_net_billing_offpeak_values[Sensitivity] ]
            ur_ec_tou_mat[1] = [ 2,   1,   9e+37,   0,   TOU_retail_2,   buyback_TOU_net_billing_peak_values[Sensitivity] ]
            metering = 2
            NEM_sale_rate = 0

        fixed_charge = 8.921
        ur_dc_sched_weekday = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1]]*12
        ur_dc_sched_weekend = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]*12
        ur_dc_flat_mat = [None]*12
        ur_dc_flat_mat[0] = [ 0,   1,   9e+37,   3.7980000972747803 ]
        ur_dc_flat_mat[1] = [ 1,   1,   9e+37,   3.7980000972747803 ]
        ur_dc_flat_mat[2] = [ 2,   1,   9e+37,   3.7980000972747803 ]
        ur_dc_flat_mat[3] = [ 3,   1,   9e+37,   3.7980000972747803 ]
        ur_dc_flat_mat[4] = [ 4,   1,   9e+37,   3.7980000972747803 ]
        ur_dc_flat_mat[5] = [ 5,   1,   9e+37,   3.7980000972747803 ]
        ur_dc_flat_mat[6] = [ 6,   1,   9e+37,   3.7980000972747803 ]
        ur_dc_flat_mat[7] = [ 7,   1,   9e+37,   3.7980000972747803 ]
        ur_dc_flat_mat[8] = [ 8,   1,   9e+37,   3.7980000972747803 ]
        ur_dc_flat_mat[9] = [ 9,   1,   9e+37,   3.7980000972747803 ]
        ur_dc_flat_mat[10] = [ 10,   1,   9e+37,   3.7980000972747803 ]
        ur_dc_flat_mat[11] = [ 11,   1,   9e+37,   3.7980000972747803 ]
        ur_dc_tou_mat = [None]*2
        ur_dc_tou_mat[0] = [ 2,   1,   9e+37,   0 ]
        ur_dc_tou_mat[1] = [ 1,   1,   9e+37,   0 ]
        dc_enable = 1

    elif Customer in ["LGS", "LGS_BOI"]:
        if Customer == "LGS":
            install_cost = 1.14*1000*system_size 
        elif Customer == "LGS_BOI":
            install_cost = 1.14*1000*system_size*0.9 # *0.9: assuming BOI incentive give taxable deduction of 0.2*0.5*investment cost

        discount_rate = 6.62
        ur_ec_sched_weekday = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1]]*12
        ur_ec_sched_weekend = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]*12
        if Scheme == 1:
            ur_ec_tou_mat = [None]*2
            ur_ec_tou_mat[0] = [ 1,   1,   9e+37,   0,   TOU_retail_1,   0 ]
            ur_ec_tou_mat[1] = [ 2,   1,   9e+37,   0,   TOU_retail_2,   0 ]
            metering = 2
            NEM_sale_rate = 0
        elif Scheme == 2:
            ur_ec_tou_mat = [None]*2
            ur_ec_tou_mat[0] = [ 1,   1,   9e+37,   0,   TOU_retail_1,   0 ]
            ur_ec_tou_mat[1] = [ 2,   1,   9e+37,   0,   TOU_retail_2,   0 ]
            metering = 0
            NEM_sale_rate = buyback_TOU_net_metering_values[Sensitivity]
        elif Scheme == 3:
            ur_ec_tou_mat = [None]*2
            ur_ec_tou_mat[0] = [ 1,   1,   9e+37,   0,   TOU_retail_1,   buyback_TOU_net_billing_offpeak_values[Sensitivity] ]
            ur_ec_tou_mat[1] = [ 2,   1,   9e+37,   0,   TOU_retail_2,   buyback_TOU_net_billing_peak_values[Sensitivity] ]
            metering = 2
            NEM_sale_rate = 0

        fixed_charge = 8.921
        ur_dc_sched_weekday = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1]]*12
        ur_dc_sched_weekend = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]*12
        ur_dc_flat_mat = [None]*12
        ur_dc_flat_mat[0] = [ 0,   1,  9e+37,   3.7980000972747803 ]
        ur_dc_flat_mat[1] = [ 1,   1,  9e+37,   3.7980000972747803 ]
        ur_dc_flat_mat[2] = [ 2,   1,  9e+37,   3.7980000972747803 ]
        ur_dc_flat_mat[3] = [ 3,   1,  9e+37,   3.7980000972747803 ] 
        ur_dc_flat_mat[4] = [ 4,   1,  9e+37,   3.7980000972747803 ]
        ur_dc_flat_mat[5] =[ 5,   1,   9e+37,   3.7980000972747803 ]
        ur_dc_flat_mat[6] =[ 6,   1,   9e+37,   3.7980000972747803 ]
        ur_dc_flat_mat[7] =[ 7,   1,   9e+37,   3.7980000972747803 ]
        ur_dc_flat_mat[8] =[ 8,   1,   9e+37,   3.7980000972747803 ]
        ur_dc_flat_mat[9] =[ 9,   1,   9e+37,   3.7980000972747803 ]
        ur_dc_flat_mat[10] =[ 10,   1,   9e+37,   3.7980000972747803 ]
        ur_dc_flat_mat[11] =[ 11,   1,   9e+37,   3.7980000972747803 ]
        ur_dc_tou_mat = [None]*2
        ur_dc_tou_mat[0] = [ 2,   1,   9e+37,   0 ]
        ur_dc_tou_mat[1] = [ 1,   1,   9e+37,   0 ]
        dc_enable = 1
    ################################################################################################################
    #Simulation
    if __name__ == "__main__":
        ssc = PySSC()
        ssc.module_exec_set_print(0)
        data = ssc.data_create()
        ssc.data_set_number( data, b'itc_fed_percent', 0 )
        om_fixed =[ 0 ];
        ssc.data_set_array( data, b'om_fixed',  om_fixed);
        ssc.data_set_number( data, b'pbi_oth_escal', 0 )
        occ_schedule =[ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 ];
        ssc.data_set_array( data, b'occ_schedule',  occ_schedule);
        ssc.data_set_number( data, b'cbi_uti_tax_fed', 1 )
        ssc.data_set_number( data, b'cbi_fed_deprbas_fed', 0 )
        ssc.data_set_number( data, b'dc_ac_ratio', 1.1000000238418579 )
        #Input data
        ssc.data_set_string( data, b'solar_resource_file', weather_file);
        #ur_ec_sched_weekday = mat_TOU_weekday;

        ssc.data_set_matrix( data, b'ur_ec_sched_weekday', ur_ec_sched_weekday );
        ssc.data_set_number( data, b'itc_sta_amount_deprbas_sta', 0 )
        ssc.data_set_number( data, b'debt_fraction', 0 )
        ssc.data_set_number( data, b'cbi_sta_maxvalue', 9.9999996802856925e+37 )
        ssc.data_set_number( data, b'ibi_uti_percent_tax_sta', 1 )

        #Input data
        #ur_dc_sched_weekend = mat_TOU_weekend;
        ssc.data_set_matrix( data, b'ur_dc_sched_weekend', ur_dc_sched_weekend );

        ssc.data_set_number( data, b'en_fridge', 1 )
        ssc.data_set_number( data, b'itc_fed_amount', 0 )
        pbi_sta_amount =[ 0 ];
        ssc.data_set_array( data, b'pbi_sta_amount',  pbi_sta_amount);
        ssc.data_set_number( data, b'cbi_oth_deprbas_fed', 0 )
        ssc.data_set_number( data, b'cbi_sta_deprbas_fed', 0 )
        ssc.data_set_number( data, b'ibi_oth_percent_maxvalue', 9.9999996802856925e+37 )
        #Input data on TOU rate
        #ur_ec_tou_mat = [[ 1,   1,   30000000,   0,   TOU_buy1,   TOU_sell1 ], [ 2,   1,   30000000,   0,   TOU_buy2,   TOU_sell2 ], [ 3,   0,   0,   0,   0,   0 ]];
        ssc.data_set_matrix( data, b'ur_ec_tou_mat', ur_ec_tou_mat );
        ssc.data_set_number( data, b'loan_term', 0 )
        ssc.data_set_number( data, b'ur_metering_option', metering )
        ssc.data_set_number( data, b'inv_eff', 96 )
        ssc.data_set_number( data, b'ibi_uti_amount_tax_fed', 1 )
        #Input data
        ssc.data_set_number( data, b'ur_monthly_fixed_charge', fixed_charge )
        ssc.data_set_number( data, b'en_wash', 1 )
        ssc.data_set_number( data, b'pbi_fed_tax_fed', 1 )
        ssc.data_set_number( data, b'ibi_sta_amount_deprbas_sta', 0 )
        pbi_oth_amount =[ 0 ];
        ssc.data_set_array( data, b'pbi_oth_amount',  pbi_oth_amount);
        ssc.data_set_number( data, b'pbi_sta_tax_sta', 1 )
        ssc.data_set_number( data, b'ibi_fed_percent_deprbas_sta', 0 )
        ssc.data_set_number( data, b'yrbuilt', 1980 )
        ssc.data_set_number( data, b'en_heat', 1 )
        monthly_util =[ 725, 630, 665, 795, 1040, 1590, 1925, 1730, 1380, 1080, 635, 715 ];
        ssc.data_set_array( data, b'monthly_util',  monthly_util);
        ssc.data_set_number( data, b'pbi_uti_tax_sta', 1 )
        ssc.data_set_number( data, b'ibi_oth_percent', 0 )
        ssc.data_set_number( data, b'en_dry', 1 )
        ssc.data_set_number( data, b'cbi_sta_deprbas_sta', 0 )
        ssc.data_set_number( data, b'state_tax_rate', 0 )
        ssc.data_set_number( data, b'federal_tax_rate', 0 )
        ssc.data_set_number( data, b'pbi_uti_escal', 0 )
        ssc.data_set_number( data, b'ibi_sta_amount', 0 )
        ssc.data_set_number( data, b'ibi_oth_amount', 0 )
        om_capacity =[ 10 ];
        ssc.data_set_array( data, b'om_capacity',  om_capacity);
        ssc.data_set_number( data, b'cbi_oth_tax_fed', 1 )
        ssc.data_set_number( data, b'floor_area', 2000 )
        ssc.data_set_number( data, b'cbi_uti_deprbas_fed', 0 )
        ssc.data_set_number( data, b'itc_sta_percent_deprbas_sta', 0 )
        #ur_dc_sched_weekday = [[ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ]];
        ssc.data_set_matrix( data, b'ur_dc_sched_weekday', ur_dc_sched_weekday );
        ssc.data_set_number( data, b'ibi_fed_amount_tax_sta', 1 )
        ssc.data_set_number( data, b'ibi_uti_percent_tax_fed', 1 )
        ssc.data_set_number( data, b'tcool', 76 )
        ssc.data_set_number( data, b'adjust:constant', 0 )
        ssc.data_set_number( data, b'ibi_oth_amount_deprbas_sta', 0 )
        ssc.data_set_number( data, b'ibi_oth_amount_tax_fed', 1 )
        ssc.data_set_number( data, b'itc_sta_percent_deprbas_fed', 0 )
        ssc.data_set_number( data, b'cbi_uti_amount', 0 )
        ssc.data_set_number( data, b'cbi_oth_maxvalue', 9.9999996802856925e+37 )
        ssc.data_set_number( data, b'prop_tax_assessed_decline', 0 )
        om_production =[ 0 ];
        ssc.data_set_array( data, b'om_production',  om_production);
        ssc.data_set_number( data, b'itc_fed_percent_deprbas_sta', 1 )
        ssc.data_set_number( data, b'itc_fed_amount_deprbas_sta', 1 )
        pbi_fed_amount =[ 0 ];
        ssc.data_set_array( data, b'pbi_fed_amount',  pbi_fed_amount);
        ssc.data_set_number( data, b'pbi_sta_tax_fed', 1 )
        ssc.data_set_number( data, b'tilt', 13.699999809265137 )
        load_escalation =[ 3.5 ];
        ssc.data_set_array( data, b'load_escalation',  load_escalation);
        ssc.data_set_number( data, b'salvage_percentage', 0 )
        ssc.data_set_number( data, b'ibi_sta_percent_deprbas_sta', 0 )
        ssc.data_set_number( data, b'itc_fed_percent_deprbas_fed', 1 )
        ssc.data_set_number( data, b'property_tax_rate', 0 )
        ssc.data_set_number( data, b'ibi_sta_amount_deprbas_fed', 0 )
        ssc.data_set_number( data, b'theat', 68 )
        ssc.data_set_number( data, b'cbi_oth_amount', 0 )
        ssc.data_set_number( data, b'ibi_uti_percent_maxvalue', 9.9999996802856925e+37 )
        ssc.data_set_number( data, b'azimuth', 180 )
        ssc.data_set_number( data, b'pbi_fed_term', 0 )
        ssc.data_set_number( data, b'ur_annual_min_charge', 0 )
        ssc.data_set_number( data, b'itc_fed_amount_deprbas_fed', 1 )
        ssc.data_set_number( data, b'battery_per_kwh', 600 )
        ssc.data_set_number( data, b'ptc_fed_term', 10 )
        ssc.data_set_number( data, b'pbi_oth_tax_sta', 1 )
        ssc.data_set_number( data, b'pbi_sta_escal', 0 )
        ssc.data_set_number( data, b'ibi_oth_amount_deprbas_fed', 0 )
        ssc.data_set_number( data, b'theatsb', 68 )
        ptc_fed_amount =[ 0 ];
        ssc.data_set_array( data, b'ptc_fed_amount',  ptc_fed_amount);
        ssc.data_set_number( data, b'sales_tax_rate', 0 )
        ssc.data_set_number( data, b'insurance_rate', 0.25 )
        ssc.data_set_number( data, b'ptc_sta_escal', 0 )
        ssc.data_set_number( data, b'ur_monthly_min_charge', 0 )
        ssc.data_set_number( data, b'itc_fed_percent_maxvalue', 9.9999996802856925e+37 )
        ssc.data_set_number( data, b'ibi_oth_percent_tax_fed', 1 )
        ssc.data_set_number( data, b'cbi_oth_deprbas_sta', 0 )
        ssc.data_set_number( data, b'en_belpe', 0 )
        ssc.data_set_number( data, b'pbi_oth_term', 0 )
        ssc.data_set_number( data, b'cbi_fed_tax_sta', 1 )
        ssc.data_set_number( data, b'analysis_period', 25 )
        ssc.data_set_number( data, b'om_production_escal', 0 )
        ssc.data_set_number( data, b'ibi_sta_amount_tax_sta', 1 )
        ssc.data_set_number( data, b'cbi_sta_tax_fed', 1 )
        ssc.data_set_number( data, b'om_capacity_escal', 2.2000000476837158 )
        ssc.data_set_number( data, b'ibi_fed_amount_deprbas_sta', 0 )
        ssc.data_set_number( data, b'loan_rate', 0 )
        ssc.data_set_number( data, b'pbi_oth_tax_fed', 1 )
        ssc.data_set_number( data, b'ibi_fed_percent_deprbas_fed', 0 )
        #ur_dc_flat_mat = [[ 0,   1,   168.69999694824219,   3.7980000972747803 ], [ 1,   1,   200,   3.7980000972747803 ], [ 2,   1,   178.60000610351562,   3.7980000972747803 ], [ 3,   1,   193.1300048828125,   3.7980000972747803 ], [ 4,   1,   189.92999267578125,   3.7980000972747803 ], [ 5,   1,   184.92999267578125,   3.7980000972747803 ], [ 6,   1,   176.6199951171875,   3.7980000972747803 ], [ 7,   1,   168.80000305175781,   3.7980000972747803 ], [ 8,   1,   177.66000366210938,   3.7980000972747803 ], [ 9,   1,   171.44000244140625,   3.7980000972747803 ], [ 10,   1,   189.21000671386719,   3.7980000972747803 ], [ 11,   1,   177.3800048828125,   3.7980000972747803 ]];
        ssc.data_set_matrix( data, b'ur_dc_flat_mat', ur_dc_flat_mat );
        ssc.data_set_number( data, b'cbi_fed_tax_fed', 1 )
        ssc.data_set_number( data, b'ibi_sta_percent_deprbas_fed', 0 )
        ssc.data_set_number( data, b'cbi_sta_tax_sta', 1 )
        ssc.data_set_number( data, b'ibi_fed_amount_deprbas_fed', 0 )
        ssc.data_set_number( data, b'system_use_lifetime_output', 0 )
        ssc.data_set_number( data, b'en_mels', 1 )
        t_sched =[ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 ];
        ssc.data_set_array( data, b't_sched',  t_sched);
        ssc.data_set_number( data, b'mortgage', 0 )
        ssc.data_set_number( data, b'pbi_fed_tax_sta', 1 )
        ssc.data_set_number( data, b'array_type', 0 )
        ssc.data_set_number( data, b'pbi_uti_term', 0 )
        ssc.data_set_array_from_csv( data, b'load', load_file);
        ssc.data_set_number( data, b'ibi_fed_percent_maxvalue', 9.9999996802856925e+37 )
        ssc.data_set_number( data, b'ibi_fed_amount_tax_fed', 1 )
        ssc.data_set_number( data, b'total_installed_cost', install_cost )
        ssc.data_set_number( data, b'cbi_uti_deprbas_sta', 0 )
        ssc.data_set_number( data, b'ptc_sta_term', 10 )
        degradation =[ 0.5 ];
        ssc.data_set_array( data, b'degradation',  degradation);
        ssc.data_set_number( data, b'itc_sta_amount_deprbas_fed', 0 )
        ssc.data_set_number( data, b'en_dish', 1 )
        ssc.data_set_number( data, b'ur_nm_yearend_sell_rate', NEM_sale_rate )
        ssc.data_set_number( data, b'ptc_fed_escal', 0 )
        ssc.data_set_number( data, b'ibi_sta_percent_tax_fed', 1 )
        ssc.data_set_number( data, b'cbi_fed_maxvalue', 9.9999996802856925e+37 )
        ssc.data_set_number( data, b'ibi_oth_amount_tax_sta', 1 )
        ssc.data_set_number( data, b'itc_sta_amount', 0 )
        ssc.data_set_number( data, b'ibi_fed_percent_tax_sta', 1 )
        ssc.data_set_number( data, b'ibi_sta_amount_tax_fed', 1 )
        #ur_dc_tou_mat = [[ 1,   1,   9.9999996802856925e+37,   0 ]];
        ssc.data_set_matrix( data, b'ur_dc_tou_mat', ur_dc_tou_mat );
        ssc.data_set_number( data, b'ibi_uti_amount_deprbas_fed', 0 )
        ssc.data_set_number( data, b'ibi_sta_percent_maxvalue', 9.9999996802856925e+37 )
        ssc.data_set_number( data, b'om_fixed_escal', 0 )
        ssc.data_set_number( data, b'ibi_uti_amount_tax_sta', 1 )
        ssc.data_set_number( data, b'ibi_sta_percent_tax_sta', 1 )
        ssc.data_set_number( data, b'cbi_sta_amount', 0 )
        ssc.data_set_number( data, b'occupants', 4 )
        #Input data for system capacity
        ssc.data_set_number( data, b'system_capacity', system_size )
        ssc.data_set_number( data, b'om_fuel_cost_escal', 0 )
        ssc.data_set_number( data, b'pbi_uti_tax_fed', 1 )
        ssc.data_set_number( data, b'ibi_oth_percent_deprbas_fed', 0 )
        ssc.data_set_number( data, b'ibi_uti_amount_deprbas_sta', 0 )
        rate_escalation =[ 3.5 ];
        ssc.data_set_array( data, b'rate_escalation',  rate_escalation);
        pbi_uti_amount =[ 0 ];
        ssc.data_set_array( data, b'pbi_uti_amount',  pbi_uti_amount);
        ssc.data_set_number( data, b'ibi_fed_percent_tax_fed', 1 )
        ssc.data_set_number( data, b'cbi_uti_tax_sta', 1 )
        ssc.data_set_number( data, b'pbi_fed_escal', 0 )
        #ur_ec_sched_weekend = [[ 2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2 ], [ 2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2 ], [ 2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2 ], [ 2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2 ], [ 2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2 ], [ 2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2 ], [ 2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2 ], [ 2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2 ], [ 2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2 ], [ 2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2 ], [ 2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2 ], [ 2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2 ]];
        ssc.data_set_matrix( data, b'ur_ec_sched_weekend', ur_ec_sched_weekend );
        ssc.data_set_number( data, b'prop_tax_cost_assessed_percent', 0 )
        ssc.data_set_number( data, b'ur_dc_enable', dc_enable )
        ssc.data_set_number( data, b'pbi_sta_term', 0 )
        ssc.data_set_number( data, b'itc_sta_percent', 0 )
        ssc.data_set_number( data, b'losses', 14.075660705566406 )
        om_fuel_cost =[ 0 ];
        ssc.data_set_array( data, b'om_fuel_cost',  om_fuel_cost);
        ssc.data_set_number( data, b'cbi_uti_maxvalue', 9.9999996802856925e+37 )
        ssc.data_set_number( data, b'tcoolsb', 76 )
        ptc_sta_amount =[ 0 ];
        ssc.data_set_array( data, b'ptc_sta_amount',  ptc_sta_amount);
        ssc.data_set_number( data, b'ibi_uti_percent_deprbas_sta', 0 )
        ssc.data_set_number( data, b'inflation_rate', 2.5 )
        ssc.data_set_number( data, b'ibi_fed_amount', 0 )
        ssc.data_set_number( data, b'ibi_uti_percent_deprbas_fed', 0 )
        ssc.data_set_number( data, b'real_discount_rate', discount_rate )
        ssc.data_set_number( data, b'module_type', 0 )
        ssc.data_set_number( data, b'market', 0 )
        ssc.data_set_number( data, b'ibi_uti_percent', 0 )
        ssc.data_set_number( data, b'stories', 2 )
        ssc.data_set_number( data, b'ibi_oth_percent_deprbas_sta', 0 )
        ssc.data_set_number( data, b'ibi_fed_percent', 0 )
        ssc.data_set_number( data, b'en_cool', 1 )
        ssc.data_set_number( data, b'cbi_fed_amount', 0 )
        ssc.data_set_number( data, b'ibi_uti_amount', 0 )
        ssc.data_set_number( data, b'retrofits', 0 )
        ssc.data_set_number( data, b'en_range', 1 )
        ssc.data_set_number( data, b'gcr', 0.40000000596046448 )
        ssc.data_set_number( data, b'cbi_fed_deprbas_sta', 0 )
        ssc.data_set_number( data, b'itc_sta_percent_maxvalue', 9.9999996802856925e+37 )
        ssc.data_set_number( data, b'ibi_oth_percent_tax_sta', 1 )
        ssc.data_set_number( data, b'ibi_sta_percent', 0 )
        ssc.data_set_number( data, b'cbi_oth_tax_sta', 1 )
        module = ssc.module_create(b'pvwattsv5')	
        ssc.module_exec_set_print( 0 );
        if ssc.module_exec(module, data) == 0:
            print ('pvwattsv5 simulation error')
            idx = 1
            msg = ssc.module_log(module, 0)
            while (msg != None):
                print ('	: ' + msg.decode("utf - 8"))
                msg = ssc.module_log(module, idx)
                idx = idx + 1
            SystemExit( "Simulation Error" );
        ssc.module_free(module)
        module = ssc.module_create(b'belpe')	
        ssc.module_exec_set_print( 0 );
        if ssc.module_exec(module, data) == 0:
            print ('belpe simulation error')
            idx = 1
            msg = ssc.module_log(module, 0)
            while (msg != None):
                print ('	: ' + msg.decode("utf - 8"))
                msg = ssc.module_log(module, idx)
                idx = idx + 1
            SystemExit( "Simulation Error" );
        ssc.module_free(module)
        module = ssc.module_create(b'utilityrate4')	
        ssc.module_exec_set_print( 0 );
        if ssc.module_exec(module, data) == 0:
            print ('utilityrate4 simulation error')
            idx = 1
            msg = ssc.module_log(module, 0)
            while (msg != None):
                print ('	: ' + msg.decode("utf - 8"))
                msg = ssc.module_log(module, idx)
                idx = idx + 1
            SystemExit( "Simulation Error" );
        ssc.module_free(module)
        module = ssc.module_create(b'cashloan')	
        ssc.module_exec_set_print( 0 );
        if ssc.module_exec(module, data) == 0:
            print ('cashloan simulation error')
            idx = 1
            msg = ssc.module_log(module, 0)
            while (msg != None):
                print ('	: ' + msg.decode("utf - 8"))
                msg = ssc.module_log(module, idx)
                idx = idx + 1
            SystemExit( "Simulation Error" );
        ssc.module_free(module)
        annual_energy = ssc.data_get_number(data, b'annual_energy');
        #print ('Annual energy (year 1) = ', annual_energy)
        capacity_factor = ssc.data_get_number(data, b'capacity_factor');
        #print ('Capacity factor (year 1) = ', capacity_factor)
        kwh_per_kw = ssc.data_get_number(data, b'kwh_per_kw');
        #print ('Energy yield (year 1) = ', kwh_per_kw)
        lcoe_nom = ssc.data_get_number(data, b'lcoe_nom');
        #print ('Levelized COE (nominal) = ', lcoe_nom)
        lcoe_real = ssc.data_get_number(data, b'lcoe_real');
        #print ('Levelized COE (real) = ', lcoe_real)
        elec_cost_without_system_year1 = ssc.data_get_number(data, b'elec_cost_without_system_year1');
        #print ('Electricity bill without system (year 1) = ', elec_cost_without_system_year1)
        elec_cost_with_system_year1 = ssc.data_get_number(data, b'elec_cost_with_system_year1');
        #print ('Electricity bill with system (year 1) = ', elec_cost_with_system_year1)
        savings_year1 = ssc.data_get_number(data, b'savings_year1');
        #print ('Net savings with system (year 1) = ', savings_year1)
        npv = ssc.data_get_number(data, b'npv');
        #print ('Net present value = ', npv)
        payback = ssc.data_get_number(data, b'payback');
        #print ('Payback period = ', payback)
        adjusted_installed_cost = ssc.data_get_number(data, b'adjusted_installed_cost');
        #print ('Net capital cost = ', adjusted_installed_cost)
        first_cost = ssc.data_get_number(data, b'first_cost');
        #print ('Equity = ', first_cost)
        loan_amount = ssc.data_get_number(data, b'loan_amount');
        #print ('Debt = ', loan_amount)
        cash_flow = ssc.data_get_array(data,b'cf_after_tax_cash_flow');
        #print ('Cash flow = ', cash_flow)

        #calculate IRR using NumPy
        IRR = numpy.irr(cash_flow)

        hourly_energy = ssc.data_get_array(data,b'gen');
        hourly_load = ssc.data_get_array(data, b'load');
        hourly_to_grid = ssc.data_get_array(data, b'year1_hourly_e_togrid');
        hourly_from_grid = ssc.data_get_array(data, b'year1_hourly_e_fromgrid');
        hourly_system_to_load = ssc.data_get_array(data, b'year1_hourly_system_to_load');
    ##########################################################################################################
    #output
    return [Customer,     Scheme,     Sensitivity,     NEM_sale_rate,    Region,     annual_energy,     capacity_factor,     kwh_per_kw,     lcoe_nom,     lcoe_real,     elec_cost_without_system_year1,     elec_cost_with_system_year1,     savings_year1,     npv,     payback,     IRR,     adjusted_installed_cost,     weather_file];


# Now, we are running through cases in the main script.

# Define key-value pairs for all provinces. Region 14 = North, Region 15 = Northeast, Region 16 = Central, Region 17 = South

# In[83]:

RegionValues = {"UTTARADIT":14,  "TAK":14,    "MAE-SOT":14, "PRAE":14,         "PITSANULOK":14, 
				"PHETCHABUN":14, "PHAYAO":14, "NAN":14,     "NAKHON-SAWAN":14, "MAE-SARIANG":14, 
				"MAE-HONG-SON":14, "LOP-BURI":14, "LAMPHUN":14, "LAMPANG":14,  "KAM-PAENG-PHET":14,
				"CHIANG-RAI":14, "CHIANG-MAI":14,
                "UDON-THANI":15, "UBON-RATCHATHANI":15, "THA-TUM":15, "SURIN":15, 
				"SAKON-KAKHON":15, "ROI-ET":15, "NONG-KHAI":15, "NAKHON-RATCHASIMA":15, "NAKHON-PHANOM":15, 
				"MUKDAHAN":15, "LOEI":15, "KHON-KAEN":15, "CHAIYAPHUM":15,
                "ARANYAPRATHET":16, "THONG-PHA-PHUM":16, "SUPHAN-BURI":16, "SATTAHIP":16, 
				"PRACHIN-BURI":16, "KOH-SICHANG":16, "KHLONG-YAI":16, "KANCHANABURI":16, "CHON-BURI":16, 
				"CHANTHABURI":16,
                "TRANG":17, "SURAT-THANI":17, "SONGKHLA":17, "RANONG":17, "PRACHUAP-KHIRIKHAN":17, 
				"PHUKET-AP":17, "PHUKET":17, "PATTANI":17, "NARATHIWAT":17, "NAKHON-SI-THAMMARAT":17, 
				"KOH-SAMUI":17, "KOH-LANTA":17, "HUA-HIN":17, "HAT-YAI":17, "CHUMPHON":17
         }


# Start the main loop.

# In[84]:

for system_size in system_sizes:
    for Customer in Customers:
        for Scheme in Schemes: 
            for Sensitivity in Sensitivities:
                for weather_filename in weather_filenames:
                    weather_file = DataDir + b'SAM/THA_weather_data/' + weather_filename + b'/' + weather_filename + b'.EPW'
                    Province = weather_filename.decode(encoding='UTF-8').split('_')
                    Province = Province[1]
                    #call the function
                    writer.writerow(simulate(Customer, Scheme, Sensitivity, weather_file, RegionValues[Province], system_size))


# In[87]:

f.close()


# Note that this can be quite slow to run in the notebook. Conversion to .py file is recommend.
