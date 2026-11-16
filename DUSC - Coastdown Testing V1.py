import numpy as np
import matplotlib.pyplot as plt

# User Inputs

m_car = 100 # kg
m_wheel = 4 # kg - one wheel
m_eff = m_car + 2*m_wheel # effective mass for rolling car

R = 287.058 # specific gas constant for air
p = 101325 # 1atm, roughly constant
T_celsius = 10 # MEASURE ON TRACK DAY
T = T_celsius + 273.15 # Conversion to Kelvin
rho = p / (R * T) # density relationship with temperature (for air)

A = 1 # m^2 for solar car
g = 9.81


# Finding C_rr, low speed test in both directions, can assume F_aero approx = 0
# We expect a linear relationship with v and t decreasing with gradient -C_rr * m_car * g / (m_eff)
# Plot v against t twice, extract gradient of curve, extract C_rr from gradient * (m_eff) / -m_car * g

# Will use weighted least squares regression - scipy optimise?

# VALIDATION - pass c_rr into the theoretical low speed model along with initial velocity

c_rr = 0.005 # calculated
v_0_slow = 20 # known from track test

def low_v_model(c_rr,m_car,g,t,m_eff,v_0_slow):
    
    v = -c_rr * m_car * g * t / m_eff + v_0_slow
    
    return v

t = np.linspace(0, 50, 100)
v = np.zeros(len(t))

for i in range(0, len(t)):
    velocity = low_v_model(c_rr,m_car,g,t[i],m_eff,v_0_slow)
    v[i] = velocity

plt.figure()
plt.plot(t, v)
plt.xlabel("Time (s)")
plt.ylabel("Velocity (m/s)")
plt.title("Low Velocity Test - Finding c_rr")
plt.show()


# Pass c_rr as a variable into our high speed coast down equation of motion

# High speed differential equation: dv/dt = Xv^2 + Y for the constants X and Y
# PLOT V AGAINST T, USE FINITE DIFFERENCE (or a better tool from a library) TO EXTRACT DV/DT, WE KNOW Y SO CAN FIND X - C_D!

c_d = 0.1 #guess
v_0_fast = 100 #guess

Y = -c_rr*m_car*g / m_eff # determined from low speed test

X = -rho*c_d*A / (2*m_eff) # seek to find X for c_d

# VALIDATION - pass c_rr and c_d into the theoretical high speed model along with initial velocity

def high_v_model(X,Y,t): # this is the analytic solution to the coastdown equations of motion
    
    v = np.sqrt(Y / X) * np.tan(np.arctan(v_0_fast * np.sqrt(X / Y)) - np.sqrt(X * Y) * t)
    
    return v

t = np.linspace(0, 50, 100)
v = np.zeros(len(t))

for i in range(0, len(t)):
    velocity = high_v_model(X,Y,t[i])
    v[i] = velocity

plt.figure()
plt.plot(t, v)
plt.xlabel("Time (s)")
plt.ylabel("Velocity (m/s)")
plt.title("High Velocity Test - Extract c_d")
plt.show()


# In[ ]:




