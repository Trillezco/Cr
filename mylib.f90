module mylib
contains

  subroutine quantities(x, y, z, mfx, mfy, mfz, mass, density, len_snap, output_array) bind(C, name='quantities')
    use iso_c_binding
    implicit none
    
    integer(C_INT), intent(in) :: len_snap
    real(C_DOUBLE), dimension(len_snap), intent(in) :: x, y, z, mfx, mfy, mfz, mass, density
    real(C_DOUBLE), dimension(len_snap), intent(out) :: output_array
	integer :: i

	do i=1, 100
		output_array(i) = mfx(i)
		print*, output_array(i)
	end do
		
  end subroutine quantities
end module mylib






