program test
    use penetration
    implicit none


    type(hedge):: heg
    type(kernel):: ker
    type(pen_prob):: prob
    real(c_double):: ys(4, 1000)
    integer(c_int):: n_tsteps = 1000, i=1

    call set_hedge_material(heg, 970e6_dp, 7850.0_dp, 4.5_dp, 1.3_dp)
    call set_kernel_material(ker, 970e6_dp, 7850.0_dp, 4.01_dp, 1.5_dp)

    call init_hedge(heg, 201e9_dp, 0.33_dp, 0.95_dp)
    call init_kernel(ker, 4500.0_dp, 0.044_dp, 0.367_dp, 1733.0_dp)

    call dense_compute_penetration(ys, n_tsteps, prob, ker, heg, 1e-6_dp, 1.0_dp)

    do i=1, n_tsteps

        print *, ys(:, i)
    end do
    
end program test
