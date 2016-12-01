# -*- coding: utf-8 -*-
"""
Created on Tue Nov 01 16:05:31 2016

@author: Mauro

Methode 3: calculate equation which relates illuminance and irradiation.
"""




import os, sys
import numpy as np
import csv
import matplotlib.pyplot as plt


def IlluminanceFunction():
    
    #create plot if true
    Plot = False
    
    paths= {}
    
    # define path of weather file:
    paths['weather'] = 'C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\WeatherData\Zuerich_Kloten_2013.epw' #paths['epw_name']
    
    paths['main'] = os.path.abspath(os.path.dirname(sys.argv[0]))
    
    # define paths of subfolders:
    paths['data'] =os.path.join(paths['main'], 'data')
    paths['python'] = os.path.join(paths['main'], 'python')
    
    #paths['radiation_wall'] = os.path.join(paths['main'], 'radiation_wall_7_11')
    paths['radiation_wall'] = os.path.join(paths['main'], 'IlluminanceResults\\radiation_wall_ZH13_Illuminance')
    
    # add python_path to system path, so that all files are available:
    #sys.path.insert(0, paths['python'] + '\\aux_files')
    sys.path.insert(0, paths['python'])
    
    from epwreader import epw_reader
    #read epw file of needed destination
    weatherData = epw_reader(paths['weather'])
    
    
    roomFloorArea = 4900/1000.0 * 7000/1000.0 #[m^2] floor area
    DAY = 15
    y_angle = 0
    RadiationData = {}
    
    timeRange = range(5,19)
    
    for x_angle in [0,90]:
        RadiationData[x_angle]= {}
        
        for monthi in range(1,13):
            RadiationData[x_angle][monthi] = {}
            for HOD in  timeRange:
                RadiationData[x_angle][monthi][HOD] = {}        
         
                             
                BuildingRadiationData = np.array([])
                
                with open(os.path.join(paths['radiation_wall'], 'RadiationWall' + '_' + str(int(HOD)) +'_'+ str(DAY)+'_'+ str(monthi) + '_'+ str(x_angle) + '_' + str(y_angle) + '.csv'), 'r') as csvfile:
                   reader = csv.reader(csvfile)
                   for idx,line in enumerate(reader):
                       if idx == 1:
                           BuildingRadiationData = np.append(BuildingRadiationData, [float(line[0])])
                           break
                
                RadiationData[x_angle][monthi][HOD]= BuildingRadiationData[0] *1000   #Wh  
    
    
    
      
    glbRad = weatherData['glohorrad_Whm2']
    glbIll = weatherData['glohorillum_lux']
    #Measured data for plotting
    X=glbRad
    Y=glbIll
    
    #Aquire best fit vector of coefficients. 1st order
    Ill_Eq = np.polyfit(X,Y,1)
    
    print 'equation:', Ill_Eq
    
    Plot = False
    
    if Plot == True:
        x,y = [],[]
        
        x.append (weatherData['glohorrad_Whm2'])
        y.append (weatherData['glohorillum_lux'])
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(x,y,'o-')
        
        #plt.title('Zurich 2013')
        
        plt.xlabel('global horizontal Radiation [Wh/m2]', fontsize=12)
        plt.ylabel('global horizontal illuminance [lux]', fontsize=12)
        plt.tight_layout()
                
        save = True
    
        if save == True:
            path = r'C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\New_SimulationEnvironment\PlotMidTerm'
            fig.savefig(path + '\\IlluminanceFunction' + '.pdf')
            fig.savefig(path + '\\IlluminanceFunction' + '.png')
            print 'saved!'
    else:
        pass
    
    fenstIll = {}
    TransIll = {}
    
    glass_light_transmittance = 0.744 # visible light transmittance window
    
    y_angle = 0
   
       
    for x_angle in [0,90]:
        fenstIll[x_angle] = {}
        TransIll[x_angle] = {}
        
        for monthi in range(1,13):
            fenstIll[x_angle][monthi] = {}
            TransIll[x_angle][monthi] = {}
    
            for HOD in timeRange:
                fenstIll[x_angle][monthi][HOD] = {}
                TransIll[x_angle][monthi][HOD] = {}
            
                #Calculate Illuminance in the room. 
                fenstIll[x_angle][monthi][HOD] =RadiationData[x_angle][monthi][HOD]*Ill_Eq[0]/roomFloorArea #Lux.  Note that the constant has been ignored because it should be 0
                
                #Illuminance after transmitting through the window 
                Lighting_Utilisation_Factor=0.64
                
                TransIll[x_angle][monthi][HOD] = fenstIll[x_angle][monthi][HOD]*glass_light_transmittance * Lighting_Utilisation_Factor
    
        
    
    illuFun = {}
    for x_angle in [0,90]:
        z = []
        for monthi in range(1,13):
            for HOD in range(6,17):  
                z.append(TransIll[x_angle][monthi][HOD])
        
        z = np.array(z)
        
        illuFun[x_angle]= np.reshape(z,(12,11))

    paths['save_results_path'] = paths['main'] + '\IlluminanceResults\Data'    
    np.save(os.path.join(paths['save_results_path'],'IlluminanceFunctionRadiation.npy'), illuFun)
    np.save(os.path.join(paths['save_results_path'],'IlluminanceFunctionDict.npy'), TransIll)            
    np.save(os.path.join(paths['save_results_path'],'RadiationWindow.npy'), fenstIll)  
#        
    return illuFun, TransIll, RadiationData

illuFun, TransIll, RadiationData = IlluminanceFunction()
#
#IlluminanceFunction()
##print "test"



#from scipy.stats import linregress
#
#x1 = weatherData['glohorrad_Whm2'].as_matrix()
#y1 = weatherData['glohorillum_lux'].as_matrix()
#
#slope, intercept, r_value, p_value, std_err = linregress(x1,y1)