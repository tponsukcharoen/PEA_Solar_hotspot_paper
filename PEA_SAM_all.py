from PySSC import PySSC
import csv
import os
import numpy


def simulate(Customer,Scheme,weather_file,Region,result_file1, result_file2, Sensitivity):

	#Buyback rate for block rate customers for scheme 2 and 3:
		#average_wholesale, average_block, average_block_5

	#Buyback rate for TOU customers for scheme 2 (NEM takes only one buyback value)
		#average_wholesale, average_TOU, average_TOU_5

	#Buyback rate for TOU customers for scheme 3
		#TOU_wholesale, TOU_retail, TOU_retail_5

	#Retail Tariff rate
		#block rate
	block1 = 0.083
	block2 = 0.111
	block3 = 0.117
	block_average = (block1 + block2 + block3)/3
		#TOU for SGS
	TOU_s_2 = 0.156
	TOU_s_1 = 0.066
	TOU_s_average = (TOU_s_1 + TOU_s_2)/2
		#TOU for MGS/LGS
	TOU_ml_2 = 0.111
	TOU_ml_1 = 0.066
	TOU_ml_average = (TOU_ml_1 + TOU_ml_2)/2

	#Wholesale TOU rate
		# SGS
	TOU_s_wholesale2 = 0.111183
	TOU_s_wholesale1 = 0.057823
	TOU_s_wholesale_average = (TOU_s_wholesale1 + TOU_s_wholesale2)/2
		# MGS/LGS
	TOU_ml_wholesale2 = 0.087409
	TOU_ml_wholesale1 = 0.057106
	TOU_ml_wholesale_average = (TOU_ml_wholesale1 + TOU_ml_wholesale2)/2
	
	#Buyback rate for residential/SGS block (Sensitivity: 1 = below retail, 2 = retail/central case, 3 = above retail)
	if Sensitivity == 1:
		#buyback_block = TOU_s_wholesale_average #for non-TOU scheme 3
		buyback_block = 1/35 #for non-TOU scheme 3

		buyback_s_TOU_2 = TOU_s_wholesale_average #for scheme 2 (NEM)
		buyback_s_TOU_3_op = 1/35 #for scheme 3
		buyback_s_TOU_3_p = 1/35 #for scheme 3	
		#buyback_s_TOU_3_op = TOU_s_wholesale1 #for scheme 3
		#buyback_s_TOU_3_p = TOU_s_wholesale2 #for scheme 3	

		buyback_ml_TOU_2 = TOU_ml_wholesale_average #for scheme 2 (NEM)
		#buyback_ml_TOU_3_op = TOU_ml_wholesale1 #for scheme 3
		#buyback_ml_TOU_3_p = TOU_ml_wholesale2 #for scheme 3	
		buyback_ml_TOU_3_op = 1/35 #for scheme 3
		buyback_ml_TOU_3_p = 1/35 #for scheme 3	

	elif Sensitivity == 2:
		#buyback_block = block_average #for non-TOU scheme 3
		buyback_block = 2/35 #for non-TOU scheme 3

		buyback_s_TOU_2 = TOU_s_average #for scheme 2 (NEM)
		buyback_s_TOU_3_op = 2/35 #for scheme 3
		buyback_s_TOU_3_p = 2/35 #for scheme 3	
		#buyback_s_TOU_3_op = TOU_s_1 #for scheme 3
		#buyback_s_TOU_3_p = TOU_s_2 #for scheme 3		

		buyback_ml_TOU_2 = TOU_ml_average #for scheme 2 (NEM)
		buyback_ml_TOU_3_op = 2/35 #for scheme 3
		buyback_ml_TOU_3_p = 2/35 #for scheme 3
		#buyback_ml_TOU_3_op = TOU_ml_1 #for scheme 3
		#buyback_ml_TOU_3_p = TOU_ml_2 #for scheme 3

	elif Sensitivity == 3:
		#buyback_block = block_average*1.05 #for non-TOU scheme 3
		buyback_block = 3/35 #for non-TOU scheme 3

		buyback_s_TOU_2 = TOU_s_average*1.05 #for scheme 2 (NEM)
		buyback_s_TOU_3_op = 3/35 #for scheme 3
		buyback_s_TOU_3_p = 3/35 #for scheme 3	
		#buyback_s_TOU_3_op = TOU_s_1*1.05 #for scheme 3
		#buyback_s_TOU_3_p = TOU_s_2*1.05 #for scheme 3

		buyback_ml_TOU_2 = TOU_ml_average*1.05 #for scheme 2 (NEM)
		buyback_ml_TOU_3_op = 3/35 #for scheme 3
		buyback_ml_TOU_3_p = 3/35 #for scheme 3
		#buyback_ml_TOU_3_op = TOU_ml_1*1.05 #for scheme 3
		#buyback_ml_TOU_3_p = TOU_ml_2*1.05 #for scheme 3


	#metering option: "2" for pilot scheme and real-time buyback, "0" for net metering
	#scheme3_buyback
	#NEM_sale_rate

	if Customer in ["Res", "Res_TOU"]:
		Customer_type = b'11'
	elif Customer in ["SGS", "SGS_TOU"]:
		Customer_type = b'20'
	elif Customer == "MGS":
		Customer_type = b'30'
	elif Customer in ["LGS", "LGS_BOI"]:
		Customer_type = b'40' 
	Region_type = str(Region).encode('utf-8')

	#load_file = b'/Users/carrotchang/Dropbox/TDRI/Solar NEM (ERI)/Data manipulation/2015/load profile/DATA' + Region_type + b'_' + Customer_type + b'.csv'
	load_file = b'../2015/load profile/DATA' + Region_type + b'_' + Customer_type + b'.csv'


	if Customer in ["Res","SGS"] :
		system_size = 3
		install_cost = 1.93*1000*system_size 
		discount_rate = 2.67
		ur_ec_sched_weekday = [[ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ]];
		ur_ec_sched_weekend = [[ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ]];
		if Scheme == 1: #pilot
			ur_ec_tou_mat = [[ 1,   1,   150,   0,   block1,   0 ], [ 1,   2,   400,   0,   block2,   0 ], [ 1,   3,   300000000,   0,   block3,   0 ]];
			metering = 2
			NEM_sale_rate = 0

		elif Scheme == 3: #net-billing
			ur_ec_tou_mat = [[ 1,   1,   150,   0,   block1,   buyback_block], [ 1,   2,   400,   0,   block2,   buyback_block], [ 1,   3,   300000000,   0,   block3,   buyback_block]];
			metering = 2
			NEM_sale_rate = 0
		elif Scheme == 2: #net-metering
			metering = 0
			ur_ec_tou_mat = [[ 1,   1,   150,   0,   block1,   0 ], [ 1,   2,   400,   0,   block2,   0 ], [ 1,   3,   300000000,   0,   block3,   0 ]];
			NEM_sale_rate = buyback_block

		fixed_charge = 1.0920000076293945
		ur_dc_sched_weekday = [[ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ]];
		ur_dc_sched_weekend = [[ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ]];
		ur_dc_flat_mat = [[ 0,   1,   168.69999694824219,   3.7980000972747803 ], [ 1,   1,   200,   3.7980000972747803 ], [ 2,   1,   178.60000610351562,   3.7980000972747803 ], [ 3,   1,   193.1300048828125,   3.7980000972747803 ], [ 4,   1,   189.92999267578125,   3.7980000972747803 ], [ 5,   1,   184.92999267578125,   3.7980000972747803 ], [ 6,   1,   176.6199951171875,   3.7980000972747803 ], [ 7,   1,   168.80000305175781,   3.7980000972747803 ], [ 8,   1,   177.66000366210938,   3.7980000972747803 ], [ 9,   1,   171.44000244140625,   3.7980000972747803 ], [ 10,   1,   189.21000671386719,   3.7980000972747803 ], [ 11,   1,   177.3800048828125,   3.7980000972747803 ]];
		ur_dc_tou_mat = [[ 1,   1,   9.9999996802856925e+37,   0 ]];
		dc_enable = 0

	elif Customer in ["Res_TOU","SGS_TOU"] :
		system_size = 3
		install_cost = 1.93*1000*system_size 
		discount_rate = 2.67
		ur_ec_sched_weekday = [[ 1,   1,   1,   1,   1,   1,   1,   1,   1,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   1 ]];
		ur_ec_sched_weekend = [[ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ]];
		if Scheme == 1:
			ur_ec_tou_mat = [[ 1,   1,   9e+37,   0,   TOU_s_1,   0 ], [ 2,   1,   9e+37,   0,   TOU_s_2,   0 ]];
			metering = 2
			NEM_sale_rate = 0
		elif Scheme == 3:
			ur_ec_tou_mat = [[ 1,   1,   9e+37,   0,   TOU_s_1,   buyback_s_TOU_3_op], [ 2,   1,   9e+37,   0,   TOU_s_2,  buyback_s_TOU_3_p]];
			metering = 2
			NEM_sale_rate = 0
		elif Scheme == 2:
			ur_ec_tou_mat = [[ 1,   1,   9e+37,   0,   TOU_s_1,   0 ], [ 2,   1,   9e+37,   0,   TOU_s_2,   0 ]];
			metering = 0
			NEM_sale_rate = buyback_s_TOU_2

		fixed_charge = 1.0920000076293945

		ur_dc_sched_weekday = [[ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ]];
		ur_dc_sched_weekend = [[ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ]];
		ur_dc_flat_mat = [[ 0,   1,   168.69999694824219,   3.7980000972747803 ], [ 1,   1,   200,   3.7980000972747803 ], [ 2,   1,   178.60000610351562,   3.7980000972747803 ], [ 3,   1,   193.1300048828125,   3.7980000972747803 ], [ 4,   1,   189.92999267578125,   3.7980000972747803 ], [ 5,   1,   184.92999267578125,   3.7980000972747803 ], [ 6,   1,   176.6199951171875,   3.7980000972747803 ], [ 7,   1,   168.80000305175781,   3.7980000972747803 ], [ 8,   1,   177.66000366210938,   3.7980000972747803 ], [ 9,   1,   171.44000244140625,   3.7980000972747803 ], [ 10,   1,   189.21000671386719,   3.7980000972747803 ], [ 11,   1,   177.3800048828125,   3.7980000972747803 ]];
		ur_dc_tou_mat = [[ 1,   1,   9.9999996802856925e+37,   0 ]];
		dc_enable = 0

	elif Customer in ["MGS"]:
		system_size = 100
		install_cost = 1.29*1000*system_size 
		discount_rate = 6.62
		ur_ec_sched_weekday = [[ 1,   1,   1,   1,   1,   1,   1,   1,   1,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   1 ]];
		ur_ec_sched_weekend = [[ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ]];
		if Scheme == 1:
			ur_ec_tou_mat = [[ 1,   1,   9e+37,   0,   TOU_ml_1,   0 ], [ 2,   1,   9e+37,   0,   TOU_ml_2,   0 ]];
			metering = 2
			NEM_sale_rate = 0
		elif Scheme == 3:
			ur_ec_tou_mat = [[ 1,   1,   9e+37,   0,   TOU_ml_1,   buyback_ml_TOU_3_op], [ 2,   1,   9e+37,   0,   TOU_ml_2,   buyback_ml_TOU_3_p]];
			metering = 2
			NEM_sale_rate = 0
		elif Scheme == 2:
			ur_ec_tou_mat = [[ 1,   1,   9e+37,   0,   TOU_ml_1,   0 ], [ 2,   1,   9e+37,   0,   TOU_ml_2,   0 ]];
			metering = 0
			NEM_sale_rate = buyback_ml_TOU_2

		fixed_charge = 8.921

		ur_dc_sched_weekday = [[ 1,   1,   1,   1,   1,   1,   1,   1,   1,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   1 ]];
		ur_dc_sched_weekend = [[ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ]];
		ur_dc_flat_mat = [[ 0,   1,  9e+37,   3.7980000972747803 ], [ 1,   1,  9e+37,   3.7980000972747803 ], [ 2,   1,   9e+37,   3.7980000972747803 ], [ 3,   1, 9e+37,   3.7980000972747803 ], [ 4,   1,  9e+37,   3.7980000972747803 ], [ 5,   1,   9e+37,   3.7980000972747803 ], [ 6,   1,   9e+37,   3.7980000972747803 ], [ 7,   1,   9e+37,   3.7980000972747803 ], [ 8,   1,   9e+37,   3.7980000972747803 ], [ 9,   1,   9e+37,   3.7980000972747803 ], [ 10,   1,   9e+37,   3.7980000972747803 ], [ 11,   1,   9e+37,   3.7980000972747803 ]];
		ur_dc_tou_mat = [[ 2,   1,   9e+37,   0 ], [ 1,   1,   9e+37,   0 ]];
		dc_enable = 1

	elif Customer in ["LGS", "LGS_BOI"]:
		system_size = 1000
		if Customer == "LGS":
			install_cost = 1.14*1000*system_size 
		elif Customer == "LGS_BOI":
			install_cost = 1.14*1000*system_size*0.9 # *0.9: assuming BOI incentive give taxable deduction of 0.2*0.5*investment cost
		
		discount_rate = 6.62
		ur_ec_sched_weekday = [[ 1,   1,   1,   1,   1,   1,   1,   1,   1,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   1 ]];
		ur_ec_sched_weekend = [[ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ]];
		if Scheme == 1:
			ur_ec_tou_mat = [[ 1,   1,   9e+37,   0,   TOU_ml_1,   0 ], [ 2,   1,   9e+37,   0,   TOU_ml_2,   0 ]];
			metering = 2	
			NEM_sale_rate = 0	
		elif Scheme == 3:
			ur_ec_tou_mat = [[ 1,   1,   9e+37,   0,   TOU_ml_1,   buyback_ml_TOU_3_op], [ 2,   1,   9e+37,   0,   TOU_ml_2,   buyback_ml_TOU_3_p]];
			metering = 2
			NEM_sale_rate = 0
		elif Scheme == 2:
			ur_ec_tou_mat = [[ 1,   1,   9e+37,   0,   TOU_ml_1,   0 ], [ 2,   1,   9e+37,   0,   TOU_ml_2,   0 ]];
			metering = 0
			NEM_sale_rate = buyback_ml_TOU_2

		fixed_charge = 8.921

		ur_dc_sched_weekday = [[ 1,   1,   1,   1,   1,   1,   1,   1,   1,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   1 ]];
		ur_dc_sched_weekend = [[ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ]];
		ur_dc_flat_mat = [[ 0,   1,  9e+37,   3.7980000972747803 ], [ 1,   1,  9e+37,   3.7980000972747803 ], [ 2,   1,   9e+37,   3.7980000972747803 ], [ 3,   1, 9e+37,   3.7980000972747803 ], [ 4,   1,  9e+37,   3.7980000972747803 ], [ 5,   1,   9e+37,   3.7980000972747803 ], [ 6,   1,   9e+37,   3.7980000972747803 ], [ 7,   1,   9e+37,   3.7980000972747803 ], [ 8,   1,   9e+37,   3.7980000972747803 ], [ 9,   1,   9e+37,   3.7980000972747803 ], [ 10,   1,   9e+37,   3.7980000972747803 ], [ 11,   1,   9e+37,   3.7980000972747803 ]];
		ur_dc_tou_mat = [[ 2,   1,   9e+37,   0 ], [ 1,   1,   9e+37,   0 ]];
		dc_enable = 1

	#------------------Starting SAM Simulation Program----------------------------------
	if __name__ == "__main__":
		ssc = PySSC()
		print ('Current folder = Solar NEM (ERI)/Data manipulation/SAM')
		print ('SSC Version = ', ssc.version())
		print ('SSC Build Information = ', ssc.build_info().decode("utf - 8"))
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

		#Write summary results
		result_file1.writerow([Customer, \
		Scheme, \
		Sensitivity, \
		NEM_sale_rate,\
		Region, \
		annual_energy, \
	    capacity_factor, \
	    kwh_per_kw, \
	    lcoe_nom, \
	    lcoe_real, \
	    elec_cost_without_system_year1, \
	    elec_cost_with_system_year1, \
	    savings_year1, \
	    npv, \
	    payback, \
	    IRR, \
	    adjusted_installed_cost, \
	    weather_file])


		#write detailed, hourly results
		# if Sensitivity == 2:
		# 	month = zip([Customer]*8760, \
		# 	[Scheme]*8760, \
		# 	[Sensitivity]*8760, \
		# 	[Region]*8760, \
		# 	[1]*24*31 + [2]*24*28 + [3]*24*31 + [4]*24*30 + [5]*24*31 + [6]*24*30 + [7]*24*31 + [8]*24*31 + [9]*24*30 + [10]*24*31 + [11]*24*30 + [12]*24*31, \
		# 	[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]*365, \
		# 	hourly_energy, \
		# 	hourly_load, \
		# 	hourly_to_grid, \
		# 	hourly_from_grid, \
		# 	hourly_system_to_load)

		# 	for row in month:
		# 		result_file2.writerow(row)

		# ssc.data_free(data);
		# return;

#----------------define inputs for each customer and scheme--------------------------------
#write headers for the result file
filename = 'Results/SAM_results'+ '_NetBilling_WG'  + '.csv'
f = csv.writer(open(filename,'w', encoding = 'utf-8'))
f.writerow(['Customer type','Scheme', 'Sensitivity','NEM sales rate', 'Region', 'Annual energy', \
	'Capacity factor', \
	'Energy yield', \
	'LCOE (nominal)', \
	'LCOE (real)', \
	'Bill without system', \
	'Bill with system', \
	'Net saving with system', \
	'NPV', \
	'Payback period', \
	'IRR', \
	'Net capital cost', \
	'File name'])

filename2 = 'Results/SAM_results'+ '_monthly'  + '.csv'
f2 = csv.writer(open(filename2,'w', encoding = 'utf-8'))
f2.writerow(['Customer type','Scheme', 'Sensitivity', 'Region', \
	'Month', 'Hour','Energy', 'Load', \
	'Energy_to_grid', 'Energy_from_grid', 'Energy_system_to_load'])

#Customer: Res, Res_TOU, SGS, SGS_TOU, MGS, LGS, LGS_BOI
#Scheme: 1. pilot, 2. NEM, 3. real-time buyback 

Cust = ["Res","Res_TOU",'SGS','SGS_TOU','MGS','LGS', 'LGS_BOI']
#Cust = ["LGS"]
list = os.listdir(b'THA_weather_data/')
#print(list)
#-------------------------------Run simulation for all provinces-----------------------------------------------------

for c in Cust:
	Customer = c
	for s in range(1,4): 
		Scheme = s
		print(s)
		for ss in range(1,4):
			Sens = ss
			for i in range(2,len(list)-1):
				weather_file = b'THA_weather_data/' + list[i] + b'/' + list[i] + b'.EPW'
				changwat1 = list[i].decode(encoding='UTF-8')
				changwat2 = changwat1.split('_')
				changwat = changwat2[1]
				print(changwat)
				#assign region from changwat name
				N = ["UTTARADIT", "TAK", "MAE-SOT", "PRAE","PITSANULOK", \
				"PHETCHABUN", "PHAYAO", "NAN", "NAKHON-SAWAN", "MAE-SARIANG", \
				"MAE-HONG-SON", "LOP-BURI", "LAMPHUN", "LAMPANG", "KAM-PAENG-PHET", \
				"CHIANG-RAI", "CHIANG-MAI"]

				NE = ["UDON-THANI", "UBON-RATCHATHANI", "THA-TUM", "SURIN", \
				"SAKON-KAKHON", "ROI-ET", "NONG-KHAI", "NAKHON-RATCHASIMA", "NAKHON-PHANOM", \
				"MUKDAHAN", "LOEI", "KHON-KAEN", "CHAIYAPHUM"]

				C = ["ARANYAPRATHET", "THONG-PHA-PHUM", "SUPHAN-BURI", "SATTAHIP", \
				"PRACHIN-BURI", "KOH-SICHANG", "KHLONG-YAI", "KANCHANABURI", "CHON-BURI", \
				"CHANTHABURI"]

				S = ["TRANG", "SURAT-THANI", "SONGKHLA", "RANONG", "PRACHUAP-KHIRIKHAN", \
				"PHUKET-AP", "PHUKET", "PATTANI", "NARATHIWAT", "NAKHON-SI-THAMMARAT", \
				"KOH-SAMUI", "KOH-LANTA", "HUA-HIN", "HAT-YAI", "CHUMPHON"]

				if changwat in N:
					Region = 14
				elif changwat in NE:
					Region = 15
				elif changwat in C:
					Region = 16
				elif changwat in S:
					Region = 17

				simulate(Customer, Scheme, weather_file, Region, f, f2, Sens)
