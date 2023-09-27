import subfunctions
from define_rovers import *
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import root_scalar
rover, planet = define_rover_1()
Crr=0.2
slope_list_deg=np.linspace(-10,35,25)
omega_max=np.zeros((slope_list_deg.size),dtype=float)
omega_nl=rover['wheel_assembly']['motor']['speed_noload']
omega_st=np.linspace(0,omega_nl,25)
omega_bk=np.linspace(omega_nl,1,25)
x=subfunctions.F_gravity(slope_list_deg, rover, planet)
y=subfunctions.F_drive(omega_st, rover)
z=subfunctions.F_rolling(omega_st, slope_list_deg, rover, planet, Crr)
a=x+y+z

import numpy as np
from scipy.optimize import root_scalar


import numpy as np
def myfun(x,place):
    x = subfunctions.F_gravity(slope_list_deg, rover, planet)[place]
    y = subfunctions.F_drive(omega_st, rover)[place]
    z = subfunctions.F_rolling(omega_st, slope_list_deg, rover, planet, Crr)[place]
    return x+y-z

def bisection(lb,xu,err_max,pl):
    big=[]
    turtle=[]
    iter_Max=10000
    root=(xu+lb)/2
    iter=0
    done=False
    while not done:
        iter+=1
        f_new=myfun(root,pl)
        if myfun(lb,pl)*f_new<0:
            xu=root
        else:
            lb=root
        error_est=abs(((xu-lb)/(xu+lb)))*100 # you a RuntimeWarning because I didn't code this for 0
        root=(xu+lb)/2
        if error_est < err_max:
            done = True
        if iter == iter_Max:
            done = True
        big.append(root)
        turtle.append(iter)
    return root

final=[]
for i in range(slope_list_deg.size):
    bor=bisection(0,omega_bk[i],0.00001,i)*float(rover['wheel_assembly']['wheel']['radius'])/subfunctions.get_gear_ratio(rover['wheel_assembly']['speed_reducer'])
    final.append(bor)

fig, (ax1) = plt.subplots(1)
ax1.plot(slope_list_deg,final,color='blue')
ax1.set_title('Graphs for analysis_terrain_slope')
ax1.set_xlabel('Terrain Angle [deg]')
ax1.set_ylabel('Max Rover speed [m/s]')
plt.show()
