import os
import sys
import pynbody
import numpy as np
from ctypes import cdll, c_double, c_float, POINTER, CDLL, c_int, byref
from subprocess import call


# *********************
# this class 
class Interface:

    # ********************
    # class constructor, debug=True compile F90 in debug mode
	def __init__(self, debug=False):

        # compile library by just calling make with subprocess
		self.compile_library(debug)

        # where you want to put your library
		library_path = './mylib.so'

		# check if library exists
		if not os.path.exists(library_path):
			print("ERROR: library " + library_path + " not found, check for compilation errors!")
			sys.exit()

        # load f90 library compiled with fpic and shared
		self.library = cdll.LoadLibrary(library_path)

        # loaded message
		print("Library " + library_path + " loaded!")

    # *********************
    # not-so-elegant way of unlinking the library
    # from here
    # https://stackoverflow.com/questions/359498/how-can-i-unload-a-dll-using-ctypes-in-python
    #def __del__(self):
    #    def isLoaded(lib):
    #        libp = os.path.abspath(lib)
    #        ret = os.system("lsof -p %d | grep %s > /dev/null" % (os.getpid(), libp))
    #        return ret == 0
    #
    #    handle = self.library._handle
    #    name = self.library._name
    #    del self.library
    #    while isLoaded(name):
    #        libdl = CDLL("libdl.so")
    #        libdl.dlclose(handle)

    # *******************
    # compile library to obtain .so
	@staticmethod
	def compile_library(debug):
		print("Compiling f90 files...")
		if debug:
			call(["make", "clean"])
			call(["make", "debug"])
		else:
			call(["make"])

    # *********************
    # solve chemistry from initial conditions
	def extract_qties(self, filename):
		snap = pynbody.load(filename)
		snap.set_units_system(velocity = 'km s^-1', mass = 'Msol', temperature = 'K', distance = 'pc') 
		snap['rho'].convert_units('g cm**-3')
		snap['mass'].convert_units('g')
		
		#	Create POINTERs and give the corresponding types.
		pos = snap['pos'].view(dtype=np.ndarray)
		c_pos = pos.astype('double')
		c_pos = c_pos.ctypes.data_as(POINTER(c_double))		
		
		magne = snap['MagneticField'].view(dtype=np.ndarray)
		c_magne = magne.astype('double')
		c_magne = c_magne.ctypes.data_as(POINTER(c_double))	
		
		mass = snap['mass'].view(dtype=np.ndarray)
		c_mass = (c_double*len(mass) )(*mass)
		
		rho = snap['rho'].view(dtype=np.ndarray)
		c_rho = (c_double*len(rho) )(*rho)
		
		# Dimensions
		rows, cols = len(snap['mass']), 3
		
		#	Empty output array for python-fortran -> python result.
		c_empty_multidim = np.empty(shape=(rows,cols), dtype='double')
		c_empty_multidim = c_empty_multidim.ctypes.data_as(POINTER(c_double))	
		
		
		# call library
		self.library.quantities.argtypes = [POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), c_int, c_int]
		self.library.quantities.restype = None
		
		self.library.quantities(c_pos, c_magne, c_mass, c_rho, c_empty_multidim, c_int(rows), c_int(cols))
		
		# uni_subroutine = c_empty_unidim

		# from pointers to numpy data
		# uni_subroutine = np.ctypeslib.as_array(uni_subroutine, shape=(rows,))
		# multi_subroutine = np.ctypeslib.as_array(multi_subroutine, shape=(rows, cols))
		
		# print('Output array returned on python\n', uni_subroutine[0:10])
		# print(uni_subroutine[0,9]
		return
	
	
	def extract_qties_to_binary(self, filename):
		snap = pynbody.load(filename)
		snap.set_units_system(velocity = 'km s^-1', mass = 'Msol', temperature = 'K', distance = 'pc') 
		snap['rho'].convert_units('g cm**-3')
		snap['mass'].convert_units('g')
		
		# Convert to normal numpy array type
		pos = snap['pos'].view(dtype=np.ndarray)
		B = snap['MagneticField'].view(dtype=np.ndarray)
		mass = snap['mass'].view(dtype=np.ndarray)
		rho = snap['rho'].view(dtype=np.ndarray)
		
		# Dimension of arrays.
		row = len(pos)
		cols = 3
		
		# Pass to binary.
		indexs1D = np.array([4, row, 4]) 
		indexsKD = np.array([8, row, cols, 8])
		
		indexs1D_bin = st.pack('iii', *indexs1D)
		indexsKD_bin = st.pack('iiii', *indexsKD)
		
		with open('Dimension1D.bin', 'wb') as fdimen00:
			fdimen00.write(indexs1D_bin)

		with open('DimensionKD.bin', 'wb') as fdimen01:
			fdimen01.write(indexsKD_bin)
		
		# Snap's data to binary #
			# Positions 
		flatten_pos = pos.flatten('F')
		flatten_pos = np.insert(flatten_pos, 0, 12)
		flatten_pos = np.insert(flatten_pos, len(flatten_pos), 12)
		flatten_pos_bin = st.pack('f'*flatten_pos.size, *flatten_pos)
		
		with open('Positions.bin', 'wb') as Coords:
			Coords.write(flatten_pos_bin)
		
			# Magnetic Field
		flatten_B = B.flatten('F')
		flatten_B = np.insert(flatten_B, 0, 12)
		flatten_B = np.insert(flatten_B, len(flatten_B), 12)
		flatten_B_bin = st.pack('f'*flatten_B.size, *flatten_B)
		
		with open('B.bin', 'wb') as Magnetic:
			Magnetic.write(flatten_B_bin)
			
			# Mass
		flatten_mass = mass.flatten('F')
		flatten_mass = np.insert(flatten_mass, 0, 12)
		flatten_mass = np.insert(flatten_mass, len(flatten_mass), 12)
		flatten_mass_bin = st.pack('f'*flatten_mass.size, *flatten_mass)
		
		with open('Mass.bin', 'wb') as Masses:
			Masses.write(flatten_mass_bin)
			
			# Rho
		flatten_rho = rho.flatten('F')
		flatten_rho = np.insert(flatten_rho, 0, 12)
		flatten_rho = np.insert(flatten_rho, len(flatten_rho), 12)
		flatten_rho_bin = st.pack('f'*flatten_rho.size, *flatten_rho)

		with open('Rho.bin', 'wb') as Rho0:
			Rho0.write(flatten_rho_bin)
		
	
	
