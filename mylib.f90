module mylib
contains

	subroutine quantities(Positions, MagneticField, Mass, Rho, Out_MultiArray, Out_UniArray, Rows, Cols) bind(C, name='quantities')
	use iso_c_binding
	implicit none
    
	integer, intent(in), value :: Rows, Cols
	real(C_DOUBLE), intent(in) :: Positions(Cols, Rows), MagneticField(Cols, Rows), Mass(Rows), Rho(Rows)
	real(C_DOUBLE), intent(out) :: Out_MultiArray(Cols, Rows), Out_UniArray(Rows)
	integer :: i
    
	Out_UniArray = Mass !*10
	Out_MultiArray = MagneticField!*100
	return
	
!	do i=1, 100
!		print*, Out_MultiArray(2, i)
!	enddo

  end subroutine quantities
end module mylib
