ImpKinPy is library for mechanics and astronomy

There is 2 modules in ImpKinPy - mechanics and astro_time. In mechanics there is 2 classes - Impulse_Energy and Gravity that inherits from Impulse_Energy.
How to install: Write "pip install impkinpy" in console log.

  Module mechanics
       |
class Impulse_Energy

impulse_k_energy: this function receives list of masses and list of velocity vectors of the bodies and returns impulse(m*v) vectors and kinetic energy(m*v**2/2) vectors of the bodies.

all_impulse_k_energy: this function receives list of impulse vectors and kinetic energy vectors of the bodies and returns impulse and kinetic energy of whole body sistem.

impulse: this function receives mass and scalar velocity of the body and returns impulse of the body.

mass_center: this function receives array of masses, array of coordinate vectors, array of velocity vectors and returns coordinate vector and velocity vector of mass center of the body system.

rotate_coords_2D: this function receives array of 2D coords and rotation angle and returns array of rotated 2D coords.

rotate_coords_3D: this function receives array of 3D coords, rotation angle and plane of rotation and returns array of rotated 3D coords.

rotate_coords_nD: this function receives array of nD coords, rotation angle and plane of rotation (array of coords numbers) and returns array of rotated nD coords.

Example of using the functions:

from ImpKinPy import mechanics as mcn
e = mcn.Impulse_Energy()
e.impulse_k_energy([0.2, 0.5], [[3, 2, 0], [3, 2, 0]])
e.all_impulse_k_energy([[0.6000000000000001, 0.4, 0.0], [1.5, 1.0, 0.0]], [(1.2999999999999998), (3.2499999999999996)])
e.mass_center([5, 2], [[0, 4, 10], [3, 5, 2]], [[2, 5, 8], [2, 5, 7]])
e.rotate_coords_2D([2, 5], 45)
e.rotate_coords_3D([2, 5, 7], 45, "XY")
e.rotate_coords_nD([2, 5, 7, 20, 13], 45, ["x4", "x1"]) 

  Module mechanics
       |
class Gravity(Impulse_Energy)

class Gravity reveives name of planet, moon or star and then his g (gravitational acceleration) is g on this planet.
for example:

e = Gravity("Earth")

Here is all the names of space objects you can to write and they gravitational acceleration:

"Mercury": 3.7, "Venus": 8.87, "Earth": 9.81, "Mars": 3.71, "Jupiter": 24.79, 
"Saturn": 10.44, "Uranus": 8.69, "Neptune": 11.15, "Pluto": 0.62, "Sun": 274.0,
"Io": 1.79, "Moon": 1.62, "Europa": 1.31, "Ganymede": 1.43, "Callisto": 1.24, 
"Enceladus": 0.113, "Titan": 1.35, "Rhea": 0.264, "Miranda": 0.079, "Ariel": 0.269,
"Triton": 0.779, "Charon": 0.288, "Amalthea": 0.020, "Himalia": 0.062, 
"Mimas": 0.064, "Tethys": 0.147, "Dione": 0.233, "Hyperion": 0.017, "Iapetus": 0.224,
"Phoebe": 0.042, "Umbriel": 0.2, "Titania": 0.38, "Oberon": 0.35, "Nereid": 0.003,
"Styx": 0.005, "Nix": 0.012, "Kerberos": 0.003, "Hydra": 0.008

functions:

def angle__v0x(self, v0, v0x):
    """
    Receives:
        v0 (float) – initial velocity magnitude
        v0x (float) – horizontal velocity component
    Returns:
        angle (float, radians) – angle of projection from v0x
    """
    return np.acos(v0x / v0)

def angle__v0y(self, v0, v0y):
    """
    Receives:
        v0 (float) – initial velocity magnitude
        v0y (float) – vertical velocity component
    Returns:
        angle (float, radians) – angle of projection from v0y
    """
    return np.asin(v0y / v0)

def v0__v0x_angle(self, v0x, angle_deg):
    """
    Receives:
        v0x (float) – horizontal component of velocity
        angle_deg (float) – angle in degrees
    Returns:
        v0 (float) – total initial velocity
    """
    angle_deg = np.radians(angle_deg)
    return v0x / np.cos(angle_deg)

def v0__v0y_angle(self, v0y, angle_deg):
    """
    Receives:
        v0y (float) – vertical component of velocity
        angle_deg (float) – angle in degrees
    Returns:
        v0 (float) – total initial velocity
    """
    angle_deg = np.radians(angle_deg)
    return v0y / np.sin(angle_deg)

def v0__L_angle(self, L, angle):
    """
    Receives:
        L (float) – horizontal range
        angle (float, radians) – launch angle
    Returns:
        v0 (float) – initial velocity needed for given range
    """
    return np.sqrt(L * self.g / np.sin(2 * angle))

def v0x__L_tfall(self, L, tfall):
    """
    Receives:
        L (float) – range
        tfall (float) – time of flight
    Returns:
        v0x (float) – horizontal velocity
    """
    return L / tfall

def v0x__xt_tfall(self, xt, tfall):
    """
    Receives:
        xt (float) – horizontal displacement at time t
        tfall (float) – time of flight
    Returns:
        v0x (float) – horizontal velocity
    """
    return xt / tfall

def v0x__v0_angle(self, v0, angle_deg):
    """
    Receives:
        v0 (float) – initial velocity
        angle_deg (float) – launch angle in degrees
    Returns:
        v0x (float) – horizontal velocity component
    """
    angle_deg = np.radians(angle_deg)
    return v0 * np.cos(angle_deg)

def v0y__tfall(self, tfall):
    """
    Receives:
        tfall (float) – time of flight
    Returns:
        v0y (float) – vertical velocity component (symmetric case)
    """
    return tfall * self.g / 2

def v0y__H(self, H):
    """
    Receives:
        H (float) – max height
    Returns:
        v0y (float) – initial vertical velocity
    """
    return np.sqrt(2 * self.g * H)

def v0y__vy_tfall(self, vy, tfall):
    """
    Receives:
        vy (float) – vertical velocity at time t
        tfall (float) – time of flight
    Returns:
        v0y (float) – initial vertical velocity
    """
    return vy + (self.g * tfall)

def v0y__yt_tfall(self, yt, tfall):
    """
    Receives:
        yt (float) – vertical displacement at time t
        tfall (float) – time of flight
    Returns:
        v0y (float) – initial vertical velocity
    """
    return (yt + 0.5 * self.g * tfall ** 2) / tfall

def v0y__v0_angle(self, v0, angle_deg):
    """
    Receives:
        v0 (float) – initial velocity
        angle_deg (float) – angle in degrees
    Returns:
        v0y (float) – vertical component of velocity
    """
    angle_deg = np.radians(angle_deg)
    return v0 * np.sin(angle_deg)

def H(self, v0y):
    """
    Receives:
        v0y (float) – vertical velocity component
    Returns:
        H (float) – maximum height reached
    """
    return v0y ** 2 / (2 * self.g)

def tfall__v0y(self, v0y):
    """
    Receives:
        v0y (float) – vertical velocity
    Returns:
        tfall (float) – total time of flight (symmetric)
    """
    return 2 * v0y / self.g

def tfall__L_v0x(self, L, v0x):
    """
    Receives:
        L (float) – horizontal range
        v0x (float) – horizontal velocity
    Returns:
        tfall (float) – time of flight
    """
    return L / v0x

def L__v0x_tfall(self, v0x, tfall):
    """
    Receives:
        v0x (float) – horizontal velocity
        tfall (float) – time of flight
    Returns:
        L (float) – horizontal distance
    """
    return v0x * tfall

def L__v0_angle(self, v0, angle_deg):
    """
    Receives:
        v0 (float) – initial velocity
        angle_deg (float) – launch angle in degrees
    Returns:
        L (float) – total horizontal range
    """
    angle_deg = np.radians(angle_deg)
    return v0 ** 2 / self.g * np.sin(2 * angle_deg)

def xt(self, v0x, tfall):
    """
    Receives:
        v0x (float) – horizontal velocity
        tfall (float) – time
    Returns:
        xt (float) – horizontal position at time t
    """
    return v0x * tfall

def yt(self, v0y, tfall):
    """
    Receives:
        v0y (float) – vertical velocity
        tfall (float) – time
    Returns:
        yt (float) – vertical position at time t
    """
    return v0y * tfall - self.g * tfall ** 2 / 2

def vx(self, v0x):
    """
    Receives:
        v0x (float) – horizontal velocity
    Returns:
        vx (float) – horizontal velocity at any time (constant)
    """
    return v0x

def vy(self, v0y, tfall):
    """
    Receives:
        v0y (float) – vertical initial velocity
        tfall (float) – time
    Returns:
        vy (float) – vertical velocity at time t
    """
    return v0y - (self.g * tfall)

trajectory_2_parameters: receives 2 parameters names and their values
height - trajectory max height
length - trajectory length
time - time of fall
angle - angle of throw
v0x - x component of start velocity vector
v0y - y component of start velocity vector
v0 - start velocity (scalar)

here is all the combinations of the parameters that the function can receive:
v0x, v0y
v0, angle
v0, height
height, length
time, angle
time, length
v0x, height
v0x, time

plot_trajectory: receives str of using the trajectory_2_parameters function and plots the trajectory. For example: "self.trajectory_2_parameters(Height=10, v0x=20)".

pendulum: this function receives shape of pendulum, pendulum axis position, mass, length, start angle and v0. 
If the shape is rectangle, write rectangle height and rectangle width. If the shape is annular plate, write inner radius and outer radius.
If pendulum axis is in distance d from the center, write distance d.
The function returns angles list, angle derivatives list, t of equal math pendulum, angle velocity of equal math pendulum and l of equal math pendulum.

nD_pendulum: this function receives shape - hypercube, hypersphere or symplex (nD cube, nD sphere or nD triangle), dimensions number, length of edge (if shape is hypercube or symplex)
or radius if shape is hypersphere, array of planes of rotation, array of start angles in this planes, array of start phases, mass density on meter^dimensions_number of the shape
and the particles number - number of particles into which the shape is divided for integration. The function returns list of periods, list of angle velocity,
list of inertia moments, mean period, mean angle velocity, mean moment of inertia, list of pendulum angles and list of rotation matrixes of the pendulum in different hyperplanes.

plot_pendulum: receives str of using the pendulum function and plots phase trajectory of pendulum for small angles and phase trajectory of pendulum for small angles with equal axes.

plot_nd_pendulum: receives str of using the nD_pendulum function, calculates pendulum angle derivatives in different hyperplanes with the function np.gradient and plots
phase trajectories of pendulum in different hyperplanes.

Example of using the functions:

g = mcn.Gravity("Earth")
g.trajectory_2_parameters(v0=10, angle=100)
g.pendulum("rod", "end", 100, 10, 45, 20, 5, 0, 0, 0, 0)
g.nD_pendulum("symplex", 5, 5, [["x1", "x2"], ["x3", "x2"]], [50, 20], [0, 0], 100, 1000)
g.plot_nD_pendulum('self.nD_pendulum("hypersphere", 5, 5, [["x1", "x2"], ["x3", "x2"]], [50, 20], [0, np.pi/2], 100, 1000)')
g.plot_trajectory("self.trajectory_2_parameters(Height=10, v0x=20)")
g.plot_pendulum('self.pendulum("rod", "end", 100, 10, 45, 20, 5, 0, 0, 0, 0)')

Module astro_time
       |
   class Time

JD: this function receives year, month, month day, hours, minutes, seconds and returns Julian date for this time.

day_number: this function receives month, day and if year leap or no and returns year day number for this month day.

GST_date_Earth: receives UTC year, UTC month, UTC month day, UTC hour, UTC minutes and UTC seconds and returns sidereal time on Greenvich meridian for this UTC time.

LST_date_Earth: receives longitude, UTC_year, UTC_month, UTC month_day, UTC hour, UTC minutes and UTC seconds and returns sidereal time on this longitude for this UTC time.

PTC_offset: receives True if planet is Mars and False if planet is not Mars (because usually on Mars start epoch is 6 january 2000 and for other planets it`s 1 january 2000),
start PJD, start Julian date and day on planet in Earth hours and returns offset - the number that we need to correct PTC (Planetary Time Coordinated) time in next function.
    |
Start PJD - the counter value (in seconds) that you want to set at the epoch start_JD  
Essentially, this is the reference point for counting seconds before or after the J2000.0 epoch  
You define how many seconds before or after the epoch have passed at the moment of start_PJD  
For example, if I want start_JD to be 2451540, I can specify that at this moment start_PJD is 0 (or any other number)

PTC_date: this function receives planet day length in seconds, offset, True if planet is Mars and False if not, UTC year, UTC month, UTC day, UTC hour, UTC minutes and UTC seconds
and returns time on "Greenvich" meridian of other planet (PTC) for this UTC time.

PTC_ST_date: this function receives planet day length in seconds, offset, True if planet is Mars and False if no, sidereal time at J2000.0 epoch on "Greenvich" meridian of the planet you want sidereal time for,
UTC year, UTC month, UTC month day, UTC hour, UTC minutes and UTC seconds and returns sidereal time on "Greenvich" meridian of this planet for this UTC time.

Example of using the functions:

from ImpKinPy import astro_time as ast
t = ast.Time()
t.JD(2025, 5, 24, 14, 28, 0)
t.day_number(5, 31, False)
t.GST_date_Earth(2025, 5, 24, 14, 28, 0)
t.LST_date_Earth(15, 2025, 5, 24, 14, 28, 0)
t.PTC_date(86400, 0, True, 2025, 5, 24, 14, 28, 0)
t.PTC_offset(True, 0, 2451540.0, 24.65)
t.PTC_ST_date(86400, 44795.9998, True, 12.0, 2025, 5, 24, 14, 28, 0)

Thank you for using ImpKinPy!


