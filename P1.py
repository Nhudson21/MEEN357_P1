#MEEN 357 502
#Alvaro Guerra
#Noah Hudson
#Brendan
#Phase 1
#What's our team number?????

import numpy as np
import math

#constants found in appendix
wheel_radius = 0.3 #m
wheel_mass = 1 #kg
tau_s = 170 #Nm , Motor Stall Torque
tau_nl = 0 #Nm, motor no-load torque
omega_nl = 3.80 #rad/s, Motor no-load speed
motor_mass = 5.0 #kg
payload_mass = 75 #kg, Combined mass of all scientific instruments
rtg_mass = 90 #kg, RTG --> supplies electric power for rover
chassis_mass = 659 #kg, mass of rover structure
p_dia = 0.04 #m, speed reducer pinion diameter
g_dia = 0.07 #m, speed reducer gear diamter
reduce_mass = 1.5 #kg, speed reducer mass
g_mars = 3.72 #m/s**2, gravity on mars

#input dictionaries
rover = {'wheel_assembly':{'wheel':{'radius':0.3, 'mass':1},
                           'speed_reducer':{'type':'reverted', 'diam_pinion': 0.04, 'diam_gear': 0.07, 'mass': 1.5 },
                           'motor':{'torque_stall':170, 'torque_noload':0, 'speed_noload':3.80, 'mass':5}},
         'chassis':{'mass':659},
         'science_payload':{'mass':75},
         'power_subsys':{'mass':90}}

speed_reducer = {'type':'reverted', 'diam_pinion': 0.04, 'diam_gear': 0.07, 'mass': 1.5 }

#omega = array of motor shaft speeds


#Part 1 Python Functions

#computer total mass of rover
def get_mass(rover):
    #a
    if type(rover) == dict:
        m = rover['chassis']['mass'] + rover['power_subsys']['mass']+ rover['science_payload']['mass'] + 6*rover['wheel_assembly']['wheel']['mass'] + 6*rover['wheel_assembly']['speed_reducer']['mass']+ 6*rover['wheel_assembly']['motor']['mass']
    else:
        raise Exception("Input argument is not dictionary type!")
    return m
    

m = get_mass(rover)
#print(m)
    
#returns speed reduction ratio based on speed_reducer dict
def get_gear_ratio(speed_reducer):
    if type(speed_reducer) != dict:
        raise Exception("Input argument is not dictionary type!")
    if speed_reducer['type'] != 'reverted':
        raise Exception("type field does not equal 'reverted' string")
    else:
        #Ng = (d2/d1)**2  ; d2 = diameter gear ; d1 = pinion diamter
        Ng = (speed_reducer['diam_gear']/speed_reducer['diam_pinion'])**2
    return Ng
    
Ng = get_gear_ratio(speed_reducer)
#print(Ng)

#returns magnitude of net force acting on rover in direction of translational motion
def F_net(omega, terrain_angle, rover, planet, Crr):
    #to be cont.
    
