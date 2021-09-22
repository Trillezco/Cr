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

		c_x = (c_double*len(snap['x'].view(np.ndarray)))(*snap['x'].view(np.ndarray))
		c_y = (c_double*len(snap['y'].view(np.ndarray)))(*snap['y'].view(np.ndarray))
		c_z = (c_double*len(snap['z'].view(np.ndarray)))(*snap['z'].view(np.ndarray))
		c_mfx = (c_double*len(snap['MagneticField_x'].view(np.ndarray)))(*snap['MagneticField_x'].view(np.ndarray))
		c_mfy = (c_double*len(snap['MagneticField_y'].view(np.ndarray)))(*snap['MagneticField_y'].view(np.ndarray))
		c_mfz = (c_double*len(snap['MagneticField_z'].view(np.ndarray)))(*snap['MagneticField_z'].view(np.ndarray))
		c_mass = (c_double*len(snap['mass'].view(np.ndarray)))(*snap['mass'].view(np.ndarray))
		c_rho = (c_double*len(snap['rho'].view(np.ndarray)))(*snap['rho'].view(np.ndarray))
		c_empty = (c_double*len(snap['rho'].view(np.ndarray)))(*snap['rho'].view(np.ndarray))
		
		self.library.quantities.argtypes = [POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), c_int, POINTER(c_double)]
		self.library.quantities.restype = None
		
		self.library.quantities(c_x, c_y, c_z, c_mfx, c_mfy, c_mfz, c_mass, c_rho, len(c_x), c_empty)

		# print("PYTHON\n")
		# for i in range(100):
			# print(c_mfx[i])
		















# solve chemistry from initial conditions
    # def do_something(self, var_array, var_double):

        # array size
        # var_int = len(var_array)

        # define library function INPUT types
        # self.library.do_something.argtypes = [POINTER(c_double), POINTER(c_double), POINTER(c_int)]

        # library function returns None as OUTPUT, since f90 subroutine
        # self.library.do_something.restype = None

        # convert array to c_double array
        # var_array_ctype = (c_double * var_int)(*var_array)  # pointer to double array

        # convert double argument to c_double
        # var_double_ctype = c_double(var_double)

        # convert integer to c_int
        # var_int_ctype = c_int(var_int)

        # do something
        # self.library.do_something(var_array_ctype, var_double_ctype, var_int_ctype)

        # return c_double results as list
        # return list(var_array_ctype)
