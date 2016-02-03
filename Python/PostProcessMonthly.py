# -*- coding: utf-8 -*-
"""
Created on Tue Feb 02 15:58:24 2016

average monthly data

@author: Jeremias
"""
import numpy as np

from average_monthly import average_monthly, daysPassedMonth
from PostProcessThermal_functions import pcolorMonths, pcolorEnergyMonths

importMonthlyRadiationFlag = True

daysPassedMonth=daysPassedMonth()

C_month = average_monthly(C,daysPassedMonth)
H_month = average_monthly(H,daysPassedMonth)
L_month = average_monthly(L,daysPassedMonth)
E_month = average_monthly(E,daysPassedMonth)

#import monthly radiation results:
if importMonthlyRadiationFlag == True:
    pass
    

    
 # Optimal x-angle combinations for every hour of the year
figcounter+=1
fig = plt.figure(num = figcounter, figsize=(16, 12))
plt.suptitle("Angle Distribution around x-axis", size=16)
p1 = plt.subplot(2,3,1)
pcolorMonths(H_month, 'x', x_angle_location, y_angle_location, allAngles)
plt.title("Heating Demand")
p1 = plt.subplot(2,3,2)
pcolorMonths(C_month, 'x', x_angle_location, y_angle_location, allAngles)
plt.title("Cooling Demand")
p1 = plt.subplot(2,3,3)
pcolorMonths(L_month, 'x', x_angle_location, y_angle_location, allAngles)
plt.title("Lighting Demand")
p1 = plt.subplot(2,3,4)
pcolorMonths(R_month, 'x', x_angle_location, y_angle_location, allAngles, 'max')
plt.title("PV Electricity Production")
p1 = plt.subplot(2,3,5)
pcolorMonths(E_month, 'x', x_angle_location, y_angle_location, allAngles)
plt.title("Total Thermal/Lighting Demand")
p1 = plt.subplot(2,3,6)
pcolorMonths(E_month_withPV, 'x', x_angle_location, y_angle_location, allAngles)
plt.title("Net Demand with PV")
fig.subplots_adjust(right=0.8)
cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
cbar = plt.colorbar(cax=cbar_ax, ticks=range(0,len(x_angles)))
cbar.ax.set_yticklabels(x_angles)
plt.show()   
    
    
 # Optimal y-angle combinations for every hour of the year
figcounter+=1
fig = plt.figure(num = figcounter, figsize=(16, 12))
plt.suptitle("Angle Distribution around y-axis", size=16)
p1 = plt.subplot(2,3,1)
pcolorMonths(H_month, 'y', x_angle_location, y_angle_location, allAngles)
plt.title("Heating Demand")
p1 = plt.subplot(2,3,2)
pcolorMonths(C_month, 'y', x_angle_location, y_angle_location, allAngles)
plt.title("Cooling Demand")
p1 = plt.subplot(2,3,3)
pcolorMonths(L_month, 'y', x_angle_location, y_angle_location, allAngles)
plt.title("Lighting Demand")
p1 = plt.subplot(2,3,4)
pcolorMonths(R_month, 'y', x_angle_location, y_angle_location, allAngles, 'max')
plt.title("PV Electricity Production")
p1 = plt.subplot(2,3,5)
pcolorMonths(E_month, 'y', x_angle_location, y_angle_location, allAngles)
plt.title("Total Thermal/lighting Demand")
p1 = plt.subplot(2,3,6)
pcolorMonths(E_month_withPV, 'y', x_angle_location, y_angle_location, allAngles)
plt.title("Net Demand with PV")
fig.subplots_adjust(right=0.8)
cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
cbar = plt.colorbar(cax=cbar_ax, ticks=range(0,len(y_angles)))
cbar.ax.set_yticklabels(y_angles)
plt.show()   

 # Optimal x- and y-angle combinations for every hour of the year
figcounter+=1
fig = plt.figure(num = figcounter, figsize=(16, 12))
plt.suptitle("Angle Distribution around x- and y-axis", size=16)
p1 = plt.subplot(2,3,1)
pcolorMonths(H_month, 'xy', x_angle_location, y_angle_location, allAngles)
plt.title("Heating Demand")
p1 = plt.subplot(2,3,2)
pcolorMonths(C_month, 'xy', x_angle_location, y_angle_location, allAngles)
plt.title("Cooling Demand")
p1 = plt.subplot(2,3,3)
pcolorMonths(L_month, 'xy', x_angle_location, y_angle_location, allAngles)
plt.title("Lighting Demand")
p1 = plt.subplot(2,3,4)
pcolorMonths(R_month, 'xy', x_angle_location, y_angle_location, allAngles, 'max')
plt.title("PV Electricity Production")
p1 = plt.subplot(2,3,5)
pcolorMonths(E_month, 'xy', x_angle_location, y_angle_location, allAngles)
plt.title("Total Thermal/lighting Demand")
p1 = plt.subplot(2,3,6)
pcolorMonths(E_month_withPV, 'xy', x_angle_location, y_angle_location, allAngles)
plt.title("Net Demand with PV")
fig.subplots_adjust(right=0.8)
cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
cbar = plt.colorbar(cax=cbar_ax, ticks=range(0,len(allAngles[0])))
cbar.ax.set_yticklabels(allAngles[0])
plt.show()   

 # Optimal x- and y-angle combinations for every hour of the year
figcounter+=1
fig = plt.figure(num = figcounter, figsize=(16, 12))
plt.suptitle("Angle Distribution around x-axis", size=16)
p1 = plt.subplot(1,6,1)
pcolorMonths(H_month, 'xy', x_angle_location, y_angle_location, allAngles)
plt.title("Heating Demand")
p1 = plt.subplot(1,6,2)
pcolorMonths(C_month, 'xy', x_angle_location, y_angle_location, allAngles)
plt.title("Cooling Demand")
p1 = plt.subplot(1,6,3)
pcolorMonths(L_month, 'xy', x_angle_location, y_angle_location, allAngles)
plt.title("Lighting Demand")
p1 = plt.subplot(1,6,4)
pcolorMonths(R_month, 'xy', x_angle_location, y_angle_location, allAngles, 'max')
plt.title("PV Electricity Production")
p1 = plt.subplot(1,6,5)
pcolorMonths(E_month, 'xy', x_angle_location, y_angle_location, allAngles)
plt.title("Total Thermal/lighting Demand")
p1 = plt.subplot(1,6,6)
pcolorMonths(E_month_withPV, 'xy', x_angle_location, y_angle_location, allAngles)
plt.title("Net Demand with PV")
fig.subplots_adjust(right=0.8)
cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
cbar = plt.colorbar(cax=cbar_ax, ticks=range(0,len(allAngles[0])))
cbar.ax.set_yticklabels(allAngles[0])
plt.show()   
#
## Optimal x-angle combinations for every hour of the year
#figcounter+=1
#fig = plt.figure(num = figcounter, figsize=(16, 12))
#plt.suptitle("Angle Distribution around x-axis", size=16)
#p1 = plt.subplot(2,2,1)
#pcolorMonths(H_month, 'x', x_angle_location, y_angle_location, allAngles)
#plt.title("Heating Demand")
#p1 = plt.subplot(2,2,2)
#pcolorMonths(C_month, 'x', x_angle_location, y_angle_location, allAngles)
#plt.title("Cooling Demand")
#p1 = plt.subplot(2,2,3)
#pcolorMonths(L_month, 'x', x_angle_location, y_angle_location, allAngles)
#plt.title("Lighting Demand")
#p1 = plt.subplot(2,2,4)
#pcolorMonths(E_month, 'x', x_angle_location, y_angle_location, allAngles)
#plt.title("Total Energy Demand")
#fig.subplots_adjust(right=0.8)
#cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
#cbar = plt.colorbar(cax=cbar_ax, ticks=range(0,len(x_angles)))
#cbar.ax.set_yticklabels(x_angles)
#plt.show()
#
## Optimal y-angle combinations for every hour of the year
#figcounter+=1
#fig = plt.figure(num = figcounter, figsize=(16, 12))
#plt.suptitle("Angle Distribution around y-axis", size=16)
#plt.subplot(2,2,1)
#pcolorMonths(H_month, 'y', x_angle_location, y_angle_location, allAngles)
#plt.title("Heating Demand")
#plt.subplot(2,2,2)
#pcolorMonths(C_month, 'y', x_angle_location, y_angle_location, allAngles)
#plt.title("Cooling Demand")
#plt.subplot(2,2,3)
#pcolorMonths(L_month, 'y', x_angle_location, y_angle_location, allAngles)
#plt.title("Lighting Demand")
#plt.subplot(2,2,4)
#pcolorMonths(E_month, 'y', x_angle_location, y_angle_location, allAngles)
#plt.title("Total Energy Demand")
#fig.subplots_adjust(right=0.8)
#cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
#cbar = plt.colorbar(cax=cbar_ax, ticks=range(0,len(y_angles)))
#cbar.ax.set_yticklabels(y_angles)
#plt.show()
#
#figcounter+=1
#fig = plt.figure(num = figcounter, figsize=(16, 12))
#plt.suptitle("Angle Distribution around x and y axis", size=16)
#p1 = plt.subplot(2,2,1)
#pcolorMonths(H_month, 'xy', x_angle_location, y_angle_location, allAngles)
#plt.title("Heating Demand")
#p1 = plt.subplot(2,2,2)
#pcolorMonths(C_month, 'xy', x_angle_location, y_angle_location, allAngles)
#plt.title("Cooling Demand")
#p1 = plt.subplot(2,2,3)
#pcolorMonths(L_month, 'xy', x_angle_location, y_angle_location, allAngles)
#plt.title("Lighting Demand")
#p1 = plt.subplot(2,2,4)
#pcolorMonths(E_month, 'xy', x_angle_location, y_angle_location, allAngles)
#plt.title("Total Energy Demand")
#fig.subplots_adjust(right=0.8)
#cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
#plt.title("(x-angle, y-angle)", fontsize=12, loc='left', verticalalignment = 'bottom')
#cbar = plt.colorbar(cax=cbar_ax, ticks=range(0,len(allAngles[0])))
#cbar.ax.set_yticklabels(allAngles[0])
#plt.show()

## Energy Use at opmtimum angle combination for the hole year:
#figcounter+=1
#fig = plt.figure(num = figcounter, figsize=(16, 12))
#plt.suptitle("Energy Use at optimum angle combination", size=16)
#plt.subplot(2,2,1)
#pcolorEnergyMonths(H_month)
#plt.title("Heating Demand")
#plt.subplot(2,2,2)
#pcolorEnergyMonths(C_month)
#plt.title("Cooling Demand")
#plt.subplot(2,2,3)
#pcolorEnergyMonths(L_month)
#plt.title("Lighting Demand")
#plt.subplot(2,2,4)
#pcolorEnergyMonths(E_month)
#plt.title("Total Energy Demand")
#fig.subplots_adjust(right=0.8)
#cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
#cbar = plt.colorbar(cax=cbar_ax, ticks=np.asarray(range(0,int(E_month.max()))))
#cbar.set_label('Power Use in kWh', rotation=270, labelpad=20)
#plt.show()

# Energy Use at opmtimum angle combination for the hole year:
figcounter+=1
fig = plt.figure(num = figcounter, figsize=(16, 12))
plt.suptitle("Energy Use at optimum angle combination", size=16)
plt.subplot(2,3,1)
pcolorEnergyMonths(H_month,'min')
plt.title("Heating Demand")
plt.subplot(2,3,2)
pcolorEnergyMonths(C_month,'min')
plt.title("Cooling Demand")
plt.subplot(2,3,3)
pcolorEnergyMonths(L_month,'min')
plt.title("Lighting Demand")
plt.subplot(2,3,4)
pcolorEnergyMonths(PV_month,'max')
plt.title("PV Production")
plt.subplot(2,3,5)
pcolorEnergyMonths(E_month,'min')
plt.title("Thermal/Lighting Demand")
plt.subplot(2,3,6)
pcolorEnergyMonths(E_month_withPV,'min')
plt.title("Net Energy Demand")
fig.subplots_adjust(right=0.8)
cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
#cbar = plt.colorbar(cax=cbar_ax, ticks=np.asarray(range(0,int(E_month.max()))))
cbar = plt.colorbar(cax=cbar_ax, ticks=np.asarray(range(0,30)))
cbar.set_label('Energy Use in kWh', rotation=270, labelpad=20)
plt.show()

# Energy Use at fixed angle combination for the hole year:
combination=12
figcounter+=1
fig = plt.figure(num = figcounter, figsize=(16, 12))
plt.suptitle("Energy Use at combination " + str(combination), size=16)
plt.subplot(2,3,1)
pcolorEnergyMonths(H_month,'min',combination)
plt.title("Heating Demand")
plt.subplot(2,3,2)
pcolorEnergyMonths(C_month,'min',combination)
plt.title("Cooling Demand")
plt.subplot(2,3,3)
pcolorEnergyMonths(L_month,'min',combination)
plt.title("Lighting Demand")
plt.subplot(2,3,4)
pcolorEnergyMonths(PV_month,'max',combination)
plt.title("PV Production")
plt.subplot(2,3,5)
pcolorEnergyMonths(E_month,'min',combination)
plt.title("Thermal/Lighting Demand")
plt.subplot(2,3,6)
pcolorEnergyMonths(E_month_withPV,'min',combination)
plt.title("Net Energy Demand")
fig.subplots_adjust(right=0.8)
cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
#cbar = plt.colorbar(cax=cbar_ax, ticks=np.asarray(range(0,int(E_month.max()))))
cbar = plt.colorbar(cax=cbar_ax, ticks=np.asarray(range(0,30)))
cbar.set_label('Energy Use in kWh', rotation=270, labelpad=20)
plt.show()

# Energy Use at fixed angle combination for the hole year:
combination=0
figcounter+=1
fig = plt.figure(num = figcounter, figsize=(16, 12))
plt.suptitle("Energy Use at combination " + str(combination), size=16)
plt.subplot(2,3,1)
pcolorEnergyMonths(H_month,'min',combination)
plt.title("Heating Demand")
plt.subplot(2,3,2)
pcolorEnergyMonths(C_month,'min',combination)
plt.title("Cooling Demand")
plt.subplot(2,3,3)
pcolorEnergyMonths(L_month,'min',combination)
plt.title("Lighting Demand")
plt.subplot(2,3,4)
pcolorEnergyMonths(PV_month,'max',combination)
plt.title("PV Production")
plt.subplot(2,3,5)
pcolorEnergyMonths(E_month,'min',combination)
plt.title("Thermal/Lighting Demand")
plt.subplot(2,3,6)
pcolorEnergyMonths(E_month_withPV,'min',combination)
plt.title("Net Energy Demand")
fig.subplots_adjust(right=0.8)
cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
#cbar = plt.colorbar(cax=cbar_ax, ticks=np.asarray(range(0,int(E_month.max()))))
cbar = plt.colorbar(cax=cbar_ax, ticks=np.asarray(range(0,30)))
cbar.set_label('Energy Use in kWh', rotation=270, labelpad=20)
plt.show()