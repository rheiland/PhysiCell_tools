import sys,pathlib
import math
import scipy.io
import matplotlib.pyplot as plt
#import matplotlib.colors as mplc



if (len(sys.argv) < 3):
  frame_idx = 0
  field_index = 4
else:
  kdx = 1
  frame_idx = int(sys.argv[kdx])
  kdx += 1
  field_index = int(sys.argv[kdx])

print('frame, field = ',frame_idx, field_index)

def plot_substrate(FileId):

    # select whichever substrate index you want, e.g., for one model:
    # 4=tumor cells field, 5=blood vessel density, 6=growth substrate
#    field_index = 4  
#    field_index = 5  

#     print('debug> plot_substrate: idx=',FileId)
    fname = "output%08d_microenvironment0.mat" % FileId
    output_dir_str = '.'
    fullname = output_dir_str + "/" + fname
    if not pathlib.Path(fullname).is_file():
        print("file not found",fullname)
        return

    info_dict = {}
    scipy.io.loadmat(fullname, info_dict)
    M = info_dict['multiscale_microenvironment']
#     global_field_index = int(mcds_field.value)
    print('plot_substrate: field_index=',field_index)
    f = M[field_index,:]   # 
    #plt.clf()
    #my_plot = plt.imshow(f.reshape(400,400), cmap='jet', extent=[0,20, 0,20])
    
#    fig = plt.figure(figsize=(7,7))
    fig = plt.figure(figsize=(7,5.8))

    N = int(math.sqrt(len(M[0,:])))
    grid2D = M[0,:].reshape(N,N)
    xvec = grid2D[0,:]
    #xvec.size
    #xvec.shape
    num_contours = 30
    num_contours = 10
#    my_plot = plt.contourf(xvec,xvec,M[field_index,:].reshape(100,100), num_contours, cmap='viridis') #'viridis'
    my_plot = plt.contourf(xvec,xvec,M[field_index,:].reshape(N,N), num_contours, cmap='viridis') #'viridis'
    plt.colorbar(my_plot)
    axes_min = 0
    axes_min = -2000
    axes_max = 2000
#    plt.xlim(axes_min,axes_max)
#    plt.ylim(axes_min,axes_max)
#     plt.title(fname)
#     ax.set_title(fname)
#    plt.axis('equal')
    plt.show()

plot_substrate(frame_idx)
