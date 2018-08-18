# 
# Recolor pixels in an image.
#
# Author: Randy Heiland
#
from skimage.io import imread, imsave
import matplotlib.pyplot as plt
import numpy as np

img = imread('try1.png')
#img = imread('try2.png')

fig, axes = plt.subplots(ncols=2, figsize=(12, 6))
ax = axes.ravel()
ax[0].imshow(img)

print("img.size=",img.size)
print("img.shape=",img.shape)
print("avg R=",np.average(img[:,:,0]))
print("avg G=",np.average(img[:,:,1]))
print("avg B=",np.average(img[:,:,2]))

# Extract indices of pixels meeting RGB critera
#  (e.g., orange-ish parenchyma and white pixels)
p=np.where((img[:,:,0] > 210) & (img[:,:,1] < 150))
w=np.where((img[:,:,0] > 254) & (img[:,:,1] > 254) & (img[:,:,2] > 254))

# Color those pixels black
img[p[0],p[1],0:3] = 0

img[w[0],w[1],0:3] = 0

ax[1].imshow(img)
plt.show()
