import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle


WIDTH, HEIGHT, DPI = 700, 700, 100 

def E(q, ro, x, y):
    # User must input a charge q that is radius ro[xo,yo] from point P(x,y)
    denominator = ((x-ro[0])**2 + (y-ro[1])**2)**1.5
    k = 8.99*(10**9)
    x_comp = (q * k * (x-ro[0])) / (denominator)
    y_comp = (q * k * (y-ro[1])) / (denominator)
    return x_comp, y_comp

# Creating grid
nx, ny = 128,128
x = np.linspace(-5,5,nx)
y = np.linspace(-5,5,ny)
X,Y = np.meshgrid(x,y)
    
# Model a capacitor via multipole arrangement of charges
nq, d = 20, 2
charges = []
for i in range(nq):
    charges.append((1, (i/(nq - 1)*2 - 1, -d/2))) # Establish charge and x,y coordinates for positive plate ; careful with brackets
    charges.append((-1, (i/(nq - 1)*2 - 1, d/2))) # Establish charge and x,y coordinates for negative plate
    
# Electric field vector where E = (Ex, Ey) are separate components
Ex, Ey = np.zeros((ny, nx)), np.zeros((ny,nx))
for charge in charges:

    ex, ey = E(*charge, x=X, y=Y) # Unpack each charge and distribute the x and y variables to their meshgrid equivalent
    Ex += ex
    Ey += ey
    
figure = plt.figure(figsize=(WIDTH/DPI, HEIGHT/DPI), facecolor='k')
ax = figure.add_subplot(facecolor='k')
figure.subplots_adjust(left=0, right=1, bottom=0, top=1)

# Plot streamlines
color = np.log2(np.sqrt(Ex**2 + Ey**2)) # create a variance in colours using the logarithm of the magnitude
ax.streamplot(x, y, Ex, Ey, color=color, linewidth=1, cmap=plt.cm.plasma, density=3, arrowstyle='fancy')

# Represent charges as circles
charge_colours = {True: '#aa0000', False: '#0000aa'} # colour-defining dictionary 
for charge, position in charges:
    ax.add_artist(Circle(position, 0.05, color=charge_colours[charge>0], zorder=10)) # set circles with position, radius, and colour
    # zorder is a prominence ranking - a higher zorder means it is placed above other artists
    
ax.set_xlabel('$x$') # Display x in LaTeX
ax.set_ylabel('$y$')
ax.set_xlim(-5,5)
ax.set_ylim(-5,5)
ax.set_aspect('equal')
plt.show()
