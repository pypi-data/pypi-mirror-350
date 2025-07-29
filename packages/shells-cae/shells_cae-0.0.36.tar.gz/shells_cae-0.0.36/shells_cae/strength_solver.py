import numpy as np
from typing import TypedDict
from .solvers_abc import ABCSolver


class data(TypedDict):
    Pmax: float
    qp_max: float
    l1: float
    l2: float
    d: float
    hb: float
    delta: float
    rp: float
    sigma_sh: float
    eps_b: float
    sigma_Tp: float
    Est: float
    c: float
    rzp: float
    a: float
    b: float
    d_d: float
    d_p: float
    f0: float
    V: float
    mu: float
    q: float
    n: float
    eta_n: float
    eta_k: float
    Ln: float
    C: float
    mu_c: float
    rho_w: float
    E: float
    Ef: float
    lambd: float
    sigma_t: float
    sigma_tsh: float
    sigma_dt: float
    eps_sh: float

    type_material: str

    rho_d: float
    Rpr: float

    corpus_coord: np.ndarray
    fuse_coord: np.ndarray
    explosive_coord: np.ndarray
    belt_coord: np.ndarray

    corpus_material: np.ndarray
    explosive_material: np.ndarray
    belt_material: np.ndarray

    res_geo: dict
    res_mcc: dict
    res_section: dict
    res_press_mass: dict
    res_stress: dict
    res_ramp: dict

# Определение координат сечений для расчёта прочности
class CoordSectionSolver:
    name = 'st_section_solver'

    preprocessed_data: data = dict(
        corpus_coord=None,
        fuse_coord=None,
        explosive_coord=None,
        belt_coord=None
    )

    def preprocessor(self, data: dict, global_state: dict):
        self.preprocessed_data['corpus_coord'] = global_state['geometry_solver']['corpus_coord']
        self.preprocessed_data['fuse_coord'] = global_state['geometry_solver']['fuse_coord']
        self.preprocessed_data['explosive_coord'] = global_state['geometry_solver']['explosive_coord']
        self.preprocessed_data['belt_coord'] = global_state['geometry_solver']['belt_coord']

    # Определяем координаты для каждого сечения
    def run(self, data: dict, state: dict):

        p_data = self.preprocessed_data

        # Выкидываем узлы под поясок
        corp = np.delete(p_data['corpus_coord'], [4, 5], axis=1)

        expl = p_data['explosive_coord']
        fuse = p_data['fuse_coord']


        # Координаты 1 сечения
        x_1 = corp[0, -3]
        ind_1 = np.searchsorted(corp[0], x_1)
        y_1 = np.interp(x_1, [corp[0, ind_1-1], corp[0, ind_1]], [corp[1, ind_1-1], corp[1, ind_1]])
        r_1 = corp[1, -3]
        corp_sec_1 = np.array([[x_1, r_1], [x_1, y_1]])

        mask = corp[0, :] >= x_1
        corp_cd_1 = np.insert(corp[:, mask], 0, corp_sec_1, axis=1)
        corp_cd_1 = np.delete(corp_cd_1, -1, axis=1)
        expl_cd_1 = expl

        data_1 = {'R': y_1, 'r': r_1, 'x': x_1, 'corp_cd': corp_cd_1, 'expl_cd': expl_cd_1, 'n': 1}


        # Координаты 2 сечения
        x_2 = corp[0, -4]
        ind_2 = np.searchsorted(corp[0], x_2)
        y_2 = np.interp(x_2, [corp[0, ind_2-1], corp[0, ind_2]], [corp[1, ind_2-1], corp[1, ind_2]])
        r_2 = expl[1, 2]
        corp_sec_2 = np.array([[x_2, r_2], [x_2, y_2]])
        expl_sec_2 = np.array([[x_2, 0],[x_2, r_2]])
        mask = corp[0, :] >= x_2
        corp_cd_2 = np.insert(corp[:, mask], 0, corp_sec_2, axis=1)

        mask = expl[0, :] >= x_2
        expl_cd_2 = np.insert(expl[:, mask], 0, expl_sec_2, axis=1)
        expl_cd_2 = np.append(expl_cd_2, [[x_2], [0]], axis=1)

        data_2 = {'R': y_2, 'r': r_2, 'x': x_2, 'corp_cd': corp_cd_2, 'expl_cd': expl_cd_2, 'n': 2}

        # Координаты 3 сечения
        x_3 = corp[0, -5]
        ind_3 = np.searchsorted(corp[0], x_3)
        y_3 = np.interp(x_3, [corp[0, ind_3 - 1], corp[0, ind_3]], [corp[1, ind_3 - 1], corp[1, ind_3]])
        r_3 = expl[1, 3]
        corp_sec_3 = np.array([[x_3, r_3], [x_3, y_3]])
        expl_sec_3 = np.array([[x_3, 0],[x_3, r_3]])
        mask = corp[0, :] >= x_3
        corp_cd_3 = np.insert(corp[:, mask], 0, corp_sec_3, axis=1)

        mask = expl[0, :] >= x_3
        expl_cd_3 = np.insert(expl[:, mask], 0, expl_sec_3, axis=1)
        expl_cd_3 = np.append(expl_cd_3, [[x_3], [0]], axis=1)

        data_3 = {'R': y_3, 'r': r_3, 'x': x_3, 'corp_cd': corp_cd_3, 'expl_cd': expl_cd_3, 'n': 3}

        # Координаты 0 сечения
        x_0 = (corp[0, 4] - corp[0, 3]) / 2 + corp[0, 3]
        ind_0 = np.searchsorted(corp[0], x_0)
        y_0 = np.interp(x_0, [corp[0, ind_0-1], corp[0, ind_0]], [corp[1, ind_0-1], corp[1, ind_0]])
        ind_0 = np.searchsorted(expl[0], x_0)
        r_0 = np.interp(x_0, [expl[0, ind_0-1], expl[0, ind_0]], [expl[1, ind_0-1], expl[1, ind_0]])

        corp_sec_0 = np.array([[x_0, r_0], [x_0, y_0]])
        expl_sec_0 = np.array([[x_0, 0], [x_0, r_0]])
        h0 = corp[1, 3] - r_0
        a0 = r_0 + h0 / 2

        mask = corp[0, :] >= x_0
        corp_cd_0 = np.insert(corp[:, mask], 0, corp_sec_0, axis=1)
        corp_cd_0 = np.append(corp_cd_0, [[x_0], [r_0]], axis=1)

        mask = expl[0, :] >= x_0
        expl_cd_0 = np.insert(expl[:, mask], 0, expl_sec_0, axis=1)
        expl_cd_0 = np.append(expl_cd_0, [[x_0], [0]], axis=1)

        data_0 = {'R': y_0, 'r': r_0, 'x': x_0, 'corp_cd': corp_cd_0, 'expl_cd': expl_cd_0, 'a0': a0, 'h0': h0, 'n': 0}

        # Координаты 4 сечения
        x_4 = (1.94 * np.sqrt(a0 * h0)) + x_0
        ind_4 = np.searchsorted(corp[0], x_4)
        y_4 = np.interp(x_4, [corp[0, ind_4 - 1], corp[0, ind_4]], [corp[1, ind_4 - 1], corp[1, ind_4]])
        ind_4 = np.searchsorted(expl[0], x_4)
        r_4 = np.interp(x_4, [expl[0, ind_4-1], expl[0, ind_4]], [expl[1, ind_4-1], expl[1, ind_4]])

        corp_sec_4 = np.array([[x_4, r_4], [x_4, y_4]])
        expl_sec_4 = np.array([[x_4, 0], [x_4, r_4]])
        mask = corp[0, :] >= x_4
        corp_cd_4 = np.insert(corp[:, mask], 0, corp_sec_4, axis=1)
        corp_cd_4 = np.append(corp_cd_4, [[x_4], [r_4]], axis=1)

        mask = expl[0, :] >= x_4
        expl_cd_4 = np.insert(expl[:, mask], 0, expl_sec_4, axis=1)
        expl_cd_4 = np.append(expl_cd_4, [[x_4], [0]], axis=1)

        data_4 = {'R': y_4, 'r': r_4, 'x': x_4, 'corp_cd': corp_cd_4, 'expl_cd': expl_cd_4, 'x4': x_4-x_0, 'n': 4}

        # Координаты 5 сечения
        x_5 = x_1 + (x_0 - x_1)/2
        ind_5 = np.searchsorted(corp[0], x_5)
        y_5 = np.interp(x_5, [corp[0, ind_5 - 1], corp[0, ind_5]], [corp[1, ind_5 - 1], corp[1, ind_5]])
        ind_5 = np.searchsorted(expl[0], x_5)
        r_5 = np.interp(x_5, [expl[0, ind_5-1], expl[0, ind_5]], [expl[1, ind_5-1], expl[1, ind_5]])

        corp_sec_5 = np.array([[x_5, r_5], [x_5, y_5]])
        expl_sec_5 = np.array([[x_5, 0], [x_5, r_5]])
        mask = corp[0, :] >= x_5
        corp_cd_5 = np.insert(corp[:, mask], 0, corp_sec_5, axis=1)
        corp_cd_5 = np.append(corp_cd_5, [[x_5], [r_5]], axis=1)

        mask = expl[0, :] >= x_5
        expl_cd_5 = np.insert(expl[:, mask], 0, expl_sec_5, axis=1)
        expl_cd_5 = np.append(expl_cd_5, [[x_5], [0]], axis=1)

        data_5 = {'R': y_5, 'r': r_5, 'x': x_5, 'corp_cd': corp_cd_5, 'expl_cd': expl_cd_5, 'n': 5}

        # Координаты 6 сечения
        x_6 = fuse[0, 3]
        max_i = np.argmax(corp[0])
        ind_6 = np.searchsorted(corp[0, :max_i], x_6)
        y_6 = np.interp(x_6, [corp[0, ind_6 - 1], corp[0, ind_6]], [corp[1, ind_6 - 1], corp[1, ind_6]])
        # max_i = np.argmax(expl[0])
        # ind_6 = np.searchsorted(expl[0, :max_i], x_6)
        # r_6 = np.interp(x_6, [expl[0, ind_6-1], expl[0, ind_6]], [expl[1, ind_6-1], expl[1, ind_6]])
        r_6 = fuse[1, 3]

        corp_sec_6 = np.array([[x_6, r_6], [x_6, y_6]])
        mask = corp[0, :] >= x_6
        corp_cd_6 = np.insert(corp[:, mask], 0, corp_sec_6, axis=1)
        corp_cd_6 = np.append(corp_cd_6, [[x_6], [r_6]], axis=1)

        data_6 = {'R': y_6, 'r': r_6, 'x': x_6, 'corp_cd': corp_cd_6, 'expl_cd': np.zeros((2, 2)), 'n': 6}

        # Координаты 7 сечения
        x_7 = x_3 + (x_6 - x_3) / 2
        max_i = np.argmax(corp[0])
        ind_7 = np.searchsorted(corp[0, :max_i], x_7)
        y_7 = np.interp(x_7, [corp[0, ind_7 - 1], corp[0, ind_7]], [corp[1, ind_7 - 1], corp[1, ind_7]])
        max_i = np.argmax(expl[0])
        ind_7 = np.searchsorted(expl[0, :max_i], x_7)
        r_7 = np.interp(x_7, [expl[0, ind_7-1], expl[0, ind_7]], [expl[1, ind_7-1], expl[1, ind_7]])

        corp_sec_7 = np.array([[x_7, r_7], [x_7, y_7]])
        expl_sec_7 = np.array([[x_7, 0], [x_7, r_7]])
        mask = corp[0, :] >= x_7
        corp_cd_7 = np.insert(corp[:, mask], 0, corp_sec_7, axis=1)
        corp_cd_7 = np.append(corp_cd_7, [[x_7], [r_7]], axis=1)

        mask = expl[0, :] >= x_7
        expl_cd_7 = np.insert(expl[:, mask], 0, expl_sec_7, axis=1)
        expl_cd_7 = np.append(expl_cd_7, [[x_7], [0]], axis=1)

        data_7 = {'R': y_7, 'r': r_7, 'x': x_7, 'corp_cd': corp_cd_7, 'expl_cd': expl_cd_7, 'n': 7}

        results = [data_0, data_1, data_2, data_3, data_4, data_5, data_6, data_7]

        state[CoordSectionSolver.name] = results


# Определение наседающих масс
class PressMassSolver:
    name = 'st_press_mass_solver'

    preprocessed_data: data = dict(
        corpus_material=None,
        explosive_material=None,
        belt_material=None,

        res_geo=None,
        res_section=None,
        res_mcc=None
    )

    def preprocessor(self, data: dict, global_state: dict):
        self.preprocessed_data['corpus_material'] = data['materials']['corpus']
        self.preprocessed_data['explosive_material'] = data['materials']['explosive']
        self.preprocessed_data['belt_material'] = data['materials']['belt']

        self.preprocessed_data['res_geo'] = global_state['geometry_solver']
        self.preprocessed_data['res_section'] = global_state['st_section_solver']
        self.preprocessed_data['res_mcc'] = global_state['mcc_solver']

    @staticmethod
    # Считаем основные параметры для конуса
    def get_params_conus(r1, r2, x1, x2, rho):
        if r1 < r2:
            r1, r2 = r2, r1
            x1, x2 = x2, x1

        hi = min(x1, x2)
        h = max(x1,  x2) - hi

        lambd = r2 / r1
        # Положение цм конуса
        beta = (1 + 2 * lambd + 3 * lambd**2) / (4 * (1 + lambd + lambd**2))
        ksi = beta * h
        xc = ksi + hi

        #Объём конуса
        V =  (np.pi / 3) * (r1 ** 2 + r1 * r2 + r2 ** 2) * h
        #Масса
        q = V * rho
        #Статический момент
        S = q * xc

        # Осевой момент конуса
        mu = 0.3 * (1 + lambd + lambd**2 + lambd**3 + lambd**4) / (1 + lambd + lambd**2)
        r_xc = r1 + (r2 - r1) / (x2 - x1) * (xc - x1)
        Av = mu * V * r_xc**2
        A = Av * rho

        # Экваториальный момент конуса относительно донного среза (B')
        vu = (3 * (1 + lambd)**4 + 4 * lambd**2) / (80 * (1 + lambd + lambd**2)**2)
        Bv = 0.5 * Av + V * (vu * h**2 + xc**2)
        B_sh = Bv * rho

        # Левая часть статического момента (без плотности)
        res_params = {'h': h, 'V': V, 'S': S, 'q': q, 'xc': xc, 'r_xc': r_xc, 'A': A, 'B_sh': B_sh}
        return res_params

    @staticmethod
    # Считаем основные параметры для цилиндра
    def get_params_cyl(r, x1, x2, rho):
        h = abs(x1 - x2)
        lambd = 1
        beta = 0.5
        # Положение цм цилиндра
        hi = min(x1, x2)
        ksi = beta * h
        xc = ksi + hi

        #Объём цилиндра
        V =  np.pi * r**2 * h
        #Масса
        q = V * rho
        #Статический момент
        S = q * xc
        # Осевой момент цилиндра
        mu = 0.5
        r_xc = r
        Av = mu * V * r_xc**2
        A = Av * rho
        # Экваториальный момент цилиндра относительно донного среза (B')
        vu = (3 * (1 + lambd)**4 + 4 * lambd**2) / (80 * (1 + lambd + lambd**2)**2)
        Bv = 0.5 * Av + V * (vu * h**2 + xc**2)
        B_sh = Bv * rho
        res_params = {'h': h, 'V': V, 'S': S, 'q': q, 'xc': xc, 'r_xc': r_xc, 'A': A, 'B_sh': B_sh}

        return res_params

    # Определения массовых параметров корпуса в заданном сечении
    def solve_corp(self, corp_coord):
        rho = self.p_data['corpus_material']['rho']
        x_coord = corp_coord[0]
        y_coord = corp_coord[1]
        count_nodes = len(x_coord)
        V, S, q, A, B_sh = 0, 0, 0, 0, 0

        for i in range(1, count_nodes):
            if x_coord[i] == x_coord[i - 1]:
                continue

            elif y_coord[i] == y_coord[i - 1]:
                cyl = self.get_params_cyl(r=y_coord[i], x1=x_coord[i], x2=x_coord[i - 1], rho=rho)

                if x_coord[i] > x_coord[i - 1]:
                    V += cyl['V']
                    S += cyl['S']
                    q += cyl['q']
                    A += cyl['A']
                    B_sh += cyl['B_sh']
                    # print('+Цилиндр', cyl['q'])
                else:
                    V -= cyl['V']
                    S -= cyl['S']
                    q -= cyl['q']
                    A -= cyl['A']
                    B_sh -= cyl['B_sh']
                    # print('-Цилиндр', cyl['q'])
            else:
                konus = self.get_params_conus(r1=y_coord[i], r2=y_coord[i - 1], x1=x_coord[i], x2=x_coord[i - 1],
                                          rho=rho)
                if x_coord[i] > x_coord[i - 1]:
                    V += konus['V']
                    S += konus['S']
                    q += konus['q']
                    A += konus['A']
                    B_sh += konus['B_sh']
                    # print('+Конус', konus['q'])
                else:
                    V -= konus['V']
                    S -= konus['S']
                    q -= konus['q']
                    A -= konus['A']
                    B_sh -= konus['B_sh']
                    # print('-Конус', konus['q'])
        # print('---------------------------------------')

        result_params = {'V': V, 'S': S, 'q': q, 'A': A, 'B_sh': B_sh}

        return result_params

    # Определения массовых параметров ВВ в заданном сечении
    def solve_explosive(self, expl_coord):
        rho = self.p_data['explosive_material']['rho']
        x_coord = expl_coord[0]
        y_coord = expl_coord[1]
        count_nodes = len(x_coord)
        V, S, q, A, B_sh = 0, 0, 0, 0, 0

        for i in range(1, count_nodes - 1):

            if x_coord[i] == x_coord[i - 1]:
                continue

            elif y_coord[i] == y_coord[i - 1]:
                if x_coord[i] > x_coord[i - 1]:
                    # Параметры цилиндрической части ВВ
                    cyl = self.get_params_cyl(r=y_coord[i], x1=x_coord[i], x2=x_coord[i - 1], rho=rho)
                    V += cyl['V']
                    S += cyl['S']
                    q += cyl['q']
                    A += cyl['A']
                    B_sh += cyl['B_sh']
                else:
                    # Параметры очка под дно взрывателя
                    och = self.get_params_cyl(r=y_coord[i], x1=x_coord[i], x2=x_coord[i - 1], rho=rho)
                    V -= och['V']
                    S -= och['S']
                    q -= och['q']
                    A -= och['A']
                    B_sh -= och['B_sh']
            else:
                # Параметры конусной части ВВ
                konus = self.get_params_conus(r1=y_coord[i], r2=y_coord[i - 1], x1=x_coord[i], x2=x_coord[i - 1], rho=rho)
                V += konus['V']
                S += konus['S']
                q += konus['q']
                A += konus['A']
                B_sh += konus['B_sh']

        result_params = {'V': V, 'S': S, 'q': q, 'A': A, 'B_sh': B_sh}
        return result_params


    # Определение массы воображаемого цилиндра
    def solve_imag_cyl(self, resMass):
        expl = self.p_data['res_geo']['explosive_coord']
        max_exp_x = max(expl[0])
        x2 = np.zeros(8)
        h = np.zeros(8)
        q_0 = np.zeros(8)
        q_1 = np.zeros(8)
        q = np.zeros(8)

        # Считаем: точки пересчения цилиндра с каморой, высоту, массы цилиндров (без прибавки)
        for i in range(8):

            r = resMass['r'][i]
            x = resMass['x_sec'][i]
            mask = expl[0, :] <= x
            cur_coord = np.delete(expl, mask, axis=1)

            mask = cur_coord[1, :] > r
            cur_coord = np.delete(cur_coord, mask, axis=1)

            if r < expl[1, -5]:
                x2[i] = max_exp_x
            elif x >= max_exp_x:
                x2[i] = x
            else:
                x2[i] = cur_coord[0, 0] + (cur_coord[0, 1] - cur_coord[0, 0]) / (
                        cur_coord[1, 1] - cur_coord[1, 0]) * (r - cur_coord[1, 0])

            # Сразу же находим высоту цилиндра
            h[i] = x2[i] - x

            # Зануляем размеры, близкие к нулю (ибо у нас не реальное оживало, а конусы)
            if h[i] < 1e-3:
                h[i] = 0.0

            # Считаем массы воображаемых цилиндров (без прибавки)
            q_0[i] = (np.pi * h[i] * resMass['r'][i] ** 2) * self.p_data['explosive_material']['rho']

            # Считаем массу ВВ, выше сечения разреза
            x = resMass['x_sec'][i]
            mask = expl[0, :] < x2[i]
            cur_coord = np.delete(expl, mask, axis=1)
            if cur_coord.any():
                q_1[i] = self.solve_explosive(cur_coord)['q']
            else:
                q_1[i] = 0.0

            # Общая масса воображаемого цилиндра
            q = q_0 + q_1

        return q

    def run(self, data: dict, state: dict):
        self.p_data = self.preprocessed_data

        n_sec = []
        x_sec = []
        q_expl = []
        q_corp = []
        q_shell = []
        R_size = []
        r_size = []

        for data in self.p_data['res_section']:
            n_sec.append(data['n'])
            r_size.append(data['r'])
            R_size.append(data['R'])
            x_sec.append(data['x'])
            q_expl.append(self.solve_explosive(data['expl_cd'])['q'])
            q_corp.append(self.solve_corp(data['corp_cd'])['q'])

        # Корректировка массы корпуса (вычитание массы канавки)
        q_grove = self.p_data['res_mcc']['corp']['q_grove']
        q_corp[1] -= q_grove
        q_corp[5] -= q_grove
        q_corp[0] -= q_grove / 2

        # Суммарная наседающая масса
        q_fuse = self.p_data['res_mcc']['fuse']['q']
        q_belt = self.p_data['res_mcc']['belt']['q']
        q_shell.append(q_corp[0] + q_expl[0] + q_fuse + q_belt / 2)
        q_shell.append(q_corp[1] + q_expl[1] + q_fuse + q_belt)
        q_shell.append(q_corp[2] + q_expl[2] + q_fuse)
        q_shell.append(q_corp[3] + q_expl[3] + q_fuse)
        q_shell.append(q_corp[4] + q_expl[4] + q_fuse)
        q_shell.append(q_corp[5] + q_expl[5] + q_fuse + q_belt)
        q_shell.append(q_corp[6] + q_expl[6] + q_fuse)
        q_shell.append(q_corp[7] + q_expl[7] + q_fuse)

        results = {'n_sec': n_sec, 'x_sec': x_sec, 'R': R_size, 'r': r_size, 'q_corp': q_corp, 'q_shell': q_shell, 'q_expl': q_expl}

        # Воображаемые цилиндры
        q_expl_imag = self.solve_imag_cyl(results)
        results['q_expl_imag'] = q_expl_imag

        state[PressMassSolver.name] = results

# Расчёт давлений и напряжений в корпусе снаряда
class StressSolver:
    name = 'st_stress_solver'

    preprocessed_data: data = dict(
        Pmax=None,
        qp_max=None,
        a=None,
        b=None,
        d_d=None,
        d_p=None,
        f0=None,
        V=None,
        mu=None,
        q=None,
        n=None,
        eta_n=None,
        eta_k=None,
        Ln=None,
        C=None,
        mu_c=None,
        rho_w=None,
        res_press_mass=None
    )

    def preprocessor(self, data: dict, global_state: dict):
        self.preprocessed_data['qp_max'] = data['settings']['strength']['qp_max']
        self.preprocessed_data['Pmax']=data['initial_cond']['Pmax']
        self.preprocessed_data['V']=data['initial_cond']['V']
        self.preprocessed_data['C'] = data['shell_size']['R3']
        self.preprocessed_data['a']=data['gun_char']['a']
        self.preprocessed_data['b']=data['gun_char']['b']
        self.preprocessed_data['d_d']=data['gun_char']['d_dn']
        self.preprocessed_data['d_p']=data['gun_char']['d']
        self.preprocessed_data['n']=data['gun_char']['n']
        self.preprocessed_data['eta_n']=data['gun_char']['eta_n']
        self.preprocessed_data['eta_k']=data['gun_char']['eta_k']
        self.preprocessed_data['Ln']=data['gun_char']['l_n']
        self.preprocessed_data['f0']=data['materials']['belt']['f0']
        self.preprocessed_data['mu_c']=data['materials']['explosive']['mu']
        self.preprocessed_data['rho_w']=data['materials']['explosive']['rho']
        self.preprocessed_data['mu']=global_state['mcc_solver']['shell']['mu']
        self.preprocessed_data['q']=global_state['mcc_solver']['shell']['q']


        self.preprocessed_data['res_press_mass']=global_state['st_press_mass_solver']

    # Определяем координаты для каждого сечения
    def run(self, data: dict, state: dict):
        p_data = self.preprocessed_data

        Pmax = p_data['Pmax']
        a = p_data['a']
        b = p_data['b']
        d_d = p_data['d_d']
        d_p = p_data['d_p']
        f0 = p_data['f0']
        V = p_data['V']
        mu = p_data['mu']
        q = p_data['q']
        n = p_data['n']
        alpha_n = np.arctan(np.pi / p_data['eta_n'])
        alpha_k = np.arctan(np.pi / p_data['eta_k'])
        Ln = p_data['Ln']
        C = p_data['C']
        mu_c = p_data['mu_c']
        rho_w = p_data['rho_w']
        qp = p_data['qp_max']

        # Рабочая ширина ведущего пояска
        lp = C * 0.9

        # Расчётное давление ПГ
        P = 1.1 * Pmax
        # Приведенный радиус канала ствола
        R_pr = 0.5 * np.sqrt((a * d_p ** 2 + b * d_d ** 2) / (a + b))

        # Реакция боевой грани нареза
        v = 0.5 * V
        # Угол нарезки при макс. давлении ПГ
        alpha = (2 * alpha_n + alpha_k) / 3
        k = (np.tan(alpha_k) - np.tan(alpha_n)) / Ln
        N = mu / n * (P * np.pi * R_pr ** 2 * np.tan(alpha) + k * q * v ** 2)

        # Сила споротивления движению
        fv = (1 + 0.0213 * v) / (1 + 0.133 * v) * f0
        T_N = N * n * np.cos(alpha) * (np.tan(alpha) + fv)
        T_1 = T_N / (P * np.pi * R_pr ** 2)
        # qp = 300E6
        T_qp = qp * n * (a + b) * lp * fv * np.cos(alpha)
        T_2 = T_qp / (P * np.pi * R_pr ** 2)
        T_0 = T_1 + T_2

        # Напряжения в поперечных сечениях корпуса
        # Продольные силы в сечениях корпуса выше ВП (включая 0 сечение)
        mass = p_data['res_press_mass']
        Nx = np.zeros(8)
        for i in (0, 2, 4, 3, 7, 6):
            Nx[i] = P * np.pi * R_pr ** 2 * (1 - T_0) * (mass['q_shell'][i] / q)

        for i in (1, 5):
            Nx[i] = P * np.pi * R_pr ** 2 * (1 - T_0) * (
                        mass['q_shell'][i] / q - 1 + mass['R'][i] ** 2 / ((1 - T_0) * R_pr ** 2))

        # Определение нормальных напряжений в сечениях корпуса и ВВ
        sigma_x = np.zeros(8)
        sigma_xw = np.zeros(8)
        for i in range(8):
            sigma_x[i] = - Nx[i] / (np.pi * (mass['R'][i] ** 2 - mass['r'][i] ** 2))
            if mass['x_sec'][i] <= mass['x_sec'][2]:
                sigma_xw[i] = - (P * (R_pr ** 2 / mass['r'][i] ** 2) * (mass['q_expl_imag'][i] / q)) * (1 - T_0)
            else:
                sigma_xw[i] = - (P * (R_pr ** 2 / mass['r'][i] ** 2) * (mass['q_expl'][i] / q)) * (1 - T_0)
                # В ЛР4 В ЭТУ ФОРМУЛУ ПОЧЕМУ ТО ПОДСТАВЛЯЕТСЯ НЕ МАССА ВВ, А МАССА В ВООБРАЖАЕМОМ ЦИЛИНДРЕ

        # self.test_plot(x=mass['x_sec'], y=-sigma_x)
        # self.test_plot(x=mass['x_sec'], y=-sigma_xw)

        # Давление снаряжения
        # Определеяем порядок заполнения массивов, посколько 2 и 4 сечения могут меняться
        if mass['x_sec'][4] > mass['x_sec'][2]:
            order_up = (2, 4, 3, 7, 6)
            order_down = (5, 0)  # 1 и 2 сечения не учитываются
        else:
            order_up = (2, 3, 7, 6)
            order_down = (5, 0, 4)

        # Давление на цилиндрическую и оживальную части каморы (обычно только для 4, 2, 3, 7, 6 сечений)
        Pc = np.empty(8)
        Pc[:] = np.nan
        Pc_sh = np.zeros(8)

        for i in order_up:
            Pc[i] = mu_c * np.abs(sigma_xw[i]) / (1 - mu_c)
            Pc_sh[i] = Pc[i]

        # Давление снаряжения в конусной части каморы

        # Давление во 2 сечении
        fi = mass['r'][1] / mass['r'][2]
        H = mass['x_sec'][2] - mass['x_sec'][1]
        Kpc = (H * np.pi * mass['r'][2] ** 2) / (mass['q_expl'][2] / rho_w)
        lambd = (1 - mu_c) * (1 + mu_c - (1 - 2 * mu_c) * fi ** 3) / (mu_c * (1 + mu_c + 2 * (1 - 2 * mu_c) * fi ** 3))
        lambd += (1 + mu_c) * (1 - 2 * mu_c) * (1 - fi) * (1 + 2 * fi + 3 * fi ** 2) / (
                    4 * mu_c * (1 + mu_c + 2 * (1 - 2 * mu_c) * fi ** 3)) * Kpc
        Pc_sh[2] = Pc[2] * lambd

        # Давление в 1 сечении
        kappa = 6 * (1 - mu_c) + Kpc * (3 + (1 - 2 * mu_c) * (fi ** 3 * fi ** 2 + fi))
        kappa /= 2 * (1 + mu_c) + 4 * (1 - 2 * mu_c) * fi ** 3
        Pc_sh[1] = Pc[2] * kappa

        # Интерполяция напряжений по конусу (поскольку их распределение имеет линейный закон)
        for i in order_down:
            Pc_sh[i] = np.interp(mass['x_sec'][i], [mass['x_sec'][1], mass['x_sec'][2]], [Pc_sh[1], Pc_sh[2]])

        # Расчёт радиальных и тангенциальных напряжений
        Pr = np.array([0, P, 0, 0, 0, P, 0, 0])
        sigma_r = np.zeros(8)
        sigma_t = np.zeros(8)

        for i in range(8):
            K = mass['R'][i] ** 2 / mass['r'][i] ** 2
            sigma_r[i] = ((Pc_sh[i] - K * Pr[i]) / (K - 1)) - ((Pc_sh[i] - Pr[i]) / (K - 1)) * K
            sigma_t[i] = ((Pc_sh[i] - K * Pr[i]) / (K - 1)) + ((Pc_sh[i] - Pr[i]) / (K - 1)) * K

        # Расчёт приведенных напряжений
        sigma_pr = np.zeros(8)

        for i in range(8):
            # Сортируем значения (от меньшего к большему)
            s = np.array([sigma_x[i], sigma_r[i], sigma_t[i]])
            s.sort(kind='quicksort')
            sigma_pr[i] = 1 / np.sqrt(2) * np.sqrt((s[2] - s[1]) ** 2 + (s[1] - s[0]) ** 2 + (s[0] - s[2]) ** 2)

        results = {'sigma_x': sigma_x, 'sigma_xw': sigma_xw, 'sigma_r': sigma_r, 'sigma_t': sigma_t, 'sigma_pr': sigma_pr,
               'Pc': Pc, 'Pc_sh': Pc_sh,
               'other': {'P': P, 'R_pr': R_pr, 'qp': qp, 'N': N, 'T_N': T_N, 'T_qp': T_qp, 'T_0': T_0}}

        state[StressSolver.name] = results

# Расчёт коэфф. запаса по пределу текучести материала корпуса снаряда
class SafeFactorSolver:
    name = 'st_safe_factor_solver'

    preprocessed_data: data = dict(
        L_n=None,
        V=None,
        E=None,

        res_stress=None
    )

    def preprocessor(self, data: dict, global_state: dict):
        self.preprocessed_data['res_stress'] = global_state['st_stress_solver']
        self.preprocessed_data['Ln'] = data['gun_char']['l_n']
        self.preprocessed_data['V'] = data['initial_cond']['V']
        self.preprocessed_data['E'] = data['materials']['corpus']['E']
        self.preprocessed_data['sigma_t'] = data['materials']['corpus']['sigma_t']



    # Определяем координаты для каждого сечения
    def run(self, data: dict, state: dict):
        p_data = self.preprocessed_data
        sigma_pr_max = np.max(p_data['res_stress']['sigma_pr']) * 1e-9 # в ГПа

        # Время нарастания давления до макс. значения
        t_d = p_data['Ln'] / (0.5 * p_data['V'])
        t_Pm = 0.3 * t_d

        # Скорость нагружения (в ГПа/с)
        sigma_sh = sigma_pr_max / t_Pm

        # Скорость деформации
        E = p_data['E'] * 1e-9  # в ГПа
        eps = sigma_sh / E

        # Расчёт коэффициента динамичности
        if p_data['sigma_t'] < 1e9:
            n = 0.8
        else:
            n = 2

        sigma_t = p_data['sigma_t'] * 1e-9  # в ГПа
        A = 1 + 0.1 * 3 ** (0.22 * np.log(eps))
        Kt = 1 + np.log(A) / (1.35 * sigma_t ** n)

        # Динамический предел текучести материала корпуса снаряда
        sigma_dt = sigma_t * 1e9 * Kt  # в Па

        # Расчёт коэффициента запаса
        sigma_pr_max *= 1e9
        nz = sigma_dt / sigma_pr_max

        results = {'nz': nz, 'sigma_pr_max': sigma_pr_max, 'sigma_dt': sigma_dt, 't_Pm': t_Pm, 'sigma_sh': sigma_sh,
                   'eps': eps, 'Kt': Kt}

        state[SafeFactorSolver.name] = results

# Расчёт толщины дна снаряда
class BottomThickSolver:
    name = 'st_bottom_thick_solver'

    preprocessed_data: data = dict(
        Pmax=None,
        q=None,
        rho_d=None,
        # sigma_tsh=None,
        sigma_dt=None,
        Ef=None,
        res_press_mass=None,
        res_stress=None
    )

    def preprocessor(self, data: dict, global_state: dict):
        self.preprocessed_data['rho_d'] = data['materials']['corpus']['rho']
        self.preprocessed_data['Pmax'] = data['initial_cond']['Pmax']
        self.preprocessed_data['q'] = global_state['mcc_solver']['shell']['q']
        self.preprocessed_data['sigma_dt'] = global_state['st_safe_factor_solver']['sigma_dt']
        # self.preprocessed_data['sigma_tsh'] = data['materials']['corpus']['sigma_tsh']
        self.preprocessed_data['Ef'] = data['materials']['corpus']['Ef']
        self.preprocessed_data['res_stress'] = global_state['st_stress_solver']
        self.preprocessed_data['res_press_mass'] = global_state['st_press_mass_solver']


    # Определяем координаты для каждого сечения
    def run(self, data: dict, state: dict):
        p_data = self.preprocessed_data

        p_sd = p_data['res_stress']['Pc_sh'][1]
        hd = p_data['res_press_mass']['x_sec'][1]
        r1 = p_data['res_press_mass']['r'][1]
        R1 = p_data['res_press_mass']['R'][1]
        rho_d = p_data['rho_d']

        # Масса дна снаряда (только по внутр. радиусу)
        qd = np.pi * r1**2 * hd * rho_d

        # Приведенное к срединной поверхности дна осевое давления
        Pr = p_data['Pmax'] * 1.1
        q = p_data['q']
        w_v1 = p_data['res_press_mass']['q_expl_imag'][1]
        Rpr = p_data['res_stress']['other']['R_pr']
        poc = Pr * (1 - Rpr**2/r1**2 * ((w_v1 + qd)/q))

        # Коэффициент связи дна со стенками корпуса
        hc = R1 - r1
        K = (1 + 0.4 * (hd/hc)**3)**-1

        # ОСНОВНЫЕ РАСЧЁТЫ
        # Толщина дна, обеспечивающая прочность на изгиб
        # по оси симметрии:
        mu_d = 1/3

        # ПРИМЕЧАНИЕ. По методичке М.Я. Водопьянова нужно подставлять условный предел текучести меди, однако тогда расчёт
        # по периметру дна показывает очень большую мин. доп. толщину. Было принято решения учитывать динамический
        # предел текучести материала (по рекомендации Кравцова В.О.)

        # sigma_tsh = p_data['sigma_tsh']
        sigma_dt = p_data['sigma_dt']
        h1_sh = r1 / 2 * np.sqrt((3 * poc  / (2 * (sigma_dt - p_sd))) * (3 + mu_d - 2 * K))
        # # по периметру дна:

        h2_sh = r1 / 2 * np.sqrt((3 * poc / (sigma_dt - Pr)) * K)  # ПОКА НЕ УЧИТЫВАЕМ, СЧИТАЕТСЯ ОЧЕНЬ СТРАННО


        # Расчёт дна на срезание
        # h3_sh = poc * r1 / sigma_dt

        # Прогиб посередине дна снаряда
        Ef = p_data['Ef']
        f = 0.5 * (r1**4 / hd **3) * (poc / Ef)

        # Критическое давление
        pkr = 2.42 * sigma_dt * (hd / r1)**2

        results = {'hd': hd, 'h1_sh': h1_sh, 'h2_sh': h2_sh, 'f': f, 'pkr': pkr, 'poc': poc, 'p_sd': p_sd, 'qd': qd,
                   'K': K}


        state[BottomThickSolver.name] = results

# Расчёт деформации ВСЕХ цилиндрических частей корпуса снаряда (2, 4, 3 сечения)
class DeformCylSolver:
    name = 'st_deform_cyl_solver'

    preprocessed_data: data = dict(
        sigma_dt=None,
        lambd=None,
        Ef=None,
        mu=None,

        res_press_mass=None,
        res_stress=None

    )

    def preprocessor(self, data: dict, global_state: dict):
        self.preprocessed_data['sigma_dt'] = global_state['st_safe_factor_solver']['sigma_dt']
        self.preprocessed_data['lambd'] = data['materials']['corpus']['lambda']
        self.preprocessed_data['Ef'] = data['materials']['corpus']['Ef']
        self.preprocessed_data['mu'] = data['materials']['corpus']['mu']

        self.preprocessed_data['res_press_mass'] = global_state['st_press_mass_solver']
        self.preprocessed_data['res_stress'] = global_state['st_stress_solver']
    # Определяем координаты для каждого сечения
    def run(self, data: dict, state: dict):
        p_data = self.preprocessed_data

        # Общие данные по корпусу
        sigma_dt = p_data['sigma_dt']
        lambd = p_data['lambd']
        Ef = p_data['Ef']
        mu = p_data['mu']

        sec = (2, 4, 3)
        results = {}

        for i in sec:
            sigma_xi = p_data['res_stress']['sigma_x'][i]
            sigma_ti = p_data['res_stress']['sigma_t'][i]
            sigma_intens = np.sqrt(sigma_xi**2 + sigma_ti**2 - sigma_xi * sigma_ti)
            R = p_data['res_press_mass']['R'][i]

            # Если деформации пластические
            if sigma_intens >= sigma_dt:
                def_type = 'Пластические'
                deltaDi = R * ((sigma_intens - sigma_dt * lambd) /
                              (Ef * (1 - lambd) * sigma_intens)) * (2*sigma_ti - sigma_xi)
                deltaDi_ost = R * (((sigma_intens - sigma_dt) * lambd) /
                              (Ef * (1 - lambd) * sigma_intens)) * (2*sigma_ti - sigma_xi)
            # Если деформации упругие
            else:
                def_type='Упругие'
                deltaDi = 2 * R * (sigma_ti - mu * sigma_xi) / Ef
                deltaDi_ost = 0.

            # Добавляем сечение в словарь с результатами
            results[i] = dict(def_type=def_type, deltaDi=deltaDi, deltaDi_ost=deltaDi_ost, sigma_intens=sigma_intens)

        state[DeformCylSolver.name] = results

# Расчёт жёсткости и устойчивости ЗП части корпуса
class RampCorpSolver:
    name = 'st_ramp_corp_solver'

    preprocessed_data: data = dict(
        Pmax=None,
        sigma_tsh=None,
        eps_sh=None,
        lambd=None,

        res_press_mass=None,
        res_stress=None
    )

    def preprocessor(self, data: dict, global_state: dict):
        self.preprocessed_data['Pmax'] = data['initial_cond']['Pmax']
        self.preprocessed_data['lambd'] = data['materials']['corpus']['lambda']
        self.preprocessed_data['eps_sh'] = data['materials']['corpus']['eps_sh']
        self.preprocessed_data['sigma_tsh'] = data['materials']['corpus']['sigma_tsh']

        self.preprocessed_data['res_press_mass'] = global_state['st_press_mass_solver']
        self.preprocessed_data['res_stress'] = global_state['st_stress_solver']

    # Определяем координаты для каждого сечения
    def run(self, data: dict, state: dict):
        p_data = self.preprocessed_data
        status = 'не определено'
        # параметры для расчёта
        r5 = p_data['res_press_mass']['r'][5]
        R5 = p_data['res_press_mass']['R'][5]
        Pm = p_data['Pmax']
        Pcd_5 = p_data['res_stress']['Pc_sh'][5]
        sigma_tsh = p_data['sigma_tsh']
        lambd = p_data['lambd']
        eps_sh = p_data['eps_sh']
        sigma_x5 = p_data['res_stress']['sigma_x'][5]
        l = p_data['res_press_mass']['x_sec'][0] - p_data['res_press_mass']['x_sec'][1]

        # Выполнение расчёта
        ro_5 = r5 / R5
        Prasch = 1.1 * Pm

        # Расчёт действительного радиального давления
        q_oc = np.abs(sigma_x5) / sigma_tsh - (Prasch - Pcd_5 * ro_5 ** 2) / (sigma_tsh * (1 - ro_5 ** 2))

        P_rad = ((Prasch - Pcd_5) * np.sqrt(3)) / (sigma_tsh * (1 - ro_5 ** 2))
        u = ((1 - ro_5 ** 2) / (2 * ro_5 ** 2 * abs(q_oc))) * np.sqrt(
            (((1 + ro_5 ** 2) / (1 - ro_5 ** 2)) ** 2 - q_oc ** 2) * (1 - q_oc ** 2))

        # Расчёт первого критического давления
        Pkr1 = (1 / (1 - ro_5 ** 2)) * np.log(
            ((u + np.sqrt(1 + u ** 2)) / (ro_5 ** 2 * u + np.sqrt(1 + ro_5 ** 4 * u ** 2))))

        # Расчёт второго критического давления
        deltaPkr1 = ((u + 1 / (ro_5 ** 2 * u)) / (np.sqrt(1 + ro_5 ** 4 * u ** 2))) - (
                np.abs(q_oc) / (ro_5 ** 2 * u)) - Pkr1
        Pkr2 = Pkr1 + deltaPkr1 * (1 - lambd)

        # Третье критическое давление
        x_5 = l
        Pkr3 = 24.6 * ((1 - lambd) / (eps_sh * (1 + np.sqrt(1 - lambd)) ** 2)) * ((1 - ro_5) ** 2 / (1 + ro_5) ** 4) * \
               (1 + 3.4 * ((R5 + r5) / x_5) ** 4)


        # Прогиб наружней поверхности корпуса снаряда
        k = q_oc/np.abs(q_oc) * -1  # меняем знак для последнего множителя формул
        # Если мы в упругой зоне, считаем упругий прогиб
        if P_rad < Pkr1:
            Wh_sh = (np.sqrt(3) / 2) * eps_sh * r5 * (P_rad - (q_oc / (ro_5 * np.sqrt(3))))
            status = 'материал в упругой зоне'
        # Если мы в сложно-напряженном состоянии
        elif Pkr1 <= P_rad < Pkr2:
            Wh_sh = (np.sqrt(3) / 2) * eps_sh * r5 * (1 / np.sqrt(1 + u ** 2 * ro_5 ** 4)) * (
                        u + (k * (1 / (ro_5 * np.sqrt(3)))))
            status = 'материал в упруго-пластической зоне'
        # Если мы в пластической зоне
        elif Pkr2 <= P_rad < Pkr3:
            Wh_sh = (np.sqrt(3) / 2) * eps_sh * r5 * (1 / (np.sqrt(1 + u ** 2 * ro_5 ** 4)) +
                                                       ((u * ro_5 ** 2) / (1 + ro_5 ** 2 * u ** 2)) * (
                                                                   (P_rad - Pkr2) / (1 - lambd))) * (
                                 u + (k * (1 / (ro_5 * np.sqrt(3)))))
            status = 'материал в пластической зоне'

        # Влияние близости дна
        a_5 = (R5 + r5) / 2
        h_5 = R5 - r5
        Y_5 = 0.5 * (np.sqrt(3) / np.sqrt(2)) * (l / np.sqrt(a_5 * h_5))
        k_s = 1 - (np.cos(Y_5) + np.sin(Y_5)) * np.exp(-Y_5)


        # Прогиб стенки корпуса снаряда
        WH = k_s * Wh_sh

        # Прогиб срединной поверхности
        W_sr = WH * (1 + h_5 / (2 * a_5))

        # Остаточный прогиб срединной поверхности
        WH_sh_elc = (np.sqrt(3) / 2) * eps_sh * r5 * (P_rad - (q_oc / (ro_5 * np.sqrt(3)))) # упругая состовляющая
        WH_zv = WH - WH_sh_elc * k_s # отнимаем из общего прогиба упругую составляющую с учётом близости дна



        # Допустимое значение прогиба (РАССЧИТЫВАЕТСЯ В 7 ЛР!!!)
        results = {'P_rad': P_rad, 'Pkr1': Pkr1, 'Pkr2': Pkr2, 'Pkr3': Pkr3, 'W5': W_sr, 'WH5': WH, 'WH5_ost': WH_zv,
                   'q_oc': q_oc, 'k_s': k_s, 'l': l, 'status': status}

        state[RampCorpSolver.name] = results

# Расчёт зоны ведущего пояска
class BeltZoneSolver:
    name = 'st_belt_zone_solver'

    preprocessed_data: data = dict(
        d=None,
        l1=None,
        l2=None,
        n=None,
        f=None,
        hb=None,
        delta=None,
        c=None,
        rp=None,
        rzp=None,

        type_material=None,
        lambd=None,
        sigma_sh=None,
        eps_sh=None,
        eps_b=None,
        E=None,
        Ef=None,
        Est=None,
        sigma_Tp=None,

        res_section = None,
        res_press_mass=None,
        res_stress=None,
        res_ramp=None,
        belt_coord=None,
    )

    def preprocessor(self, data: dict, global_state: dict):
        self.preprocessed_data['d'] = data['gun_char']['d']
        self.preprocessed_data['l1'] = data['gun_char']['a']
        self.preprocessed_data['l2'] = data['gun_char']['b']
        self.preprocessed_data['n'] = data['gun_char']['n']
        self.preprocessed_data['f0'] = data['materials']['belt']['f0']
        self.preprocessed_data['hb'] = data['belt_coord']['hb']
        self.preprocessed_data['delta'] = data['gun_char']['t']
        self.preprocessed_data['c'] = data['shell_size']['R3']
        self.preprocessed_data['rp'] = data['shell_size']['R17']
        self.preprocessed_data['rzp'] = data['shell_size']['r']

        self.preprocessed_data['lambd'] = data['materials']['corpus']['lambda']
        self.preprocessed_data['sigma_sh'] = data['materials']['corpus']['sigma_tsh']
        self.preprocessed_data['eps_sh'] = data['materials']['corpus']['eps_sh']
        self.preprocessed_data['eps_b'] = data['materials']['corpus']['eps_b']
        self.preprocessed_data['E'] = data['materials']['corpus']['E']
        self.preprocessed_data['Ef'] = data['materials']['corpus']['Ef']
        self.preprocessed_data['sigma_Tp'] = data['materials']['belt']['sigma_t']
        self.preprocessed_data['Est'] = data['materials']['gun']['E']
        self.preprocessed_data['type_material'] = data['materials']['corpus']['type']


        self.preprocessed_data['res_section'] = global_state['st_section_solver']
        self.preprocessed_data['res_press_mass'] = global_state['st_press_mass_solver']
        self.preprocessed_data['res_stress'] = global_state['st_stress_solver']
        self.preprocessed_data['res_ramp'] = global_state['st_ramp_corp_solver']
        self.preprocessed_data['belt_coord'] = global_state['geometry_solver']['belt_coord']

    # Расчёт площади пояска выше сечения
    def calc_F(self, belt_coord):
        coord = belt_coord

        # Ставим поясок на ось
        x_coord = coord[0, 1:-2]
        y_coord = coord[1, 1:-2] - belt_coord[1, 1]
        count_nodes = len(x_coord)
        ind = 1
        S = 0

        for ind in range(1, count_nodes):
            if x_coord[ind] == x_coord[ind - 1]:
                ind += 1
            elif y_coord[ind] == y_coord[ind - 1]:
                S_cur = (x_coord[ind] - x_coord[ind-1]) * y_coord[ind]
                S += S_cur
                ind += 1
            else:
                S_cur = (y_coord[ind-1] + y_coord[ind]) / 2 * (x_coord[ind] - x_coord[ind-1])
                S += S_cur
                ind += 1

        return S



    # Определяем координаты для каждого сечения
    def run(self, data: dict, state: dict):

        # Расчёт параметров кривой врезания
        def calc_coef(curr_lambd, qN_g, qPR):

            if curr_lambd == 0:
                A = ((2 * sigma_sh * h0) / c) * np.sqrt(2 * h0 / (3 * a0)) * ((delta + delta_forc) / (a0 * eps_sh))
                B = ((2 * sigma_sh * h0) / c) * np.sqrt(2 * h0 / (3 * a0)) * (delta / (a0 * eps_sh))

            else:
                A = ((2 * sigma_sh * h0) / (c * (1 + h0 / (2 * a0)))) * np.sqrt(2 * h0 / (3 * a0)) * (
                        0.9 * curr_lambd + (1 - 0.9 * curr_lambd) * (1 + h0 / (2 * a0)) * (
                            (delta + delta_forc) / (a0 * eps_sh)))
                B = ((2 * sigma_sh * h0) / (c * (1 + h0 / (2 * a0)))) * np.sqrt((2 * h0) / (3 * a0)) * (
                            1 - 0.9 * curr_lambd) * (
                            1 + h0 / (2 * a0)) * (delta / (a0 * eps_sh))

            # Параметры прямой 0A
            dqp_dKSI_AB = (450 * 1e6 * delta_sh) / (fi_p * hp_sh) * (1 - 0.6 * t_sh)
            KSI_1 = (5.83 * (1 + 2.55 * l1_sh) * (1 - 12 * hb_sh)) / (delta_sh * 1e3)
            q_pA = (312 * 1e6 * l1_sh ** 1.24 * (2 - t_sh)) / fi_p

            # Параметры прямой AB
            k = 1.4 * (1 + 0.00041 * (100 * (hp_sh - delta_sh)) ** np.pi)
            KSI_0 = 0.54 * (1 + 2 * l1_sh) * (1 - l1_sh) * (
                    1 - 1.42 * ((1 - 0.6 * t_sh) / (1 + 0.5 * t_sh)) * hp_sh ** (k - 1)) + \
                    8.3 * 1e-3 * (1 / delta_sh) * (1 + 2.55 * l1_sh) * (1 - 12 * hb_sh) * (
                            (1 - 0.6 * t_sh) / (1 + 0.5 * t_sh)) * hp_sh ** (k - 1) - \
                    1.95 * (1 / delta_sh) * l1_sh ** 1.24 * hp_sh ** k * (1 - 0.5 * t_sh) / (1 + 0.5 * t_sh)
            dq_dKSI_BC = (160 * 1e6 * delta_sh * (2 + t_sh)) / (fi_p * hp_sh ** k)
            KSI_2 = 0.54 * (1 + 2 * l1_sh) * (1 - l1_sh)

            # Координаты точки B
            b_for_func = q_pA - (dqp_dKSI_AB * KSI_1)
            yB = dqp_dKSI_AB * KSI_2 + b_for_func

            # Относительное врезание ведущего пояска
            KSI = (A + KSI_0 * dq_dKSI_BC) / (B + dq_dKSI_BC)

            # Реакция ВП в момент врезания
            qp = dq_dKSI_BC * (KSI - KSI_0)

            # Прогиб срединной поверхности, без учёта коэффициента:
            W0_sh = (delta_forc + delta * (1 - KSI)) * (1 + h0 / (2 * a0))
            x4 = 1.94 * np.sqrt(a0 * h0)

            if l0 <= x4:
                # Кривизна срединной поверхности
                beta = (2 * hd / h0) * np.sqrt(3 * a0 / (2 * h0))
                # Коэффициент учёта близости дна
                kp = 1 - (2 * beta / (beta + 1) + (beta - 1) / (beta + 1) * np.sin(
                    2 * l0 * np.sqrt(3) / np.sqrt(2 * a0 * h0)) - np.cos(
                    2 * l0 * np.sqrt(3) / np.sqrt(2 * a0 * h0))) * np.exp(
                    -(2 * l0 * np.sqrt(3) / (np.sqrt(2 * a0 * h0))))
            else:
                kp = 1

            # ПРОГИБ СРЕДИННОЙ ПОВЕРХНОСТИ ОБОЛОЧКИ
            W0 = W0_sh * kp



            # Вычисление KSI4
            if qN_g is not None:
                if qN_g <= q_pA:
                    x = qN_g / (q_pA / KSI_1)
                    return x
                elif (qN_g > q_pA) and (qN_g <= yB):
                    x = (qN_g - b_for_func) / dqp_dKSI_AB
                    return x
                elif qN_g > yB:
                    x = (qN_g - (qp - (dq_dKSI_BC * KSI))) / dq_dKSI_BC
                    return x

            # Вычисление KSI5
            if qPR is not None:
                if qPR <= q_pA:
                    x = qPR / (q_pA / KSI_1)
                    return x
                elif (qPR > q_pA) and (qPR <= yB):
                    x = (qPR - b_for_func) / dqp_dKSI_AB
                    return x
                elif qPR > yB:
                    x = (qPR - (qp - (dq_dKSI_BC * KSI))) / dq_dKSI_BC
                    return x

            return W0, qp


        p_data = self.preprocessed_data

        # Инициализация исходный данных
        l0 = p_data['res_press_mass']['x_sec'][0] - p_data['res_press_mass']['x_sec'][1]
        hd = p_data['res_press_mass']['x_sec'][1]
        l1 = p_data['l1']
        l2 = p_data['l2']
        d = p_data['d']
        n = p_data['n']
        f0 = p_data['f0']
        N = p_data['res_stress']['other']['N']
        hb = p_data['hb']
        delta = p_data['delta']
        d_dno = d + 2 * delta
        rp = p_data['rp']

        lambd = p_data['lambd']
        sigma_sh = p_data['sigma_sh']
        eps_sh = p_data['eps_sh']
        eps_b = p_data['eps_b']
        E = p_data['E']
        Ef = p_data['Ef']
        sigma_Tp = p_data['sigma_Tp']
        Est = p_data['Est']

        c = p_data['c']
        rzp = p_data['rzp']
        hp = rp - rzp

        F = self.calc_F(p_data['belt_coord'])

        a0 = p_data['res_section'][0]['a0']


        h0 = p_data['res_section'][0]['h0']
        W5 = p_data['res_ramp']['W5']
        a5 = (p_data['res_press_mass']['R'][5] + p_data['res_press_mass']['r'][5]) / 2

        res = {}

        # Ширина полей нарезов
        t = l1 + l2

        # Относительные величины
        t_sh = t / c
        l1_sh = l1 / t
        delta_sh = delta / c
        hp_sh = hp / c
        hb_sh = hb / c


        fi_p = (0.84 * c * hp) / F

        delta_forc = rp - (d_dno / 2)

    # 1. Остаточные деформации корпуса снаряда в зоне ведущего пояска

        # Определение текущего и остаточного значения прогиба стенки и реакции пояска в момент врезания
        W0_curr, qp = calc_coef(lambd, qN_g=None, qPR=None)


        if W0_curr < a0 * eps_sh:
            res['stat_deform'] = 'elastic'
            curr_lambda = 0
            W0_curr, qp = calc_coef(curr_lambda, qN_g=None, qPR=None)
            if W0_curr <= W5:
                eta = (a0 * W5) / (a5 * W0_curr)
            else:
                eta = 1
            # Остаточный прогиб по наружнему диаметру тогда считается при labmda = 0
            WH0 = 0
        else:
            res['stat_deform'] = 'plastic'
            curr_lambda = lambd
            W0_curr, qp = calc_coef(curr_lambda, qN_g=None, qPR=None)

            if W0_curr <= W5:
                eta = (a0 * W5) / (a5 * W0_curr)
            else:
                eta = 1
            WH0 = (2 * eta / (1 + h0 / (2 * a0))) * (W0_curr - (Ef / E) * (0.9 * lambd * a0 * eps_sh +
                                                                           (1 - 0.9 * lambd) * W0_curr))

        # Определение допустимого значения остаточного прогиба корпуса по наружнему диаметру
        WH0_limit = (0.9 * lambd * eta * a0 / (1 + h0 / (2 * a0))) * (eps_b - 2 * eps_sh)
        # Определение допустимого значения остаточного прогиба корпуса по внутреннему диаметру (материал играет роль!)
        if p_data['type_material'] == 'CastIron':
            WBH0_limit = (1.6 * eta * a0 * eps_sh / (1 - h0 / (2 * a0)))
            WBH0_limit *= (eps_b / eps_sh * (1 - (1 - 0.9 * lambd) * Ef / E) - 0.9 * lambd * Ef / E)
        else:
            WBH0_limit = (0.9 * lambd * eta * a0 / (1 - h0 / (2 * a0))) * (eps_b - 2 * eps_sh)
        # Расчёт относительной осевой деформации
        alpha = W0_curr / (a0 * eps_sh)
        beta = 1 + 2 * alpha
        eps_0 = 0.5 * eps_sh * (alpha + 3 * beta / 2)
        eps_1 = eps_0 * (1 + h0 / (2 * a0))

        res['WH0'] = WH0
        res['WH0_limit'] = WH0_limit
        res['WBH0_limit'] = WBH0_limit
        res['eps_0'] = eps_0
        res['eps_1'] = eps_1
        res['W0_curr'] = W0_curr
        res['a0'] = a0
        res['eps_sh'] = eps_sh
        res['qp'] = qp

    # 2. Расчёт прочности ведущего пояска на срез

        # Нормальное напряжение на контактной поверхности
        sigma_N = (N / (delta * c))

        # Минимально необходимое значение реакции ВП

        qN = (E * W5 * h0 / (c * a0 * (1 + h0 / (2 * a0)))) * np.sqrt(2 * h0 / (3 * a0)) - 2 * sigma_Tp / np.sqrt(3) + sigma_N

        # Расчёт KSI4 через функцию для построения графика
        if qN < 0:
            KSI4 = 0
        else:
            KSI4 = calc_coef(curr_lambda, qN_g=qN, qPR=None)
        # Прогиб срединной поверхности
        W0SR = (delta_forc + delta * (1 - KSI4)) * (1 + h0 / (2 * a0))
        # Допустимый прогиб срединной поверхности
        W0SR_lim = (1.8 * 0.96 * eta / (1 + h0 / (2 * a0))) * (W0SR - a0 * eps_sh)
        res['W0SR_lim'] = W0SR_lim
        res['W0SR'] = W0SR
        res['qN'] = qN
        res['KSI4'] = KSI4

    # 3. Расчёт на обтюрацию пороховых газов

        # Коэффициент смятия
        fi_sm = (4 * E / Est) * pow(np.sqrt(2 * h0 / (3 * a0)), 3) * (
                2 * c / d_dno + 2 * np.log(d_dno / (2 * c)) / np.pi) / \
                (1 + pow(2 * c / d_dno, 2))
        # Величина относительного прогиба
        alpha0 = (1 + h0 / (2 * a0)) / (a0 * eps_sh) * (delta_forc + (delta * (l1 / (l1 + l2))))
        # Допустимый прогиб СРЕДИННОЙ ПОВЕРХНОСТИ если деформации упругие
        if W0_curr < a0 * eps_sh:
            W0OB_lim = a0 * eps_sh * alpha0 / (1 + fi_sm)
            res['W0OB_lim'] = W0OB_lim
        # Допустимый остаточный прогиб НАРУЖНОЙ ПОВЕРХНОСТИ если деформации пластические
        else:
            W0OBp_lim = a0 * eps_sh * ((alpha0 - 0.9 * lambd * fi_sm) / (1 + (1 - 0.9 * lambd) * fi_sm))
            WHOB_lim = 2 * eta * (a0 * eps_sh / (1 + h0 / (2 * a0))) * (
                    ((alpha0 - 0.9 * lambd * fi_sm) / (1 + (1 - 0.9 * lambd) * fi_sm)) *
                    (1 - (1 - 0.9 * lambd) * Ef / E) - 0.9 * lambd * Ef / E)
            res['WHOB_lim'] = WHOB_lim
            res['W0OBp_lim'] = W0OBp_lim

    # 4. Расчёт для определения непроворачиваемости ведущего пояска

        # Минимальная необходимая реакция ведущего пояска
        q_PR = (E * W5 * h0 / (c * a0 * (1 + h0 / (2 * a0)))) * np.sqrt(
            2 * h0 / (3 * a0)) + sigma_N * n * delta / (np.pi * f0 * d)


        # Определение KSI5 по графику
        KSI5 = calc_coef(curr_lambda, None, q_PR)
        # Прогиб срединной поверхности
        W0PR = (delta_forc + delta * (1 - KSI5)) * (1 + h0 / (2 * a0))
        # Допустимый остаточный прогиб наружной поверхности корпуса
        WHPR_lim = 1.8 * eta * lambd * (W0PR - a0 * eps_sh) / (1 + h0 / (2 * a0))
        res['WHPR_lim'] = WHPR_lim
        res['q_PR'] = q_PR
        res['KSI5'] = KSI5
        res['W0PR'] = W0PR


    # 5. Расчёт обеспечения контакта между пояском и каналом ствола арт. орудия

        # Если деформации упругие
        if W0_curr < a0 * eps_sh:
            W5_con = 2 * W0_curr
        else:
            W5_con = 1.8 * eps_sh * a0 * lambd + 2 * (1 - 0.9 * lambd) * W0_curr

        res['W5_con'] = W5_con

        state[BeltZoneSolver.name] = res

class apfsds_strenght_solver_data(TypedDict):
    m_bt: float # Масса бал наконечника
    m_pl: float# Масса стабилизатора
    m_k: float# Масса корпуса
    m_db: float# Масса ВУ
    m_fl: float
    m_total: float
    l_db: float# Длина гребенки ВУ
    x_db_0: float# Координата начала ВУ от хвоста
    x_db_n: float# Координата пояска
    la: float# Ддина активной части
    da: float# Диаметр активной части
    d: float# Калибр орудия
    p_max: float# Макисмальное давление ПГ

class APFSDStrengthSolver(ABCSolver):

    name = 'apfsds_strenght_solver'

    preprocessed_data: apfsds_strenght_solver_data = dict(
        m_bt=None,
        m_pl=None,
        m_k=None,
        m_db=None,
        m_fl=None,
        m_total=None,
        l_db=None,
        x_db_0=None,
        x_db_n=None,
        la=None,
        da=None,
        d=None,
        p_max=None
    )

    def get_Fg_tg(self):
        p_data = self.preprocessed_data
        m_db = p_data['m_db']
        m_fl = p_data['m_fl']
        m_total = p_data['m_total']
        s = 0.25 * np.pi * p_data['d'] ** 2
        sk = 0.25 * np.pi * p_data['da'] ** 2
        p_max = p_data['p_max']

        Fg = 0.5 * p_max * ((s - 2. * sk) - s * (m_db - m_fl) / m_total)
        tg = 2. * Fg / (np.pi * p_data['da'] * p_data['l_db'])

        return Fg, tg

    @np.vectorize
    def get_sigma_x(self, x, Fg):
        p_data = self.preprocessed_data
        m_bt = p_data['m_bt']
        m_pl = p_data['m_pl']
        m_k = p_data['m_k']
        m_db = p_data['m_db']
        m_total = p_data['m_total']
        la = p_data['la']
        l_db = p_data['l_db']
        x_db_0 = p_data['x_db_0']
        s = 0.25 * np.pi * p_data['d'] ** 2
        sk = 0.25 * np.pi * p_data['da'] ** 2
        p_max = p_data['p_max']

        if la >= x > (x_db_0 + l_db):
            sigma = -(m_bt + m_k * (1. - x / la)) / m_total
            sigma *= s * p_max / sk
            return sigma
        if (x_db_0 + l_db) >= x > x_db_0:
            sigma = -(m_bt + m_k * (1. - x / la)) / m_total
            sigma *= s * p_max / sk
            sigma += Fg * (l_db + x_db_0 - x) / (l_db * sk)
            return sigma
        if x_db_0 >= x >= 0.:
            sigma = -(m_bt + m_k * (1. - x / la)) / m_total
            sigma *= s * p_max / sk
            sigma += Fg / sk
            return sigma
        return 0.

    @np.vectorize
    def get_sigma_r(self, x):
        p_data = self.preprocessed_data
        x_db_n = p_data['x_db_n']
        p_max = p_data['p_max']
        if 0. <= x <= x_db_n:
            return p_max
        return 0.

    def run(self, data: dict, global_state: dict):
        n_points = data['settings'][APFSDStrengthSolver.name]['n_points']
        x = np.linspace(0., self.preprocessed_data['la'], n_points)

        Fg, tg = self.get_Fg_tg()

        sigma_x = self.get_sigma_x(self, x, Fg)
        sigma_r = self.get_sigma_r(self, x)

        sigma_t = abs(sigma_x + sigma_r)

        global_state[APFSDStrengthSolver.name] = dict(
            x_mesh=x,
            sigma_x=sigma_x,
            sigma_r=sigma_r,
            sigma_t=sigma_t,
            Fg=Fg,
            tg=tg,
            sigma_x_max=sigma_x.max(),
            sigma_r_max=sigma_r.max(),
            sigma_t_max=sigma_t.max()
        )
