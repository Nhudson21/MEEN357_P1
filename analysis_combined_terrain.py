from subfunctions import *
from define_rovers import *
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import root_scalar
from mpl_toolkits.mplot3d import Axes3D
rover, planet = define_rover_1()
slope_array_deg=np.linspace(-10,35,25)
omega_max=np.zeros((slope_array_deg.size),dtype=float)
omega_nl=rover['wheel_assembly']['motor']['speed_noload']
omega_st=np.linspace(0,omega_nl,25)
omega_bk=np.linspace(omega_nl,1,25)
# Step 1: Generate rolling resistance array
Crr_array = np.linspace(0.01, 0.4, 25)

# Step 3: Create matrices for independent variables
CRR, SLOPE = np.meshgrid(Crr_array, slope_array_deg)

# Step 4: Create a matrix to store rover speed data
VMAX = np.zeros(np.shape(CRR), dtype = float)
#Bisection method and function implementation
def myfun(x,place):
    x = F_gravity(slope_array_deg, rover, planet)[place]
    y = F_drive(omega_st, rover)[place]
    z = F_rolling(omega_st, slope_array_deg, rover, planet, Crr_array[place])[place]
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
# Step 5: Double loop to iterate through Crr and SLOPE matrices for max speed calcs
######## This the troublsome part, 1-4 and 6 should all be good
final = []
N = np.shape(CRR)[0]
N = CRR.shape[0]
for i in range(N):
    for j in range(N):
        Crr_sample = float(CRR[i, j])
        slope_sample = float(SLOPE[i, j])

        # Implement root-finding method
        bor = bisection(0, omega_bk[j], 0.00001, j) * float(rover['wheel_assembly']['wheel']['radius']) / get_gear_ratio(rover['wheel_assembly']['speed_reducer'])

        # Store the result in VMAX
        VMAX[i, j] = bor

# Step 6: Create a 3D surface plot
figure = plt.figure()
ax = Axes3D(figure, elev=30, azim=45)  # Adjust as needed to see graph
ax.plot_surface(CRR, SLOPE, VMAX)

# Add axis labels and a title
ax.set_xlabel('Coefficient of Rolling Resistance')
ax.set_ylabel('Terrain Slope (degrees)')
ax.set_zlabel('Rover Speed')
plt.title('Rover Speed vs. Rolling Resistance and Terrain Slope')

# Show the plot
plt.show()
