import define_rovers
import subfunctions
from define_rovers import *
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import root_scalar
import math
def myfun(x,si):
    rover, planet = define_rover_1()
    a = (math.sin(math.radians(si))) * subfunctions.get_mass(rover) * 3.72 * -1

    Ng = ((rover['wheel_assembly']['speed_reducer']['diam_gear'] )/ (rover['wheel_assembly']['speed_reducer']['diam_pinion'])) ** 2

    g = float(planet.get('g'))
    m = float(subfunctions.get_mass(rover))
    rad = float(rover['wheel_assembly']['wheel']['radius'])
    Crr=0.2
    v_rover = 2 * math.pi * rad * (x / Ng)
    b = (m * g * math.cos(math.radians(si))) * Crr * math.erf(40 * v_rover)

    y = (subfunctions.get_mass(rover) *float(planet.get('g')) * math.cos(math.radians(si))) * 0.2 * math.erf((40 * 2 * math.pi * float(rover['wheel_assembly']['wheel']['radius']) * x ))

    torque_stall = rover['wheel_assembly']['motor']['torque_stall']
    speed_noload = rover['wheel_assembly']['motor']['speed_noload']
    torque_noload = rover['wheel_assembly']['motor']['torque_noload']
    if x >= speed_noload:
        tau= 0.000000000000000000001
    elif x < 0:
        tau = torque_stall
    else:
        tau = (torque_stall - ((torque_stall - torque_noload) / speed_noload) * x)



    z=(tau/ float(rover['wheel_assembly']['wheel']['radius'])) * Ng * 6


    return a-b+z


rover, planet = define_rover_1()
Crr=0.2
slope_list_deg=np.linspace(-10,35,25)
omega_nl=rover['wheel_assembly']['motor']['speed_noload']
omega_st=np.linspace(0,omega_nl,25)
omega_bk=np.linspace(omega_nl,0.1,25)
x=subfunctions.F_gravity(slope_list_deg, rover, planet)
y=subfunctions.F_drive(omega_st, rover)
z=subfunctions.F_rolling(omega_st, slope_list_deg, rover, planet, Crr)
final=[]
for i in range(slope_list_deg.size):
    fun=lambda x:myfun(x,slope_list_deg[i])
    sol=root_scalar(fun,method='bisect',bracket=[0,omega_nl])
    x=sol.root/10
    final.append(x)
fig, (ax1) = plt.subplots(1)
ax1.plot(slope_list_deg,final,color='blue')
ax1.set_title('Graphs for analysis_terrain_slope')
ax1.set_xlabel('Terrain Angle [deg]')
ax1.set_ylabel('Max Rover speed [m/s]')
plt.show()








