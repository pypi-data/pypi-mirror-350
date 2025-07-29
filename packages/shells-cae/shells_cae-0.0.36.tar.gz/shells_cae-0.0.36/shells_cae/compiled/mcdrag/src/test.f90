program test_mcdrag
    use mcdrag
    implicit none

    type(shell):: my_shell
    real(dp):: res, am

    integer(c_int):: i, n_tsteps=200, n_machs = 30

    real(dp):: m(30), cd0_array(30), cdh_array(30), cdbt_array(30), cdb_array(30), cdrb_array(30), cdsf_array(30)

    do i=1, 30
        m(i) = i * 0.2_dp
    end do

    call set_shell_geo(my_shell, 152.4_dp, 5.65_dp, 3.01_dp, 0.58_dp, 0.09_dp, 1.02_dp, 0.848_dp, 0.5_dp, 2)

    call get_aerodynamics(m, n_machs, my_shell, cd0_array, cdh_array, cdbt_array, cdb_array, cdrb_array, cdsf_array)

    print *, cd0_array, m

end program test_mcdrag