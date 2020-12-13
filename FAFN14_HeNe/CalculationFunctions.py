# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 23:12:07 2020
@author: Vidar Flodgren
Github: https://github.com/DeltaMod
"""
import numpy as np
from scipy.constants import c
n = 1
d = 0.4
R_1 = np.inf
R_2 = -1

def z012(d,R_1,R_2):
    #z_0 = np.sqrt( (-d*(R_1 + d)*(R_2 + d)*(R_1 +R_2+ d))/((R_2+R_1+2*d)**2) )
    z_0 = d/2 * np.sqrt( 2 * abs(R_2)/d - 1)
    z_1 = (-d*(R_2+d))/(R_2+R_1 +2*d)
    z_2 = z_1 + d
    return(z_0,z_1,z_2)

def dfreq(c,n,d):
    return(c/(2*n*d))

def Dupsilon(z_0,z_1,z_2,Dq,Dlm,ups):
    at_terms = np.arctan(z_2/z_0)-np.arctan(z_1/z_0)
    return(ups*(Dq+(1/np.pi)*(Dlm)*(at_terms)))
           

    

z = list(z012(d,R_1,R_2))  
print(z)  

dvups = dfreq(c,n,d)

Dups  = Dupsilon(z[0],z[1],z[2],0,2,dvups)

print(Dups/10**6)


lambd = 633*10**-9
n1 = 1
n2 = 1.5
def ResPow(lambd,n1,n2,d):
    mmax = 2*d/lambd
    
    R1 = (n1-n2)**2/(n1+n2)**2
    R2 = (n2-n1)**2/(n2+n1)**2
    
    r = np.sqrt(R1*R2)
    
    FIN  = np.pi*np.sqrt(abs(r))/(1-abs(r))  
    Rs = np.pi/2 *mmax* np.sqrt(FIN)
    return(Rs)

def ResPow2(lamb,d,**kwargs):
    if 'n1' in kwargs.keys():
        if 'n0' not in kwargs.keys():
            kwargs['n0'] = 1    
        n1 =  kwargs['n1']
        n0 = kwargs['n0']
        R     =  (n0-n1)**2/(n0+n1)**2
        r     =  R*R
    if 'r' in kwargs.keys():
        r = kwargs['r']
        
    F     =  ( np.pi*np.sqrt(abs(r))) / (1- np.sqrt(abs(r)))
    P_res =  np.pi/2 * 2*d/lambd * np.sqrt(F)
    return({'r':r,'F':F,'P_res':P_res})

P_res_a = ResPow2(lambd,10**-3,n0=1,n1=1.5)
print(P_res_a)
P_res_b = ResPow2(lambd,0.05,r=0.85)
print(P_res_b)
P = ResPow(lambd,n1,n2,10**-3)

print(P)

def LasingPow(I,Wp):
    return(I/Wp*10**-3)

def RCalc(d,g_1):
    return(1/(1/d - g_1/d))