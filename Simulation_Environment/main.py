# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 11:14:42 2016

main file for simulation environment

@author: Jeremias
"""

import os, sys
import numpy as np
import json
import time
import warnings

######### -----USER INTERACTION------ #############

# set mode of this main script ('initialize', 'post_processing')
#mainMode = 'initialize' #'initialize'
mainMode = 'post_processing' #'initialize'

# specify the location used for the analysis - this name must be the same as a
# folder in the directory .../ASF_Simulation/Simulation_Environment/data/geographical_location
# new locations can be added with the grasshopper main script for any .epw weather data
geoLocation = 'Zuerich-Kloten' # 'Zuerich-Kloten', 'MADRID_ESP', 'SINGAPORE_SGP'
#geoLocation = 'MADRID_ESP' # 'Zuerich-Kloten', 'MADRID_ESP'
#geoLocation = 'SINGAPORE_SGP' # 'Zuerich-Kloten', 'MADRID_ESP', 'SINGAPORE_SGP'


# set folder name of DIVA simulation data (in data\grasshopper\DIVA):
#diva_folder = 'Simulation_Madrid_25comb' #'Simulation_Kloten_25comb'
#diva_folder = 'DIVA_Kloten_25comb'
diva_folder = 'DIVA_Kloten_49comb'
#diva_folder = 'DIVA_Singapore_25comb'


# set folder name of LadyBug simulation data (in data\grasshopper\LadyBug). 
# This folder has the same name as the generated folder for the electrical 
# results in data\python\electrical:
#radiation_folder = 'Radiation_electrical_monthly_25comb'
#radiation_folder = 'Radiation_Kloten_tracking'
radiation_folder = 'Radiation_Kloten_49comb'
#radiation_folder = 'Radiation_electrical_monthly_25comb_Madrid'
#radiation_folder = 'Radiation_Singapore_25comb'


# set option to change the size of the PV area for the electrical simulation, 
# this is done in steps of 2 times the radiation gridsize, so 0 corresponds a 
# PV-size of 400mm, 1 corresponds to PV-size of 350mm, 2 corresponds to 300mm 
# etc.:
pvSizeOption = 0


# specify if  plots should be created (True or False):
createPlots = True


# only tradeoffs flag, set true if general data plots should not be evaluated:
onlyTradeoffs = False


# post processing tradeoff options: change efficiencies of heating(COP)/
# cooling(COP)/lighting(Lighting Load)/PV(Factor by which results are multiplied)
# set changeEfficiency to True if data should be changed, set False if simulation efficiencies should be used:
efficiencyChanges = {'changeEfficiency':True, 'H_COP': 5, 'C_COP': 5, 'L_Load': 3, 'PV': 1}


# define tradeoff period and if it should be enabled, startHour and endHour are
# inclusive, so startHour=1 and endHour=24 corresponds to a time period from 
# 0:00-24:00. month is defined in the classical sense, so month=1 corresponds to 
# january.
tradeoffPeriod = {'enabled':False, 'month':7, 'startHour':1, 'endHour':24}
    
######### -----END OF USER INTERACTION------ #############
    
# get current time
now = time.strftime("%Y_%m_%d %H.%M.%S", time.localtime())
print "simulation start: " + now

print "variables set"

# create empty dictionary with auxiliary variables
auxVar = {}

# create dictionary to write all paths:
paths = {}

# find path of current folder (simulation_environment)
paths['main'] = os.path.abspath(os.path.dirname(sys.argv[0]))

# define paths of subfolders:
paths['data'] = paths['main'] + '\\data'
paths['python'] = paths['main'] + '\\python'
paths['gh'] = paths['main'] + '\\grasshopper'
paths['results'] = paths['main'] + '\\results'

# add python_path to system path, so that all files are available:
sys.path.insert(0, paths['python'])

# define paths of data_folders:
paths['diva'] = os.path.join(( paths['data'] + "\grasshopper\DIVA"), diva_folder)
paths['lb'] = os.path.join(( paths['data'] + "\grasshopper\LadyBug"), radiation_folder)
paths['electrical'] = os.path.join(( paths['data'] + "\python\electrical_simulation"), radiation_folder)

print "paths defined"

if mainMode == 'initialize':
    
    print "start initializing"
    

    
    # define path of geographical location:
    paths['geo'] = os.path.join(( paths['data'] + "\geographical_location"), geoLocation)
    # create sun data based on grasshopper file
    execfile(paths['python'] + "\SunAngles_Tracking_and_temperature.py")

    # calculate and save lookup table if it does not yet exist:
    if not os.path.isfile(paths['data'] + '\python\electrical_simulation\curr_model_submod_lookup.npy'): 
        execfile(paths['python'] + '\create_lookup_table.py')
    else:
        print 'lookup table not created as it already exists'
    
# calculate and save PV electricity production:
if mainMode == 'post_processing':
    
    print "start post processing"
    
    from prepareData import prepareMonthlyRadiatonData, importDIVAresults, readLayoutAndCombinations, CalcXYAnglesAndLocation, sum_monthly
    
    # create dictionary to save monthly data:
    monthlyData = {}
    
    # create dictionary with ladybug simulation settings:
    lbSettings = {}
    
    # panelsize used for simulation:
    lbSettings['panelsize'] = readLayoutAndCombinations(paths['lb'])['panelSize']  
    
    # desired grid point size used for simulation:
    lbSettings['desiredGridPointSize'] = readLayoutAndCombinations(paths['lb'])['desiredGridPointSize']  
    
    # actual grid point size used for simulation:
    lbSettings['actualGridPointSize'] = lbSettings['panelsize']/(round(lbSettings['panelsize']/float(lbSettings['desiredGridPointSize'])))
    
    # calculate aperturesize according to pvSizeOption:
    lbSettings['aperturesize'] = int(lbSettings['panelsize'] - pvSizeOption*2*lbSettings['actualGridPointSize'])
    
    # define path of geographical location:
    paths['geo'] = os.path.join(( paths['data'] + "\geographical_location"), geoLocation)
    
    # load sunTrackingData used for the LadyBug simulation:
    with open(paths['geo'] + '\SunTrackingData.json', 'r') as fp:
        SunTrackingData = json.load(fp)
        fp.close()
        
    # find the number of hours analysed by ladybug:
    lbSettings['numHoursLB'] = np.shape(SunTrackingData['HOY'])[0]
    
    # find the number of combinations analysed by ladybug:
    lbSettings['numCombLB'] = len(CalcXYAnglesAndLocation(readLayoutAndCombinations(paths['lb']))['allAngles'][0])

    # check if pv results already exist, if not, create them, else load them
    if not os.path.isfile(paths['electrical'] + '\\aperturesize_' + str(lbSettings['aperturesize']) + '\PV_electricity_results.npy'): 
        if not os.path.isdir(paths['electrical'] + '\\aperturesize_' + str(lbSettings['aperturesize'])):
            os.makedirs(paths['electrical'] + '\\aperturesize_' + str(lbSettings['aperturesize']))
        from asf_electricity_production import asf_electricity_production
        print 'calculating PV electricity production'     
        
        if createPlots:
            PV_electricity_results, PV_detailed_results, fig1, fig2 = \
            asf_electricity_production(createPlots=createPlots, 
                                       lb_radiation_path=paths['lb'], 
                                       panelsize=lbSettings['panelsize'], 
                                       pvSizeOption=pvSizeOption, 
                                       save_results_path = paths['electrical'] + '\\aperturesize_' + str(lbSettings['aperturesize']),
                                       lookup_table_path = paths['data'] + '\python\electrical_simulation',
                                       geo_path=paths['geo'])
        else:
            PV_electricity_results, PV_detailed_results= \
            asf_electricity_production(createPlots=createPlots, 
                                       lb_radiation_path=paths['lb'], 
                                       panelsize=lbSettings['panelsize'], 
                                       pvSizeOption=pvSizeOption, 
                                       save_results_path = paths['electrical'] + '\\aperturesize_' + str(lbSettings['aperturesize']),
                                       lookup_table_path = paths['data'] + '\python\electrical_simulation',
                                       geo_path=paths['geo'])
    else: 
        PV_electricity_results = np.load(paths['electrical'] + '\\aperturesize_' + str(lbSettings['aperturesize']) + '\PV_electricity_results.npy').item()
        PV_detailed_results = np.load(paths['electrical'] + '\\aperturesize_' + str(lbSettings['aperturesize']) + '\PV_detailed_results.npy').item()
        print 'PV_electricity_results loaded from folder'
        
    print "preparing data"
    
    # prepare monthly PV and Radiation data and write it to the monthlyData dictionary:
    monthlyData['efficiencies'] = {}
    monthlyData['PV'], monthlyData['R'], monthlyData['efficiencies']['PV'],  monthlyData['R_avg'],\
    monthlyData['R_theo'], monthlyData['PV_avg'], monthlyData['PV_eff'] \
                                        = prepareMonthlyRadiatonData(PV_electricity_results)
    
    # make data negative to be consitent:    
    monthlyData['PV'] = -monthlyData['PV']
    monthlyData['R'] = monthlyData['R']
    
    # import DIVA results:
    DIVA_results = importDIVAresults(paths['diva'])    
    
    # import DIVA LayoutAndCombinations and write to DIVA_results dict.:
    DIVA_results['LayoutAndCombinations'] = readLayoutAndCombinations(paths['diva'])
    
    # calculate angles of DIVA_results
    DIVA_results['angles'] = CalcXYAnglesAndLocation(DIVA_results['LayoutAndCombinations'])

    # import LadyBug LayoutAndCombinations and write to PV_electricity_results dict.:
    PV_electricity_results['LayoutAndCombinations'] = readLayoutAndCombinations(paths['lb'])
    
    # check if the two LayoutAndCombinations files are the same
    if DIVA_results['LayoutAndCombinations'] == PV_electricity_results['LayoutAndCombinations']:
        # calculate angles corresponding to the layoutAndCombination file:
        monthlyData['angles'] = CalcXYAnglesAndLocation(DIVA_results['LayoutAndCombinations'])
        # set variable that allows combined analysis of DIVA and LB results:
        auxVar['combineResults'] = True
    else:
        warnings.warn('LayoutAndCombination of DIVA and LadyBug files are not the same, check the data-folders!')
        
        # assign layout and combinations seperately:
        monthlyData['divaAngles'] =  CalcXYAnglesAndLocation(DIVA_results['LayoutAndCombinations'])
        monthlyData['lbAngles'] =  CalcXYAnglesAndLocation(PV_electricity_results['LayoutAndCombinations'])
        
        # set variable that prevents combined analysis of DIVA and LB:
        auxVar['combineResults'] = False
        
    # sum up data for every month:
    monthlyData['H'] = sum_monthly(DIVA_results['H'])
    monthlyData['C'] = sum_monthly(DIVA_results['C'])
    monthlyData['L'] = sum_monthly(DIVA_results['L'])
    monthlyData['E_HCL'] = sum_monthly(DIVA_results['E'])
    
    if auxVar['combineResults']:
        monthlyData['E_tot'] = monthlyData['E_HCL'] + monthlyData['PV']
    
    # add DIVA efficiencies to monthly data dictionary:
    #monthlyData['efficiencies']['L_load'] = DIVA_results['efficiencies'][] 
    monthlyData['efficiencies'].update(DIVA_results['efficiencies'])
    
    if createPlots and not onlyTradeoffs:
        
        print "creating plots"
        

        from createMasks import createDIVAmask, createLBmask
        from createFigures import createCarpetPlots, createDIVAcarpetPlots
        from plotDataFunctions import pcolorMonths, pcolorEnergyMonths, pcolorDays, pcolorEnergyDays
        
        # plot detailed DIVA Results:
        createDIVAcarpetPlots(pcolorDays, DIVA_results, 'xy')
        createDIVAcarpetPlots(pcolorDays, DIVA_results, 'x')
        createDIVAcarpetPlots(pcolorDays, DIVA_results, 'y')
        createDIVAcarpetPlots(pcolorEnergyDays, DIVA_results)        
        
        # create masks for plotting:
        monthlyData['DIVAmask'] = createDIVAmask(monthlyData['L'])
        monthlyData['LBmask'] = createLBmask(monthlyData['R'])
        
        if auxVar['combineResults']:
            # plot the optimum angles of the monthly data:
            createCarpetPlots(pcolorMonths, monthlyData, 'xy')
            createCarpetPlots(pcolorMonths, monthlyData, 'x')
            createCarpetPlots(pcolorMonths, monthlyData, 'y')
        
            # plot the energy use at the corresponding optimum orientation:
            createCarpetPlots(pcolorEnergyMonths, monthlyData)
    
    
    from auxFunctions import create_evalList
    from Tradeoffs import compareTotalEnergy
    
    if tradeoffPeriod['enabled']:
        tradeoffPeriod['evalList'] = create_evalList('monthly', tradeoffPeriod['month'], tradeoffPeriod['startHour'], tradeoffPeriod['endHour'])
    else:
        tradeoffPeriod['evalList'] = []
    
    # evaluate tradeoffs:
    TradeoffResults = compareTotalEnergy(monthlyData, efficiencyChanges, createPlots, tradeoffPeriod, auxVar)
    
    monthList = ['January','February','March','April','May','June','July','August','September','November','October','December']
    
    # create folder where results will be saved:
    os.makedirs(paths['results'] + '\\' + now )
    
    if auxVar['combineResults']:
        # write csv file that summarizes results  
        with open(paths['results'] + '\\' + now + '\\summary.csv', 'w') as f:
            f.write('Simulation Results\n\n')
            f.write('Location\n' + geoLocation + '\n\n')
            f.write('Number of Combinations\n' + str(lbSettings['numCombLB']) + '\n\n')
            f.write('Azimuth Angles\n')
            [f.write('{0};'.format(value)) for value in PV_electricity_results['LayoutAndCombinations']['Yangles']]
            f.write('\n\nAltitude Angles\n')
            [f.write('{0};'.format(value)) for value in PV_electricity_results['LayoutAndCombinations']['Xangles']]
            f.write('\n\nNumber of Clusters\n')
            f.write(str(int(PV_electricity_results['LayoutAndCombinations']['NoClusters'])) + '\n\n')
            f.write('Panel Size [mm]\n')
            f.write(str(int(PV_electricity_results['LayoutAndCombinations']['panelSize'])) + '\n\n')
            f.write('Panel Spacing [mm] (shortest midpoint to midpoint distance)\n')
            f.write(str(int(PV_electricity_results['LayoutAndCombinations']['panelSpacing'])) + '\n\n')
            f.write('Number of Panels\n')
            f.write(str(int(np.shape(PV_detailed_results['Ins_ap'])[1])) + '\n\n')
            f.write('Evaluation Period\n')
            if tradeoffPeriod['enabled']:
                f.write('Energy Usage evaluated for the cumulative hours ' + 
                        str(tradeoffPeriod['startHour']-1) + ':00-' + 
                        str(tradeoffPeriod['endHour']) + ':00 in ' + 
                        monthList[tradeoffPeriod['month']-1] +'\n\n')
            else:
                f.write('Energy Usage evaluated for the whole year\n\n')
                
            if efficiencyChanges['changeEfficiency']:
                f.write('Heating COP\n')
                f.write(str(efficiencyChanges['H_COP']) + '\n\n')
                f.write('Cooling COP\n')
                f.write(str(efficiencyChanges['C_COP']) + '\n\n')
                f.write('Lighting Load [W/m2]\n')
                f.write(str(efficiencyChanges['L_Load']) + '\n\n')
                f.write('Average PV Efficiency [%]\n')
                f.write(str(np.round(efficiencyChanges['PV']*monthlyData['efficiencies']['PV']*100, decimals = 1)) + '\n\n')
            else:
                f.write('Heating COP\n')
                f.write(str(monthlyData['efficiencies']['H_COP']) + '\n\n')
                f.write('Cooling COP\n')
                f.write(str(monthlyData['efficiencies']['C_COP']) + '\n\n')
                f.write('Lighting Load [W/m2]\n')
                f.write(str(monthlyData['efficiencies']['L_Load']) + '\n\n')
                f.write('Average PV Efficiency [%]\n')
                f.write(str(np.round(monthlyData['efficiencies']['PV']*100, decimals = 1)) + '\n\n')
            
            f.write('Net Energy Demand [kWh]\n')
            f.write(';optimized;fixed at 90 deg;fixed at 45 deg;fixed at 0 deg\n')
            f.write('Heating;'+str(TradeoffResults['energy_opttot']['H'])+';'+str(TradeoffResults['energy_90']['H'])+';'+str(TradeoffResults['energy_45']['H'])+';'+str(TradeoffResults['energy_0']['H']) +'\n')
            f.write('Cooling;'+str(TradeoffResults['energy_opttot']['C'])+';'+str(TradeoffResults['energy_90']['C'])+';'+str(TradeoffResults['energy_45']['C'])+';'+str(TradeoffResults['energy_0']['C'])+'\n')
            f.write('Lighting;'+str(TradeoffResults['energy_opttot']['L'])+';'+str(TradeoffResults['energy_90']['L'])+';'+str(TradeoffResults['energy_45']['L'])+';'+str(TradeoffResults['energy_0']['L'])+'\n')
            f.write('PV;'+str(TradeoffResults['energy_opttot']['PV'])+';'+str(TradeoffResults['energy_90']['PV'])+';'+str(TradeoffResults['energy_45']['PV'])+';'+str(TradeoffResults['energy_0']['PV'])+'\n')
            f.write('Total;'+str(TradeoffResults['energy_opttot']['E_tot'])+';'+str(TradeoffResults['energy_90']['E_tot'])+';'+str(TradeoffResults['energy_45']['E_tot'])+';'+str(TradeoffResults['energy_0']['E_tot'])+'\n')
    
            f.close()
    
    if auxVar['combineResults']:
        # bundle all results into one dictionary
        all_results = {'DIVA_results':DIVA_results, 'PV_detailed_results':PV_detailed_results, 
                       'PV_electricity_results':PV_electricity_results, 'SunTrackingData':SunTrackingData, 
                       'TradeoffResults':TradeoffResults, 'diva_folder':diva_folder, 'efficiencyChanges':efficiencyChanges,
                       'geoLocation':geoLocation, 'lbSettings':lbSettings, 'monthlyData':monthlyData, 
                       'radiation_folder':radiation_folder, 'tradeoffPeriod':tradeoffPeriod}
    else:
        # bundle all results into one dictionary
        all_results = {'DIVA_results':DIVA_results, 'PV_detailed_results':PV_detailed_results, 
                       'PV_electricity_results':PV_electricity_results, 'SunTrackingData':SunTrackingData, 
                       'diva_folder':diva_folder, 'efficiencyChanges':efficiencyChanges,
                       'geoLocation':geoLocation, 'lbSettings':lbSettings, 'monthlyData':monthlyData, 
                       'radiation_folder':radiation_folder}
    # save all results
    np.save(paths['results'] + '\\' + now + '\\all_results.npy', all_results)
    
print "simulation end: " + time.strftime("%Y_%m_%d %H.%M.%S", time.localtime())