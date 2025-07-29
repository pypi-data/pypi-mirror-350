module mcdrag
use iso_c_binding

implicit none
integer, parameter:: dp=(kind(0.d0))

type, bind(c) :: shell
    real(c_double):: d
    real(c_double):: L
    real(c_double):: h_l
    real(c_double):: b_l
    real(c_double):: m_d
    real(c_double):: b_d
    real(c_double):: bs_d
    real(c_double):: hs_p
    real(c_double):: t_r
    integer(c_int):: bl_code
end type shell

    contains

        subroutine set_shell_geo(ashell, d, L, h_l, b_l, m_d, b_d, bs_d, hs_p, bl_code) bind(c, name='set_shell_geo')
            type(shell), intent(out):: ashell
            real(c_double), intent(in), value:: d, L, h_l, b_l, m_d, b_d, bs_d, hs_p
            integer(c_int), intent(in), value:: bl_code

            ashell%d = d
            ashell%L = L
            ashell%h_l = h_l
            ashell%b_l = b_l
            ashell%m_d = m_d
            ashell%b_d = b_d
            ashell%bs_d = bs_d
            ashell%hs_p = hs_p

            ashell%t_r = (1.0_dp - m_d) / h_l

            ashell%bl_code = bl_code


        end subroutine set_shell_geo

        pure real(c_double) function cdsf(M, ashell) bind(c, name='cdsf')
            real(c_double), intent(in), value:: M
            type(shell), intent(in):: ashell

            real(c_double):: Re, r3, cfl, cft, d5, sw_nose, sw_cyl, sw_total, c9, c10

            Re = 23296.3_dp * M * ashell%L * ashell%d
            r3 = 0.4343_dp * log(Re)
            cfl = (1.328_dp / sqrt(Re)) / (1.0_dp + 0.12_dp * M ** 2) ** 0.12_dp
            cft = (0.455 / r3 ** 2.58) / (1.0_dp + 0.21 * M ** 2) ** 0.32_dp
            d5 = 1.0_dp + ((0.333_dp + (0.02_dp / ashell%h_l ** 2)) * ashell%hs_p)

            sw_nose = 1.5708_dp * ashell%h_l * d5 * (1.0_dp + (1.0_dp / (8.0_dp * ashell%h_l ** 2)))
            sw_cyl = 3.1415 * (ashell%L - ashell%h_l)
            sw_total = sw_nose + sw_cyl

            select case (ashell%bl_code)
                case (0)
                    c9 = 1.2732_dp * sw_total * cfl
                    c10 = c9

                case (1)
                    c9 = 1.2732_dp * sw_total * cfl
                    c10 = 1.2732_dp * sw_total * cft

                case (2)
                    c9 = 1.2732_dp * sw_total * cft
                    c10 = c9
            end select

            cdsf = (c9 * sw_nose + c10 * sw_cyl) / sw_total
        end function cdsf

        pure real(c_double) function cdrb(M, ashell) bind(c, name='cdrb')
            real(c_double), intent(in), value:: M
            type(shell), intent(in):: ashell

            if (M < 0.95_dp) then
                cdrb = (M ** 12.5) * (ashell%b_d - 1.0_dp)
            else
                cdrb = (0.21_dp + 0.28_dp / M ** 2) * (ashell%b_d - 1.0_dp)
            end if

        end function cdrb

        pure real(c_double) function cdb(M, ashell) bind(c, name='cdb')
            real(c_double), intent(in), value:: M
            type(shell), intent(in):: ashell

            real(c_double):: p1, p2, p4

            if (M < 1.0_dp) then
                p2 = 1.0_dp / (1.0_dp + 0.1875_dp * M ** 2 + 0.0531_dp * M ** 4)
            else
                p2 = 1.0_dp / (1.0_dp + 0.2477_dp * M ** 2 + 0.0345_dp * M ** 4)
            end if

            p4 = (1.0_dp + 9.000001E-02 * (1.0_dp - exp(ashell%h_l - ashell%L)) * M ** 2)
            p4 = p4 * (1.0_dp + 0.25_dp * (1.0_dp - ashell%bs_d)* M ** 2)

            p1 = p2 * p4

            if (p1 < 0.0_dp) then
                p1 = 0.0_dp
            end if

            cdb = (1.4286 * (1.0_dp - p1) * ashell%bs_d ** 2) / M ** 2
        end function cdb

        pure real(c_double) function cdbt(M, ashell) bind(c, name='cdbt')
            real(c_double), intent(in), value:: M
            type(shell), intent(in):: ashell

            real(c_double):: t2, t3, c15, e1, b4, b2, b, b3, a12, a11, e2, x3, a1, r5, e3, a2

            if (ashell%b_l <= 0.0_dp .or. M <= 0.85_dp) then 
                cdbt = 0.0_dp
                return
            end if

            t2  = (1.0_dp - ashell%bs_d) / (2 * ashell%b_l)

            if (M <= 1.0_dp) then
                t3 = 2.0_dp * t2 ** 2 + t2 ** 3
                c15 = (M ** 2 - 1.0_dp) / (2.4_dp * M ** 2)
                e1 = exp(-2.0_dp * ashell%b_l)
                b4 = 1.0_dp - e1 + 2 * t2 * ((e1 * (ashell%b_l + 0.5_dp)) - 0.5_dp)

                cdbt = 2.0_dp * t3 * b4 * (1.0_dp / (0.564_dp + 1250.0_dp * c15 ** 2))

            elseif (M <= 1.1_dp) then
                t3 = 2.0_dp * t2 ** 2 + t2 ** 3
                c15 = (M ** 2 - 1.0_dp) / (2.4_dp * M ** 2)
                e1 = exp(-2.0_dp * ashell%b_l)
                b4 = 1.0_dp - e1 + 2 * t2 * ((e1 * (ashell%b_l + 0.5_dp)) - 0.5_dp)

                cdbt = 2.0_dp * t3 * b4 * (1.774_dp - 9.3_dp * c15)

            else
                b2 = M ** 2 - 1.0_dp
                b = sqrt(b2)
                b3 = 0.85_dp / b
                a12 = (5 * ashell%t_r) / (6 * b)
                a12 = a12 + (0.5_dp * ashell%t_r) ** 2
                a12 = a12 - (0.734_dp / M ** 2) * ((ashell%t_r * M) ** 1.6_dp)

                a11 = (1.0_dp - 0.6_dp * ashell%hs_p / M) * a12

                e2 = exp((ashell%L - ashell%h_l - ashell%b_l) * (-1.1952_dp / M))
                x3 = ((2.4_dp * M ** 4 - 4 * b2) * (t2 ** 2)) / (2 * b2 ** 2)
                a1 = a11 * e2 - x3 + 2 * t2 / b
                r5 = 1 / b3
                e3 = exp(-b3 * ashell%b_l)
                a2 = 1 - e3 + (2 * t2 * (e3 * (ashell%b_l + r5) - r5))

                cdbt = 4 * a1 * t2 * a2 * r5
            end if

        end function cdbt

        pure real(c_double) function cdh(M, ashell) bind(c, name='cdh')
            real(c_double), intent(in), value:: M
            type(shell), intent(in):: ashell

            real(c_double):: p5, mc, b2, b, s4, z, r_4, c11, c12, c13, c14, c15, c16, c17, c18

            if (M < 1.0_dp) then
                p5 = (1.0_dp + 0.2_dp * M ** 2) ** 3.5
            else
                p5 = ((1.2_dp * M ** 2) ** 3.5_dp) * (6.0_dp / (7.0_dp * M ** 2 - 1.0_dp)) ** 2.5_dp
            end if

            c15 = (M ** 2 - 1.0_dp) / (2.4_dp * M ** 2)
            c16 = (1.122 * (p5 - 1.0_dp) * ashell%m_d ** 2) / M ** 2

            if (M <= 0.91) then
                c18 = 0.0_dp
            elseif (M >= 1.41) then
                c18 = 0.85_dp * c16
            else
                c18 = (0.254_dp + 2.88_dp * c15) * c16
            end if

            if (M <= 1.0_dp) then
                mc = 1.0_dp / sqrt(1.0_dp + 0.552_dp * (ashell%t_r ** 0.8_dp))

                if (M < mc) then
                    c17 = 0.0_dp
                else
                    c17 = 0.368_dp * (ashell%t_r ** 1.8_dp) + 1.6_dp * ashell%t_r * C15
                end if
                
                cdh = c17 + c18
            end if

            if (M > 1.0_dp) then
                b2 = M ** 2 - 1.0_dp
                b = sqrt(b2)
                s4 = 1.0_dp + 0.368_dp * (ashell%t_r ** 1.85_dp)

                if (M >= S4) then
                    z = b
                else
                    z = sqrt(s4 ** 2 - 1.0_dp)
                end if

                r_4 = 1.0_dp / z ** 2
                c11 = 0.7156_dp - 0.5313_dp * ashell%hs_p + 0.595_dp * ashell%hs_p ** 2
                c12 = 0.0796_dp + 0.0779_dp * ashell%hs_p
                c13 = 01.587_dp + 0.049_dp * ashell%hs_p
                c14 = 0.1122_dp + 0.1658_dp * ashell%hs_p

                c17 = (c11 - c12 * (ashell%t_r ** 2)) * r_4 * ((ashell%t_r * z) ** (c13 + c14 * ashell%t_r))

                cdh = c17 + c18
            end if

        end function cdh

        pure real(c_double) function cd0(M, ashell) bind(c, name='cd0')
            real(c_double), intent(in), value:: M
            type(shell), intent(in):: ashell

            cd0 = cdh(M, ashell) + cdbt(M, ashell) + cdb(M, ashell) + cdrb(M, ashell) + cdsf(M, ashell)
        end function cd0

        subroutine get_aerodynamics_(M, ashell, cd0_, cdh_, cdbt_, cdb_, cdrb_, cdsf_)
            real(c_double), intent(in):: M
            type(shell), intent(in):: ashell

            real(c_double), intent(out):: cd0_, cdh_, cdbt_, cdb_, cdrb_, cdsf_

            real(c_double):: cd0_1, cdh_1, cdbt_1, cdb_1, cdrb_1, cdsf_1

            cdh_1 = cdh(M, ashell)
            cdbt_1 = cdbt(M, ashell)
            cdb_1 = cdb(M, ashell)
            cdrb_1 = cdrb(M, ashell)
            cdsf_1 = cdsf(M, ashell)

            cdh_= cdh_1
            cdbt_ = cdbt_1
            cdb_ = cdb_1
            cdrb_ = cdrb_1
            cdsf_ = cdsf_1

            cd0_ = cdh_1 + cdbt_1 + cdb_1 + cdrb_1 + cdsf_1

        end subroutine get_aerodynamics_

        subroutine get_aerodynamics(M, n_machs, ashell, cd0_array, cdh_array, cdbt_array, cdb_array, cdrb_array, cdsf_array) bind(c, name='get_aerodynamics')
            real(c_double), dimension(:), intent(in):: M(n_machs)
            integer(c_int), intent(in), value:: n_machs
            type(shell), intent(in):: ashell

            real(c_double), dimension(:), intent(inout):: cd0_array(n_machs), cdh_array(n_machs), cdbt_array(n_machs), cdb_array(n_machs), cdrb_array(n_machs), cdsf_array(n_machs)

            integer(c_int):: i

            do concurrent (i=1:n_machs)

                cdh_array(i) = cdh(M(i), ashell)
                cdbt_array(i) = cdbt(M(i), ashell)
                cdb_array(i) = cdb(M(i), ashell)
                cdrb_array(i) = cdrb(M(i), ashell)
                cdsf_array(i) = cdsf(M(i), ashell)

                cd0_array(i) = cdh_array(i) + cdbt_array(i) + cdb_array(i) + cdrb_array(i) + cdsf_array(i)

            end do
            
        end subroutine get_aerodynamics

end module mcdrag