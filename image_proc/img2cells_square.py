# 
# Process a binary image: 
#   - generate code for PhysiCell to create cells at black pixels and Dirichlet nodes at white pixels
#
# Author: Randy Heiland
#
from skimage.io import imread, imsave
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, Ellipse, Rectangle
from matplotlib.collections import PatchCollection
from collections import deque

fig = plt.figure(figsize=(7,7))
ax = fig.gca()
#ax.set_aspect("equal")
#plt.ion()

count = -1
#while True:

#-----------------------------------------------------
def circles(x, y, s, c='b', vmin=None, vmax=None, **kwargs):
    """
    See https://gist.github.com/syrte/592a062c562cd2a98a83 

    Make a scatter plot of circles. 
    Similar to plt.scatter, but the size of circles are in data scale.
    Parameters
    ----------
    x, y : scalar or array_like, shape (n, )
        Input data
    s : scalar or array_like, shape (n, ) 
        Radius of circles.
    c : color or sequence of color, optional, default : 'b'
        `c` can be a single color format string, or a sequence of color
        specifications of length `N`, or a sequence of `N` numbers to be
        mapped to colors using the `cmap` and `norm` specified via kwargs.
        Note that `c` should not be a single numeric RGB or RGBA sequence 
        because that is indistinguishable from an array of values
        to be colormapped. (If you insist, use `color` instead.)  
        `c` can be a 2-D array in which the rows are RGB or RGBA, however. 
    vmin, vmax : scalar, optional, default: None
        `vmin` and `vmax` are used in conjunction with `norm` to normalize
        luminance data.  If either are `None`, the min and max of the
        color array is used.
    kwargs : `~matplotlib.collections.Collection` properties
        Eg. alpha, edgecolor(ec), facecolor(fc), linewidth(lw), linestyle(ls), 
        norm, cmap, transform, etc.
    Returns
    -------
    paths : `~matplotlib.collections.PathCollection`
    Examples
    --------
    a = np.arange(11)
    circles(a, a, s=a*0.2, c=a, alpha=0.5, ec='none')
    plt.colorbar()
    License
    --------
    This code is under [The BSD 3-Clause License]
    (http://opensource.org/licenses/BSD-3-Clause)
    """

    if np.isscalar(c):
        kwargs.setdefault('color', c)
        c = None

    if 'fc' in kwargs:
        kwargs.setdefault('facecolor', kwargs.pop('fc'))
    if 'ec' in kwargs:
        kwargs.setdefault('edgecolor', kwargs.pop('ec'))
    if 'ls' in kwargs:
        kwargs.setdefault('linestyle', kwargs.pop('ls'))
    if 'lw' in kwargs:
        kwargs.setdefault('linewidth', kwargs.pop('lw'))
    # You can set `facecolor` with an array for each patch,
    # while you can only set `facecolors` with a value for all.

    zipped = np.broadcast(x, y, s)
    patches = [Circle((x_, y_), s_)
               for x_, y_, s_ in zipped]
    collection = PatchCollection(patches, **kwargs)
    if c is not None:
        c = np.broadcast_to(c, zipped.shape).ravel()
        collection.set_array(c)
        collection.set_clim(vmin, vmax)

    #ax = plt.gca()
    ax.add_collection(collection)
    ax.autoscale_view()
    plt.draw_if_interactive()
    if c is not None:
        plt.sci(collection)
    return collection

#-------------------------------
img = imread('blob_annulus.png')

# fig, axes = plt.subplots(ncols=1, figsize=(12, 6))
#ax = axes.ravel()
#ax[0].imshow(img)
#fig, ax = plt.subplots()

print("img.size=",img.size)
print("img.shape=",img.shape)
# print("avg R=",np.average(img[:,:,0]))
# print("avg G=",np.average(img[:,:,1]))
# print("avg B=",np.average(img[:,:,2]))

# Extract indices of pixels meeting RGB critera
p = np.where((img[:,:,0] > 200) & (img[:,:,1] < 20))
#		if (img[idx,idy,0] > 200 and img[idx,idy,2] < 20):

# Color those pixels differently
# img[p[0],p[1],0:3] = 255
# img[p[0],p[1],1] = 0

# img.shape= (720, 960, 4)  NOTE: 1st index is Y(vertical) axis; 2nd index = X(horiz)
'''
for iy in range(450,455):
  for ix in range(540,545):
    img[iy,ix,0] = 0
    img[iy,ix,1] = 0
    img[iy,ix,2] = 0
'''

xmin = ymin = -1500.
xmax = ymax = 1500.
x_range = xmax - xmin
y_range = ymax - ymin
xdel = 20.
#x = y = np.arange(xmin, xmax, xdel)

xlist = deque()
ylist = deque()
rlist = deque()
rgb_list = deque()

#	cell_radius = cell_defaults.phenotype.geometry.radius; 
cell_radius = 8.412710547954228
cell_spacing = 0.95 * 2.0 * cell_radius; 
print("cell radius and spacing = ",cell_radius,cell_spacing)

yval = 0.0
num_cells = 0

img_xrange = img.shape[0]
img_yrange = img.shape[1]

# (x-xmin)/x_range = (idx-0)/img_xrange

fp = open('cells.dat','w')

# idx = img_xrange * (xval-xmin)/x_range 
# idy = img_yrange * (yval-ymin)/y_range 
#for ny in range(0,y_range):
ydel = cell_spacing * np.sqrt(3.0)/2.0
ny = 0
zval = 0.0
for yval in np.arange(ymin,ymax,ydel):
	idy = int(img_yrange * (yval-ymin)/y_range)
#	xval = 0.0
	xdel = 0.0
	if ny % 2:
#		xval = 0.5*cell_spacing
		xdel = 0.5*cell_spacing
	ny += 1
#	for nx in range(0,x_range):
#	for nx in range(0,x_range):
	for xval in np.arange(xmin+xdel,xmax+xdel,cell_spacing):
		idx = int(img_xrange * (xval-xmin)/x_range)
#		if ((img[idx,idy,0] > 200) and (img[idx,idy,2] > 200)):
		if ((img[idx,idy,0] < 20) and (img[idx,idy,1] < 20)):  # black
#		if ((img[idy,idx,0] < 20) and (img[idy,idx,1] < 20)):  # black
# 		if (img[idy,idx,0] > 200) and (img[idy,idx,2] > 200):
			xlist.append(yval)
			ylist.append(-xval)
			rlist.append(cell_radius)
			rgb = list(map(int, "90,90,90".split(","))) 
			rgb[:]=[x/255. for x in rgb]
			rgb_list.append(rgb)

			cell_type = 0
			cell_str = '%f %f %f %d\n' % (yval , -xval, zval, cell_type)
			fp.write(cell_str)
		elif ((img[idx,idy,0] > 200) and (img[idx,idy,1] < 20)):  # red
#		elif ((img[idy,idx,0] > 200) and (img[idy,idx,1] < 20)):  # red
# 		if (img[idy,idx,0] > 200) and (img[idy,idx,2] > 200):
			xlist.append(yval)
			ylist.append(-xval)
			rlist.append(cell_radius)
			rgb = list(map(int, "255,0,0".split(","))) 
			rgb[:]=[x/255. for x in rgb]
			rgb_list.append(rgb)

			cell_type = 1
			cell_str = '%f %f %f %d\n' % (yval , -xval, zval, cell_type)
			fp.write(cell_str)
	#		xval += cell_spacing
	#		if xval > 700.0:
	#			break
			num_cells += 1
#	yval += cell_spacing * np.sqrt(3.0)/2.0
#	if yval > 700.0:
#		break

fp.close()

xvals = np.array(xlist)
yvals = np.array(ylist)
rvals = np.array(rlist)
rgbs = np.array(rgb_list)

#  print('type(rgbs) = ',type(rgbs))
#  print('rgbs = ',rgbs)
#print("xvals[0:5]=",xvals[0:5])
#print("rvals[0:5]=",rvals[0:5])
#  print("rvals.min, max=",rvals.min(),rvals.max())

# plt.cla()
#   title_str += " (" + str(num_cells) + " agents)"
#   plt.title(title_str)
axes_min = xmin
axes_max = xmax
plt.xlim(axes_min,axes_max)
plt.ylim(axes_min,axes_max)
circles(xvals,yvals, s=rvals, color=rgbs, edgecolor='black')    # alpha=1.0, edgecolor='black'

'''
from heterogeneity.cpp:

void setup_tissue( void )
{
	// place a cluster of tumor cells at the center 
	
	double cell_radius = cell_defaults.phenotype.geometry.radius; 
	double cell_spacing = 0.95 * 2.0 * cell_radius; 
	
	double tumor_radius = parameters.doubles( "tumor_radius" ); // 250.0; 
	
	// Parameter<double> temp; 
	
	std::cout << parameters << std::endl; 
	int i = parameters.doubles.find_index( "tumor_radius" ); 
	
	Cell* pCell = NULL; 
	
	double x = 0.0; 
	double x_outer = tumor_radius; 
	double y = 0.0; 
	
	double p_mean = parameters.doubles( "oncoprotein_mean" ); 
	double p_sd = parameters.doubles( "oncoprotein_sd" ); 
	double p_min = parameters.doubles( "oncoprotein_min" ); 
	double p_max = parameters.doubles( "oncoprotein_max" ); 
	
	int n = 0; 
	while( y < tumor_radius )
	{
		x = 0.0; 
		if( n % 2 == 1 )
		{ x = 0.5*cell_spacing; }
		x_outer = sqrt( tumor_radius*tumor_radius - y*y ); 
		
		while( x < x_outer )
		{
			pCell = create_cell(); // tumor cell 
			pCell->assign_position( x , y , 0.0 );
			pCell->custom_data[0] = NormalRandom( p_mean, p_sd );
			if( pCell->custom_data[0] < p_min )
			{ pCell->custom_data[0] = p_min; }
			if( pCell->custom_data[0] > p_max )
			{ pCell->custom_data[0] = p_max; }
			
			if( fabs( y ) > 0.01 )
			{
				pCell = create_cell(); // tumor cell 
				pCell->assign_position( x , -y , 0.0 );
				pCell->custom_data[0] = NormalRandom( p_mean, p_sd );
				if( pCell->custom_data[0] < p_min )
				{ pCell->custom_data[0] = p_min; }
				if( pCell->custom_data[0] > p_max )
				{ pCell->custom_data[0] = p_max; }				
			}
			
			if( fabs( x ) > 0.01 )
			{ 
				pCell = create_cell(); // tumor cell 
				pCell->assign_position( -x , y , 0.0 );
				pCell->custom_data[0] = NormalRandom( p_mean, p_sd );
				if( pCell->custom_data[0] < p_min )
				{ pCell->custom_data[0] = p_min; }
				if( pCell->custom_data[0] > p_max )
				{ pCell->custom_data[0] = p_max; }
		
				if( fabs( y ) > 0.01 )
				{
					pCell = create_cell(); // tumor cell 
					pCell->assign_position( -x , -y , 0.0 );
					pCell->custom_data[0] = NormalRandom( p_mean, p_sd );
					if( pCell->custom_data[0] < p_min )
					{ pCell->custom_data[0] = p_min; }
					if( pCell->custom_data[0] > p_max )
					{ pCell->custom_data[0] = p_max; }
				}
			}
			x += cell_spacing; 
			
		}
		
		y += cell_spacing * sqrt(3.0)/2.0; 
		n++; 
	}
  '''

            # if num_cells > 3:   # for debugging
            #   print(fname,':  num_cells= ',num_cells," --- debug exit.")
            #   sys.exit(1)
            #   break

            # print(fname,':  num_cells= ',num_cells)



#ax.imshow(img)
plt.show()
