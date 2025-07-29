module solve_ebh
    use iso_c_binding

    use solve_eb

    implicit none
    
    real(c_double), dimension(:), parameter :: km_list(25) = [0.97, 0.98, 1.0, 1.03, 1.06, 1.07, 1.06, 1.05, 1.04, 1.03, 1.02, 1.01,&
    1.0, 0.99, 0.98, 0.97, 0.96, 0.95, 0.94, 0.93, 0.92, 0.91, 0.9, 0.89, 0.88]

    real(c_double), dimension(:), parameter :: km_mach_list(25) =  [0.762, 0.821, 0.88, 0.938, 0.997, 1.173, 1.232, 1.291,&
    1.349, 1.467, 1.525, 1.643, 1.701, 1.76, 1.877, 1.995, 2.053, 2.171, 2.23, 2.347, 2.491, 2.64, 3.08, 3.227, 3.374]

    type, bind(c) :: shell
        real(c_double):: d
        real(c_double):: L
        real(c_double):: q
        real(c_double):: A
        real(c_double):: B
        real(c_double):: mu
        real(c_double):: c_q
        real(c_double):: h
    end type shell

    contains

    real(c_double) function get_km(v) result(km)
        real(c_double), intent(in):: v

        real(c_double):: mach
        integer(c_int) :: i


        mach = v / linear_interp(1.0_dp, h_list, a_list, 15)
        km = linear_interp(mach, km_mach_list, km_list, 25)

        km = km * 1e-3

    end function get_km

    subroutine ext_bal_rs_h(dy, y, cx_list, mach_list, n_machs, ashell)
        ! Функция правых частей вместе с угловой скоростью
        real(c_double), intent(out) :: dy(5)
        real(c_double), intent(in) :: y(5), cx_list(n_machs), mach_list(n_machs)
        type(shell), intent(in):: ashell

        integer(c_int), intent(in):: n_machs

        real(c_double):: hy

        hy = rho_0 * ((20000.0 - y(2)) / (20000.0 + y(2)))

        call ext_bal_rs(dy(:4), y(:4), ashell%d, ashell%q, cx_list, mach_list, n_machs)

        dy(5) = -ashell%d ** 3 * ashell%L / ashell%A * 1e3_dp * hy * y(3) * 1.5e-6_dp * y(5)

    end subroutine ext_bal_rs_h

    subroutine dense_count_eb_h(y_array, cx_list, mach_list, n_machs, ashell, diag_vals, eta, sigma_dop, delta_dop, sigma_array, delta_array, max_distance, tstep, tmax, n_tsteps) bind(c, name="dense_count_eb_h")
        real(c_double), intent(inout) :: y_array(5, n_tsteps), diag_vals(4), sigma_array(n_tsteps), delta_array(n_tsteps), cx_list(n_machs), mach_list(n_machs)
        type(shell), intent(in):: ashell
        integer(c_int), intent(inout) :: n_tsteps
        integer(c_int), intent(in), value:: n_machs
        real(c_double), intent(in), value :: max_distance, tstep, tmax, eta, sigma_dop, delta_dop
        ! real(c_double), intent(in):: sigma_dop, delta_dop

        real(c_double) :: dy(5, 4), t0, d
        integer(c_int) :: i, i_s
        i_s = 0

        d = ashell%d * 1e-3_dp

        t0 = 0.0

        y_array(5, 1) = 2.0_dp * pi * y_array(3, 1) / (eta * ashell%d)

        do i=2, n_tsteps
            call compute_sigma_delta(ashell, y_array(:, i-1), sigma_array(i-1), delta_array(i-1)) ! Расчет коэффициента гироскопической устойчивости и угла нутации

            call ext_bal_rs_h(dy(:, 1), y_array(:, i-1), cx_list, mach_list, n_machs, ashell)
            call ext_bal_rs_h(dy(:, 2), y_array(:, i-1) + 0.5*tstep*dy(:, 1), cx_list, mach_list, n_machs, ashell)
            call ext_bal_rs_h(dy(:, 3), y_array(:, i-1) + 0.5*tstep*dy(:, 2), cx_list, mach_list, n_machs, ashell)
            call ext_bal_rs_h(dy(:, 4), y_array(:, i-1) + tstep*dy(:, 3), cx_list, mach_list, n_machs, ashell)
            t0 = t0 + tstep
            y_array(:, i) = y_array(:, i-1) + tstep*(dy(:, 1) + 2*dy(:, 2) + 2*dy(:, 3) + dy(:, 4))/6

            if ((y_array(2, i) - y_array(2, i-1) < 0.0_dp) .and. (i_s == 0)) then
                i_s = i
            end if

            if(y_array(2, i) < 0.0 .or. y_array(1, i) > max_distance) then
                n_tsteps = i
                exit
            end if
            if(t0 > tmax) then
                n_tsteps = i
                return
            end if
        end do

        if (y_array(2, n_tsteps) < 0.0) then
            y_array(:, n_tsteps) = y_array(:, n_tsteps-1) + (0.0 - y_array(2, n_tsteps-1)) * ((y_array(:, n_tsteps)-y_array(:, n_tsteps-1))/(y_array(2, n_tsteps)-y_array(2, n_tsteps-1)))
        end if
        if (y_array(1, n_tsteps) > max_distance) then
            y_array(:, n_tsteps) = y_array(:, n_tsteps-1) + (max_distance - y_array(1, n_tsteps-1)) * ((y_array(:, n_tsteps)-y_array(:, n_tsteps-1))/(y_array(1, n_tsteps)-y_array(1, n_tsteps-1)))
        end if

        call compute_sigma_delta(ashell, y_array(:, n_tsteps), sigma_array(n_tsteps), delta_array(n_tsteps))
        call compute_diagram(y_array(:, 1), y_array(:, i_s), diag_vals, ashell, sigma_dop, delta_dop)

    end subroutine dense_count_eb_h

    subroutine compute_sigma_delta(ashell, y_s, sigma_i, delta_i)
        type(shell), intent(in):: ashell
        real(c_double), intent(in):: y_s(5)
        real(c_double), intent(inout):: sigma_i, delta_i

        real(c_double):: beta, alpha, h_y, k_ms, d, h, sqrt_l

        h = ashell%h
        d = ashell%d
        k_ms = get_km(y_s(3))
        h_y = (20000.0 - y_s(2)) / (20000.0 + y_s(2))

        if (ashell%L <= 4.5_dp * d) then
            sqrt_l = 1.0_dp
        else
            sqrt_l = sqrt(ashell%L / (4.5_dp * d))
        end if

        beta = (d ** 2 * h * 1e3_dp * h_y * y_s(3) ** 2 * k_ms * sqrt_l) / ashell%B

        alpha = 0.5_dp * ashell%A / ashell%B * y_s(5)

        sigma_i = 1.0_dp - beta / alpha ** 2

        if (sigma_i > 0.0_dp) then
            sigma_i = sqrt(sigma_i)
        else
            sigma_i = 0.0_dp
        end if

        delta_i = (2.0_dp * alpha / beta) * (g * cos(y_s(4)) / y_s(3))

    end subroutine compute_sigma_delta

    subroutine compute_diagram(y_0, y_s, diag_vals, ashell, sigma_dop, delta_dop)
        real(c_double), intent(inout):: y_0(5), y_s(5), diag_vals(4)
        real(c_double), intent(in):: sigma_dop, delta_dop
        type(shell), intent(in):: ashell

        real(c_double):: km_s, km_0, m, n, hd_kr, eta_kr, c_q, mu, d, omega_0, omega_s, h_y, sqrt_l

        d = ashell%d

        h_y = (20000.0 - y_s(2)) / (20000.0 + y_s(2))

        mu = ashell%mu

        c_q = ashell%c_q

        if (ashell%L <= 4.5_dp * d) then
            sqrt_l = 1.0_dp
        else
            sqrt_l = sqrt(ashell%L / (4.5_dp * d))
        end if

        km_0 = get_km(y_0(3))
        km_0 = km_0 * sqrt_l

        m = mu * c_q * (1.0_dp - sigma_dop ** 2) * pi ** 2
        m = m / (4.0_dp * km_0 * ashell%B / ashell%A)

        km_s = get_km(y_s(3))

        km_s = km_s * sqrt_l

        omega_0 = y_0(5)

        omega_s = y_s(5)

        n = (mu * c_q * y_0(3) * d) / (km_s * delta_dop * h_y * y_s(3) ** 3)

        n = 0.5_dp * pi * g * n

        n = n * omega_s / omega_0

        eta_kr = n / m
        hd_kr = n ** 2 / m

        diag_vals(1) = m
        diag_vals(2) = n
        diag_vals(3) = hd_kr
        diag_vals(4) = eta_kr

        ! diag_vals - результаты расчета
        ! 1 - m расчетное
        ! 2 - n расчетное
        ! 3 - m критическое
        ! 4 - n критическое

    end subroutine compute_diagram

end module solve_ebh