from .solvers_abc import ABCSolver
import numpy as np

class APFSDFlStableSolver(ABCSolver):

    name = 'apfsd_fl_stable_solver'

    preprocessed_data = dict(
        b_kr=None,
        da=None,
        b_kc=None,
        l_op=None,
        L_op=None,
        b_sr=None,
        s_op=None,
        n=None,
        ksi=None,
        M=None,
        delta=None,
        L=None,
        H=None,
        xcm=None
    )

    def _compute_plum_cy(self, p_data):
        lambd = p_data['l_op'] / p_data['b_sr']
        S_kr = p_data['ksi'] * p_data['s_op']
        s_mid = 0.25 * np.pi * p_data['da'] ** 2
        M = p_data['M']

        if M < 0.9:
            Cy_op = (1.84 * np.pi * lambd * p_data['delta']) / (2.4 + lambd)
            Cy_op *= S_kr / s_mid
        elif M < 1.1:
            Cy_op = (1.84 * np.pi * lambd * p_data['delta']) / (2.4 + lambd)
            Cy_op *= 1 / np.sqrt(1. - M ** 2)
            Cy_op *= S_kr / s_mid
        else:
            if lambd >= (1 / np.sqrt(M ** 2 - 1.)):
                Cy_op = 4 * p_data['delta'] / np.sqrt(M ** 2 - 1.)
                Cy_op *= (1. - 1 / (2 * lambd * np.sqrt(M ** 2 - 1.)))
                Cy_op *= S_kr / s_mid
            else:
                Cy_op = 1.35 * p_data['delta'] * (lambd + 1 / np.sqrt(M ** 2 - 1.))
                Cy_op *= S_kr / s_mid

        return Cy_op

    def _compute_kernel_cy(self, p_data):
        if p_data['M'] < 1.:
            return p_data['delta']
        else:
            return 2.4 * p_data['delta']

    def _compute_kernel_cd(self, p_data):
        lambd_m = p_data['H'] / p_data['da']
        lambd_k = p_data['L'] / p_data['da']
        lambd_len = lambd_k / lambd_m

        cd = 0.733 + 0.667 * p_data['delta'] * lambd_m * (lambd_len ** 2 - 1.)
        cd /= lambd_len * (1.57 + 1.334 * p_data['delta'] * lambd_m * (lambd_len - 1.))

        return cd

    def _compute_plum_cd(self, p_data):
        return (p_data['L'] - 0.5 * p_data['b_sr']) / p_data['L']

    def run(self, data: dict, global_state: dict):
        p_data = self.preprocessed_data

        plum_cy = self._compute_plum_cy(p_data)
        ker_cy = self._compute_kernel_cy(p_data)
        kernel_xcd = self._compute_kernel_cd(p_data) * p_data['L']
        plum_xcd = self._compute_plum_cd(p_data) * p_data['L']

        cy_total = plum_cy + ker_cy
        xcd_total = (ker_cy * kernel_xcd + plum_cy * plum_xcd) / cy_total
        h = xcd_total - p_data['xcm']
        ksi = (h / p_data['L']) * 100

        global_state[APFSDFlStableSolver.name] = dict(
            plum_cy=plum_cy,
            ker_cy=ker_cy,
            kernel_xcd=kernel_xcd,
            plum_xcd=plum_xcd,
            cy_total=cy_total,
            xcd_total=xcd_total,
            h=h,
            ksi=ksi
        )





