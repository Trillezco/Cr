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
	
	
