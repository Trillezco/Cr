import pynbody
import numpy as np
import matplotlib as mpl
import matplotlib.pylab as pylab
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
from matplotlib.colors import LogNorm
import mpl_scatter_density
import Functions as F

rut = "/home/gonzatrille/Escritorio/Universidad/Tesis/My Algorithm/kde/centimeter"

SNAP= pynbody.load('meh.hdf5')
SNAP.set_units_system(velocity = 'km s^-1', mass = 'Msol', temperature = 'K', distance = 'pc') 

Slice, particles = F.MakeSlices(SNAP, 0.01, 999)
# F.Compare2DHistogram(SNAP, Slice, Width=0.4, Units="Msol pc^-2", Bins=75, Range= [[0.0001,0.0001], [0.0001, 0.0001]], Title="Column Density")
F.CompareKDE(SNAP, Array=Slice, Width=0.4, Units="g cm^-2", Points=500, Density=True, Bandwidth=0.05, Savefig=rut, Show=False)




















# #histograma
# nbins = 300 #500 #680
# fig, axes = plt.subplots(ncols=2, nrows=1, figsize=(21,8)) 
# i=pynbody.plot.image(Test, qty='rho', width='0.4 pc', units='Msol pc**-2', av_z=False, cmap='Spectral_r', title='Column Density Pynbody', log=True, subplot=axes[1])#,vmin=57, vmax=1949)
# Title = 'Column Density Check'
# axes[0].set_title(Title)	

# g = axes[0].hist2d(array_x, array_y, bins=nbins,cmap='Spectral_r', norm=mpl.colors.LogNorm(), vmin=i.min(), vmax=i.max())
# colorbar = fig.colorbar(g[3], ax=axes[0])
# colorbar.set_label('[ $pc^{-2}$]')
# axes[0].set_xlabel('[pc]')
# axes[0].set_ylabel('[pc]')
# axes[0].set_xlim(-0.2, 0.2) 
# axes[0].set_ylim(-0.2,0.2)  
# plt.show()


#mpl_scatter
# norm = ImageNormalize(vmin=i.min(), vmax=i.max(), stretch=LogStretch())

# i=pynbody.plot.image(Test, qty='rho', width='0.4 pc', units='Msol pc**-2', av_z=False, cmap='Spectral_r', title='Column Density Pynbody', log=True)#,vmin=57, vmax=1949)
# fig = plt.figure()
# ax = fig.add_subplot(1,1,1, projection="scatter_density")
# density = ax.scatter_density(array_x, array_y, cmap="Spectral_r")
# fig.colorbar(density)
# ax.set_xlim(-0.2, 0.2)
# ax.set_ylim(-0.2, 0.2)
# plt.show()



#kde
# test_pos = np.vstack([array_x ,array_y ])
# k = gaussian_kde(test_pos)# ,bw_method="scott")
# z = k(test_pos)
# x = np.linspace(array_x .min(), array_x .max(), 500)
# y = np.linspace(array_y.min(), array_y.max(), 500)
# posxx, posyy = np.meshgrid(x,y)
# gridpoints = np.array([posxx.ravel(), posyy.ravel()])
# zz = np.reshape(k(gridpoints), posxx.shape)


# fig, axes = plt.subplots(ncols=2, nrows=1, figsize=(21,8)) 
# i=pynbody.plot.image(Test, qty='rho', width='0.4 pc', units='Msol pc**-2', cmap='Spectral_r', title='Column Density Pynbody', subplot=axes[1], log=False)

# im = axes[0].imshow(f, cmap="Spectral_r", origin="lower",  extent=[array_x.min(),array_x.max(), array_y.min(), array_y.max()]) # With LogNorm the image is all red.
# axes[0].set_title("Column Density without pynbody")
# axes[0].set_xlabel("x/[pc]")
# axes[0].set_ylabel("y/[pc]")
# axes[0].set_xlim(-0.5,0.5)
# axes[0].set_ylim(-0.5,0.5)

# colorbar = fig.colorbar(im, ax=axes[0])
# colorbar.set_label('[ $pc^{-2}$]')
# plt.show()
