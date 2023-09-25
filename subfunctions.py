def get_mass(rover):
    #a
    if type(rover) == dict:
        m = rover['chassis']['mass'] + rover['power_subsys']['mass']+ rover['science_payload']['mass'] + 6*rover['wheel_assembly']['wheel']['mass'] + 6*rover['wheel_assembly']['speed_reducer']['mass']+ 6*rover['wheel_assembly']['motor']['mass']
    else:
        raise Exception("Input argument is not dictionary type!")
    return m
# returns speed reduction ratio based on speed_reducer dict
def get_gear_ratio(speed_reducer):
    if type(speed_reducer) != dict:
        raise Exception("Input argument is not dictionary type!")
    if speed_reducer['type'] != 'reverted':
        raise Exception("type field does not equal 'reverted' string")
    else:
        # Ng = (d2/d1)**2  ; d2 = diameter gear ; d1 = pinion diamter
        Ng = (speed_reducer['diam_gear'] / speed_reducer['diam_pinion']) ** 2
    return Ng


# print(Ng)


# to be cont.

# computes rolling ressitance in newtons acting in the direction of translation
def F_rolling(omega, terrain_angle, rover, planet, Crr):
    import numpy as np
    import math
    if (type(omega) != type(terrain_angle)) and np.iscalar(omega) and isinstance(omega, np.ndarray):
        raise Exception("Sorry, omega and terrain_angle must be a vector or scalar of the same type")

    if len(omega) != len(terrain_angle):
        raise Exception("Sorry omega and terrain_angle must be the same size")
    if np.any((terrain_angle < -75) | (terrain_angle > 75)):
        raise Exception(
            "Sorry all values of terrain_angle must be greater than or equal to -75 and less than or equal to 75")
    if type(rover) != dict or type(planet) != dict:
        raise Exception("Sorry both rover and planet must be a dict")
    if np.isscalar(Crr) == False and Crr <= 0:
        raise Exception("Sorry crr must be both scalar and posistive")
    frr=[]
# gets the value for g from the planet dict
    g = float(planet.get('g'))
# gets the gear ratio and mass of the rover
    m = float(get_mass(rover))
    Ng = get_gear_ratio(rover['wheel_assembly']['speed_reducer'])
    rad = float(rover['wheel_assembly']['wheel']['radius'])
# calculates the velocity of the rover
    v_rover = 2 * math.pi * rad * (omega / Ng)
# calculates the simplified vlaue for rolling resistance
    for x in range((v_rover.size)):
       b= (m * g * math.cos(math.radians(terrain_angle[x]))) * Crr*math.erf(40 *v_rover[x])
       frr.append(b)
    Frr=np.array(frr)
    return Frr

def F_gravity(terrain_angle, rover, planet):
    import numpy as np
    import math
    final=[]
    if isinstance(rover, dict) == False:
        raise Exception("Data structure specifying rover parameters in not in correct form")
    if isinstance(planet, dict) == False:
        raise Exception("Data structure specifying planet parameters in not in correct form")
    if any(terrain_angle) / 75 < -1 or any(terrain_angle) / 75 > 1:
        raise Exception("The some angles may be too large")
    mass = get_mass(rover)
    gravity = float(planet['g'])
    for i in terrain_angle:
        x=(math.sin(math.radians(i)))
        y=mass * gravity* x*-1
        final.append(y)
    Nam=np.array(final)
    return Nam
def tau_dcmotor(omega, motor):
    import numpy as np
    if isinstance(omega, (int, float, str)) and isinstance(omega, np.ndarray):
        raise Exception("Array of motor shaft speed is not in the correct form")
    if not isinstance(motor, dict):
        raise Exception("Data structure specifying rover parameters is not in the correct form")

    # Get values from the motor dict and convert to variables with the same name
    torque_stall = float(motor.get('torque_stall'))
    speed_noload = float(motor.get('speed_noload'))
    torque_noload = float(motor.get('torque_noload'))
    omega = omega.tolist()
    tau = np.array([])

    for i in range(len(omega)):
        if omega[i] >= speed_noload:
            tau = np.append(tau, [0])
        elif omega[i] < 0:
            tau = np.append(tau, [torque_stall])
        else:
            tau = np.append(tau, [torque_stall - ((torque_stall - torque_noload) / speed_noload) * omega[i]])
    return tau

def F_drive(omega, rover):
    import numpy as np
    if isinstance(omega, (int, float, str)) and isinstance(omega, np.ndarray):
        raise Exception("Array of motor shaft speed in not in correct form")
    if isinstance(rover, dict) == False:
        raise Exception("Data structure specifying rover parameters in not in correct form")
    rad = float(rover['wheel_assembly']['wheel']['radius'])
    tor_b = tau_dcmotor(omega, rover['wheel_assembly']['motor'])
    Gear_rat = get_gear_ratio(rover['wheel_assembly']['speed_reducer'])
    Fd = (tor_b / rad)*Gear_rat*6
    return Fd


def F_net(omega, terrain_angle, rover, planet, Crr):
    import numpy as np
    if (type(omega) != type(terrain_angle)) and np.iscalar(omega) and isinstance(omega, np.ndarray):
        raise Exception("Sorry, omega and terrain_angle must be a vector or scalar of the same type")

    if len(omega) != len(terrain_angle):
        raise Exception("Sorry omega and terrain_angle must be the same size")
    if np.any((terrain_angle < -75) | (terrain_angle > 75)):
        raise Exception(
            "Sorry all values of terrain_angle must be greater than or equal to -75 and less than or equal to 75")
    if type(rover) != dict or type(planet) != dict:
        raise Exception("Sorry both rover and planet must be a dict")
    if np.isscalar(Crr) == False and Crr <= 0:
        raise Exception("Sorry crr must be both scalar and posistive")
    else:
        # Fnet = Fgrav + Frr - Fd
        big= []
        grav=F_gravity(terrain_angle, rover, planet)
        roll=F_rolling(omega, terrain_angle, rover, planet,Crr)
        drive=F_drive(omega, rover)
        for x in range(grav.size):
            a=grav[x] -(roll[x])+ drive[x]
            big.append(a)
        net = np.array(big)
        return net
