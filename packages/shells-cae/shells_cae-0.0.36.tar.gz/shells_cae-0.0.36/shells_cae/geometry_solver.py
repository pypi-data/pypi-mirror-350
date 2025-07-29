import numpy as np

from typing import TypedDict

class data(TypedDict):
    d: float
    r: float
    R1: float
    R2: float
    R3: float
    R4: float
    R5: float
    R6: float
    R7: float
    R8: float
    R9: float
    R10: float
    R11: float
    R12: float
    R13: float
    R14: float
    R15: float
    R16: float
    R17: float
    R18: float
    R19: float
    R20: float
    R21: float
    R22: float
    R23: float
    R24: float
    R25: float
    R26: float
    R27: float
    R28: float
    R29: float
    const1: float
    const2: float
    belt_geometry: np.ndarray

class GeometrySolver:
    name = 'geometry_solver'
    preprocessed_data: data = dict(
        d = None,
        r = None,
        R1 = None,
        R2 = None,
        R3 = None,
        R4 = None,
        R5 = None,
        R6 = None,
        R7 = None,
        R8 = None,
        R9 = None,
        R10 = None,
        R11 = None,
        R12 = None,
        R13 = None,
        R14 = None,
        R15 = None,
        R16 = None,
        R17 = None,
        R18 = None,
        R19 = None,
        R20 = None,
        R21 = None,
        R22 = None,
        R23 = None,
        R24 = None,
        R25 = None,
        R26 = None,
        R27 = None,
        R28 = None,
        R29 = None,
        const1 = None,
        const2 = None,
        belt_geometry = None
    )

    def __init__(self):
        self.corpus_coords = None
        self.explosives_coords = None

    def preprocessor(self, data: dict, global_state: dict):

        shell_size = data['shell_size']
        self.preprocessed_data.update(shell_size)

        self.preprocessed_data['d'] = data['shell_size']['d']
        self.preprocessed_data['belt_geometry'] = np.array([data['belt_coord']['x'], data['belt_coord']['y']])
        self.preprocessed_data['R13'] = self.preprocessed_data['R8'] - data['shell_size']['const2']
        self.preprocessed_data['R15'] = self.preprocessed_data['R14'] - data['shell_size']['const1']


    def _get_shell_coord(self, p_data):

        const1 = p_data['R14'] - p_data['R15']
        const2 = p_data['R8'] - p_data['R13']

        # Рассчитываем иксы всех точек корпуса ОФС
        x_0 = 0
        x_1 = 0
        x_2 = p_data['R1']
        x_3 = x_2 + p_data['R2']
        x_4 = x_3 - ((p_data['r'] - p_data['R16']) / np.tan(np.deg2rad(75)))
        x_5 = x_3 + p_data['R3'] + ((p_data['r'] - p_data['R16']) / np.tan(np.deg2rad(75)))
        x_6 = x_5 - ((p_data['r'] - p_data['R16']) / np.tan(np.deg2rad(75)))
        x_7 = x_6 + p_data['R4']
        x_8 = x_7
        x_9 = x_8 + p_data['R6']
        x_10 = x_9
        x_11 = x_10 + p_data['R7']
        x_12 = x_11 + p_data['R8']
        x_13 = x_12
        x_14 = x_13 - p_data['R11']
        x_15 = x_14
        x_16 = x_12 - p_data['R13']
        x_17 = p_data['R20'] + p_data['R18']
        x_18 = p_data['R20']
        x_19 = x_18
        x_20 = 0

        # Рассчитываем игреки всех точек корпуса ОФС
        y_0 = 0
        y_1 = p_data['r'] - p_data['R1'] * np.tan(p_data['R23'])
        y_2 = p_data['r']
        y_3 = p_data['r']
        y_4 = p_data['R16']
        y_5 = p_data['R16']
        y_6 = p_data['d'] * 0.5
        y_7 = p_data['d'] * 0.5
        y_8 = p_data['r']
        y_9 = p_data['r']
        y_10 = p_data['d'] * 0.5
        y_11 = p_data['d'] * 0.5
        y_12 = p_data['R9']
        y_13 = p_data['R10']
        y_14 = p_data['R10']
        y_15 = p_data['R12']
        y_16 = p_data['R14']
        y_17 = p_data['R15']
        y_18 = p_data['R19']
        y_19 = 0
        y_20 = 0

        all_shell_coord = np.array([[x_0, x_1, x_2, x_3, x_4, x_5, x_6, x_7, x_8, x_9, x_10, x_11, x_12, x_13, x_14,
                                     x_15, x_16, x_17, x_18, x_19, x_20],
                                    [y_0, y_1, y_2, y_3, y_4, y_5, y_6, y_7, y_8, y_9, y_10, y_11, y_12, y_13, y_14,
                                     y_15, y_16, y_17, y_18, y_19, y_20]])

        self.corpus_nodes = all_shell_coord

    def _get_belt_coord(self, p_data):

        # Переводим координаты в общую систему координат

        x_belt = p_data['belt_geometry'][0] + self.corpus_nodes[0, 3]
        y_belt = p_data['belt_geometry'][1] + p_data['r']

        # Координаты пояска для построения графика
        x3, x4, x5, x6 = self.corpus_nodes[0, 3], self.corpus_nodes[0, 4], self.corpus_nodes[0, 5], \
                         self.corpus_nodes[0, 6]
        y3, y4, y5, y6 = self.corpus_nodes[1, 3], self.corpus_nodes[1, 4], self.corpus_nodes[1, 5], \
                         self.corpus_nodes[1, 6]

        x_belt_plot = np.concatenate([[x4], x_belt, [x5, x4]])
        y_belt_plot = np.concatenate([[y4], y_belt, [y5, y4]])

        self.belt_nodes = np.array([x_belt_plot, y_belt_plot])

    def _get_explosive_coord(self, p_data):
        # Рассчитываем иксы всех точек ВВ
        x_0 = self.corpus_nodes[0, 19]
        x_1 = self.corpus_nodes[0, 18]
        x_2 = self.corpus_nodes[0, 17]
        x_3 = self.corpus_nodes[0, 16]
        x_4 = self.corpus_nodes[0, 12] - p_data['R25']
        x_5 = x_4
        x_6 = self.corpus_nodes[0, 13] - p_data['R26']
        x_7 = x_6
        x_8 = x_0

        # Рассчитываем игреки всех точек ВВ
        y_0 = 0
        y_1 = self.corpus_nodes[1, 18]
        y_2 = self.corpus_nodes[1, 17]
        y_3 = self.corpus_nodes[1, 16]
        y_4 = np.interp(x_4, [self.corpus_nodes[0, 16], self.corpus_nodes[0, 15]],
                        [self.corpus_nodes[1, 16], self.corpus_nodes[1, 15]])
        y_5 = p_data['R24']
        y_6 = p_data['R24']
        y_7 = 0
        y_8 = y_0

        all_explosives_coord = np.array([[x_0, x_1, x_2, x_3, x_4, x_5, x_6, x_7, x_8],
                                         [y_0, y_1, y_2, y_3, y_4, y_5, y_6, y_7, y_8]])

        self.explosive_nodes = all_explosives_coord

    def _get_fuse_coord(self, p_data):
        # Рассчитываем иксы всех точек взрывателя
        x_0 = self.explosive_nodes[0, 7]
        x_1 = self.explosive_nodes[0, 6]
        x_2 = self.corpus_nodes[0, 14]
        x_3 = x_2
        x_4 = self.corpus_nodes[0, 13]
        x_5 = self.corpus_nodes[0, 12]
        x_6 = x_5 + p_data['R27'] - p_data['R29']
        x_7 = x_6 + p_data['R29']
        x_8 = x_7
        x_9 = x_0

        # Рассчитываем игреки всех точек взрывателя
        y_0 = self.explosive_nodes[1, 7]
        y_1 = self.explosive_nodes[1, 6]
        y_2 = y_1
        y_3 = self.corpus_nodes[1, 14]
        y_4 = self.corpus_nodes[1, 13]
        y_5 = self.corpus_nodes[1, 12]
        y_6 = p_data['R28']
        y_7 = y_6
        y_8 = 0
        y_9 = y_0

        all_fuse_coord = np.array([[x_0, x_1, x_2, x_3, x_4, x_5, x_6, x_7, x_8, x_9],
                                   [y_0, y_1, y_2, y_3, y_4, y_5, y_6, y_7, y_8, y_9]])
        self.fuse_nodes = all_fuse_coord

    # Определяем внешний радиус и все координаты точек для построения
    def _get_Roj(self, p_data):
        x = self.corpus_nodes[0, 11]
        y = self.corpus_nodes[1, 11]

        x0 = x - p_data['R22']
        x_hord_center = x + p_data['R8'] / 2
        y_hord_center = np.interp(x_hord_center, [x, self.corpus_nodes[0, 12]], [y, self.corpus_nodes[1, 12]])
        len_hord = np.sqrt((x_hord_center - x) ** 2 + (y_hord_center - y) ** 2)

        # Подобие треугольников
        c = p_data['R22'] * len_hord / (x_hord_center - x) + len_hord
        b = p_data['R22'] * (p_data['d'] * 0.5 - y_hord_center) / (x_hord_center - x)
        y0 = len_hord * c / (y_hord_center - y) + p_data['d'] * 0.5 + b

        Roj = np.sqrt((x - x0) ** 2 + (y - y0) ** 2)

        x_plot = np.linspace(self.corpus_nodes[0, 11], self.corpus_nodes[0, 12], 10)
        y_plot = np.sqrt(Roj ** 2 - (x_plot - x0) ** 2) + y0

        results = np.array([x_plot, y_plot])

        return results, Roj

    # Определяем внутренний радиус и все координаты точек для построения
    def _get_roj(self, p_data):
        x = self.corpus_nodes[0, 16]
        y = self.corpus_nodes[1, 16]
        x0 = x - p_data['R21']

        x_hord_center = x + (p_data['R13'] - p_data['R11']) / 2
        y_hord_center = np.interp(x_hord_center, [x, self.corpus_nodes[0, 15]], [y, self.corpus_nodes[1, 15]])
        len_hord = np.sqrt((x_hord_center - x) ** 2 + (y_hord_center - y) ** 2)

        # экстраполяция
        y_extrp = lambda x_n, x1, y1, x2, y2: y1 + ((y2 - y1) / (x2 - x1)) * (x_n - x1)

        # Подобие треугольников
        A_y = y_extrp(x0, x_hord_center, y_hord_center, x, y)
        A = np.sqrt((x - x0) ** 2 + (A_y - y) ** 2) + len_hord
        C = A / (self.corpus_nodes[1, 16] - y_hord_center) * len_hord
        B_y = y_hord_center + (y - y_hord_center) / (x - x_hord_center) * (x0 - x_hord_center)
        y0 = B_y - C

        roj = np.sqrt((x - x0) ** 2 + (y - y0) ** 2)

        x_plot = np.linspace(self.corpus_nodes[0, 16], self.corpus_nodes[0, 15], 10)
        y_plot = np.sqrt(roj ** 2 - (x_plot - x0) ** 2) + y0


        # Считаем точки оживала для ВВ
        # x_roj_explosive = np.linspace(self.explosive_nodes[0, 3], self.explosive_nodes[0, 4], 10)
        # y_roj_explosive = np.sqrt(roj ** 2 - (x_roj_explosive - x0) ** 2) + y0

        results_corp = np.array([x_plot[::-1], y_plot[::-1]])
        # results_explosive = np.array([x_roj_explosive, y_roj_explosive])

        return results_corp, roj

    # Определяем hsp для головной части снаряда
    def _get_hs_p(self, p_data, R_real):
        alpha = np.rad2deg(np.arctan(p_data['R8'] / (p_data['d'] / 2 - p_data['R9'])))
        beta = 180 - 2 * alpha
        Rt = p_data['R8'] / np.sin(np.deg2rad(beta))
        hs_p = Rt / R_real

        return hs_p



    def run(self, data: dict, state: dict):
        # Словарь с исходными данными
        # self.preprocessor(data, state)
        p_data = self.preprocessed_data

        self._get_shell_coord(p_data)
        self._get_belt_coord(p_data)
        self._get_explosive_coord(p_data)
        self._get_fuse_coord(p_data)

        # Добавляем данные по оживалам в общий массив координат корпуса и ВВ
        # Считываем данные по внешнему оживалу
        Roj_data, Roj = self._get_Roj(p_data)

        # Считываем данные по внутреннему оживалу
        roj_data, roj = self._get_roj(p_data)
        self.corpus_coords = np.insert(np.delete(self.corpus_nodes, [15, 16], axis=1), [15], roj_data, axis=1)
        roj_data_revers = np.flip(roj_data, axis=1)
        x_expl_last = self.explosive_nodes[0, -4]
        roj_expl = np.delete(roj_data_revers, np.where(roj_data_revers[0, :] > x_expl_last), axis=1)
        ind = np.searchsorted(roj_data_revers[0], x_expl_last)
        y_expl_last = np.interp(x_expl_last, [roj_data_revers[0, ind-1], roj_data_revers[0, ind]],
                                            [roj_data_revers[1, ind-1], roj_data_revers[1, ind]])
        roj_expl = np.append(roj_expl, [[x_expl_last], [y_expl_last]], axis=1)



        self.explosives_coords = np.insert(np.delete(self.explosive_nodes, [3, 4], axis=1), [3], roj_expl, axis=1)
        self.corpus_coords = np.insert(np.delete(self.corpus_coords, [11, 12], axis=1), [11], Roj_data, axis=1)



        # Определяем hs_p для аэродинамики (форма оживальной части)
        hsp = self._get_hs_p(p_data=p_data, R_real=Roj)

        # Сохраняем псевдо-варьируемые параметры
        R13 = round(p_data['R13'], 4)
        R15 = round(p_data['R15'], 4)
        R6 = round(p_data['R6'], 4)

        # Считаем нужные геометрические размеры
        sizes = data['shell_size']
        L_corp = sizes['R1'] + sizes['R2'] + sizes['R3'] + sizes['R4'] + R6 + sizes['R7'] + sizes['R8']
        L_all = L_corp + sizes['R27']
        L_vv = L_corp - sizes['R20'] - sizes['R25']

        state[GeometrySolver.name] = dict(
            corpus_coord=self.corpus_coords,
            explosive_coord=self.explosives_coords,
            fuse_coord=self.fuse_nodes,
            belt_coord=self.belt_nodes,
            Roj=Roj,
            roj=roj,
            R13=R13,
            R15=R15,
            R6=R6,
            hs_p=hsp,
            L_corp=L_corp,
            L_all=L_all,
            L_vv=L_vv
        )




