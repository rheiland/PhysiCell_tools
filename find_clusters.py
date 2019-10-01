from pyMCDS import pyMCDS
import numpy as np
from sklearn.cluster import AffinityPropagation
from sklearn import metrics

#mcds = pyMCDS('output00000600.xml', '/Users/heiland/Documents/Paul/John/leader_follower_invasionSep2019/frozen')
#mcds = pyMCDS('output00000600.xml', '.')
fname = 'output00000600.xml'
fname = 'output00000014.xml'
print('reading ',fname)
mcds1 = pyMCDS(fname)

print(mcds1.get_time())
# print(mcds1.get_menv_species_list())
#print(mcds1.get_concentrations('quorum'))

cell_ids = mcds1.data['discrete_cells']['ID']
print(cell_ids.shape)
print(cell_ids[:4])

#cell_vec = np.zeros((cell_ids.shape, 3))
cell_vec = np.zeros((cell_ids.shape[0], 3))
vec_list = ['position_x', 'position_y', 'position_z']
for i, lab in enumerate(vec_list):
  cell_vec[:, i] = mcds1.data['discrete_cells'][lab]
#xvals = cell_vec[:, 0]
#print('x range: ',xvals.min(), xvals.max())
#yvals = cell_vec[:, 1]
#print('y range: ',yvals.min(), yvals.max())

#print(mcds1.get_cell_variables())

xy_pts = cell_vec[:,0:2]

# https://scikit-learn.org/stable/auto_examples/cluster/plot_affinity_propagation.html#sphx-glr-auto-examples-cluster-plot-affinity-propagation-py
#af = AffinityPropagation(preference=-50).fit(xy)
af = AffinityPropagation().fit(xy_pts)
cluster_centers_indices = af.cluster_centers_indices_
labels = af.labels_

n_clusters_ = len(cluster_centers_indices)

print('Estimated number of clusters: %d' % n_clusters_)
# print("Homogeneity: %0.3f" % metrics.homogeneity_score(labels_true, labels))
# print("Completeness: %0.3f" % metrics.completeness_score(labels_true, labels))
# print("V-measure: %0.3f" % metrics.v_measure_score(labels_true, labels))
# print("Adjusted Rand Index: %0.3f"
#       % metrics.adjusted_rand_score(labels_true, labels))
# print("Adjusted Mutual Information: %0.3f"
#       % metrics.adjusted_mutual_info_score(labels_true, labels,
#                                            average_method='arithmetic'))
print("Silhouette Coefficient: %0.3f"
      % metrics.silhouette_score(xy_pts, labels, metric='sqeuclidean'))

# #############################################################################
# Plot result
import matplotlib.pyplot as plt
from itertools import cycle

plt.close('all')
plt.figure(1)
plt.clf()

colors = cycle('bgrcmykbgrcmykbgrcmykbgrcmyk')
for k, col in zip(range(n_clusters_), colors):
    class_members = labels == k
    cluster_center = xy_pts[cluster_centers_indices[k]]
    plt.plot(xy_pts[class_members, 0], xy_pts[class_members, 1], col + '.')
    plt.plot(cluster_center[0], cluster_center[1], 'o', markerfacecolor=col,
             markeredgecolor='k', markersize=14)
    for x in xy_pts[class_members]:
        plt.plot([cluster_center[0], x[0]], [cluster_center[1], x[1]], col)

axes_min = -500.
axes_max = 500.
plt.xlim(axes_min, axes_max)
plt.ylim(axes_min, axes_max)
plt.axes().set_aspect('equal')
plt.title('Estimated number of clusters: %d' % n_clusters_)
plt.show()
