#executable name
shared_object = mylib.so

#test if ifort is present, otherwise uses gfortran
wres = $(shell which ifort > /dev/null; echo $$?)
ifeq "$(wres)" "0"
	fc = ifort
	switchOPT = -O3 -xHost -unroll -g -pg -fPIC
	switchDBG = -O0 -check all -warn all -fPIC
	switchDBG += -fpe0 -u -traceback -warn nounused -g
	switchDBG += -init=snan,zero,arrays
else
	fc = gfortran
	switchOPT = -ffree-line-length-none -O3 -g -fPIC
	switchDBG = -fbacktrace -g -fPIC
	switchDBG += -ffpe-trap=zero,overflow,invalid
	switchDBG += -fbounds-check -ffree-line-length-none -O3
endif

#default switch
switch = $(switchOPT)

#objects
objs += mylib.o

#default target
all:	$(objs)
	$(fc) -shared $(objs) -o $(shared_object) $(switch) $(lib)

#full debug target
debug: switch = $(switchDBG)
debug: all

#clean target
clean:
	rm -f *.o *.mod *__genmod.f90 *~ $(shared_object)

.PHONY: clean

#rule for f90
%.o:%.f90
	$(fc) $(switch) -c $^ -o $@

