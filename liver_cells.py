import numpy as np  
import matplotlib.pyplot as plt
from math import sqrt, pi
from scipy.spatial import Voronoi, voronoi_plot_2d

'''
rf. ~/Documents/Paul/classes/2017_18/spring2018/group_project/Yafei_code/liver_drug_physicell/custom_modules/liver_setup.cpp
    // type 0 : tumor
    // type 1 : central vein (remove!)
    // type 2 : portal triad
    // type 3 : parenchyme


    // begin defining parenchyme
    parenchyme = cell_defaults;
    parenchyme.name = "liver parenchyme";
    parenchyme.type = 3;

    // update its phenotype

    // size information
    double radius = 15.0;


    portal_triad = parenchyme;
    portal_triad.name = "portal triad";
    portal_triad.type = 2;

    // update its phenotype

    // size information
    radius = 20.0;

    --------------
set_liver_parameters.m:parameters.lobule_radius = 400; 
set_liver_parameters.m:parameters.min_central_vein_spacing = 1.5 * parameters.lobule_radius; 
set_liver_parameters.m:parameters.central_vein_radius = 26.5; 
set_liver_parameters.m:parameters.portal_triad_radius = 23.0; 
set_liver_parameters.m:parameters.parenchyme_radius = 15; 
set_liver_parameters.m:parameters.tumor_cell_radius = 8.412710547954228; % based on phenotype PhysiCell
'''

xmin = 0.0 
xmax = 2000.0 
ymin = 0.0 
ymax = 2000.0 
cell_radius = 15.0
central_vein_radius = 26.5
portal_triad_radius = 20.  
lobule_radius = 400
print('cell_radius=',cell_radius)
cell_spacing = cell_radius * sqrt( (2*pi) / sqrt(3) )
print('cell_spacing=',cell_spacing)

# If all cells will be the same size (radius), let's calculate (approx) how many we'll have in a given 2D domain.
#num_cells = 
#xy = []

y = ymin
#ydel = 1.8 * cell_radius
ydel = sqrt(3.0)*cell_spacing/2.0 
#position(2) = position(2) + sqrt(3)*parameters.parenchyme_spacing/2.0; %  parameters.parenchyme_radius

# create an array containing centers of cells

x_offset = -cell_radius
num_cells_row = int((xmax - xmin) / (2*cell_radius))
print('num_cells_row = ',num_cells_row)
xpos_row0 = np.fromiter((2*cell_radius*x for x in range(num_cells_row)),float)
xpos = xpos_row0
#ypos0 = np.ones(num_cells_row) * ymin
#ypos = ypos0
ypos_row0 = np.ones(num_cells_row)*cell_radius*1.7
ypos = ypos_row0
#xpos_row2 = np.fromiter((2*cell_radius*x + x_offset for x in range(num_cells_row)),float)

#------------------------------------------------------
# create centers of hexagonally packed parenchyme cells; put in xpos,ypos arrays
row_num = 0
while (y < ymax):
    y += ydel
#    print(y)
    row_num += 1
    ypos = np.append(ypos, ypos_row0 + row_num*ydel)
#    print('ypos=',ypos)
    if (row_num % 2):
        xpos = np.append(xpos, xpos_row0 - cell_radius)
    else:
        xpos = np.append(xpos, xpos_row0)
#    print('xpos=',xpos)
    # orangey: 219,128,55

#  while (x < xmax):

# plot the parenchyme cells
fpout = open('liver.svg','w')
fpout.write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="-20 -20 2000 2000" version="1.1">\n')
for idx in range(len(xpos)):
    circ_str = '<circle cx="%f" cy="%f" r="%f" fill="rgb(219,128,55)" stroke="none"/>\n' % (xpos[idx],ypos[idx],cell_radius)
    fpout.write(circ_str)

#------------------------------------------------------
# determine location of central veins ("center" of lobules)
num_central_veins = 0
min_cv_dist = 1.5*lobule_radius*lobule_radius
max_cv = 20  # max central veins
cv = np.zeros((max_cv,2))
#offset = lobule_radius
offset = 100
try_count = 0
np.random.seed(13)  # results in 13 central veins -- unrelated to seed :-)
while (num_central_veins < max_cv):
    x = np.random.uniform(xmin+offset, xmax-offset)
    y = np.random.uniform(ymin+offset, ymax-offset)
#    print(x,y)
    try_count += 1
    if (try_count > 900):
        print('break out after too many tries')
        break
    if (num_central_veins == 0):
        cv[num_central_veins] = [x,y]
        num_central_veins += 1
        circ_str = '<circle cx="%f" cy="%f" r="%f" fill="rgb(20,20,20)" stroke="none"/>\n' % (x,y,central_vein_radius)
        fpout.write(circ_str)
#        continue
    else:  # check if new random point is > lobule_radius away from all others
        valid_point = True
        for idx in range(num_central_veins):
#            print('checking dist to ',cv[idx])
#            if x*cv[idx][0] + y*cv[idx][1] > lr2: 

            xdel = x-cv[idx][0]
            ydel = y-cv[idx][1]
            if (xdel*xdel + ydel*ydel < min_cv_dist): 
                valid_point = False
#                print('not valid')
                break
#            else:
#                print('valid')

        if (valid_point):
            cv[num_central_veins] = [x,y]
            num_central_veins += 1
#            print('new one:',cv)
            circ_str = '<circle cx="%f" cy="%f" r="%f" fill="rgb(20,20,20)" stroke="none"/>\n' % \
                (x,y,central_vein_radius)
            fpout.write(circ_str)

#------------------------------------------------------
# Compute Voronoi tesselation of central veins ("center" of lobules)
#   --> polygon vertices = portal triads
vor = Voronoi(cv[0:num_central_veins])
for v in vor.vertices:
    circ_str = '<circle cx="%f" cy="%f" r="%f" fill="rgb(255,0,0)" stroke="none"/>\n' % \
        (v[0],v[1],portal_triad_radius)
    fpout.write(circ_str)


fpout.write('</svg>\n')
fpout.close()

# For each central vein, remove all cells that intersect it
# cv[0:num_central_veins]


#plt.scatter(xpos,ypos, s=rvals*scale_radius, c=rgbs)
scale_radius = 450.0
scale_radius = 5.0
#fig = plt.figure()
#fig.set_figwidth(9)
#fig.set_figheight(7)
plt.scatter(xpos,ypos,s=scale_radius,c='orange')
plt.scatter(cv[0:num_central_veins][:,0], cv[0:num_central_veins][:,1], s=scale_radius*2.5,c='black')
plt.scatter(vor.vertices[:][:,0], vor.vertices[:][:,1], s=scale_radius*2.0,c='red')
plt.axes().set_aspect('equal')
plt.show()