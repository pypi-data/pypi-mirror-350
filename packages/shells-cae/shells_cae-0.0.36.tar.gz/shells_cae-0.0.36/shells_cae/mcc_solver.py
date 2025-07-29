import numpy as np
from .geometry_solver import GeometrySolver
from typing import TypedDict
from .solvers_abc import ABCSolver

class data(TypedDict):
    q_fuse: float
    q_sh: float
    V: float
    corpus_material: np.ndarray
    explosive_material: np.ndarray
    belt_material: np.ndarray
    gun: dict
    shell_size: dict
    corpus_coord: np.ndarray
    fuse_coord: np.ndarray
    explosive_coord: np.ndarray
    belt_coord: np.ndarray

class OFSMCCSolver:
    name = 'mcc_solver'

    flag = True

    _geo_solver = GeometrySolver()

    preprocessed_data: data = dict(
        q_fuse=None,
        q_sh=None,
        V=None,
        L=None,
        corpus_material=None,
        explosive_material=None,
        belt_material=None,
        gun=None,
        shell_size=None,
        corpus_coord=None,
        fuse_coord=None,
        explosive_coord=None,
        belt_coord=None
    )

    def preprocessor(self, data: dict, global_state: dict):

        self.preprocessed_data['q_fuse'] = data['fuse']['q']
        self.preprocessed_data['q_sh'] = data['initial_cond']['q']
        self.preprocessed_data['V'] = data['initial_cond']['V']
        self.preprocessed_data['corpus_material'] = data['materials']['corpus']
        self.preprocessed_data['explosive_material'] = data['materials']['explosive']
        self.preprocessed_data['belt_material'] = data['materials']['belt']
        self.preprocessed_data['gun'] = data['gun_char']
        self.preprocessed_data['shell_size'] = data['shell_size']

        if self.flag:
            self.flag = False
            self._geo_solver.preprocessor(data, global_state)
            self._geo_solver.run(data, global_state)
        else:
            self._geo_solver.run(data, global_state)

        geometry_state = global_state[GeometrySolver.name]
        self.preprocessed_data['corpus_coord'] = geometry_state['corpus_coord']
        self.preprocessed_data['fuse_coord'] = geometry_state['fuse_coord']
        self.preprocessed_data['explosive_coord'] = geometry_state['explosive_coord']
        self.preprocessed_data['belt_coord'] = geometry_state['belt_coord']

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
        beta = (1 + 2 * lambd + 3 * lambd ** 2) / (4 * (1 + lambd + lambd ** 2))
        ksi = beta * h
        xc = ksi + hi

        # Объём конуса
        V =  (np.pi / 3) * (r1 ** 2 + r1 * r2 + r2 ** 2) * h
        # Масса
        q = V * rho
        # Статический момент
        S = q * xc

        # Осевой момент конуса
        mu = 0.3 * (1 + lambd + lambd ** 2 + lambd ** 3 + lambd ** 4) / (1 + lambd + lambd ** 2)
        r_xc = r1 + (r2 - r1) / (x2 - x1) * (xc - x1)
        Av = mu * V * r_xc ** 2
        A = Av * rho

        # Экваториальный момент конуса относительно донного среза (B')
        vu = (3 * (1 + lambd) ** 4 + 4 * lambd ** 2) / (80 * (1 + lambd + lambd ** 2 ) ** 2)
        Bv = 0.5 * Av + V * (vu * h** 2 + xc ** 2)
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

        # Объём цилиндра
        V = np.pi * r ** 2 * h
        # Масса
        q = V * rho
        # Статический момент
        S = q * xc
        # Осевой момент цилиндра
        mu = 0.5
        r_xc = r
        Av = mu * V * r_xc ** 2
        A = Av * rho
        # Экваториальный момент цилиндра относительно донного среза (B')
        vu = (3 * (1 + lambd) ** 4 + 4 * lambd ** 2) / (80 * (1 + lambd + lambd ** 2) ** 2)
        Bv = 0.5 * Av + V * (vu * h ** 2 + xc ** 2)
        B_sh = Bv * rho
        res_params = {'h': h, 'V': V, 'S': S, 'q': q, 'xc': xc, 'r_xc': r_xc, 'A': A, 'B_sh': B_sh}

        return res_params

    # Расчёт МЦХ корпуса
    def solve_corp(self, p_data):
        rho = p_data['corpus_material']['rho']
        all_coord = p_data['corpus_coord']
        # Выкидываем узлы под поясок
        corp_coord = np.delete(all_coord, [4, 5], axis=1)

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


        # Расчёт параметров канавки под ВП
        vp_k1 = self.get_params_conus(r1=all_coord[1, 4], r2=corp_coord[1, 3], x1=corp_coord[0, 3], x2=all_coord[0, 4], rho=rho)
        vp_c1 = self.get_params_cyl(r=corp_coord[1, 3], x1=corp_coord[0, 3],
                                    x2=corp_coord[0, 3] + (corp_coord[0, 4]-corp_coord[0, 3])/2, rho=rho)
        vp_c2 = self.get_params_cyl(r=all_coord[1, 4], x1=all_coord[0, 4],
                                    x2=all_coord[0, 4] + (all_coord[0, 5] - all_coord[0, 4]) / 2, rho=rho)

        V -= 2 * (vp_k1['V'] + vp_c1['V'] - vp_c2['V'])
        S -= 2 * (vp_k1['S'] + vp_c1['S'] - vp_c2['S'])
        q -= 2 * (vp_k1['q'] + vp_c1['q'] - vp_c2['q'])
        A -= 2 * (vp_k1['A'] + vp_c1['A'] - vp_c2['A'])
        B_sh -= 2 * (vp_k1['B_sh'] + vp_c1['B_sh'] - vp_c2['B_sh'])

        self.q_grove = 2 * (vp_k1['q'] + vp_c1['q'] - vp_c2['q'])


        # Вывод результатов
        result_params = {'V': V, 'S': S, 'q': q, 'A': A, 'B_sh': B_sh}

        return result_params

    # Расчёт МЦХ взрывателя
    def solve_fuse(self, p_data):
        q = p_data['q_fuse']
        fuse_coord = p_data['fuse_coord']
        x_coord = fuse_coord[0]
        y_coord = fuse_coord[1]

        count_nodes = len(x_coord)
        V, S, A, B_sh  = 0, 0, 0, 0
        # Определяем сначала только объём взрывателя
        for i in range(1, count_nodes - 1):
            if x_coord[i] == x_coord[i - 1]:
                continue
            elif y_coord[i] == y_coord[i - 1]:
                cyl = self.get_params_cyl(r=y_coord[i], x1=x_coord[i], x2=x_coord[i - 1], rho=0)
                V += cyl['V']
            else:
                konus = self.get_params_conus(r1=y_coord[i], r2=y_coord[i - 1], x1=x_coord[i], x2=x_coord[i - 1], rho=0)
                V += konus['V']
        try:
            rho = q / V

        except ZeroDivisionError:
            pass

        # Определяем все остальные характеристики

        for i in range(1, count_nodes - 1):
            if x_coord[i] == x_coord[i - 1]:
                continue
            elif y_coord[i] == y_coord[i - 1]:
                cyl = self.get_params_cyl(r=y_coord[i], x1=x_coord[i], x2=x_coord[i - 1], rho=rho)
                S += cyl['S']
                A += cyl['A']
                B_sh += cyl['B_sh']
            else:
                konus = self.get_params_conus(r1=y_coord[i], r2=y_coord[i - 1], x1=x_coord[i], x2=x_coord[i - 1], rho=rho)
                S += konus['S']
                A += konus['A']
                B_sh += konus['B_sh']

        result_params = {'V': V, 'S': S, 'q': q, 'A': A, 'B_sh': B_sh}

        return result_params

    # Расчёт МЦХ ВВ
    def solve_explosive(self, p_data):
        rho = p_data['explosive_material']['rho']
        coord = p_data['explosive_coord']
        x_coord = coord[0]
        y_coord = coord[1]
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

    # Расчёт МЦХ ВП
    def solve_belt(self, p_data):
        rho = p_data['belt_material']['rho']
        coord = p_data['belt_coord']

        # Ставим поясок на ось и сдвигаем до упора чтобы не вычитать объёмы
        x_coord = coord[0]
        y_coord = coord[1]

        ind = 1
        V_vp, S_vp, q_vp, A_vp, B_sh_vp = 0, 0, 0, 0, 0

        while x_coord[ind] != x_coord[-1]:

            if x_coord[ind] == x_coord[ind-1]:
                ind += 1

            elif y_coord[ind] == y_coord[ind-1]:
                c_outside =self.get_params_cyl(r=y_coord[ind], x1=x_coord[ind], x2=x_coord[ind-1], rho=rho)
                c_inside = self.get_params_cyl(r=y_coord[0], x1=x_coord[ind], x2=x_coord[ind-1], rho=rho)
                V_vp += c_outside['V'] - c_inside['V']
                S_vp += c_outside['S'] - c_inside['S']
                q_vp += c_outside['q'] - c_inside['q']
                A_vp += c_outside['A'] - c_inside['A']
                B_sh_vp += c_outside['B_sh'] - c_inside['B_sh']
                ind += 1

            else:
                k_outside = self.get_params_conus(r1=y_coord[ind], r2=y_coord[ind-1], x1=x_coord[ind], x2=x_coord[ind-1], rho=rho)
                k_inside = self.get_params_cyl(r=y_coord[0], x1=x_coord[ind], x2=x_coord[ind-1], rho=rho)
                V_vp += k_outside['V'] - k_inside['V']
                S_vp += k_outside['S'] - k_inside['S']
                q_vp += k_outside['q'] - k_inside['q']
                A_vp += k_outside['A'] - k_inside['A']
                B_sh_vp += k_outside['B_sh'] - k_inside['B_sh']
                ind += 1

        result_params = {'V': V_vp, 'S': S_vp, 'q': q_vp, 'A': A_vp, 'B_sh': B_sh_vp}

        return result_params

    # Расчёт гироскоп. коэфф. на вылете
    def gyro_stab(self, q, A, B, mu, xc, R6_cur, p_data):
        km = np.array([0.97, 0.98, 1.0, 1.03, 1.06, 1.07, 1.06, 1.05, 1.04, 1.03, 1.02, 1.01, 1.0, 0.99, 0.98, 0.97,
                       0.96, 0.95, 0.94, 0.93, 0.92, 0.91, 0.9, 0.89, 0.88])

        mach = np.array([0.762, 0.821, 0.88, 0.938, 0.997, 1.173, 1.232, 1.291,1.349, 1.467, 1.525, 1.643, 1.701, 1.76,
                         1.877, 1.995, 2.053, 2.171, 2.23, 2.347, 2.491, 2.64, 3.08, 3.227, 3.374])

        a = 340.8
        V_mach = p_data['V'] / a
        Km = np.interp(V_mach, mach, km) * 1e-3
        eta_k = p_data['gun']['eta_k']


        d = p_data['gun']['d']
        fi = 0.57
        sizes = p_data['shell_size']
        L_corp = sizes['R1'] + sizes['R2'] + sizes['R3'] + sizes['R4'] + R6_cur + sizes['R7'] + sizes['R8']
        L = L_corp + sizes['R27']

        Hg = L - p_data['corpus_coord'][0, 11]

        Cq = (q / d**3) * 1e-3
        h0 = p_data['corpus_coord'][0, 11] - xc
        h1 = fi * Hg - 0.16 * d

        h = h0 + h1

        if L <= 4.5 * d:
            sqrt_Ld = 1
        else:
            sqrt_Ld = np.sqrt(L / (4.5 * d))

        sigma_0 = np.sqrt(1 - (h/d) * (eta_k**2/(mu*Cq)) * (B/A) * (4/np.pi**2) * Km * sqrt_Ld)

        return sigma_0, h

    # Коррекция массы снаряда
    def correct_mass(self, curr_q, p_data):
        q1 = curr_q
        q = p_data['q_sh']
        ro1 = p_data['corpus_material']['rho']
        ro2 = p_data['explosive_material']['rho']
        R = p_data['corpus_coord'][1, 9]
        R6 = p_data['corpus_coord'][0, 9] - p_data['corpus_coord'][0, 8]

        ind = np.searchsorted(p_data['explosive_coord'][0], p_data['corpus_coord'][0, 9])

        r = np.interp(p_data['corpus_coord'][0, 9], [p_data['explosive_coord'][0, ind - 1], p_data['explosive_coord'][0, ind]],
                      [p_data['explosive_coord'][1, ind - 1], p_data['explosive_coord'][1, ind]])

        delta_A = (q - q1) / (np.pi * ((R ** 2 - r ** 2) * ro1 + r ** 2 * ro2))
        new_size = R6 + delta_A

        return new_size

    # Определяем параметры для будущего расчёта
    def get_params_for_kontur(self, data, state, xc):
        sizes = data['shell_size']

        # ng = 3 #Количество разбиения ГЧ
        # nh = ng + 1 #Количество участков головной и цилиндрической частей
        # nk = 5  #Общее количество участков на снаряде
        # nfl = 2 # Вид притупления
        # yint = 0 # Высота носика (0 потому что задаётся отдельным примитивом)
        # d = sizes['d']  # Калибра снаряда
        # hb = sizes['R17'] - (d / 2)   # Высота пояска
        # xct = state['geometry_solver']['L_all'] - xc # Координата центра тяжести (ОТ НОСИКА !!!)

        ng = 3 #Количество разбиения ГЧ
        nh = ng + 1 #Количество участков головной и цилиндрической частей
        nk = 5  #Общее количество участков на снаряде
        nfl = 2 # Вид притупления
        yint = 0 # Высота носика (0 потому что задаётся отдельным примитивом)
        d = sizes['d']  # Калибра снаряда
        hb = sizes['R17'] - (d / 2)   # Высота пояска
        xct = state['geometry_solver']['L_all'] - xc # Координата центра тяжести (ОТ НОСИКА !!!)

        R6_cur = state['geometry_solver']['R6']
        R_d = d / 2

        # Колпачок взрывателя

        fuse_nose = {'type': 1, 'x1': 0., 'x2': sizes['R29'], 'r1': sizes['R28'], 'r2': sizes['R28'], 'R': 0., 'n': 0.}

        # Конус взрывателя
        fuse_korp = {'type': 2, 'x1': sizes['R29'], 'x2': sizes['R27'], 'r1': sizes['R28'], 'r2': sizes['R9'], 'R': 0., 'n': 0.}

        # Оживало снаряда
        h_oj = sizes['R27'] + sizes['R8']
        R_oj = state['geometry_solver']['Roj']
        shell_ojive = {'type': 4, 'x1': sizes['R27'], 'x2': h_oj, 'r1': sizes['R9'], 'r2': R_d, 'R': R_oj, 'n': 0.}


        # Цилиндр снаряда (до зпч)
        h_cyl = h_oj + sizes['R7'] + R6_cur + sizes['R4'] + sizes['R3'] + sizes['R2']
        cyl_shell = {'type': 1, 'x1': h_oj, 'x2': h_cyl, 'r1': R_d, 'r2': R_d, 'R': 0., 'n': 0.}


        # Конус ЗПЧ
        r_zp = R_d - np.tan(sizes['R23']) * sizes['R1']
        zp_konus = {'type': 2, 'x1': h_cyl, 'x2': h_cyl + sizes['R1'], 'r1': R_d, 'r2': r_zp, 'R': 0., 'n': 0.}
        geometry_data = [fuse_nose, fuse_korp, shell_ojive, cyl_shell, zp_konus]

        result = {'ng': ng, 'nh': nh, 'nk': nk, 'nfl': nfl, 'yint': yint, 'd': d, 'hb': hb, 'xct': xct,
                  'geometry_data': geometry_data}

        return result

    def get_params_for_Spin73(self, data, state, xc):
        sizes = data['shell_size']
        R6_cur = state['geometry_solver']['R6']


        D = sizes['d']  # Калибра снаряда
        VL = sizes['R1'] + sizes['R2'] + sizes['R3'] + sizes['R4'] + R6_cur + sizes['R7'] + sizes['R8'] + sizes['R27']
        DM = sizes['R28'] * 2
        VN = sizes['R8'] + sizes['R27']
        VB = sizes['R1']
        VCG = xc
        BD = sizes['R17'] * 2
        BM = 0
        OR = state['geometry_solver']['Roj']

        result = {'D': D, 'VL': VL, 'DM': DM, 'VN': VN, 'VB': VB, 'VCG': VCG, 'BD': BD, 'BM': BM, 'OR': OR }

        return result




    # Запуск расчёта
    def run(self, data: dict, state: dict):

        settings = data['settings']['mcc']
        correct_mass_status = settings['correct_mass_status']
        # correct_mass_tol = settings['correct_mass_tol']

        p_data = self.preprocessed_data

        corpus_params = self.solve_corp(p_data)
        explosive_params = self.solve_explosive(p_data)
        belt_params = self.solve_belt(p_data)
        fuse_params = self.solve_fuse(p_data)

        # Рассчитанная масса
        q = corpus_params['q'] + explosive_params['q'] + belt_params['q'] + fuse_params['q']

        # Коррекция массы

        # Получаем новое значение R6, округляем по максимуму, до 4 знакам в мм. Дальше просто нет физического смысла
        R6 = round(self.correct_mass(q, p_data), 4)


        # Пока убираем возможность задавать точность коррекции, потому что легко свалиться в рекурсию
        # Массу снаряда подгоняем по 2 знаку после запятой
        if abs(q - p_data['q_sh']) > 1E-2 and correct_mass_status:
            self._geo_solver.preprocessed_data['R6'] = R6
            self.preprocessor(data, state)
            self.run(data, state)
        else:

            # Статический момент снаряда
            S = corpus_params['S'] + explosive_params['S'] + belt_params['S'] + fuse_params['S']

            # Осевой момент инерции снаряда
            A = corpus_params['A'] + explosive_params['A'] + belt_params['A'] + fuse_params['A']

            # Экваториальный момент снаряда относительно донного среза
            B_sh = corpus_params['B_sh'] + explosive_params['B_sh'] + belt_params['B_sh'] + fuse_params['B_sh']

            # Центр масс снаряда
            xc = S / q

            # Экваториальный момент инерции снаряда относительно его центра масс:
            B = B_sh - q * xc ** 2

            # Отношение моментов инерции
            ratio_moment = B / A

            # Коэффициент инерции снаряда
            mu = (4 * A) / (q * p_data['gun']['d']**2)
            c_q = (q / p_data['gun']['d'] ** 3) * 1e-3

            # Определяем коэфф. гироскопич. устойчивости и расст. между ЦС и ЦМ
            sigma_0, h = self.gyro_stab(q, A, B, mu, xc, R6, p_data)

            # Коэффициент наполнения
            alpha = explosive_params['q'] / q

            res_shell = {'q': q, 'S': S, 'A': A, 'B_sh': B_sh, 'xc': xc, 'h': h, 'sigma_0': sigma_0,
                         'B': B, 'ratio_moment': ratio_moment, 'mu': mu, 'c_q': c_q, 'R6_correct': R6, 'alpha': alpha}

            corpus_params['q_grove'] = self.q_grove

            # Получаем параметры для будущего расчёта аэродинамики
            kontur = self.get_params_for_kontur(p_data, state, xc)
            spin73 = self.get_params_for_Spin73(p_data, state, xc)

            results = {'shell': res_shell, 'corp': corpus_params, 'expl': explosive_params, 'belt': belt_params, 'fuse': fuse_params,
                       'kontur': kontur, 'spin73': spin73}

            # self.results = results
            self.flag = True

            state[OFSMCCSolver.name] = results


class APFSDMccSolver(ABCSolver):

    name = 'apfsd_mcc_solver'
    preprocessed_data = dict(
        # Активная часть
        la=None,
        da=None,
        rho_k=None,

        # Оперение
        b_kc=None,
        b_kr=None,
        l_op=None,
        h_op=None,
        n=None,
        rho_p=None,
        tr_koef=None,

        #Бал наконечник
        r_n=None,
        r_v=None,
        l_n=None,
        rho_b=None,

        # Ведущее устройство
        len=None,
        form_koef=None,
        d=None,
        rho_db=None
    )

    def _compute_kernel_mass_dim(self, p_data):

        ker_mass = 0.25 * p_data['rho_k'] * np.pi * p_data['la'] * p_data['da'] ** 2
        return dict(
            mass=ker_mass,
            mass_center=0.5 * p_data['la']
        )
    def _compute_plumage_mass_dim(self, p_data):

        H = p_data['l_op']
        L = p_data['b_kc']
        a = p_data['b_kr'] - L

        S1 = L*H
        S2 = 0.5 * a * H
        S = S1 + S2

        xc = (3 * L * S1 + (6 * L + 2 * a) * S2) / (6 * S)
        yc = H * (3 * S1 + 2 * S2) / (6 * S)

        volume = S * p_data['h_op']

        mass = volume * p_data['rho_p']

        total_volume = 0.25 * np.pi * p_data['b_kr'] * p_data['da'] ** 2
        total_volume += volume * p_data['n']
        total_volume *= p_data['tr_koef'] # Это для того чтобы учесть массу урезанную п

        return dict(
            mass=mass,
            s_op=S,
            total_volume=total_volume,
            total_mass=total_volume * p_data['rho_p'],
            mass_center_x=xc,
            mass_center_y=yc
        )

    def _compute_balltip_mass_dim(self, p_data):

        S0 = np.pi * p_data['r_n'] ** 2
        V0 = S0 * p_data['l_n'] / 3.

        l_n = p_data['r_v'] * p_data['l_n'] / p_data['r_n']
        S0 = np.pi * p_data['r_v'] ** 2
        V0 -= S0 * l_n / 3.

        mass_center = p_data['l_n'] * 2. / 3.

        mass = V0 * p_data['rho_b']

        return dict(
            mass_center=mass_center,
            mass=mass
        )

    def _compute_driving_band(self, p_data):
        la = p_data['la']

        rlen = p_data['len'] * la
        mass = 0.25 * p_data['form_koef'] * p_data['rho_db'] * rlen * np.pi * (p_data['d'] ** 2 - p_data['da'] ** 2)

        return dict(rlen=rlen, mass=mass)

    def _compute_mass_center(self, p_data, kernel, plumage, balltip):

        bt_mc = balltip['mass_center']
        bt_mass = balltip['mass']
        total_len = p_data['l_n']

        ker_mc = kernel['mass_center'] + total_len
        ker_mass = kernel['mass']
        total_len += p_data['la']

        plum_mc = plumage['mass_center_x'] + total_len
        plum_mass = plumage['total_mass']
        total_len += p_data['b_kr']

        # plum_mc = plumage['mass_center_x']
        # plum_mass = plumage['total_mass']
        # total_len = p_data['b_kr']
        #
        # ker_mc = kernel['mass_center'] + total_len
        # ker_mass = kernel['mass']
        # total_len += p_data['la']
        #
        # bt_mc = balltip['mass_center'] + total_len
        # bt_mass = balltip['mass']
        # total_len += balltip['mass_center']

        total_mass = plum_mass + ker_mass + bt_mass

        total_cm = (plum_mass * plum_mc + ker_mass * ker_mc + bt_mass * bt_mc) / total_mass

        return total_cm, total_mass, total_len
    def run(self, data: dict, global_state: dict):
        p_data = self.preprocessed_data
        kernel = self._compute_kernel_mass_dim(p_data)
        plumage = self._compute_plumage_mass_dim(p_data)
        balltip = self._compute_balltip_mass_dim(p_data)
        drive_band = self._compute_driving_band(p_data)
        total_cm, fl_mass, total_len = self._compute_mass_center(p_data, kernel, plumage, balltip)

        total_mass = fl_mass + drive_band['mass']

        global_state[APFSDMccSolver.name] = dict(
            kernel=kernel,
            plumage=plumage,
            balltip=balltip,
            drive_band=drive_band,
            total_cm=total_cm, total_mass=total_mass, fl_mass=fl_mass, total_len=total_len
        )
