import pynbody
import numpy as np
import sys
from ctypes import cdll, c_double, c_float, POINTER, CDLL, c_int, byref
import matplotlib.pyplot as plt



	
library_path = './Testf.so'
func = cdll.LoadLibrary(library_path)
# a =     np.array([[1,2,3], [4,5,6], [7,8,9], [10, 11, 12]], dtype='double')

# INPUT PARAMETERS
np.random.seed(200) ; POS = (np.random.random((200,3))).astype('double')
# a = np.array([[1,2,3], 
						 # [4,5,6], 
						 # [7,8,9], 
						 # [10, 11, 12]], dtype='double')
np.random.seed(200) ; aa = (np.random.random((200,3))*1).astype('double')
np.random.seed(200) ; aaa = (np.random.random((200))*1).astype('double')
np.random.seed(200) ; aaaa = (np.random.random((200))*1).astype('double')

# OUTPUT PARAMETERS
b = np.empty(shape=np.shape(POS), dtype='double') # empty 

# CREACIÓN DE LOS POINTERS
c_POS = POS.ctypes.data_as(POINTER(c_double))
# c_a = a.ctypes.data_as(POINTER(c_double))		
c_aa = aa.ctypes.data_as(POINTER(c_double))		
c_aaa = aa.ctypes.data_as(POINTER(c_double))		
c_aaaa = aa.ctypes.data_as(POINTER(c_double))		
c_b = b.ctypes.data_as(POINTER(c_double))		

# DIMENSIONES
rows, cols = 200, 3


# print(POS[0:10, 0:10])

# plt.scatter(POS[:,0], POS[:,1], s=1)
# plt.show()

# DECLARAMOS LOS TIPOS DE INPUT A FORTRAN
func.quantities.argtypes = [POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), c_int, c_int]
func.quantities.restype = None

# INGRESAMOS LOS PARAMETROS
func.quantities(c_POS, c_aa, c_aaa, c_aaaa, c_b, c_int(rows), c_int(cols))














# Fortran: Poner números aleatorios.
# Definir un radio X.
# Weight function: llamar la formúla de la esfera: (x -x_0)**2 + (y-y_0)**2 + (z-z_0)**2 = h**2
# La suma de los puntos dentro del loop es más pequeño que la condición ? 
	# Si: Entonces se multiplica por 1.1,
	# No: Entonces se multiplica por 0.9.
	# Cual sea la opción escogida, rehace el loop.

	# Input: centros y posiciones originales.
	# Restar las coordenadas de los centros a TODO,
	# Obtener el radio

	
	
	
	
	
	
		






