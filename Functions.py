import pynbody
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
from matplotlib.colors import LogNorm
import glob
import natsort
import imageio


def SimArraytoNumpyArray(SimSnap, Quantity):
	return SimSnap[Quantity].view(type=np.ndarray)
	
def MakeSlices(SimSnap, Width=0.01, Particles=999):
	Multiply = 100 if (0.01 <= Width < 0.1) else 10 if (0.1 <= Width < 1) else 1 if (1 <= Width) else None
	dlength = Width*Multiply
	Z_min, Z_max = SimArraytoNumpyArray(SimSnap, "z").min(), SimArraytoNumpyArray(SimSnap,"z").max()
	Z_min = int(Z_min*Multiply) ; Z_max = int(Z_max*Multiply)
	Z_min = float(Z_min); Z_max = float(Z_max)
	particles = np.array([]) ; Range = np.empty((0,2))
	while (True):
		lower = Z_min
		upper = lower + dlength
		if lower > Z_max:
			break
		Slice= SimSnap[pynbody.filt.BandPass('z', str(lower/Multiply)+" pc", str(upper/Multiply)+" pc")]	
		particles = np.append(particles, len(Slice["x"])) ; Range = np.append(Range, [[lower/Multiply, upper/Multiply]], axis=0)
		Z_min += dlength

	masked=np.where(particles>Particles)
	Range = Range[masked] ; Amount_Particles = particles[masked] 
	return Range, Amount_Particles

def Compare2DHistogram(SimSnap, Array=np.array([[0,1]]), Qty="rho", Width=1, Units=None, Bins=100, Range=None, Title="plot", Cmap="Spectral_r", Savefig=None, Show=False, Density=None):
	for pair in range(len(array)):

		Slice= SimSnap[pynbody.filt.BandPass('z', str(Array[pair][0])+" pc", str(Array[pair][1])+" pc")]	
		XPos, YPos = SimArraytoNumpyArray(Slice, "x"), SimArraytoNumpyArray(Slice, "y")
		density, xedges, yedges = np.histogram2d(XPos, YPos, bins=Bins, range=Range)
		density = density if Density==False else (density/ 9.521e+36 * 1.989e+33) if Density == True else None
		Xgrid,Ygrid = np.meshgrid(xedges, yedges)
		
		fig, axes = plt.subplots(ncols=2, nrows=1, figsize=(21,8)) 
		i=pynbody.plot.image(Slice, qty=Qty, width= str(Width)+" pc", units=Units, cmap=Cmap, title=str(Title)+" (pynbody)", log=True, subplot=axes[1])
		mesh = axes[0].pcolormesh(Xgrid, Ygrid, density.T, norm=mpl.colors.LogNorm(), vmin=i.min(), vmax=i.max())
		fig.suptitle("Slice from "+str(Array[pair][0])+"[pc] "+"to "+str(Array[pair][1])+"[pc] "+"with "+str(len(Slice["x"]))+" particles", fontsize=16)
		axes[0].set_title(Title)	;	axes[0].set_xlabel('x/[pc]')	; 	axes[0].set_ylabel('y/x[pc]')	; 	axes[0].set_xlim(-Width/2, Width/2)	;	axes[0].set_ylim(-Width/2,Width/2)  
		colorbar = fig.colorbar(mesh, ax=axes[0])
		colorbar.set_label("["+str(Units+"]"))	
		plt.savefig(str(Savefig)+"/"+str(pair)+".png", dpi=150)  if Savefig != None else None
		plt.show() if Show != False else None
	return
	
def CompareKDE(SimSnap, Array, Qty="rho", Width=1, Units=None, Title="plot", Cmap="Spectral_r", Points=100, Density=False, Bandwidth=None, Savefig=None, Show=False):
	for pair in range(len(Array)):
		Slice= SimSnap[pynbody.filt.BandPass('z', str(Array[pair][0])+" pc", str(Array[pair][1])+" pc")]
		Mass = SimArraytoNumpyArray(Slice, "mass")  if Density == False else  SimArraytoNumpyArray(Slice, "mass")*1.989e+33 if Density == True else  None
		XPos, YPos= SimArraytoNumpyArray(Slice, "x"), SimArraytoNumpyArray(Slice, "y")
		Positions = np.vstack([XPos ,YPos])
		k = gaussian_kde(Positions, bw_method=Bandwidth, weights=Mass)
		ZPos = k(Positions)
		Xpoints = np.linspace(XPos .min(), XPos .max(), Points) ; Ypoints = np.linspace(YPos.min(), YPos.max(), Points)
		Xpoints, Ypoints = np.meshgrid(Xpoints, Ypoints)
		Gridpoints = np.array([Xpoints.ravel(), Ypoints.ravel()])
		Z = np.reshape(k(Gridpoints), Xpoints.shape)
		Z = Z if Density==False else (Z/ 9.521e+36 * 1.989e+33) if Density == True else None

		fig, axes = plt.subplots(ncols=2, nrows=1, figsize=(21,8)) 
		i=pynbody.plot.image(Slice, qty=Qty, width= str(Width)+" pc", units=Units, cmap=Cmap, title=str(Title)+" (pynbody)", log=True, subplot=axes[1])
		im = axes[0].imshow(Z, cmap=Cmap, origin="lower", interpolation="gaussian", extent=[Slice["x"].min(), Slice["x"].max(), Slice["y"].min(), Slice["y"].max()], vmin= i.min(), vmax=i.max(), norm=LogNorm())
		# axes[0].scatter(XPos, YPos, marker="*", color="black", s=1, alpha=0.8)	# Uncomment to see particles plotted.
		fig.suptitle("Slice from "+str(Array[pair][0])+"[pc] "+"to "+str(Array[pair][1])+"[pc] "+"with "+str(len(Slice["x"]))+" particles", fontsize=16)
		axes[0].set_title(Title)	;	axes[0].set_xlabel('x/[pc]')	; 	axes[0].set_ylabel('y/x[pc]')	; 	axes[0].set_xlim(-Width/2, Width/2)	;	axes[0].set_ylim(-Width/2,Width/2)  
		colorbar = fig.colorbar(im, ax=axes[0])
		colorbar.set_label("["+str(Units+"]"))
		plt.savefig(str(Savefig)+"/plot"+str(pair)+".png", dpi=150)  if Savefig != None else None
		plt.show() if Show != False else None
	return

def Animator(Root):
	plots = glob.glob(Root+"/**")
	plots = natsort.natsorted(plots)	;	List = []
	for Plot in plots:
		List.append(imageio.imread(Plot))
	imageio.mimsave("Animation.gif", List, fps=10, duration=0.2)
	return

	
	
