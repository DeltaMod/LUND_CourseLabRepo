# -*- coding: utf-8 -*-
"""
Created on Thu Dec 10 17:15:14 2020
@authors: Vidar and Isa
"""
import numpy as np
import matplotlib
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import cv2
from scipy import optimize
import os

C = 30*10**-6 #F  
V_pump = [5,23,4,23,25,26] #kV
rate = 10        #Hz
lasing_treshold = None #kv #J

def Func_E_Cap(C,V):
    E_cap  = C*np.power(V,2)/2
    return(E_cap)

E_Cap = Func_E_Cap(C,V_pump)

data = {'IR_NQ':{},'IR_Q':{},'532_Q':{}}

for key in data.keys():
    L = 0.52 #m
    Vfsr = 239*10**6 #Hz for no q=switching
    
    
    data[key] = {'V_pump' : np.array([]),
                 'E_cap'  : np.array([]),
                 'pow_avg': np.array([]),
                 'E_Pulse': np.array([]),
                 'eff'    : np.array([]),
                 'P_Peak' : np.array([]),
                 
                 't_FWHM' : np.array([]),
                 'C':30*10**-6,
                 'rate':10,
                 'duration': None,
                 'LT':None,
                 'f_prof':0.94}

M = {'Cu':   {'EV':4.73 * 10**6,'MD':8960}, #J/kg, and kg/m^3
     'Al':   {'EV':10.53* 10**6,'MD':2700},
     'Steel':{'EV':6.80 * 10**6,'MD':8050},
     'Fe':   {'EV':6.09 * 10**6,'MD':7874},
     'Brass':{'EV':4.73 * 10**6,'MD':8730}}

data['IR_NQ']['LT'] =  np.array([0.91*10**3])
data['IR_NQ']['V_pump'] = np.array([0.91,0.95,1.0,1.05,1.1,1.15, 1.2, 1.25, 1.3, 1.35, 1.4,1.45, 1.5  ]) *10**3 #V
data['IR_NQ']['pow_avg'] = np.array([8.1,73.4,181.5,340,480,680,885, 1130, 1380, 1630, 1880, 2175,2430 ])*10**-3 #W
data['IR_NQ']['t_FWHM'] = np.array([194.05])*10**-9

data['IR_Q']['LT'] =  np.array([0.94*10**3])
data['IR_Q']['V_pump']  = np.array([0.94,0.95,1.0,1.05,1.1,1.15, 1.2, 1.25, 1.3, 1.35, 1.4,1.45,1.5  ])   * 10**3 #V
data['IR_Q']['pow_avg'] = np.array([7.5, 95.6,298,522,728, 965, 1195,1478, 1701,1975,2204,2470, 2700   ]) * 10**-3
data['IR_Q']['t_FWHM'] = np.array([27.9])*10**-9 #s
data['IR_Q']['duration'] = np.array([ ])*10**-9 #s

data['532_Q']['LT'] =  np.array([0.91*10**3])
data['532_Q']['V_pump']  = np.array([1.2,1.5  ])*10**3
data['532_Q']['pow_avg'] = np.array([260 , 680 ])*10**-3
data['532_Q']['t_FWHM'] = np.array([ 17.25 ])*10**-9

#note: we get approx a 25% ratio between this q switching and the original, so the original should be reduced by about 25%
#if we measure the zero rystal, we got 2000 ish, which is aout 0.75% from 2700 MW 

#dye laser: from 1.2 kV, we get 9 mW, calculate efficiency
#The cell is rotated at the rewster angle, and as suvj, it selects only one polarisation to leave the cell.

def Func_PulseEnergy(Pow,Rep):
    E_pulse = Pow/Rep
    return(E_pulse)

def Func_PeakPow(f_prof, E_pul, t_FWHM ):
    P_p = f_prof*E_pul/t_FWHM
    
    return(P_p)

def Func_CapEnergy(Cap,Volt):
    E_cap = Cap*np.power(Volt,2)/2
    print(Cap)
    print(Volt)
    return(E_cap)
    
def Func_Efficiency(E_in,E_out):
    Eff = E_out/E_in
    return(Eff)

def Func_EToBurn(H,r_spot,d,rho):
    return(H*np.pi*r_spot**2*d*rho)


    
for key in data.keys():
    data[key]['E_Pulse'] = Func_PulseEnergy(data[key]['pow_avg'],data[key]['rate'])
    data[key]['P_Peak']  = Func_PeakPow(data[key]['f_prof'], data[key]['E_Pulse'],data[key]['t_FWHM'])
    data[key]['E_cap']   = Func_CapEnergy(data[key]['C'],data[key]['V_pump'])
    data[key]['eff']     = Func_Efficiency(data[key]['E_cap'],data[key]['E_Pulse']) #Check later
    


for key in data.keys():
    print(key+'\n==============')
    STRL = len(max(data['IR_NQ'].keys(),key=len))
    for subkey in data[key].keys():
        pad = [' ' for n in range(STRL-len(subkey))]
        
        print(subkey+"".join(pad)+str(data[key][subkey]))

E_burn = Func_EToBurn(M['Steel']['EV'],15.9*10**-6,0.001,M['Steel']['MD'])    


#Example of Figure Plotting
fig = plt.figure(1) # This ensures you can plot over the old figure
fig.clf()           # This clears the old figure

#2D plot
ax1 = fig.gca()
ax1.set_xlabel('$V_{pump}$ [V]')
ax1.set_ylabel('Efficiency')
ax1.plot(data['IR_NQ']['V_pump'],data['IR_NQ']['eff'],'xr',)
fig.tight_layout()
ax1.grid(True)

#Example of Figure Plotting

ax1.plot(data['IR_Q']['V_pump'],data['IR_Q']['eff'],'xb')
ax1.legend(['non Q-Switching','Q-Switching'])


fig = plt.figure(2) # This ensures you can plot over the old figure
fig.clf()           # This clears the old figure

#2D plot
ax2 = fig.gca()
ax2.set_xlabel('$V_{pump}$ [V]')
ax2.set_ylabel('Efficiency')
ax2.plot(data['IR_NQ']['V_pump'],data['IR_NQ']['eff'],'xr')
fig.tight_layout()
ax2.grid(True)

#Example of Figure Plotting
fig = plt.figure(3) # This ensures you can plot over the old figure
fig.clf()           # This clears the old figure

#2D plot
ax3 = fig.gca()
ax3.set_xlabel('$V_{pump}$ [V]')
ax3.set_ylabel('Efficiency')
ax3.plot(data['IR_Q']['V_pump'],data['IR_Q']['eff'],'xb')
fig.tight_layout()
ax3.grid(True)

def PrintTable(DATA):
    """
    Format of DATA:
        DATA = [['ColumnName',np.array(Data)],['ColumnName',np.array(Data)],...]
    """
    tnames = [d[0] for d in DATA]
    tab_headers  = " & ".join(tnames)+'\\\\'
    

    drows = [] 
    for n in range(len(DATA[0][1])):
        drows.append(" & ".join([str(round(d[1][n],5)) for d in DATA]))
    
    print(tab_headers)
    for row in drows:
        print(row+'\\\\')
        
#Table for No Q-Switching
print('\nTables\n===========')
print('\n\nno Q-Switching Data\n===========')
PrintTable([['$V_{Pump}$ [V]',data['IR_NQ']['V_pump']],
            ['Average Power [W]',data['IR_NQ']['pow_avg']],
            ['Pulse Energy [J]',data['IR_NQ']['E_Pulse']],
            ['Efficiency',data['IR_NQ']['eff']]])


#Table for  Q-Switching
print('\n\nQ-Switching Data\n===========')
PrintTable([['$V_{Pump}$ [V]',data['IR_Q']['V_pump']],
            ['Average Power [W]',data['IR_Q']['pow_avg']],
            ['Pulse Energy [J]',data['IR_Q']['E_Pulse']],
            ['Efficiency',data['IR_Q']['eff']]])

print('\n\Peak Powers\n===========')
print('\multicolumn{3}{c}{non Q-switched} & \multicolumn{3}{c}{Q-switched} \\\\')
PrintTable([['$E_{pulse}$ [J]',np.array([data['IR_NQ']['E_Pulse'][2]])],
            ['$t_{FWHM}$ [ns]',            data['IR_NQ']['t_FWHM']*1e+9],
            ['$P_{peak}$ [kW]',  np.array([data['IR_NQ']['P_Peak'][2]*1e-3])],
            ['$E_{pulse}$ [J]',np.array([data['IR_Q']['E_Pulse'][2]])],
            ['$t_{FWHM}$ [ns]',            data['IR_Q']['t_FWHM']*1e+9],
            ['$P_{Peak}$ [kW]',  np.array([data['IR_Q']['P_Peak'][2]*1e-3])]])


#List of LAB TASK Calculations: Literally just for reference later:
print('\n\nExercise Notes')
Ex = {}
Ex['2.1'] = {}
E = 50 #J 
C = 30e-6
Ex['2.1']['1_V'] = np.sqrt(2*E/C)
V_t = data['IR_NQ']['LT'][0]
Ex['2.1']['2_E'] = C*V_t**2/2

Ex['2.1']['2_1_V'] = np.sqrt(2*E/C)
V_t = data['IR_Q']['LT'][0]
Ex['2.1']['2_2_E'] = C*V_t**2/2

print(Ex['2.1'])


## Generating a gaussian 3d plot from the intensity map
Dirpath = os.listdir()
imgfile = [file for file in Dirpath if file.endswith('.png')][0]

fig = plt.figure(4)
fig.clf()
ax4 = fig.gca(projection='3d')

img = plt.imread(imgfile)
rez = 500
img = cv2.resize(img, (int(img.shape[0]*rez/100),int(img.shape[1]*rez/100)), interpolation = cv2.INTER_CUBIC)

img = cv2.bilateralFilter(img,9,75,75)

xm = img.shape[0]
ym = img.shape[1]
xl = [1700,xm-1350]
yl = [1650,ym-1500]
img = img[xl[0]:xl[1],yl[0]:yl[1]]

def set_3daxes_equal(ax):
    '''Make axes of 3D plot have equal scale so that spheres appear as spheres,
    cubes as cubes, etc..  This is one possible solution to Matplotlib's
    ax.set_aspect('equal') and ax.axis('equal') not working for 3D.

    Input
      ax: a matplotlib axis, e.g., as output from plt.gca().
    '''

    x_limits = ax.get_xlim3d()
    y_limits = ax.get_ylim3d()
    z_limits = ax.get_zlim3d()

    x_range = abs(x_limits[1] - x_limits[0])
    x_middle = np.mean(x_limits)
    y_range = abs(y_limits[1] - y_limits[0])
    y_middle = np.mean(y_limits)
    z_range = abs(z_limits[1] - z_limits[0])
    z_middle = np.mean(z_limits)

    # The plot bounding box is a sphere in the sense of the infinity
    # norm, hence I call half the max range the plot radius.
    plot_radius = 0.5*max([x_range, y_range, z_range])

    ax.set_xlim3d([x_middle - plot_radius, x_middle + plot_radius])
    ax.set_ylim3d([y_middle - plot_radius, y_middle + plot_radius])
    #ax.set_zlim3d([z_middle - plot_radius, z_middle + plot_radius])



ixx,iyy = np.mgrid[0:img.shape[0],0:img.shape[1]]
ax4.plot_surface(ixx,iyy, img,cmap='jet')
set_3daxes_equal(ax4)


fig = plt.figure(5)
fig.clf()


"""
Multiple Different Subplot Projection and sizes
"""
rows = 2; cols = 1
GAX = matplotlib.gridspec.GridSpec(rows,cols) #This makes a 3x2 sized grid 

ax4 = fig.add_subplot(GAX[0],projection='3d') # Makes a graph that covers a 2x2 size and has 3D projection
ax4.plot_surface(ixx,iyy, img,cmap='jet')
ax4.set_xlabel('x-pixels')
ax4.set_ylabel('y-pixels')
ax4.set_zlabel('pixel intensity')
ax5 = fig.add_subplot(GAX[1]) # Top right, small graph has 2D projection



ax5.plot(img[:,246],'-.')

def gaussian(x, mu, sig,AMP):
    return AMP*1./(np.sqrt(2.*np.pi)*sig)*np.exp(-np.power((x - mu)/sig, 2.)/2)

x  = np.arange(0,img[:,246].shape[0])
mu  =  240
sig =  50
AMP = 150

#How to do curve optimisations
dat = {}
g_par, g_covar= optimize.curve_fit(gaussian, x, img[:,246], p0=[240, 50,100])

g_space = np.linspace(0,max(x),200)

g_fit = gaussian(g_space,g_par[0],g_par[1],g_par[2])

ax5.plot(g_space,g_fit,'-')

ax5.legend(['Imaged Spot Intensity','Gaussian Fit'])
ax5.grid(True)
ax5.set_xlabel('Pixel number')
ax5.set_ylabel('Pixel Intensity')
fig.tight_layout()
#gaussfit = gaussian(x,mu,sig,AMP)


