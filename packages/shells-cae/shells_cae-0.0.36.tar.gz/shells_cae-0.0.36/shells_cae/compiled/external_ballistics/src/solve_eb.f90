module solve_eb
    use iso_c_binding
    implicit none

    integer, parameter:: dp=(kind(0.d0))

    real(c_double), dimension(:), parameter :: h_list(15) = [0., 50., 100., 200., 300., 400., 500., 600.,&
    700., 800., 900., 1000., 5000., 10000., 20000.]

    real(c_double), dimension(:), parameter :: a_list(15) = [340.29, 340.10, 339.91, 339.53, 339.14, 338.76, 338.38,&
    337.98, 337.6, 337.21, 336.82, 336.43, 320.54, 299.53, 295.07]

    real(c_double), parameter :: g = 9.81, rho_0 = 1.2066, pi = 3.1415926536883458

    contains

    real(c_double) function linear_interp(x, x_array, y_array, n_nodes) result(y)
        real(c_double), intent(in):: x, x_array(n_nodes), y_array(n_nodes)
        integer(c_int), intent(in):: n_nodes

        integer:: i

        if(x <= x_array(1)) then
            y = y_array(1)
        elseif(x >= x_array(n_nodes)) then
            y = y_array(n_nodes)
        else
            do i=2, n_nodes-1
                if(x >= x_array(i) .and. x <= x_array(i+1)) then
                    y = y_array(i) + ((y_array(i+1) - y_array(i))*(x - x_array(i)))/(x_array(i+1) - x_array(i))
                end if
            end do
        end if


    end function linear_interp

    real(c_double) function get_cx(v, y, cx_list, mach_list, n_machs) result(cx)
        real(c_double), intent(in):: v, y, cx_list(n_machs), mach_list(n_machs)
        integer(c_int), intent(in):: n_machs
        
        real(c_double) :: a, m
        integer(c_int) :: i

        a = linear_interp(y, h_list, a_list, 15)
        
        m = v/a

        cx = linear_interp(m, mach_list, cx_list, n_machs)

    end function get_cx

    subroutine ext_bal_rs(dy, y, d, q, cx_list, mach_list, n_machs)
        real(c_double), intent(out) :: dy(4)
        real(c_double), intent(in) :: y(4), d, q, cx_list(n_machs), mach_list(n_machs)
        integer(c_int), intent(in):: n_machs

        real(c_double) :: cx, hy, jt

        hy = rho_0 * ((20000.0 - y(2)) / (20000.0 + y(2)))

        cx = get_cx(y(3), y(2), cx_list, mach_list, n_machs)

        jt = -0.5 * cx * hy * y(3)**2

        dy(1) = y(3) * cos(y(4))

        dy(2) = y(3) * sin(y(4))

        dy(3) = jt * 0.25*(pi * d ** 2)/q - g * sin(y(4))

        dy(4) = -g * cos(y(4))/y(3)
    end subroutine ext_bal_rs

    subroutine count_eb(y0, d, q, cx_list, mach_list, n_machs, max_distance, tstep, tmax) bind(c, name="count_eb")

        real(c_double), intent(inout) :: y0(4), cx_list(n_machs), mach_list(n_machs)
        real(c_double), intent(in), value :: d, q, max_distance, tstep, tmax
        integer(c_int), intent(in), value:: n_machs

        real(c_double) :: y1(4), dy(4, 4), t0

        t0 = 0.0

        do while(y0(2) >= 0.0 .and. y0(1) < max_distance)
            y1 = y0
            call ext_bal_rs(dy(:, 1), y1, d, q, cx_list, mach_list, n_machs)
            call ext_bal_rs(dy(:, 2), y1 + 0.5*tstep*dy(:, 1), d, q, cx_list, mach_list, n_machs)
            call ext_bal_rs(dy(:, 3), y1 + 0.5*tstep*dy(:, 2), d, q, cx_list, mach_list, n_machs)
            call ext_bal_rs(dy(:, 4), y1 + tstep*dy(:, 3), d, q, cx_list, mach_list, n_machs)

            t0 = t0 + tstep
            y0 = y1 + tstep*(dy(:, 1) + 2*dy(:, 2) + 2*dy(:, 3) + dy(:, 4))/6
        end do

        if (y0(2) < 0.0) then
            y0 = y1 + (0.0 - y1(2)) * ((y0-y1)/(y0(2)-y1(2)))
        end if

        if (y0(1) > max_distance) then
            y0 = y1 + (max_distance - y1(1)) * ((y0-y1)/(y0(1)-y1(1)))
        end if

    end subroutine count_eb

    subroutine dense_count_eb(y_array, d, q, cx_list, mach_list, n_machs, max_distance, tstep, tmax, n_tsteps) bind(c, name="dense_count_eb")

        real(c_double), intent(inout) :: y_array(4, n_tsteps), cx_list(n_machs), mach_list(n_machs)
        integer(c_int), intent(inout) :: n_tsteps
        integer(c_int), intent(in), value:: n_machs

        real(c_double), intent(in), value :: d, q, max_distance, tstep, tmax

        real(c_double) :: y1(4), dy(4, 4), t0

        integer(c_int) :: i

        t0 = 0.0

        do i=2, n_tsteps
            call ext_bal_rs(dy(:, 1), y_array(:, i-1), d, q, cx_list, mach_list, n_machs)
            call ext_bal_rs(dy(:, 2), y_array(:, i-1) + 0.5*tstep*dy(:, 1), d, q, cx_list, mach_list, n_machs)
            call ext_bal_rs(dy(:, 3), y_array(:, i-1) + 0.5*tstep*dy(:, 2), d, q, cx_list, mach_list, n_machs)
            call ext_bal_rs(dy(:, 4), y_array(:, i-1) + tstep*dy(:, 3), d, q, cx_list, mach_list, n_machs)

            t0 = t0 + tstep
            y_array(:, i) = y_array(:, i-1) + tstep*(dy(:, 1) + 2*dy(:, 2) + 2*dy(:, 3) + dy(:, 4))/6

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

    end subroutine dense_count_eb

end module solve_eb