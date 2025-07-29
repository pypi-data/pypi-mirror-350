module penetration
    use iso_c_binding
    implicit none
    integer, parameter:: dp=(kind(0.d0))
    real(c_double), parameter:: pi = 3.1415926536883458

    
    type, bind(c) :: material
        real(c_double):: sigma
        real(c_double):: rho
        real(c_double):: C
        real(c_double):: a
        real(c_double):: lambda
    end type material

    type, bind(c) :: hedge
        type(material) :: mat
        real(c_double):: E
        real(c_double):: nu
        real(c_double):: lambda1
        real(c_double):: A
        real(c_double):: gamma
    end type hedge

    type, bind(c) :: kernel
        type(material) :: mat
        real(c_double):: c_zv
        real(c_double):: da
        real(c_double):: la
        real(c_double):: vc
    end type kernel

    type, bind(c) :: pen_prob
        real(c_double):: u_0
        real(c_double):: d
        real(c_double):: r_g
    end type pen_prob

    contains

        subroutine set_hedge_material(ahedge, sigma, rho, a, lambda) bind(c, name="set_hedge_material")
            type(hedge), intent(out):: ahedge
            real(c_double), intent(in), value:: sigma, rho, a, lambda

            type(material):: mat

            mat%sigma = sigma
            mat%rho = rho
            mat%C = 0.5_dp * rho
            mat%a = a
            mat%lambda = lambda

            ahedge%mat = mat

        end subroutine set_hedge_material

        subroutine set_kernel_material(akernel, sigma, rho, a, lambda) bind(c, name="set_kernel_material")
            type(kernel), intent(out):: akernel
            real(c_double), intent(in), value:: sigma, rho, a, lambda

            type(material):: mat

            mat%sigma = sigma
            mat%rho = rho
            mat%C = 0.5_dp * rho
            mat%a = a
            mat%lambda = lambda

            akernel%mat = mat

        end subroutine set_kernel_material

        subroutine init_hedge(ahedge, E, nu, lambda1) bind(c, name="init_hedge")
            type(hedge), intent(out):: ahedge
            real(c_double), intent(in), value:: E, nu, lambda1

            ahedge%E = E
            ahedge%nu = nu
            ahedge%lambda1 = lambda1

        end subroutine init_hedge

        subroutine init_kernel(akernel, c_zv, da, la, vc) bind(c, name="init_kernel")
            type(kernel), intent(out):: akernel
            real(c_double), intent(in), value:: c_zv, da, la, vc

            akernel%c_zv = c_zv
            akernel%da = da
            akernel%la = la
            akernel%vc = vc
            
        end subroutine init_kernel

        subroutine compute_hedge(ahedge, u0)
            type(hedge), intent(out):: ahedge
            real(c_double), intent(in):: u0
            real(c_double):: alpha, gamma, gam0, k_u0, rho_to_rho, A, sigma_h, E_h, a_h, lam_h, A1, A2
            sigma_h = ahedge%mat%sigma
            E_h = ahedge%E
            a_h = ahedge%mat%a
            lam_h = ahedge%mat%lambda

            alpha = sigma_h / (2.0_dp * E_h * ahedge%lambda1)
            gam0 = (E_h / (3.0_dp * (1.0_dp - ahedge%nu) * sigma_h)) ** (1.0_dp / 3)
            k_u0 = (2.0_dp * gam0 ** 2 - gam0 - 1.0_dp) / ((gam0 + 1.0_dp) * (gam0 ** 3 - 1.0_dp))
            rho_to_rho = 1.0_dp - (k_u0 * u0) / (a_h + lam_h * k_u0 * u0)
            gamma = (1 - rho_to_rho * exp(-3.0_dp * alpha)) ** (-1.0_dp / 3)

            A1 = sigma_h * log(gamma)
            A2 = (1.0_dp - ahedge%lambda1) * (1.0_dp - 1.0_dp / gamma ** 3) ** 0.62 * pi ** 2 / 18.0_dp
            A2 = A2 + sigma_h / (2.0_dp * E_h * ahedge%lambda1)
            A2 = A2 * E_h * 2.0_dp / 3.0_dp

            A = 2 * (A1 + A2)

            ahedge%gamma = gamma
            ahedge%A = A

        end subroutine compute_hedge

        real(c_double) function get_u0(ahedge, akernel) result(u_0)
            type(hedge), intent(in):: ahedge
            type(kernel), intent(in):: akernel

            real(c_double):: a_0, b_0, c_0

            a_0 = akernel%mat%lambda - ahedge%mat%lambda * (ahedge%mat%rho / akernel%mat%rho)

            b_0 = 2.0_dp * akernel%mat%lambda * akernel%vc + akernel%mat%a + ahedge%mat%a * (ahedge%mat%rho / akernel%mat%rho)

            c_0 = akernel%mat%a * akernel%vc + akernel%mat%lambda * akernel%vc ** 2

            u_0 = (b_0 - sqrt((b_0 ** 2) - (4.0_dp * a_0 * c_0))) / (2.0_dp * a_0)

        end function get_u0

        real(c_double) function get_rg(ahedge, akernel, u_0) result(r_g)
            type(hedge), intent(in):: ahedge
            type(kernel), intent(in):: akernel

            real(c_double), intent(in):: u_0

            r_g = 0.5_dp * akernel%da
            r_g = r_g * (1.0_dp + sqrt((2.0_dp*akernel%mat%rho*(akernel%vc - u_0) ** 2) / ahedge%A))

        end function get_rg

        real(c_double) function get_d(ahedge, akernel, r_g) result(d)
            type(hedge), intent(in):: ahedge
            type(kernel), intent(in):: akernel

            real(c_double), intent(in):: r_g

            d = ahedge%mat%rho * r_g * ((ahedge%gamma - 1.0_dp) / (ahedge%gamma + 1.0_dp))

        end function get_d

        subroutine penetration_rs(dy, y, prob, akernel, kernel_mat, ahedge, hedge_mat)
            real(c_double), intent(out) :: dy(4)
            real(c_double), intent(in) :: y(4)
            type(pen_prob), intent(in):: prob
            type(kernel), intent(in):: akernel
            type(hedge), intent(in):: ahedge
            type(material), intent(in):: hedge_mat, kernel_mat
            
            real(c_double):: s, factor, d_u, d, dxdt, dldt, dvdt, dudt, u, v, l

            u = y(4)
            v = y(3)
            l = y(2)

            factor = 1.0_dp + (v - u) / akernel%c_zv
            s = 0.5_dp * prob%r_g * (v / u - 1.0_dp) * (1.0_dp - 1.0_dp / ahedge%gamma ** 2)
            d_u = hedge_mat%rho * s
            d = kernel_mat%rho * prob%r_g * ((ahedge%gamma - 1.0_dp) / (ahedge%gamma + 1.0_dp))
            dxdt = u
            dldt = u - v
            dudt = ((kernel_mat%sigma * factor) + (kernel_mat%C * (v - u) ** 2) - ahedge%A - (hedge_mat%C * u ** 2)) / (d + d_u)
            dvdt = -kernel_mat%sigma / (kernel_mat%rho * (l - s)) * factor

            dy(1) = dxdt
            dy(2) = dldt
            dy(3) = dvdt
            dy(4) = dudt

        end subroutine penetration_rs

        subroutine compute_penetration(y_s, prob, akernel, ahedge, tstep, tmax) bind(c, name="compute_penetration")
            real(c_double), intent(inout):: y_s(4)
            real(c_double), intent(in), value:: tstep, tmax
            type(pen_prob), intent(inout):: prob
            type(kernel), intent(inout):: akernel
            type(hedge), intent(inout):: ahedge

            type(material):: hedge_mat, kernel_mat

            real(c_double):: t0, y_s_1(4), dy(4, 4)

            logical:: stop_status


            prob%u_0 = get_u0(ahedge, akernel)
            call compute_hedge(ahedge, prob%u_0)
            prob%r_g = get_rg(ahedge, akernel, prob%u_0)
            prob%d = get_d(ahedge, akernel, prob%r_g)

            hedge_mat = ahedge%mat
            kernel_mat = akernel%mat

            t0 = 0.0_dp

            y_s_1(1) = 0.0_dp
            y_s_1(2) = akernel%la
            y_s_1(3) = akernel%vc
            y_s_1(4) = prob%u_0

            stop_status = .true.

            do while(stop_status)
                y_s = y_s_1
                call penetration_rs(dy(:, 1), y_s, prob, akernel, kernel_mat, ahedge, hedge_mat)
                call penetration_rs(dy(:, 2), y_s + 0.5*tstep*dy(:, 1), prob, akernel, kernel_mat, ahedge, hedge_mat)
                call penetration_rs(dy(:, 3), y_s + 0.5*tstep*dy(:, 2), prob, akernel, kernel_mat, ahedge, hedge_mat)
                call penetration_rs(dy(:, 4), y_s + tstep*dy(:, 3), prob, akernel, kernel_mat, ahedge, hedge_mat)

                t0 = t0 + tstep

                y_s_1 = y_s +  tstep*(dy(:, 1) + 2.0_dp * dy(:, 2) + 2.0_dp * dy(:, 3) + dy(:, 4)) / 6.0_dp

                if (t0 > tmax) then
                    stop_status = .false.
                else
                    stop_status = y_s_1(2) > 0.0_dp
                    stop_status = stop_status .and. (y_s_1(3) > 0.0_dp)
                    stop_status = stop_status .and. (y_s_1(4) > 0.0_dp)
                end if

            end do

        end subroutine compute_penetration

        subroutine dense_compute_penetration(y_s, ntsteps, prob, akernel, ahedge, tstep, tmax) bind(c, name="dense_compute_penetration")
            real(c_double), intent(inout):: y_s(4, ntsteps)
            integer(c_int), intent(inout):: ntsteps
            real(c_double), intent(in), value:: tstep, tmax
            type(pen_prob), intent(inout):: prob
            type(kernel), intent(inout):: akernel
            type(hedge), intent(inout):: ahedge

            type(material):: hedge_mat, kernel_mat

            integer(c_int):: i

            real(c_double):: t0, dy(4, 4)

            logical:: stop_status

            prob%u_0 = get_u0(ahedge, akernel)
            call compute_hedge(ahedge, prob%u_0)
            prob%r_g = get_rg(ahedge, akernel, prob%u_0)
            prob%d = get_d(ahedge, akernel, prob%r_g)


            hedge_mat = ahedge%mat
            kernel_mat = akernel%mat

            t0 = 0.0_dp

            y_s(1, 1) = 0.0_dp
            y_s(2, 1) = akernel%la
            y_s(3, 1) = akernel%vc
            y_s(4, 1) = prob%u_0

            stop_status = .true.
            
            do i=2, ntsteps
                if (.not. stop_status) then
                    ntsteps = i - 1
                    return
                end if
                call penetration_rs(dy(:, 1), y_s(:, i-1), prob, akernel, kernel_mat, ahedge, hedge_mat)
                call penetration_rs(dy(:, 2), y_s(:, i-1) + 0.5*tstep*dy(:, 1), prob, akernel, kernel_mat, ahedge, hedge_mat)
                call penetration_rs(dy(:, 3), y_s(:, i-1) + 0.5*tstep*dy(:, 2), prob, akernel, kernel_mat, ahedge, hedge_mat)
                call penetration_rs(dy(:, 4), y_s(:, i-1) + tstep*dy(:, 3), prob, akernel, kernel_mat, ahedge, hedge_mat)

                t0 = t0 + tstep

                y_s(:, i) = y_s(:, i-1) +  tstep*(dy(:, 1) + 2.0_dp * dy(:, 2) + 2.0_dp * dy(:, 3) + dy(:, 4)) / 6.0_dp

                if (t0 > tmax) then
                    stop_status = .false.
                else
                    stop_status = y_s(2, i) > 0.0_dp
                    stop_status = stop_status .and. (y_s(3, i) > 0.0_dp)
                    stop_status = stop_status .and. (y_s(4, i) > 0.0_dp)
                    stop_status = stop_status .and. (y_s(3, i) - y_s(4, i) > 0.0)
                    stop_status = stop_status .and. (y_s(3, i) - y_s(3, i-1) < 0.0)
                end if

            end do

        end subroutine dense_compute_penetration

end module penetration
