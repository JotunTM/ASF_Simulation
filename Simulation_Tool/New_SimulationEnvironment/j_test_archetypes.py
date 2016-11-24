import pandas as pd
import matplotlib.pyplot as plt
import datetime
import numpy as np
import re as re
import itertools
import csv

from j_paths import PATHS
from buildingSystem import *  
from SimulationClass import ASF_Simulation as ASF
from j_build_schedules import build_schedules
from j_build_dictionaries import  ArchT_build_df, MakeDicts, sort_dicts
import j_epw_import_tools as epw_tools

#Constants
#---------

SimulationData= {
	'optimizationTypes' : ['E_total'],
	'DataName' : 'ZH05_49comb',
	'geoLocation' : 'Zuerich_Kloten_2005',
	'EPWfile' : 'Zuerich_Kloten_2005.epw',
	'Save' : True,
	'ShowFig': False}

#Set panel data
PanelData={
	"XANGLES": [0, 15, 30, 45, 60, 75, 90],
	"YANGLES" : [-45, -30,-15,0, 15, 30, 45],
	"NoClusters":1,
	"numberHorizontal":6,
	"numberVertical":9,
	"panelOffset":400,
	"panelSize":400,
	"panelSpacing":500}
		
		#Set Building Parameters in [mm]
BuildingData={
	"room_width": 4900,     
	"room_height":3100,
	"room_depth":7000,
	"glazing_percentage_w": 0.92,
	"glazing_percentage_h": 0.97}

<<<<<<< HEAD
################################################################################################################
lighting_ontrol_d ={
"MULTI_RES":250,
"SINGLE_RES":200,
"HOTEL":300,
"OFFICE":350,
"RETAIL":400,
"FOODSTORE":400,
"RESTAURANT":250,
"INDUSTRIAL":300,
"SCHOOL":350,
"HOSPITAL":400,
"GYM":300
	
}

def ArchT_build_df(BuildingData):
	arch = pd.read_excel(paths['Archetypes_properties'],sheetname='THERMAL')
	r = re.compile("([a-zA-Z_]+)")
	m = r.match(arch["Code"][1])
	
	arch["code1"] = pd.DataFrame([r.match(string).groups() for string in arch.Code])
	arch = arch.set_index(['code1'])  
	arch = arch.drop(['SERVERROOM','PARKING','SWIMMING','COOLROOM'])
	arch = arch.reset_index(drop=False)
	arch = arch.drop('Es',axis=1)
	arch = arch.drop('Hs',axis=1)
	arch = arch.drop('U_roof',axis=1)
	arch = arch.drop('U_base',axis=1)
	
	int_loads = pd.read_excel(paths['Archetypes_properties'],sheetname='INTERNAL_LOADS')
	int_loads = int_loads.set_index(['Code'])
	int_loads = int_loads[['Qs_Wp','Ea_Wm2','El_Wm2']]
	int_loads = int_loads.reset_index(drop=False)

	T_sp = pd.read_excel(paths['Archetypes_properties'],sheetname='INDOOR_COMFORT')

	b_props = arch.merge(int_loads,how='left', left_on='code1', right_on='Code')
	b_props = b_props.merge(T_sp,how='left', left_on='code1', right_on='Code')
	b_props = b_props.drop('Code_y',axis=1)
	b_props = b_props.drop('Code',axis=1)
	b_props['setBackTempC'] = b_props['Tcs_setb_C']-b_props['Tcs_set_C']
	b_props['setBackTempH'] = b_props['Ths_set_C']-b_props['Ths_setb_C']
	
	volume = (BuildingData['room_width']/1000)*(BuildingData['room_depth']/1000)*(BuildingData['room_height']/1000)
	area = (BuildingData['room_width']/1000)*(BuildingData['room_depth']/1000)
	
	b_props['ACH_vent_p'] = b_props['Ve_lps']*3.6/volume
	
	#Assign values for Cm from ISO13790:2008, Table 12, based on archetypes
	th_mass = b_props['th_mass']
	c_m = []
	for i in range(0,len(th_mass)):
		if th_mass[i] == "T1":
			c_m.append(110*10**3) #Light
		elif th_mass[i] == "T2":
			c_m.append(165 * 10**3) #Medium
		elif th_mass[i] == "T3":
			c_m.append(260*10**3) #Heavy
	b_props['c_m_A_f'] = pd.DataFrame(c_m)

#declare variables
	occupancy = []
	lighting_control = []
#declare constants
	glass_solar_transmitance = []
	glass_light_transmitance = []
	Lighting_Utilisation_Factor = []
	Lighting_MaintenanceFactor = [] 
	ACH_infl = [] 
	ACH_vent = []
	ventilation_efficiency = [] 
	phi_c_max_A_f = [] 
	phi_h_max_A_f = [] 
	heatingSystem = []  
	coolingSystem = [] 
	heatingEfficiency = []  
	coolingEfficiency = [] 
	ActuationEnergy = []    

	for code in b_props['code1']:
		#variables
		occupancy.append('schedules_occ_%s.csv'%code)
		lighting_control.append(lighting_ontrol_d.get(code))
		
		glass_solar_transmitance.append(0.687)
		glass_light_transmitance.append(0.744)
		Lighting_Utilisation_Factor.append(0.45) 
		Lighting_MaintenanceFactor.append(0.9) 
		ACH_vent.append(1.5)
		ACH_infl.append(0.5) 
		ventilation_efficiency.append(0.6)
		phi_c_max_A_f.append(-np.inf)  
		phi_h_max_A_f.append(np.inf) 
		heatingSystem.append(DirectHeater) #DirectHeater, #ResistiveHeater #HeatPumpHeater
		coolingSystem.append(DirectCooler) #DirectCooler, #HeatPumpCooler
		heatingEfficiency.append(1)
		coolingEfficiency.append(1)
		ActuationEnergy.append(False)
		
	b_props['lighting_control'] = lighting_control
	b_props['Occupancy'] = occupancy
	b_props['ActuationEnergy'] = ActuationEnergy  
	
	b_props['glass_solar_transmitance'] = glass_solar_transmitance
	b_props['glass_light_transmitance'] = glass_light_transmitance
	b_props['Lighting_Utilisation_Factor'] = Lighting_Utilisation_Factor
	b_props['Lighting_MaintenanceFactor'] = Lighting_MaintenanceFactor
	b_props['ACH_vent'] = ACH_vent
	b_props['ACH_infl'] = ACH_infl
	b_props['ventilation_efficiency'] = ventilation_efficiency
	b_props['phi_c_max_A_f'] = phi_c_max_A_f
	b_props['phi_h_max_A_f'] = phi_h_max_A_f
	b_props['heatingSystem'] = heatingSystem
	b_props['coolingSystem'] = coolingSystem
	b_props['heatingEfficiency'] = heatingEfficiency
	b_props['coolingEfficiency'] = coolingEfficiency
	return b_props

#Create dictionaries for Archetypes:
def MakeDicts(b_props):
 
	bp_df = b_props[['Code_x',
						  'El_Wm2',
						  'lighting_control',
						  'U_wall',
						  'U_win',
						  'Ths_set_C',
						  'Tcs_set_C',
						  'c_m_A_f',
						  'Qs_Wp',    #Sensible heat gain due to occupancy [W/p]
						  'Ea_Wm2',    #Maximum electrical consumption due to appliances per unit of gross floor area [W/m2]
						  'glass_solar_transmitance',
						  'glass_light_transmitance',
						  'Lighting_Utilisation_Factor',
						  'Lighting_MaintenanceFactor',
						  'ACH_vent',
						  'ACH_infl',
						  'ventilation_efficiency',
						  'phi_c_max_A_f',
						  'phi_h_max_A_f',
						  'heatingSystem',
						  'coolingSystem',
						  'heatingEfficiency',
						  'coolingEfficiency']]
	
	bp_df = bp_df.rename(index=str,columns={'Code_x':'Code',
														'El_Wm2':'lighting_load',
														'U_win':'U_w',
														'c_m_A_f':'c_m_A_f',
														'U_wall':'U_em',
														'Ths_set_C':'theta_int_h_set',
														'Tcs_set_C':'theta_int_c_set',
														})
	bp_df = bp_df.set_index(['Code'])
	BP_dict = bp_df.to_dict(orient='index')

	so_df = b_props[['Code_x','setBackTempC','setBackTempH','Occupancy','ActuationEnergy']]
	so_df = so_df.set_index(['Code_x'])
	
	SO_dict = so_df.to_dict(orient='index')       
	return BP_dict, SO_dict
	
=======
#Set Default Values (For testing and sorting purposes)
BuildingProperties_default = {
	"glass_solar_transmitance" : 0.687,
	"glass_light_transmitance" : 0.744,
	"lighting_load" : 11.74,
	"lighting_control" : 300,
	"Lighting_Utilisation_Factor" :  0.45,
	"Lighting_MaintenanceFactor" : 0.9,
	"U_em" : 0.2,"U_w" : 1.2,
	"ACH_vent" : 1.5,
	"ACH_infl" :0.5,
	"ventilation_efficiency" : 0.6,
	"c_m_A_f" : 165 * 10**3,
	"theta_int_h_set" : 20,
	"theta_int_c_set" : 26,
	"phi_c_max_A_f": -np.inf,
	"phi_h_max_A_f":np.inf,
	"heatingSystem" : DirectHeater,
	"coolingSystem" : DirectCooler, 
	"heatingEfficiency" : 1,
	"coolingEfficiency" :1
	}

SimulationOptions_default = {
	'setBackTempH' : 4.,
	'setBackTempC' : 4., 
	'Occupancy' : 'schedules_occ_OFFICE.csv',
	'ActuationEnergy' : False}
 
>>>>>>> f613fcdf1ee24d7e87d801832e37891cb4a9e090
paths = PATHS()

b_props = ArchT_build_df(BuildingData)

#build_schedules(b_props,paths['Archetypes_schedules']) goes here. Currently still broken, schedules were generated using jupyter notebooks code. If the set remains the same, the existing scehdules will be sufficient.

#Select subset of b_props:
b_props = b_props[b_props.interval =='2005-2020']
b_props = b_props[b_props.type == 'construction']
BP_dict, SO_dict = MakeDicts(b_props)

print b_props.Ths_set_C
#Generate list of building names for iteration:
keylist = []
for key,item in BP_dict.iteritems():
	keylist.append(key)

<<<<<<< HEAD
######################################
runlist = keylist[0:1]
=======
#Runlist can be a subset of keylist:
runlist = keylist

#Create new dictionary as subsets of BP_dict and SO_dict with runlist as keys:
>>>>>>> f613fcdf1ee24d7e87d801832e37891cb4a9e090
BP_dict_run = { key:value for key,value in BP_dict.items() if key in runlist }
SO_dict_run = { key:value for key,value in SO_dict.items() if key in runlist }
#print BP_dict['GYM1']
print BP_dict_run

<<<<<<< HEAD
ASF_archetypes=ASF(SimulationData = SimulationData, PanelData = PanelData, BuildingData = BuildingData, BuildingProperties = BP_dict['GYM10'], SimulationOptions = SO_dict['GYM10'])
ASF_archetypes.SolveASF()
=======
#Run for default values
"""
ASF_archetypes=ASF(SimulationData = SimulationData, PanelData = PanelData, BuildingData = BuildingData, BuildingProperties = BuildingProperties_default, SimulationOptions = SimulationOptions_default)
ASF_archetypes.SolveASF()
all_results = ASF_archetypes.yearlyData.T
all_results['Name'] = 'Default'
all_results = all_results.set_index(['Name'])
"""
print BuildingProperties_default
#loop through building properties and simulation options dictionaries:
for i in range(0,len(runlist)):
	BP = sort_dicts(BP_dict_run[runlist[i]],BuildingProperties_default)
	SO = sort_dicts(SO_dict_run[runlist[i]],SimulationOptions_default)
	print BP
	"""ASF_archetypes=ASF(SimulationData = SimulationData, PanelData = PanelData, BuildingData = BuildingData, BuildingProperties = BP, SimulationOptions = SO)
	ASF_archetypes.SolveASF()
	current_result = ASF_archetypes.yearlyData.T
	current_result['Name'] = runlist[i]
	current_result = current_result.set_index(['Name'])
	if i == 0:
		all_results = current_result
	else:
		temp_list = [all_results,current_result]
		all_results = pd.concat(temp_list)
print '--simulations complete--'

#write results to csv:
all_results.to_csv(os.path.join(paths['CEA_folder'],'all_results.csv'))"""
>>>>>>> f613fcdf1ee24d7e87d801832e37891cb4a9e090
