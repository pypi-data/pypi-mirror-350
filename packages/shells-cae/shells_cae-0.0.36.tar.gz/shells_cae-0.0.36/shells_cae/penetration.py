import numpy as np
# from numba import njit

from typing import TypedDict

class data(TypedDict):
    d: float
    V: float
    Hg: float
    q: float
    q_belt: float
    q_corp: float
    q_expl: float
    q_grove: float
    rho_corp: float
    rho_expl: float
    mu_c_expl: float
    sigma_t: float
    sigma_b: float
    E: float
    ground: dict
    sizes: dict
    res_geo: dict

    corpus_coord: np.ndarray
    expl_coord: np.ndarray



# Расчёт прочности ГЧ при проникании в преграду

class PenetrationHeadSolver:
    name = 'penetration_head_solver'

    preprocessed_data: data = dict(
        d=None,
        V=None,
        Hg=None,
        q=None,
        q_corp=None,
        q_expl=None,
        q_belt=None,
        q_gorve=None,
        rho_corp=None,
        rho_expl=None,
        mu_c_expl=None,
        sigma_t=None,
        sigma_b=None,
        E=None,
        ground=None,
        sizes=None,
        res_geo=None,
        corpus_coord=None,
        expl_coord=None

    )

    def preprocessor(self, data: dict, global_state: dict):
        self.preprocessed_data['d'] = data['gun_char']['d']
        self.preprocessed_data['V'] = global_state['external_ballistics_3d_solver']['v_array'][-1]
        self.preprocessed_data['q'] = global_state['mcc_solver']['shell']['q']
        self.preprocessed_data['res_geo'] = global_state['geometry_solver']

        self.preprocessed_data['q_grove'] = global_state['mcc_solver']['corp']['q_grove']
        self.preprocessed_data['q_belt'] = global_state['mcc_solver']['belt']['q']
        self.preprocessed_data['q_corp'] = global_state['mcc_solver']['corp']['q']
        self.preprocessed_data['q_expl'] = global_state['mcc_solver']['expl']['q']
        self.preprocessed_data['rho_corp'] = data['materials']['corpus']['rho']
        self.preprocessed_data['rho_expl'] = data['materials']['explosive']['rho']
        self.preprocessed_data['mu_c_expl'] = data['materials']['explosive']['mu']
        self.preprocessed_data['sigma_t'] = data['materials']['corpus']['sigma_t']
        self.preprocessed_data['sigma_b'] = data['materials']['corpus']['sigma_b']
        self.preprocessed_data['E'] = data['materials']['corpus']['E']

        self.preprocessed_data['corpus_coord'] = global_state['geometry_solver']['corpus_coord']
        self.preprocessed_data['expl_coord'] = global_state['geometry_solver']['explosive_coord']
        self.preprocessed_data['sizes'] = data['shell_size']
        self.preprocessed_data['ground'] = data['ground']

    @staticmethod
    # Считаем массу конуса
    def get_params_conus(r1, r2, x1, x2, rho):
        if r1 < r2:
            r1, r2 = r2, r1
            x1, x2 = x2, x1

        hi = min(x1, x2)
        h = max(x1,  x2) - hi
        #Объём конуса
        V =  (np.pi / 3) * (r1 ** 2 + r1 * r2 + r2 ** 2) * h
        #Масса
        q = V * rho
        return q

    @staticmethod
    # Считаем массу цилиндра
    def get_params_cyl(r, x1, x2, rho):
        h = abs(x1 - x2)
        #Объём цилиндра
        V =  np.pi * r**2 * h
        #Масса
        q = V * rho
        return q

    # Определения массовых параметров корпуса в заданном сечении

    def solve_corp(self, corp_coord, rho):

        x_coord = corp_coord[0]
        y_coord = corp_coord[1]
        count_nodes = len(x_coord)
        q = 0

        for i in range(1, count_nodes):
            if x_coord[i] == x_coord[i - 1]:
                continue
            elif y_coord[i] == y_coord[i - 1]:

                q_curr = self.get_params_cyl(r=y_coord[i], x1=x_coord[i], x2=x_coord[i - 1], rho=rho)

                if x_coord[i] > x_coord[i - 1]:
                    q += q_curr
                else:
                    q -= q_curr
            else:
                q_curr = self.get_params_conus(r1=y_coord[i], r2=y_coord[i - 1], x1=x_coord[i], x2=x_coord[i - 1],
                                          rho=rho)
                if x_coord[i] > x_coord[i - 1]:
                    q += q_curr
                else:
                    q -= q_curr

        return q

    # Определения массовых параметров ВВ в заданном сечении
    def solve_explosive(self, expl_coord, rho):
        x_coord = expl_coord[0]
        y_coord = expl_coord[1]
        count_nodes = len(x_coord)
        q = 0
        for i in range(1, count_nodes - 1):

            if x_coord[i] == x_coord[i - 1]:
                continue

            elif y_coord[i] == y_coord[i - 1]:
                if x_coord[i] > x_coord[i - 1]:
                    # Параметры цилиндрической части ВВ
                    q_curr = self.get_params_cyl(r=y_coord[i], x1=x_coord[i], x2=x_coord[i - 1], rho=rho)
                    q += q_curr

                else:
                    # Параметры очка под дно взрывателя
                    q_curr = self.get_params_cyl(r=y_coord[i], x1=x_coord[i], x2=x_coord[i - 1], rho=rho)
                    q -= q_curr

            else:
                # Параметры конусной части ВВ
                q_curr = self.get_params_conus(r1=y_coord[i], r2=y_coord[i - 1], x1=x_coord[i], x2=x_coord[i - 1], rho=rho)
                q += q_curr

        return q

    # Расчёт параметров при проникании на длину ГЧ
    def gch_penetration(self, data, sec_res):

        # Характеристики преграды
        N = data['ground']['N']
        N1 = data['ground']['N1']
        N2 = data['ground']['N2']
        N3 = data['ground']['N3']
        rho = data['ground']['rho']
        rho_zv = data['ground']['rho_zv']
        a0 = data['ground']['a0']

        # Остальные данные
        q = data['q']
        H_fuse = data['sizes']['R27']
        x_sec = sec_res['x_zv'] + H_fuse
        R_sec = sec_res['Ri']
        Vc = data['V']
        # Vc = 105

        # print(f'Координаты', x_sec)
        # print(f'Радиус сечений', R_sec)

        # Разбиение ГЧ на сечения

        # Расчёт первого шага в момент встречи с преградой (kf на первом шаге считаем для взрывателя считаем с учетом взрывателя)
        kf_0 = 0.73453 - 0.49590 * np.arctan(R_sec[0] / H_fuse) + 1.23312 * (np.arctan(R_sec[0] / H_fuse)) ** 2
        S_0 = np.pi * R_sec[0] ** 2

        d0 = R_sec[0] ** 2
        Cq0 = q / d0 ** 3
        if Vc >= a0:
            Px_0 = (0.7 * N * kf_0 * rho_zv * Vc ** 2) / (1 + 0.259 * (rho_zv * N / Cq0))
        else:
            Px_0 = (0.7 * N2 * kf_0 * rho * Vc ** 2 + N3) / (1 + 0.259 * (rho * N1 / Cq0))

        V = np.zeros(10)
        Px = np.zeros(10)
        Fx = np.zeros(10)
        kf = np.zeros(10)
        S = np.zeros(10)
        t = np.zeros(10)

        V[0] = Vc
        Px[0] = Px_0
        kf[0] = kf_0
        S[0] = S_0

        for i in range(1, len(x_sec)):
            S[i] = np.pi * R_sec[i] ** 2
            di = R_sec[i] * 2
            Cqi = q / di ** 3

            dx = x_sec[i] - x_sec[i-1]
            kf[i] = 0.73453 - 0.49590 * np.arctan(R_sec[i] / x_sec[i]) + 1.23312 * (np.arctan(R_sec[i] / x_sec[i])) ** 2

            if V[i - 1] >= a0:
                k1 = 0.1 * (q + 0.33 * S[i] * rho_zv * N * di)
                k2 = 0.07 * rho_zv * N * S[i] * kf[i]
                V[i] = V[i - 1] * np.exp(- (k2 / k1) * dx)
                Px[i] = (0.7 * N * kf[i] * rho_zv * V[i] ** 2) / (1 + 0.259 * (rho_zv * N / Cqi))
                dt = (k1 / k2) * (V[i - 1] - V[i]) / (V[i - 1] * V[i])
                t[i] = t[i - 1] + dt
                Fx[i] = Px[i] * S[i]

            else:
                k1 = 0.1 * (q + 0.33 * S[i] * rho * N1 * di)
                k2 = 0.07 * S[i] * rho * kf[i] * N2
                k3 = 0.1 * S[i] * N3

                V[i] = np.sqrt(V[i - 1] ** 2 * np.exp(-2 * dx * k2 / k1) - (k3 / k2) * (1 - np.exp(-2 * dx * k2 / k1)))
                dt = k1 / np.sqrt(k2 * k3) * (np.arctan(V[i-1] * np.sqrt(k2/k3)) - np.arctan(V[i] * np.sqrt(k2/k3)))
                t[i] = t[i - 1] + dt
                Px[i] = (0.7 * N2 * kf[i] * rho * V[i] ** 2 + N3) / (1 + 0.259 * (rho * N1 / Cqi))
                Fx[i] = Px[i] * S[i]


        # Расчёт изменения скорости и давления преграды по сечениям
        # for i in range(1, len(x_sec)):
        #     S[i] = np.pi * R_sec[i] ** 2
        #     kf[i] = 0.73453 - 0.49590 * np.arctan(R_sec[i] / x_sec[i]) + 1.23312 * (np.arctan(R_sec[i] / x_sec[i])) ** 2
        #
        #     if V[i - 1] >= a0:
        #         k1 = 0.1 * (q + 0.33 * S[i] * rho_zv * N * d)
        #         k2 = 0.07 * rho_zv * N * S[i] * kf[i]
        #         V[i] = V[i - 1]  * np.exp(- (k2 / k1) * x_sec[i])
        #         Px[i] = (0.7 * N * kf[i] * rho_zv * V[i] ** 2) / (1 + 0.259 * (rho_zv * N / Cq))
        #         # print('Сверхзвук')
        #     else:
        #         k1 = 0.1 * (q + 0.33 * S[i] * rho * N1 * d)
        #         k2 = 0.07 * S[i] * rho * kf[i] * N2
        #         k3 = 0.1 * S[i] * N3
        #         V[i] = np.sqrt(V[i - 1] ** 2 * np.exp(-2 * x_sec[i] * k2 / k1) - (k3 / k2) * (1 - np.exp(-2 * x_sec[i]  * k2 / k1)))
        #         Px[i] = (0.7 * N2 * kf[i] * rho * V[i] ** 2 + N3) / (1 + 0.259 * (rho * N1 / Cq))



        results = {'x_with_fuse': x_sec, 't': t, 'V': V, 'S': S, 'kf': kf, 'Px': Px, 'Fx': Fx}

        # my_plot(x=x_sec ,y=V, title='Изменение скорости снаряда при проникании на длину ГЧ \n (преграда СПГ Vc=105)')
        # print('Давление преграды: ', Px * 1E-6)
        # print('Скорость снаряда: ', V)
        # print('Коэфф. головной части: ', kf)
        # print('Площадь: ', S)
        # print('Время проникания: ', t)

        return results


    # Определение массива сечений со значениями xi, ri, Ri
    def section_solver(self, data):
        # Формирования сечений, получение массивов xi, ri, Ri
        n_sec = 10
        xi_sec = data['corpus_coord'][0, 11:21]
        Ri_sec = data['corpus_coord'][1, 11:21]
        ri_sec = np.zeros(10)
        r_zv = np.zeros(10)
        H_shell = np.max(data['corpus_coord'][0])
        x_max_exlp = np.max(data['expl_coord'][0])
        corp_bottom = np.flip(data['corpus_coord'][:, 21:], axis=1)

        for i in range(len(xi_sec)):
            curr_x = xi_sec[i]
            ind = np.searchsorted(corp_bottom[0], curr_x)
            r = np.interp(curr_x, [corp_bottom[0, ind - 1], corp_bottom[0, ind]],
                          [corp_bottom[1, ind - 1], corp_bottom[1, ind]])
            ri_sec[i] = r

            # Храним радиусы для прочности (с занулением для сечений со взрывателем)
            if curr_x < x_max_exlp:
                r_zv[i] = r




        x_zv = H_shell - xi_sec

        result = {'n_sec': n_sec, 'x_zv': np.flip(x_zv), 'xi': np.flip(xi_sec), 'Ri': np.flip(Ri_sec),
                  'r_zv': np.flip(r_zv), 'ri': np.flip(ri_sec)}


        return result

    # Определение наседающих масс
    def press_mass_solver(self, data, sec_res):

# Постоянная наседающая масса давящая ГЧ

        # q_belt = data['q_belt']
        # q_corp = data['q_corp']
        # q_expl = data['q_expl']

        expl_coord = data['expl_coord']
        corp_coord = np.delete(data['corpus_coord'], [4, 5], axis=1)    # выкидываем координаты под поясок

        # Постоянная наседающая масса
        # Масса корпуса до ГЧ
        before_gch_corp_coord = np.delete(corp_coord, np.where(corp_coord[0] > sec_res['xi'][-1]), axis=1)
        before_gch_corp_coord = np.insert(before_gch_corp_coord, [10], [[sec_res['xi'][-1]], [sec_res['ri'][-1]]], axis=1)
        q_before_gch_corp = self.solve_corp(before_gch_corp_coord, data['rho_corp']) - data['q_grove']                      # Прибавить поясок

        # Масса ВВ до ГЧ
        # before_gch_expl_coord = np.delete(expl_coord, np.where(expl_coord[0] > sec_res['xi'][-1]), axis=1)
        # before_gch_expl_coord = np.insert(before_gch_expl_coord, [-1], [[sec_res['xi'][-1], sec_res['xi'][-1]], [sec_res['ri'][-1], 0]], axis=1)
        # q_before_gch_expl = self.solve_explosive(before_gch_expl_coord, data['rho_expl'])


# Расчёт наседающих масс по сечениям
        q_press_corp = {}
        q_press_expl = {}
        q_press_shell = {}
        q_press_im_expl = {}
        x_gch = sec_res['xi'][-1]
        r_gch = sec_res['ri'][-1]

        for i in range(len(sec_res['xi'])):
            x_sec = sec_res['xi'][i]
        # Наседающая корпуса
            # Откидываем из всех координат всё что до ГЧ
            after_gch_corp_coord = np.delete(corp_coord, np.where(corp_coord[0] < x_gch), axis=1)
            after_gch_corp_coord = np.insert(after_gch_corp_coord, [0], [[x_gch], [r_gch]], axis=1)
            after_gch_corp_coord = np.append(after_gch_corp_coord, [[x_gch], [r_gch]], axis=1)

            # Массы по сечениям
            curr_corp_coord = np.delete(after_gch_corp_coord, np.where(after_gch_corp_coord[0] > x_sec), axis=1)
            ind = curr_corp_coord[0].argmax()
            curr_corp_coord = np.insert(curr_corp_coord, [ind+1], [[sec_res['xi'][i]], [sec_res['ri'][i]]], axis=1)

            q_curr_corp = self.solve_corp(corp_coord=curr_corp_coord, rho=data['rho_corp'])
            q_press_corp[i + 1] = q_curr_corp + q_before_gch_corp
            # my_plot(curr_corp_coord, title=f'Сечение № {i + 1}')

        # Наседающая ВВ (тут считаются сечения справа-налево, а затем масса отнимается от общей массы ВВ)
            # Откидываем из всех координат всё что до ГЧ
            after_gch_expl_coord = np.delete(expl_coord, np.where(expl_coord[0] < x_gch), axis=1)
            after_gch_expl_coord = np.insert(after_gch_expl_coord, [0], [[x_gch], [r_gch]], axis=1)

            curr_expl_coord = np.delete(after_gch_expl_coord, np.where(after_gch_expl_coord[0] < x_sec), axis=1)
            curr_expl_coord = np.insert(curr_expl_coord, [0], [[sec_res['xi'][i]], [sec_res['ri'][i]]], axis=1)

            # my_plot(curr_expl_coord, title=f'Сечение № {i + 1}')

            q_curr_expl = self.solve_explosive(expl_coord=curr_expl_coord, rho=data['rho_expl'])
            q_press_expl[i + 1] = data['q_expl'] - q_curr_expl

        # Суммарная наседающая
            q_press_shell[i + 1] = q_press_corp[i + 1] + q_press_expl[i + 1]

        # Масса в воображаемом цилиндре
            n_oj_points = 10      # Число точек по которым строится оживало каморы
            r_sec = sec_res['ri'][i]
            x_expl_max = np.max(expl_coord[0])

            if x_sec > x_expl_max:
                q_curr_im_expl = 0
            else:
                # Удаляем координаты правее сечения, добавляем точки, чтобы замкнуть контур
                curr_expl_coord = np.delete(expl_coord, np.where(expl_coord[0] > x_sec), axis=1)
                # Если есть очко под взрыватель
                if (expl_coord[0, -3] != expl_coord[0, -4]) and (expl_coord[0, -3] <= x_sec <= expl_coord[0, -4]):
                    curr_expl_coord = np.insert(curr_expl_coord, [-3], [[x_sec, x_sec], [r_sec, expl_coord[1, -3]]], axis=1)
                else:
                    curr_expl_coord = np.insert(curr_expl_coord, [-1], [[x_sec, x_sec], [r_sec, 0.0]], axis=1)

                # Проверяем точку максимума по радиусу
                r_expl_max = np.max(curr_expl_coord[1])
                if r_sec >= r_expl_max:
                    q_curr_im_expl = self.solve_explosive(expl_coord=curr_expl_coord, rho=data['rho_expl'])
                else:
                    # Удаляем координаты выше сечения, добавляем точки, чтобы замкнуть контур
                    curr_expl_coord = np.delete(curr_expl_coord, np.where(curr_expl_coord[1] > r_sec), axis=1)
                    if r_sec < expl_coord[1, 1]:
                        curr_expl_coord = np.insert(curr_expl_coord, [1], [[expl_coord[0, 0]], [r_sec]], axis=1)
                        q_curr_im_expl = self.solve_explosive(expl_coord=curr_expl_coord, rho=data['rho_expl'])
                    else:
                        max_r_ind = 4 # индекс максимального радиуса по каморе
                        ind = np.searchsorted(expl_coord[1, :max_r_ind], r_sec)
                        x_interp = np.interp(r_sec, [expl_coord[1, ind-1], expl_coord[1, ind]],
                                                    [expl_coord[0, ind-1], expl_coord[0, ind]])
                        curr_expl_coord = np.insert(curr_expl_coord, [ind], [[x_interp], [r_sec]], axis=1)
                        q_curr_im_expl = self.solve_explosive(expl_coord=curr_expl_coord, rho=data['rho_expl'])

            q_press_im_expl[i + 1] = q_curr_im_expl

            # my_plot(curr_expl_coord, title=f'Сечение № {i + 1}')


        results = {'q_press_corp': q_press_corp, 'q_press_expl': q_press_expl,
                   'q_press_shell': q_press_shell, 'q_press_im_expl': q_press_im_expl}
        return results

    # Определение напряжений в головной части снаряда при проникании
    def stress_solver(self, data, pen_res, sec_res, press_mass_res):
        sec_count = len(sec_res['xi'])
        q = data['q']
        mu_c = data['mu_c_expl']
        px = pen_res['Px'][-1]
        Rx = sec_res['Ri'][-1]
        Sn = np.zeros(sec_count)
        Nn = np.zeros(sec_count)
        pc = np.zeros(sec_count)
        sigma_x = np.zeros(sec_count)
        sigma_r = np.zeros(sec_count)
        sigma_t = np.zeros(sec_count)
        sigma_pr = np.zeros(sec_count)

        for i in range(sec_count):
            Rn = sec_res['Ri'][i]
            rn = sec_res['r_zv'][i]
            qn = press_mass_res['q_press_shell'][i + 1]
            w_im_expl = press_mass_res['q_press_im_expl'][i + 1]

            # Площадь корпуса снаряда в сечении
            Sn[i] = np.pi * (Rn**2 - rn**2)

            # Сжимающая сила
            if i != 9:
                # формула для гч
                Nn[i] = px * np.pi * Rx**2 * (qn / q - 1 + Rn**2/Rx**2)
            else:
                # формула для перехода ГЧ в корпус
                Nn[i] = px * np.pi * Rx**2 * (qn / q)

            # Осевое напряжение
            sigma_x[i] = - Nn[i] / Sn[i]


            if rn!= 0.0:
                # Радиальное напряжение
                sigma_r[i] = - (mu_c / (1 - mu_c)) * px * (w_im_expl / q) * (Rx**2 / rn**2)
                # Давление снаряжения
                pc[i] = - sigma_r[i]
                # Тангенциальное напряжение
                k = Rn ** 2 / rn ** 2
                if i != 9:
                    # формула для ГЧ
                    sigma_t[i] = - 2 * px * (k / (k - 1)) + pc[i] * ((k + 1) / (k - 1))
                else:
                    # формула для перехода ГЧ в корпус
                    sigma_t[i] = pc[i] * (k + 1 / (k - 1))

            else:
                sigma_r[i] = 0.0
                pc[i] = 0.0
                sigma_t[i] = 0.0




            # Приведенное напряжение
                # Сортируем значения (от большего к меньшему)
            s = np.array([sigma_x[i], sigma_r[i], sigma_t[i]])
            s.sort(kind='quicksort')
            s = np.flip(s)
            sigma_pr[i] = 1 / np.sqrt(2) * np.sqrt((s[0] - s[1])**2 + (s[1] - s[2])**2 + (s[2] - s[0])**2)



        results = {'S': Sn, 'pc': pc, 'N': Nn, 'sigma_x': sigma_x, 'sigma_r': sigma_r,
                   'sigma_t': sigma_t, 'sigma_pr': sigma_pr}

        return results


    # Допустимое напряжение в материале корпуса снаряда
    def allowable_stress(self, data, pen_res, sigma_pr_max):
        sigma_t = data['sigma_t'] * 1E-9    # в ГПа
        E = data['E'] * 1E-9    # в ГПа
        sigma_pr_max = sigma_pr_max * 1E-9 # в ГПа
        sigma_b = data['sigma_b'] * 1E-9 # в ГПа

        if data['sigma_t'] < 1e9:
            n = 0.8
        else:
            n = 2


        # Время проникания на длину ГЧ
        tx = pen_res['t'][-1]

        eps = sigma_pr_max / (E * tx)
        A = 1 + 0.1 * (3 **  (0.22 * np.log(eps)))
        Kt = 1 + np.log(A) / (1.35 * sigma_t ** n)

        sigma_dt = Kt * sigma_t
        nz = sigma_dt / sigma_pr_max
        sigma_dop = sigma_t * Kt / 1.04

        result = {'sigma_pr_max': sigma_pr_max, 'sigma_dop': sigma_dop, 'sigma_b': sigma_b, 'nz': nz}

        return result



    # Определяем координаты для каждого сечения
    def run(self, data: dict, state: dict):
        p_data = self.preprocessed_data
        name_ground = data['ground']['name']



        sec_res = self.section_solver(p_data)
        pen_res = self.gch_penetration(p_data, sec_res)
        press_mass_res = self.press_mass_solver(p_data, sec_res)
        stress_res = self.stress_solver(p_data, pen_res, sec_res, press_mass_res)

        sigma_pr_max = np.max(stress_res['sigma_pr'])
        safe_factor_res = self.allowable_stress(p_data, pen_res, sigma_pr_max)


        # Проверка условия проникания
        N3 = p_data['ground']['N3']
        rho = p_data['ground']['rho']

        # Минимальная скорость при которой возможно проникание
        V_dop = np.sqrt(N3 / rho)

        results = {'V_dop': V_dop, 'ground': name_ground}
        results.update(pen_res)
        results.update(sec_res)
        results.update(press_mass_res)
        results.update(stress_res)
        results.update(safe_factor_res)

        state[PenetrationHeadSolver.name] = results




        # if V >= V_dop:
        #     print('Проникание в преграду возможно.')
        # else:
        #     print('ПРОНИКАНИЕ НЕВОЗМОЖНО!')
        #     return


        # my_plot(np.array([sec_res['x_zv'], stress_res['sigma_pr'] * 1e-6 ]), title='Приведенные напряжения')

