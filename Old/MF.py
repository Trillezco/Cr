import pynbody
import numpy as np
import matplotlib.pyplot as plt
import scipy as spy
from scipy.stats import gaussian_kde
import matplotlib as mpl
import Functions as F

# SNAP._array_name_ND_to_1D("Quantity in string here")

# Column Density + Magnetic Field
# 13/09 - 9AM
SNAP= pynbody.load('meh.hdf5')
SNAP.set_units_system(velocity = 'km s^-1', mass = 'Msol', temperature = 'K', distance = 'pc') 
# SS= SNAP[pynbody.filt.BandPass('z', "0.00 pc", "0.01 pc")]
# SSM = SS["MagneticField"]
# xmin, xmax, ymin,ymax = SS["x"].min(), SS["x"].max(), SS["y"].min(), SS["y"].max()
# xgrid, ygrid = np.linspace(xmin, xmax, 100), np.linspace(ymin, ymax, 100)
# x1, y1 = np.meshgrid(xgrid, ygrid)
# MGX, MGY = SSM[:,0].view(type=np.ndarray), SSM[:,1].view(type=np.ndarray)
# halfx, halfy = xgrid[2]-xgrid[1], ygrid[1]-ygrid[0]
# halfxx, halfyy = xgrid + halfx, ygrid + halfy


# Range, particles = F.MakeSlices(SNAP)


def SliceRunner(SimSnap, Slices, Runner):
	return SimSnap[pynbody.filt.BandPass('z', str(Slices[Runner][0])+" pc", str(Slices[Runner][1])+" pc")]	

def SliceQuantities(SimSnap, Slices):
	## si es 1D (mass) : a = np.empty(0,(len(SimSnap))) ; a = np.append(a, [snap[quantity]], axis=0) . La forma es de (len(SNAP), )
	## si es 3D (pos, magnetic field) : a = np.empty((0, 579780, 3)) ; a = np.append(Qty_Slices, [Mg], axis=0). La forma es de (len(SNAP, 3)) 
	Quantity = np.empty((0, len))
	for i in range(len(Slices)):
		g=SliceRunner(SimSnap, Slices, i)
		
		Slice = SNAP[pynbody.filt.BandPass('z', str(Slices[i][0])+" pc", str(Slices[i][1])+" pc")]	
		Quantity = SimArraytoNumpyArray(Slice, "MagneticField")
	return 
	
	
# snap= SNAP[pynbody.filt.BandPass('z', "0.00 pc", "0.01 pc")]
# mf = snap["MagneticField"]
# x, y = snap["x"].view(type=np.ndarray), snap["y"].view(type=np.ndarray)
# magx, magy = snap["MagneticField"][:,0].view(type=np.ndarray), snap["MagneticField"][:,1].view(type=np.ndarray)

# pynbody.plot.sph.velocity_image(SNAP, width= 0.2, cmap="Spectral_r", vector_qty="MagneticField", vector_resolution=10, mode="quiver", key_length="5 km s^-1", title="plot")
# plt.show()



##############################	1D
# Store Weights:
weight_cells = []
weight_cells2 = np.array([])


datos = np.random.random(50)*10
cellsv2=np.linspace(datos.min()-3, datos.max()+3, 30)
h = cellsv2[1] - cellsv2[0]
centersv2 = np.delete(cellsv2-h/2, 0) ; indexs = np.arange(len(centersv2))
# centerpos = cellsv2[0] +(indexs + 0.5)*h   #NO NUMPY: centerpos = cellsv2[0] +(index + 0.5)*h 
floating_point_index = (datos-cellsv2[0])/h -0.5  #NO NUMPY: floating_point_index = (datos[23]-cellsv2[0])/h -0.5
fraction =   np.abs(floating_point_index) - np.abs(np.floor(floating_point_index))




for i in range(len(cellsv2)):
	if i == 0:
		Where=np.where((cellsv2[i] < datos) & (datos <cellsv2[i+1])) # where=np.where(np.floor(floating_point_index) == 5) : más lento este
		weight_p = 1 - fraction[Where[0]] ; weight_pplusone = fraction[Where[0]]
	
	if i != 0:
		weight_cells2 = np.append(weight_cells2, weight_pplusone)
		continue
		
	if i == (len(cellsv2)-1):
		break


	Where=np.where((cellsv2[i] < datos) & (datos <cellsv2[i+1])) # where=np.where(np.floor(floating_point_index) == 5) : más lento este
	weight_p = 1 - fraction[Where[0]] ; weight_pplusone = fraction[Where[0]]
	print(weight_p)

	if i == 0:
		weight_cells = weight_cells.append(weight_p ) # weight_cells = np.append(weight_cells, weight_p )
		print(weight_cells)
		continue

		
	if i != 0:
		weight_cells2 = np.append(weight_cells2, weight_p)
		weight_cells = weight_cells.append(weight_cells2 )
		weight_cells2 = np.array([])
		continue
	




##############################	2D

xdatos = np.random.random(50)*10
ydatos = np.random.random(50)*10
xcellsv2=np.linspace(xdatos.min()-3, xdatos.max()+3, 30)
ycellsv2=np.linspace(ydatos.min()-3, ydatos.max()+3, 30)
h = xcellsv2[1] - xcellsv2[0]
xcentersv2 = np.delete(xcellsv2-h/2, 0) ; ycentersv2 = np.delete(ycellsv2-h/2, 0) ; indexs = np.arange(len(xcentersv2))
xfloating_point_index = (xdatos-xcellsv2[0])/h -0.5
yfloating_point_index = (ydatos-ycellsv2[0])/h -0.5
xfraction =   np.abs(xfloating_point_index) - np.abs(np.floor(xfloating_point_index))
yfraction =   np.abs(yfloating_point_index) - np.abs(np.floor(yfloating_point_index))

for i in range(len(xcentersv2 )):
	for ii in range(len(ycentersv2 )):
		xWhere=np.where((xcellsv2[i] < xdatos) & (xdatos < xcellsv2[i+1])) ; yWhere=np.where((ycellsv2[ii] < ydatos) & (ydatos < ycellsv2[i+1]))
		
		weight_pq = (1- xfraction[xWhere[0]] )*(1- yfraction[yWhere[0]])
		weight_pplusoneq = xfraction[xWhere[0]] *(1- yfraction[yWhere[0]])
		weight_pqplusone =  = (1- xfraction[xWhere[0]] )* yfraction[yWhere[0]]
		weight_plusoneqplusone =   = xfraction[xWhere[0]] *  yfraction[yWhere[0]]

		# pynbody:
			# B_x = Sim["MagneticField_x"][xWhere] 
			# B_y = Sim["MagneticField_y"][yWhere] 
			
		






		
# https://abaqus-docs.mit.edu/2017/English/SIMACAEANLRefMap/simaanl-c-euleriananalysis.htm#hj-top
		
		

