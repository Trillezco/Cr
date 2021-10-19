module mylib
contains
	! Change the length of DOs on lines: 57 and 115 to increased/decreased spheres generated. (those DO HAVE TO match their length).
	! Change mineffectiveneigh and maxeffectiveneigh according to the range you need.
	subroutine quantities(Positions, MagneticField, Mass, Rho, Out_UniArray, Rows, Cols) bind(C, name='quantities') 
	use iso_c_binding
	implicit none
    
    ! Input arguments from PYTHON:
	integer, intent(in), value :: Rows, Cols							! For matrix.
	real(C_DOUBLE), intent(in) :: Positions(Cols , Rows)						! Positions of data [pc].
	real(C_DOUBLE), intent(in) :: MagneticField(Cols , Rows)					! [G].
	real(C_DOUBLE), intent(in) :: Mass(Rows)							! [kg].
	real(C_DOUBLE), intent(in) :: Rho(Rows)								! [g/cm**3].
	real(C_DOUBLE), intent(out) ::  Out_UniArray(Cols, Rows)					! CRIR.

	! Parameters within FORTRAN:
	real, allocatable, dimension(: , :) :: Points							! Random point generator for interpolator.
	real :: neighbour										! Weight.
	real :: effneighbour										! Effective Neighbor Number.
	real, allocatable, dimension(: , :) :: N_NGBr							! Matrix that store effective neighbour number and then it's radius needed.	
	real :: radius 											! Kernel Length.
	real :: mincoeff = 0.9										! Coefficient to decrease kernel length
	real :: maxcoeff = 1.1										! Coefficient to increase kernel length
	real :: mineffectiveneigh = 1.61e-13, maxeffectiveneigh = 1.01e-10				! Range that weigth value needs to have.
	real :: C_v = 4.188790										! Constant
	real :: weight											! Function that actually calculates the Weigth.
	integer :: i											! Other parameters.

	Out_UniArray = Positions
		
	! Creation of dynamic matrix. In purpose to store 2 column of data and Points position coordinates randomly generated: [ [x1, y1, z1], [x2, y2, z2], ...]
	allocate( N_NGBr(2, Rows) )
	allocate( Points(Cols , Rows) )	! Twice the amount of data points.
	call random_number(Points)
	
	! Initiliaze loop to calculate the Weight expresion.
	! First do-loop: calls weight function to calculate all neighbour values of every point random  generated.
	! Second do-loop: if neighbour value doesn't fulfill the condition, it falls inside this while-loop calling the
	!                                  weight function over and over again with increased/reduced kernel length until 
	!									condition is fulfill.
	! If-statements: depend on the case the neighbour value is above the condition's range or below it, 
	!						      whatever the if-statement it falls, it will increased/decreased the kernel length.
	! Pass the while-loop: it is calculated the effective neighbour number.
	! At the end of the whole do-loop block code, it stores the total effective neighbour number and then the radius needed for it on a Matrix.
	do i = 1 , 4000
		radius = 0.7
		neighbour = weight( Points(1:3 , i), Positions, Rho, radius, Cols, Rows )
				print*, 'el neighbour inicial es:', neighbour					! Comment this line if wanted. Just to check.
	
		do while ( neighbour <= mineffectiveneigh .OR. maxeffectiveneigh <= neighbour )
			if ( neighbour <= mineffectiveneigh ) then
				print*, 'previous radius', radius						! Comment this line if wanted. Just to check.
				radius = radius*maxcoeff
				print*, 'increased radius', radius						! Comment this line if wanted. Just to check.
				neighbour = weight( Points( 1:3 , i), Positions, Rho,radius, Cols, Rows )
				print*, 'neighbour increased is:', neighbour					! Comment this line if wanted. Just to check.
			end if
			
			if	( maxeffectiveneigh <= neighbour ) then
				print*, 'previous radius', radius						! Comment this line if wanted. Just to check.
				radius = radius*mincoeff
				print*, 'decreased radius', radius						! Comment this line if wanted. Just to check.
				neighbour = weight( Points( 1:3 , i), Positions, Rho, radius, Cols, Rows )
				print*, 'neighbour decreased is:', neighbour					! Comment this line if wanted. Just to check.
			end if		
		end do 
		
		effneighbour= ( C_v )*( radius**3 )*( neighbour )
		N_NGBr(1, i) = effneighbour
		N_NGBr(2, i) = radius
		
		print*, ' Tenemos que el neighbourhood efectivo es:', effneighbour				! Comment this line if wanted. Just to check.
		print*, '**************************************'						! Comment this line if wanted. Just to check.
	end do
	
!	print*, shape(N_NGBr(1,:))										! Comment this line if wanted. Just to check.
!	print*, shape(N_NGBr(2,:))										! Comment this line if wanted. Just to check.
	
	return

  end subroutine quantities
end module mylib


function weight(center, posi, rho, r, Cols, Rows)
	use iso_c_binding
	implicit none

	! Input arguments
		! |-> From PYTHON:
	integer, value, intent(in)  :: Cols, Rows				! Dimensions of matrix.
	real :: r 								! Kernel length.
	real(C_DOUBLE), intent(in)  :: posi(Cols,Rows)     			! Data position.
	real(C_DOUBLE), intent(in)  :: rho(Rows)     				! Density.
		! |-> From FORTRAN:
	real, intent(in) :: center(3)						! Position of random points generated.

	! Other variables within this function
	real :: norm								! Distance of data positions from and with respect randoms points as new origin.
	real :: displacement(Cols, Rows)					! New coordinates components with respect random points as new origin. 
	real :: weight								! Weight function.
	integer :: I								! Other parameters.
	
	
	! Moves every component position of data to the new O-axis which are the centers of those random points generated.
	displacement(1,:) = posi(1,:) - center(1)	
	displacement(2,:) = posi(2,:) - center(2)	
	displacement(3,:) = posi(3,:) - center(3)	

	! Calcule the distance of every point from the origin.
	displacement = displacement**2
	
	! Make the loop over every row suming positions components to get the distance,
	! then, pass every of them to one filter. If fulfill the condition do the IF block code.
	do I = 1 , 1000
		norm = sum(displacement(1:3,I))
		! If norm pass the if statement, then density that belongs to each particle passed is added.
		if (norm <= r) then
			weight = weight + rho(I)
		end if
	enddo
end function weight
