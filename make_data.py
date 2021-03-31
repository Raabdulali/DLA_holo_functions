#Base imports
import holopy as hp
from holopy.scattering import Spheres,Sphere,calc_holo,Mie,calc_field
from holopy.core.io import save_image
from holopy.core.process import center_find, normalize
import random
import pandas as pd
import numpy as np






#helping functions
def rotation(x,y,z,angle,axis):
    x1=[]
    y1=[]
    z1=[]
    
    #rotation matrix
    if axis == 'x':
        for item in range(len(x)):
            x1.append (x[item]*np.cos(angle) - y[item]*np.sin(angle))
            y1.append (x[item]*np.sin(angle) + y[item]*np.cos(angle))
            z1.append (z[item])
    elif axis == 'y':
        for item in range(len(y)):
            x1.append (z[item]*np.sin(angle) + x[item]*np.cos(angle))
            y1.append (y[item])
            z1.append (z[item]*np.cos(angle) - x[item]*np.sin(angle))
    elif axis == 'z':
        for item in range(len(z)):
            x1.append (x[item])
            y1.append (y[item]*np.cos(angle) - z[item]*np.sin(angle))
            z1.append (y[item]*np.sin(angle) + z[item]*np.cos(angle))
    return x1, y1, z1


def scatter(x,y,z,particle_number, radius, detector, medium_index, illum_wavelen,
                     illum_polarization, theory=Mie):
    
    #create all spheres in object
    compiled = []
    for item in range(len(x)):
        compiled.append(Sphere(n=1.6, r=radius, center=(np.around(x[item],3), np.around(y[item],3), np.around(z[item],3))))
    collection = Spheres(compiled)


    #Actual field calculations
    field = calc_field(detector, collection, medium_index, illum_wavelen,
                     illum_polarization, theory=Mie)

    return field

def make_field(particle_number, angle_1, angle_2, radius, height):
    
    #Setting up medium, camera, and laser variables 
    shape = 200
    spacing = 0.048
    medium_index = 1.34
    illum_wavelen = 0.447
    illum_polarization = (1, 0)
    detector = hp.detector_grid(shape=shape, spacing=spacing)
    
    #read in data
    df = pd.read_csv('dla_463.csv')
    x = df['x'].tolist()
    y = df['y'].tolist()
    z = df['z'].tolist()
    
    #Clear non-essential items
    x = x[0:particle_number+1]
    y = y[0:particle_number+1]
    z = z[0:particle_number+1]
       
    #adjust distance between particles for particle size
    x = [item / (1/(2*radius)) for item in x]
    y = [item / (1/(2*radius)) for item in y]
    z = [item / (1/(2*radius)) for item in z]
    
    #rotate around x and then y axis
    x,y,z = rotation(x,y,z,angle_1,'x')
    x,y,z = rotation(x,y,z,angle_2,'y')
    
    #position agg 
    x = [(item+shape*spacing/2) for item in x]
    y = [(item+shape*spacing/2) for item in y]
    z = [(item+height) for item in z]
                        
    #scatter
    field = scatter(x,y,z,particle_number, radius, detector, medium_index, illum_wavelen,
                     illum_polarization, theory=Mie)
    return field




################ To run, unparenthesis the rest of the code #################


"""angle_1 = random.randint(1,360)
angle_2 = random.randint(1,360)        
field = make_field(particle_number = 10, angle_1=angle_1, angle_2=angle_2, radius = .1, height = 3)"""






