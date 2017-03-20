from PySSC import PySSC
if __name__ == "__main__":
	ssc = PySSC()
	print 'Current folder = C:/Users/Admin/Downloads/sam-sdk-2016-3-14-r3/languages/python'
	print 'SSC Version = ', ssc.version()
	print 'SSC Build Information = ', ssc.build_info()
	ssc.module_exec_set_print(0)
	data = ssc.data_create()
	ssc.data_set_number( data, 'azimuth', 180 )
	ssc.data_set_number( data, 'array_type', 0 )
	ssc.data_set_number( data, 'en_range', 1 )
	ssc.data_set_number( data, 'dc_ac_ratio', 1.1000000238418579 )
	ssc.data_set_number( data, 'ibi_sta_percent_tax_fed', 1 )
	ssc.data_set_number( data, 'retrofits', 0 )
	ssc.data_set_string( data, 'solar_resource_file', 'C:/SAM/2016.3.14/solar_resource/Thailand THA Bangkok (INTL).csv' );
	ssc.data_set_number( data, 'system_capacity', 800 )
	ssc.data_set_number( data, 'tilt', 13.699999809265137 )
	ur_dc_sched_weekend = [[ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ]];
	ssc.data_set_matrix( data, 'ur_dc_sched_weekend', ur_dc_sched_weekend );
	ssc.data_set_number( data, 'ur_monthly_fixed_charge', 8.9209995269775391 )
	ssc.data_set_number( data, 'module_type', 0 )
	ssc.data_set_number( data, 'loan_rate', 0 )
	ssc.data_set_number( data, 'inv_eff', 96 )
	ssc.data_set_number( data, 'en_belpe', 0 )
	ssc.data_set_number( data, 'ibi_fed_amount_deprbas_fed', 0 )
	ssc.data_set_number( data, 'ptc_sta_escal', 0 )
	ssc.data_set_number( data, 'floor_area', 2000 )
	ssc.data_set_number( data, 'losses', 14.075660705566406 )
	ssc.data_set_number( data, 'ur_annual_min_charge', 0 )
	ssc.data_set_number( data, 'pbi_fed_term', 0 )
	ssc.data_set_number( data, 'ibi_sta_percent', 0 )
	ssc.data_set_number( data, 'inflation_rate', 2.5 )
	ssc.data_set_number( data, 'gcr', 0.40000000596046448 )
	ssc.data_set_number( data, 'om_fixed_escal', 0 )
	ssc.data_set_number( data, 'adjust:constant', 0 )
	ssc.data_set_number( data, 'system_use_lifetime_output', 0 )
	ssc.data_set_array_from_csv( data, 'load', 'C:/Users/Admin/Downloads/sam-sdk-2016-3-14-r3/languages/python/load.csv');
	ssc.data_set_number( data, 'itc_sta_percent_deprbas_sta', 0 )
	ssc.data_set_number( data, 'stories', 2 )
	ssc.data_set_number( data, 'yrbuilt', 1980 )
	ssc.data_set_number( data, 'occupants', 4 )
	ssc.data_set_number( data, 'cbi_uti_deprbas_sta', 0 )
	occ_schedule =[ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 ];
	ssc.data_set_array( data, 'occ_schedule',  occ_schedule);
	ssc.data_set_number( data, 'ibi_fed_amount_tax_fed', 1 )
	ssc.data_set_number( data, 'om_fuel_cost_escal', 0 )
	ssc.data_set_number( data, 'state_tax_rate', 0 )
	ssc.data_set_number( data, 'theat', 68 )
	ssc.data_set_number( data, 'itc_sta_percent', 0 )
	ssc.data_set_number( data, 'ur_dc_enable', 1 )
	ssc.data_set_number( data, 'tcool', 76 )
	ur_dc_tou_mat = [[ 1,   1,   9.9999996802856925e+037,   0 ]];
	ssc.data_set_matrix( data, 'ur_dc_tou_mat', ur_dc_tou_mat );
	ssc.data_set_number( data, 'theatsb', 68 )
	monthly_util =[ 725, 630, 665, 795, 1040, 1590, 1925, 1730, 1380, 1080, 635, 715 ];
	ssc.data_set_array( data, 'monthly_util',  monthly_util);
	ssc.data_set_number( data, 'itc_fed_percent_deprbas_fed', 1 )
	ssc.data_set_number( data, 'tcoolsb', 76 )
	ssc.data_set_number( data, 'sales_tax_rate', 0 )
	t_sched =[ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 ];
	ssc.data_set_array( data, 't_sched',  t_sched);
	ssc.data_set_number( data, 'en_cool', 1 )
	ssc.data_set_number( data, 'en_heat', 1 )
	ssc.data_set_number( data, 'itc_fed_percent_maxvalue', 9.9999996802856925e+037 )
	ssc.data_set_number( data, 'ur_monthly_min_charge', 0 )
	ssc.data_set_number( data, 'en_fridge', 1 )
	ur_ec_sched_weekend = [[ 2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2 ], [ 2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2 ], [ 2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2 ], [ 2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2 ], [ 2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2 ], [ 2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2 ], [ 2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2 ], [ 2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2 ], [ 2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2 ], [ 2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2 ], [ 2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2 ], [ 2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2 ]];
	ssc.data_set_matrix( data, 'ur_ec_sched_weekend', ur_ec_sched_weekend );
	ssc.data_set_number( data, 'en_dish', 1 )
	ssc.data_set_number( data, 'en_wash', 1 )
	ssc.data_set_number( data, 'ibi_oth_percent_deprbas_fed', 0 )
	ssc.data_set_number( data, 'en_dry', 1 )
	ssc.data_set_number( data, 'insurance_rate', 0.25 )
	ssc.data_set_number( data, 'ibi_uti_percent_tax_fed', 1 )
	ssc.data_set_number( data, 'en_mels', 1 )
	ssc.data_set_number( data, 'analysis_period', 25 )
	pbi_oth_amount =[ 0 ];
	ssc.data_set_array( data, 'pbi_oth_amount',  pbi_oth_amount);
	ssc.data_set_number( data, 'ibi_oth_percent_tax_fed', 1 )
	degradation =[ 0.5 ];
	ssc.data_set_array( data, 'degradation',  degradation);
	ssc.data_set_number( data, 'total_installed_cost', 1024000 )
	load_escalation =[ 3.5 ];
	ssc.data_set_array( data, 'load_escalation',  load_escalation);
	ssc.data_set_number( data, 'itc_sta_amount_deprbas_fed', 0 )
	rate_escalation =[ 3.5 ];
	ssc.data_set_array( data, 'rate_escalation',  rate_escalation);
	ssc.data_set_number( data, 'mortgage', 0 )
	ssc.data_set_number( data, 'ur_metering_option', 0 )
	ssc.data_set_number( data, 'ur_nm_yearend_sell_rate', 0.065999999642372131 )
	ur_ec_sched_weekday = [[ 2,   2,   2,   2,   2,   2,   2,   2,   2,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   2,   2 ], [ 2,   2,   2,   2,   2,   2,   2,   2,   2,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   2,   2 ], [ 2,   2,   2,   2,   2,   2,   2,   2,   2,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   2,   2 ], [ 2,   2,   2,   2,   2,   2,   2,   2,   2,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   2,   2 ], [ 2,   2,   2,   2,   2,   2,   2,   2,   2,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   2,   2 ], [ 2,   2,   2,   2,   2,   2,   2,   2,   2,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   2,   2 ], [ 2,   2,   2,   2,   2,   2,   2,   2,   2,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   2,   2 ], [ 2,   2,   2,   2,   2,   2,   2,   2,   2,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   2,   2 ], [ 2,   2,   2,   2,   2,   2,   2,   2,   2,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   2,   2 ], [ 2,   2,   2,   2,   2,   2,   2,   2,   2,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   2,   2 ], [ 2,   2,   2,   2,   2,   2,   2,   2,   2,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   2,   2 ], [ 2,   2,   2,   2,   2,   2,   2,   2,   2,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   2,   2 ]];
	ssc.data_set_matrix( data, 'ur_ec_sched_weekday', ur_ec_sched_weekday );
	ur_ec_tou_mat = [[ 1,   1,   1000000000,   0,   0.11100000143051147,   0 ], [ 2,   1,   1000000000,   0,   0.065999999642372131,   0 ], [ 3,   0,   0,   0,   0,   0 ]];
	ssc.data_set_matrix( data, 'ur_ec_tou_mat', ur_ec_tou_mat );
	ur_dc_sched_weekday = [[ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ]];
	ssc.data_set_matrix( data, 'ur_dc_sched_weekday', ur_dc_sched_weekday );
	ur_dc_flat_mat = [[ 0,   1,   168.69999694824219,   3.7980000972747803 ], [ 1,   1,   200,   3.7980000972747803 ], [ 2,   1,   178.60000610351562,   3.7980000972747803 ], [ 3,   1,   193.1300048828125,   3.7980000972747803 ], [ 4,   1,   189.92999267578125,   3.7980000972747803 ], [ 5,   1,   184.92999267578125,   3.7980000972747803 ], [ 6,   1,   176.6199951171875,   3.7980000972747803 ], [ 7,   1,   168.80000305175781,   3.7980000972747803 ], [ 8,   1,   177.66000366210937,   3.7980000972747803 ], [ 9,   1,   171.44000244140625,   3.7980000972747803 ], [ 10,   1,   189.21000671386719,   3.7980000972747803 ], [ 11,   1,   177.3800048828125,   3.7980000972747803 ]];
	ssc.data_set_matrix( data, 'ur_dc_flat_mat', ur_dc_flat_mat );
	ssc.data_set_number( data, 'prop_tax_cost_assessed_percent', 0 )
	ssc.data_set_number( data, 'itc_sta_percent_maxvalue', 9.9999996802856925e+037 )
	ssc.data_set_number( data, 'federal_tax_rate', 0 )
	ssc.data_set_number( data, 'property_tax_rate', 0 )
	ssc.data_set_number( data, 'pbi_oth_tax_sta', 1 )
	ssc.data_set_number( data, 'prop_tax_assessed_decline', 0 )
	ssc.data_set_number( data, 'real_discount_rate', 6.619999885559082 )
	ssc.data_set_number( data, 'cbi_uti_deprbas_fed', 0 )
	ssc.data_set_number( data, 'loan_term', 0 )
	ssc.data_set_number( data, 'cbi_oth_deprbas_fed', 0 )
	ssc.data_set_number( data, 'debt_fraction', 0 )
	om_fixed =[ 0 ];
	ssc.data_set_array( data, 'om_fixed',  om_fixed);
	om_production =[ 0 ];
	ssc.data_set_array( data, 'om_production',  om_production);
	ssc.data_set_number( data, 'om_production_escal', 0 )
	ssc.data_set_number( data, 'ibi_fed_percent_tax_fed', 1 )
	om_capacity =[ 10 ];
	ssc.data_set_array( data, 'om_capacity',  om_capacity);
	ssc.data_set_number( data, 'cbi_oth_tax_fed', 1 )
	ssc.data_set_number( data, 'om_capacity_escal', 2.2000000476837158 )
	om_fuel_cost =[ 0 ];
	ssc.data_set_array( data, 'om_fuel_cost',  om_fuel_cost);
	ssc.data_set_number( data, 'itc_fed_amount', 0 )
	ssc.data_set_number( data, 'itc_fed_amount_deprbas_fed', 1 )
	ssc.data_set_number( data, 'itc_fed_amount_deprbas_sta', 1 )
	ssc.data_set_number( data, 'itc_sta_amount', 0 )
	ssc.data_set_number( data, 'itc_sta_amount_deprbas_sta', 0 )
	ssc.data_set_number( data, 'itc_fed_percent', 0 )
	ssc.data_set_number( data, 'itc_fed_percent_deprbas_sta', 1 )
	ssc.data_set_number( data, 'itc_sta_percent_deprbas_fed', 0 )
	ssc.data_set_number( data, 'cbi_oth_maxvalue', 9.9999996802856925e+037 )
	ptc_fed_amount =[ 0 ];
	ssc.data_set_array( data, 'ptc_fed_amount',  ptc_fed_amount);
	ssc.data_set_number( data, 'ptc_fed_term', 10 )
	ssc.data_set_number( data, 'ptc_fed_escal', 0 )
	ptc_sta_amount =[ 0 ];
	ssc.data_set_array( data, 'ptc_sta_amount',  ptc_sta_amount);
	ssc.data_set_number( data, 'ptc_sta_term', 10 )
	ssc.data_set_number( data, 'ibi_fed_amount', 0 )
	ssc.data_set_number( data, 'cbi_oth_tax_sta', 1 )
	ssc.data_set_number( data, 'cbi_uti_maxvalue', 9.9999996802856925e+037 )
	ssc.data_set_number( data, 'ibi_fed_amount_tax_sta', 1 )
	ssc.data_set_number( data, 'ibi_fed_amount_deprbas_sta', 0 )
	ssc.data_set_number( data, 'ibi_sta_amount', 0 )
	ssc.data_set_number( data, 'ibi_sta_amount_tax_fed', 1 )
	ssc.data_set_number( data, 'ibi_sta_amount_tax_sta', 1 )
	ssc.data_set_number( data, 'ibi_sta_amount_deprbas_fed', 0 )
	ssc.data_set_number( data, 'ibi_sta_amount_deprbas_sta', 0 )
	ssc.data_set_number( data, 'ibi_uti_amount', 0 )
	ssc.data_set_number( data, 'ibi_uti_amount_tax_fed', 1 )
	ssc.data_set_number( data, 'ibi_uti_amount_tax_sta', 1 )
	ssc.data_set_number( data, 'ibi_uti_amount_deprbas_fed', 0 )
	ssc.data_set_number( data, 'ibi_uti_amount_deprbas_sta', 0 )
	ssc.data_set_number( data, 'ibi_oth_amount', 0 )
	ssc.data_set_number( data, 'ibi_oth_amount_tax_fed', 1 )
	ssc.data_set_number( data, 'ibi_oth_amount_tax_sta', 1 )
	ssc.data_set_number( data, 'ibi_oth_amount_deprbas_fed', 0 )
	ssc.data_set_number( data, 'ibi_oth_amount_deprbas_sta', 0 )
	ssc.data_set_number( data, 'ibi_fed_percent', 0 )
	ssc.data_set_number( data, 'ibi_fed_percent_maxvalue', 9.9999996802856925e+037 )
	ssc.data_set_number( data, 'cbi_oth_amount', 0 )
	ssc.data_set_number( data, 'ibi_fed_percent_tax_sta', 1 )
	ssc.data_set_number( data, 'ibi_fed_percent_deprbas_fed', 0 )
	ssc.data_set_number( data, 'ibi_fed_percent_deprbas_sta', 0 )
	ssc.data_set_number( data, 'ibi_sta_percent_maxvalue', 9.9999996802856925e+037 )
	ssc.data_set_number( data, 'pbi_fed_tax_fed', 1 )
	ssc.data_set_number( data, 'ibi_sta_percent_tax_sta', 1 )
	ssc.data_set_number( data, 'ibi_sta_percent_deprbas_fed', 0 )
	ssc.data_set_number( data, 'ibi_sta_percent_deprbas_sta', 0 )
	ssc.data_set_number( data, 'ibi_uti_percent', 0 )
	ssc.data_set_number( data, 'ibi_uti_percent_maxvalue', 9.9999996802856925e+037 )
	ssc.data_set_number( data, 'ibi_uti_percent_tax_sta', 1 )
	ssc.data_set_number( data, 'ibi_uti_percent_deprbas_fed', 0 )
	ssc.data_set_number( data, 'ibi_uti_percent_deprbas_sta', 0 )
	ssc.data_set_number( data, 'pbi_uti_tax_sta', 1 )
	ssc.data_set_number( data, 'ibi_oth_percent', 0 )
	ssc.data_set_number( data, 'ibi_oth_percent_maxvalue', 9.9999996802856925e+037 )
	ssc.data_set_number( data, 'ibi_oth_percent_tax_sta', 1 )
	ssc.data_set_number( data, 'ibi_oth_percent_deprbas_sta', 0 )
	ssc.data_set_number( data, 'cbi_fed_amount', 0 )
	ssc.data_set_number( data, 'cbi_fed_maxvalue', 9.9999996802856925e+037 )
	ssc.data_set_number( data, 'cbi_uti_amount', 0 )
	ssc.data_set_number( data, 'cbi_fed_tax_fed', 1 )
	ssc.data_set_number( data, 'cbi_fed_tax_sta', 1 )
	ssc.data_set_number( data, 'cbi_fed_deprbas_fed', 0 )
	ssc.data_set_number( data, 'cbi_fed_deprbas_sta', 0 )
	ssc.data_set_number( data, 'cbi_sta_amount', 0 )
	ssc.data_set_number( data, 'cbi_sta_maxvalue', 9.9999996802856925e+037 )
	ssc.data_set_number( data, 'cbi_sta_tax_fed', 1 )
	ssc.data_set_number( data, 'cbi_sta_tax_sta', 1 )
	ssc.data_set_number( data, 'cbi_sta_deprbas_fed', 0 )
	ssc.data_set_number( data, 'cbi_sta_deprbas_sta', 0 )
	ssc.data_set_number( data, 'cbi_uti_tax_fed', 1 )
	ssc.data_set_number( data, 'cbi_uti_tax_sta', 1 )
	ssc.data_set_number( data, 'cbi_oth_deprbas_sta', 0 )
	pbi_fed_amount =[ 0 ];
	ssc.data_set_array( data, 'pbi_fed_amount',  pbi_fed_amount);
	ssc.data_set_number( data, 'pbi_fed_escal', 0 )
	ssc.data_set_number( data, 'pbi_fed_tax_sta', 1 )
	pbi_sta_amount =[ 0 ];
	ssc.data_set_array( data, 'pbi_sta_amount',  pbi_sta_amount);
	ssc.data_set_number( data, 'pbi_sta_term', 0 )
	ssc.data_set_number( data, 'pbi_sta_escal', 0 )
	ssc.data_set_number( data, 'pbi_sta_tax_fed', 1 )
	ssc.data_set_number( data, 'pbi_sta_tax_sta', 1 )
	pbi_uti_amount =[ 0 ];
	ssc.data_set_array( data, 'pbi_uti_amount',  pbi_uti_amount);
	ssc.data_set_number( data, 'pbi_uti_term', 0 )
	ssc.data_set_number( data, 'pbi_uti_escal', 0 )
	ssc.data_set_number( data, 'pbi_uti_tax_fed', 1 )
	ssc.data_set_number( data, 'pbi_oth_term', 0 )
	ssc.data_set_number( data, 'pbi_oth_escal', 0 )
	ssc.data_set_number( data, 'pbi_oth_tax_fed', 1 )
	ssc.data_set_number( data, 'battery_per_kwh', 600 )
	ssc.data_set_number( data, 'market', 0 )
	ssc.data_set_number( data, 'salvage_percentage', 0 )
	module = ssc.module_create('pvwattsv5')	
	ssc.module_exec_set_print( 0 );
	if ssc.module_exec(module, data) == 0:
		print ('pvwattsv5 simulation error')
		idx = 1
		msg = ssc.module_log(module, 0)
		while (msg != None):
			print ('	: ' + msg)
			msg = ssc.module_log(module, idx)
			idx = idx + 1
		SystemExit( "Simulation Error" );
	ssc.module_free(module)
	module = ssc.module_create('belpe')	
	ssc.module_exec_set_print( 0 );
	if ssc.module_exec(module, data) == 0:
		print ('belpe simulation error')
		idx = 1
		msg = ssc.module_log(module, 0)
		while (msg != None):
			print ('	: ' + msg)
			msg = ssc.module_log(module, idx)
			idx = idx + 1
		SystemExit( "Simulation Error" );
	ssc.module_free(module)
	module = ssc.module_create('utilityrate4')	
	ssc.module_exec_set_print( 0 );
	if ssc.module_exec(module, data) == 0:
		print ('utilityrate4 simulation error')
		idx = 1
		msg = ssc.module_log(module, 0)
		while (msg != None):
			print ('	: ' + msg)
			msg = ssc.module_log(module, idx)
			idx = idx + 1
		SystemExit( "Simulation Error" );
	ssc.module_free(module)
	module = ssc.module_create('cashloan')	
	ssc.module_exec_set_print( 0 );
	if ssc.module_exec(module, data) == 0:
		print ('cashloan simulation error')
		idx = 1
		msg = ssc.module_log(module, 0)
		while (msg != None):
			print ('	: ' + msg)
			msg = ssc.module_log(module, idx)
			idx = idx + 1
		SystemExit( "Simulation Error" );
	ssc.module_free(module)
	annual_energy = ssc.data_get_number(data, 'annual_energy');
	print 'Annual energy (year 1) = ', annual_energy
	capacity_factor = ssc.data_get_number(data, 'capacity_factor');
	print 'Capacity factor (year 1) = ', capacity_factor
	kwh_per_kw = ssc.data_get_number(data, 'kwh_per_kw');
	print 'Energy yield (year 1) = ', kwh_per_kw
	lcoe_nom = ssc.data_get_number(data, 'lcoe_nom');
	print 'Levelized COE (nominal) = ', lcoe_nom
	lcoe_real = ssc.data_get_number(data, 'lcoe_real');
	print 'Levelized COE (real) = ', lcoe_real
	elec_cost_without_system_year1 = ssc.data_get_number(data, 'elec_cost_without_system_year1');
	print 'Electricity bill without system (year 1) = ', elec_cost_without_system_year1
	elec_cost_with_system_year1 = ssc.data_get_number(data, 'elec_cost_with_system_year1');
	print 'Electricity bill with system (year 1) = ', elec_cost_with_system_year1
	savings_year1 = ssc.data_get_number(data, 'savings_year1');
	print 'Net savings with system (year 1) = ', savings_year1
	npv = ssc.data_get_number(data, 'npv');
	print 'Net present value = ', npv
	payback = ssc.data_get_number(data, 'payback');
	print 'Payback period = ', payback
	adjusted_installed_cost = ssc.data_get_number(data, 'adjusted_installed_cost');
	print 'Net capital cost = ', adjusted_installed_cost
	first_cost = ssc.data_get_number(data, 'first_cost');
	print 'Equity = ', first_cost
	loan_amount = ssc.data_get_number(data, 'loan_amount');
	print 'Debt = ', loan_amount
	ssc.data_free(data);