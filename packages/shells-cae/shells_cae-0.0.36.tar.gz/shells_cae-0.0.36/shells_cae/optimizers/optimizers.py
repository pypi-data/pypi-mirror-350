from typing import Sequence, Callable
import numpy as np
import numpy.random as npr
from abc import ABC, abstractmethod
import traceback
from copy import deepcopy
from shells_cae.solvers_abc import ABCSolver


class ABCOptObj(ABC):

    def __init__(self, id):
        self.id = id


class ABCAdapter(ABC):

    @abstractmethod
    def run(self, data: dict):
        pass


class ABConstraint(ABC):

    def __init__(self, constraint_type='ineq', *args, **kwargs):
        self.type = constraint_type

    @abstractmethod
    def run(self, data: dict, global_state: dict):
        pass


class OptProblem(ABC):

    def __init__(self, opt_objects: Sequence[ABCOptObj], adapters: Sequence[ABCAdapter], solvers: Sequence[ABCSolver],
                 data: dict, predefined_state: dict):

        self.opt_objs = opt_objects
        self.adapters = adapters
        self.solvers = solvers
        self.constraints = {solver.name: [] for solver in self.solvers}

        _obj_data = {}

        self._constraint_factor = 0.

        for obj in opt_objects:
            _obj_data[obj.id] = {'obj': obj, 'var': [], 'bounds': [], 'indexes': []}

        self._obj_data = _obj_data

        global_state = {solver.name: {} for solver in solvers}

        global_state.update(predefined_state)

        self._global_state = global_state
        self._data = data
        self._index_list = []

    @property
    def data(self):
        return self._data

    @property
    def global_state(self):
        return self._global_state

    @property
    def constraint_factor(self):
        return self._constraint_factor

    def add_var_param(self, obj_id, var, lbound=-np.inf, ubound=np.inf):
        self._obj_data[obj_id]['var'].append(var)
        self._obj_data[obj_id]['bounds'].append((lbound, ubound))

    def remove_var_param(self, obj_id, var):
        if not var in self._obj_data[obj_id]['var']:
            raise KeyError('Такого варьируемого параметра у объекта нет')
        var_index = self._obj_data[obj_id]['var'].index(var)
        self._obj_data[obj_id]['var'].pop(var_index)
        self._obj_data[obj_id]['bounds'].pop(var_index)

    def add_constraint(self, solver_name, constraint: ABConstraint):
        self.constraints[solver_name].append(constraint)

    def get_x0_w_bounds(self):
        x0_list = []
        bounds_list = []
        count = 0
        for key in self._obj_data.keys():
            obj = self._obj_data[key]['obj']
            var_params = self._obj_data[key]['var']
            if not var_params:
                continue
            indexes = []
            for i, var_param in enumerate(var_params):
                x0 = getattr(obj, var_param)
                x0_bounds = self._obj_data[key]['bounds'][i]
                bounds_list.append(x0_bounds)
                x0_list.append(x0)
                indexes.append(count)
                count += 1
            self._obj_data[key]['indexes'] = indexes
        return np.array(x0_list), np.array(bounds_list)

    def set_x(self, x_array: np.ndarray):
        for key in self._obj_data.keys():
            obj = self._obj_data[key]['obj']
            var_params = self._obj_data[key]['var']
            indexes = self._obj_data[key]['indexes']

            if not var_params:
                continue

            for var_param, index in zip(var_params, indexes):
                x = x_array[index]
                setattr(obj, var_param, x)

        self.adapt()

    def adapt(self):
        for adapter in self.adapters:
            adapter.run(data=self._data)

    @abstractmethod
    def run(self):
        '''
        Например:

        for solver in self.solvers: Цикл по всем решателям
            solver.preprocessor(self._data, self._global_state) Вызов препроцессора
            solver.run(self._data, self._global_state) Запуск решателя

        :return:
        '''
        pass
        # for solver in self.solvers:
        #     solver.preprocessor(self._data, self._global_state)
        #     solver.run(self._data, self._global_state)

    @abstractmethod
    def modify_constraint(self):
        pass

    @abstractmethod
    def user_defined_objective(self):
        pass

    @abstractmethod
    def callback(self):
        # Метод вызывается на каждом удачном шаге.
        # В реализации может быть печать на экран, запись в файл и прочие операции ввода вывода для спеццифического сохранения результатов
        pass

    def __call__(self, x: np.ndarray):
        self.set_x(x)
        self.run()
        val = self.user_defined_objective()
        return val + self._constraint_factor


class SimpleConstrainedOptProblem(OptProblem):

    def run(self):
        self._constraint_factor = 0.
        for solver in self.solvers:
            solver.preprocessor(data=self._data, global_state=self._global_state)
            solver.run(self._data, self._global_state)
            solver_constraints = self.constraints[solver.name]
            if solver_constraints:
                for constraint in solver_constraints:
                    constraint_value = constraint.run(self._data, self._global_state)
                    if constraint_value > 0.:
                        self._constraint_factor = np.inf
                        return

    def modify_constraint(self):
        pass


class PenaltyConstrainedOptProblem(OptProblem):

    def __init__(self, opt_objects: Sequence[ABCOptObj], adapters: Sequence[ABCAdapter], solvers, data: dict,
                 predefined_state: dict, r0=1., C=5.):
        super(PenaltyConstrainedOptProblem, self).__init__(opt_objects, adapters, solvers, data, predefined_state)

        self.r = r0
        self.C = C

    def modify_constraint(self):
        self.r *= self.C

    def run(self):
        eq_constaints = 0.
        ineq_constraints = 0.

        for solver in self.solvers:
            solver.preprocessor(self._data, self._global_state)
            solver.run(self._data, self._global_state)
            solver_constraints = self.constraints[solver.name]
            if solver_constraints:
                for constraint in solver_constraints:
                    constraint_value = constraint.run(self._data, self._global_state)
                    if constraint.type == 'eq':
                        eq_constaints += constraint_value ** 2
                    else:
                        ineq_constraints += max(0, constraint_value) ** 2

        self._constraint_factor = 0.5 * self.r * (eq_constaints + ineq_constraints)


class OptResult:

    def __init__(self,
                 x_history: np.ndarray,
                 f_history: np.ndarray,
                 step_mask: np.ndarray,
                 global_state_history: Sequence[dict],
                 status_code: int,
                 status_message: str,
                 error_list: Sequence[Exception]
                 ):
        self.x_history = x_history
        self.f_history = f_history
        self.step_mask = step_mask
        self.global_state_history = global_state_history
        self.status_code = status_code
        self.status_message = status_message
        self.error_list = error_list


class RandomOptimizer:

    def __init__(self, N=10, M=10, t0=0.1, R=1e-5, alpha=1.68, beta=0.68, min_delta_f=0., random_state=42,
                 PyQt_status_signal=None):
        self.N: float = N
        self.M: float = M
        self.t0: float = t0
        self.R: float = R
        self.alpha: float = alpha
        self.beta: float = beta
        self.min_delta_f = min_delta_f
        self.random_state: int = random_state
        self.PyQt_status_signal = PyQt_status_signal

    def _check_bounds(self, x_vec_cur: np.ndarray, bounds: np.ndarray):
        for i, x in enumerate(x_vec_cur):
            lbound = bounds[i, 0]
            ubound = bounds[i, 1]

            if x > ubound:
                x_vec_cur[i] = ubound
            if x < lbound:
                x_vec_cur[i] = lbound

    def _get_yj(self, x_cur, tk):
        """

        :param x_cur:
        :param tk:
        :return:
        """
        ksi = np.random.uniform(-1, 1, len(x_cur))
        # ksi = np.random.randn(len(x_cur))

        # if self._dropout:
        #     dropout_mask = np.random.rand(x_cur.shape[0]) > self._dropout_proba
        # else:
        #     dropout_mask = np.ones(x_cur.shape[0])

        yj = x_cur + tk * x_cur * ksi  # / np.linalg.norm(ksi)
        return yj

    def _get_zj(self, x_cur, yj):
        """

        :param x_cur:
        :param alpha:
        :param yj:
        :return:
        """
        zj = x_cur + self.alpha * (yj - x_cur)
        return zj

    def optimize(self, problem: OptProblem, print_limit=None):

        np.random.seed(self.random_state)

        global_state_history = []
        f_history = []
        mask = []
        exception_list = []
        x_history = []
        steps_total = 0
        bad_steps_cur = 0

        x0, bounds = problem.get_x0_w_bounds()
        last_x = np.copy(x0)

        last_f = np.inf

        try:
            last_f_try = problem(last_x)
            if last_f_try < last_f:
                last_f = last_f_try
                global_state_history.append(deepcopy(problem.global_state))
                f_history.append(last_f)
                x_history.append(np.copy(last_x))
                mask.append(1)
            else:
                mask.append(0)
                f_history.append(last_f)
                x_history.append((np.copy(x0)))
        except:
            mask.append(0)
            last_f = np.inf
            f_history.append(last_f)
            x_history.append((np.copy(x0)))

        tk = self.t0

        while steps_total < self.N:
            if self.PyQt_status_signal:
                self.PyQt_status_signal.emit((steps_total, self.N, bad_steps_cur, self.M, tk, self.R))

            while bad_steps_cur < self.M:

                try:
                    yj = self._get_yj(last_x, tk)
                    self._check_bounds(yj, bounds)

                    f_cur = problem(yj)

                    if (f_cur < last_f) & (abs(f_cur - last_f) > self.min_delta_f):

                        zj = self._get_zj(last_x, yj)
                        self._check_bounds(zj, bounds)

                        cur_f = problem(zj)

                        if (cur_f < last_f) & (abs(cur_f - last_f) > self.min_delta_f):

                            last_x = np.copy(zj)

                            tk *= self.alpha

                            steps_total += 1
                            last_f = cur_f

                            global_state_history.append(deepcopy(problem.global_state))
                            f_history.append(last_f)
                            x_history.append(np.copy(last_x))
                            mask.append(1)
                            problem.callback()

                        else:
                            bad_steps_cur += 1
                            mask.append(0)
                            f_history.append(cur_f)
                            x_history.append((np.copy(zj)))
                    else:
                        bad_steps_cur += 1
                        mask.append(0)
                        f_history.append(f_cur)
                        x_history.append((np.copy(yj)))

                except Exception as e:

                    if print_limit is not None:
                        traceback.print_exc(limit=print_limit)
                    bad_steps_cur += 1
                    exception_list.append(e)

            if tk <= self.R:
                break
            else:
                tk *= self.beta
                bad_steps_cur = 1

        f_history = np.array(f_history)
        x_history = np.array(x_history)
        mask = np.array(mask).astype(bool)

        if last_f == np.inf:
            return OptResult(x_history=x_history,
                             f_history=f_history,
                             step_mask=mask,
                             global_state_history=global_state_history,
                             status_code=1,
                             status_message='Оптимизация завершилась неудачно, т.к. не найдено ни одного оптимума',
                             error_list=exception_list
                             )
        else:
            return OptResult(x_history=x_history,
                             f_history=f_history,
                             step_mask=mask,
                             global_state_history=global_state_history,
                             status_code=0,
                             status_message='Оптимизация завершилась удачно по критерию останова',
                             error_list=exception_list
                             )


# Алгоритм 2022 года
class SRandomOptimizer:

    def __init__(self, N=100, beta=1.0, min_delta_f=0., random_state=42, PyQt_status_signal=None):
        self.N = N
        self.beta = beta
        self.min_delta_f = min_delta_f
        self.random_state = random_state

        self.n0 = 0  # Число неудачных шагов из опорной точки
        self.supn0 = 0  # Наибольшее число неудачных шагов из какой-либо опорной точки в процессе оптимизации
        self.m = 5  # Число предшествующих шагов для адаптации поиска
        self.k = None  # Число оптимизируемых параметров
        self.rs = None
        self.ss = None
        self.MF = None
        self.M01 = None
        self.cod = None
        self.mcod = self.beta  # Начальное значение коэфф. шага
        self.KxM = None
        self.PP = None
        self.PyQt_status_signal = PyQt_status_signal

    # Вырабаытывает случайный шаг
    def SHAG(self):
        mp = np.exp(-4.6 * ((self.n0 / self.N) ** 2 + (self.supn0 / self.N) ** 2)) / np.sqrt(self.k)
        su = 0
        sf = 0

        for i in range(self.m):
            sf = sf + self.MF[i]
            su = su + self.M01[i]

        for i in range(self.k):
            self.cod[i] = 0.0
            self.rs[i] = 0.0
            self.ss[i] = 0.0

            if np.abs(sf) > 1.0E-10:
                for j in range(self.m):
                    self.rs[i] = self.rs[i] - (j / self.m) * self.MF[j] * self.KxM[i, j]
                self.rs[i] = self.rs[i] * su * su / (self.m * sf)
                self.rs[i] = self.rs[i] * (su / self.m) * (sf / su)
                self.ss[i] = -(su / self.m) * mp * np.random.randn()
                self.cod[i] = self.rs[i] + self.ss[i]
            else:
                self.cod[i] = mp * np.random.randn()

            self.cod[i] = self.PP[i] + self.mcod * self.cod[i]

            if self.cod[i] < 0.0:
                self.cod[i] = 0.0
            if self.cod[i] > 1.0:
                self.cod[i] = 1.0

    # Определяет на каждом шаге размерность случайного подпространства
    def Sdv(self):
        for j in range(self.m - 1, 0, -1):
            self.MF[j] = self.MF[j - 1]
            self.M01[j] = self.M01[j - 1]
            for i in range(self.k):
                self.KxM[i, j] = self.KxM[i, j - 1]

    def optimize(self, problem: OptProblem, print_limit=None):
        np.random.seed(self.random_state)
        global_state_history = []
        f_history = []
        mask = []
        exception_list = []
        x_history = []
        steps_total = 0
        bad_steps_cur = 0
        Flag = False
        f_evals = 0
        f_evals_errs = 0
        x0, bounds = problem.get_x0_w_bounds()
        last_x = np.copy(x0)  # ВВП оразмеренный

        # Инициализируем переменные
        self.k = len(x0)
        # lims = np.array([bound.to_list() for bound in bounds])  # Ограничения 1 рода

        xx = x0.copy()  # Вектор в размерном виде
        last_xx = x0.copy()  # Прерыдущие значения вектора в размерном виде

        self.cod = (x0 - bounds[:, 0]) / ((bounds[:, 1]) - bounds[:, 0])  # Вектор кодовых параметров
        last_cod = self.cod.copy()  # предыдущие значения кодового вектора

        cur_f = np.inf
        last_f = np.inf

        self.PP = np.zeros(self.k)  # Сохраняет параметры опорной точки(в конце оптимизации содержит оптимальные точки)
        self.KxM = np.zeros(
            (self.k,
             self.m))  # Содержит приращения компонента после каждого удачного шага в последовательсти m предш. шагов
        self.MF = np.zeros(self.m)  # Содержит приращения ЦФ на каждом удачном шаге
        self.M01 = np.zeros(self.m)  # Содержит успех каждого предшествующего шага (состоит из 0 и 1)
        self.rs = np.zeros(self.k)
        self.ss = np.zeros(self.k)

        while self.n0 <= self.N:
            if self.PyQt_status_signal:
                self.PyQt_status_signal.emit((self.n0, self.N))

            xx = bounds[:, 0] + (bounds[:, 1] - bounds[:, 0]) * self.cod  # Оразмеривание
            print(self.cod)
            try:
                cur_f = problem(xx)
            except:
                cur_f = np.inf

            # Проверка условий
            if (cur_f < last_f) & (abs(cur_f - last_f) > self.min_delta_f):
                # Шаг удачный
                # print('Удачный')
                self.n0 = 0
                if Flag:
                    self.Sdv()
                    self.MF[0] = cur_f - last_f
                    self.M01[0] = 1
                    for i in range(self.k):
                        self.KxM[i, 0] = self.cod[i] - self.PP[i]

                Flag = True
                last_f = cur_f
                last_cod = self.cod.copy()
                last_xx = xx.copy()

                global_state_history.append(deepcopy(problem.global_state))
                f_history.append(last_f)
                x_history.append(np.copy(last_xx))
                mask.append(1)
                problem.callback()

                for i in range(self.k):
                    self.PP[i] = self.cod[i]

            else:
                # Шаг неудачный
                self.n0 += 1
                if self.n0 > self.supn0:
                    self.supn0 = self.n0
                self.Sdv()
                self.MF[0] = 0
                self.M01[0] = 0
                for i in range(self.k):
                    self.KxM[i, 0] = 0

                mask.append(0)
                f_history.append(cur_f)
                x_history.append(np.copy(xx))

            self.SHAG()

        # Выход из оптимизации
        f_history = np.array(f_history)
        x_history = np.array(x_history)
        mask = np.array(mask).astype(bool)

        if not Flag:
            return OptResult(x_history=x_history,
                             f_history=f_history,
                             step_mask=mask,
                             global_state_history=global_state_history,
                             status_code=1,
                             status_message='Оптимизация завершилась неудачно, т.к. не найдено ни одного оптимума',
                             error_list=exception_list
                             )
        else:
            return OptResult(x_history=x_history,
                             f_history=f_history,
                             step_mask=mask,
                             global_state_history=global_state_history,
                             status_code=0,
                             status_message='Оптимизация завершилась удачно по критерию останова',
                             error_list=exception_list
                             )


class ConstrainedOptimizer:

    def optimize(self, base_optimizer: RandomOptimizer, problem: OptProblem, print_limit=1,
                 n_iters=5, tol=1e-3):

        _x_history = []
        _f_history = []
        _global_state_history = []
        _mask = []
        _error_list = []

        constaint_status = 0

        res = base_optimizer.optimize(problem, print_limit)
        if res.status_code == 1:
            return res, constaint_status
        problem(res.x_history[res.step_mask][-1])
        factor = problem.constraint_factor
        if factor < tol:
            constaint_status = 1
            return res, constaint_status

        for i in range(n_iters):
            res_1 = base_optimizer.optimize(problem, print_limit)
            _x_history.extend(res_1.x_history)
            _f_history.extend(res_1.f_history)
            _global_state_history.extend(res_1.global_state_history)
            _mask.extend(res_1.step_mask)

            if res_1.status_code == 1:
                return OptResult(x_history=np.array(_x_history),
                                 f_history=np.array(_f_history),
                                 step_mask=np.array(_mask),
                                 global_state_history=_global_state_history,
                                 status_code=res.status_code,
                                 status_message=res.status_message,
                                 error_list=_error_list
                                 ), constaint_status

            # problem(res.x_history[-1])
            problem(res.x_history[res_1.step_mask][-1])
            factor = problem.constraint_factor
            problem.callback()

            if abs(factor) < tol:
                constaint_status = 1
                return OptResult(x_history=np.array(_x_history),
                                 f_history=np.array(_f_history),
                                 step_mask=np.array(_mask),
                                 global_state_history=_global_state_history,
                                 status_code=res.status_code,
                                 status_message=res.status_message,
                                 error_list=_error_list
                                 ), constaint_status
            res = res_1
            problem.modify_constraint()

        return OptResult(x_history=np.fromiter(_x_history, dtype=np.dtype((float, _x_history[0].shape))),
                         f_history=np.fromiter(map(float, _f_history), dtype=np.float),
                         step_mask=np.fromiter(_mask, dtype=int),
                         global_state_history=_global_state_history,
                         status_code=res.status_code,
                         status_message=res.status_message,
                         error_list=_error_list
                         ), constaint_status


class ParametricAnalyser(ABC):

    def compute_line(self, problem: OptProblem, post_func: Callable, var_idx=0, n_points=10):
        '''

        :param problem: Целевая функция
        :param post_func: Функция предназначенная для обработки global_state, чтобы отследить еще какую то переменную
        :param var_idx: Индекс переменной в массиве х0
        :param n_points: Кол-во точек
        :return: Массив переменной, массив функции
        '''

        x0, bounds = problem.get_x0_w_bounds()

        gl_state_line = []

        var_linspace = np.linspace(bounds[var_idx][0], bounds[var_idx][1], n_points)

        func_linspace = np.zeros_like(var_linspace)

        for i in range(n_points):
            xx = x0.copy()
            xx[var_idx] = var_linspace[i]
            problem(xx)
            gl_state_line.append(deepcopy(problem.global_state))
            func_linspace[i] = post_func(problem.global_state)

        problem.set_x(x0)

        return var_linspace, func_linspace, gl_state_line

    def compute_surface(self, problem: OptProblem, post_func: Callable, var_idx1=0, var_idx2=1, n_points=10):
        '''

        :param problem: Целевая функция
        :param post_func: Функция предназначенная для обработки global_state, чтобы отследить еще какую то переменную
        :param var_idx1: Индекс пераой переменной в массиве х0
        :param var_idx2: Индекс второй переменной в массиве х0
        :param n_points: Число точек разбиения
        :return: Сетку 1 переменной, сетку 2 переменной, сетку функции
        '''
        x0, bounds = problem.get_x0_w_bounds()
        gl_state_mesh = []

        var1_linspace = np.linspace(bounds[var_idx1][0], bounds[var_idx1][1], n_points)
        var2_linspace = np.linspace(bounds[var_idx2][0], bounds[var_idx2][1], n_points)

        mesh_var1, mesh_var2 = np.meshgrid(var1_linspace, var2_linspace)

        func_mesh = np.zeros_like(mesh_var1)

        for i in range(n_points):
            gl_state_i = []
            for j in range(n_points):
                xx = x0.copy()
                xx[var_idx1], xx[var_idx2] = mesh_var1[i, j], mesh_var2[i, j]
                problem(xx)
                gl_state_i.append(deepcopy(problem.global_state))
                func_mesh[i, j] = post_func(problem.global_state)
            gl_state_mesh.append(gl_state_i)

        problem.set_x(x0)

        return mesh_var1, mesh_var2, func_mesh, gl_state_mesh

    def compute_coefs(self, x_list, f_list, deriv_type='right'):
        '''

        :param x_list: Вектор варьируемого параметра
        :param f_list: Список целевых функций
        :param deriv_type: Тип аппроксимации производной для коэффициентов чувствительности
        :return: Абсолютный коэффициент чувствительности, относительный коэффициент чувствительности
        '''

        border = len(x_list) // 2 + 1

        if deriv_type == 'right':
            x_0 = x_list[border]
            x_1 = x_list[border + 1]

            f_0 = f_list[border]
            f_1 = f_list[border + 1]

            dx = x_1 - x_0
            df = f_1 - f_0

        elif deriv_type == 'left':
            x_0 = x_list[border]
            x_1 = x_list[border - 1]

            f_0 = f_list[border]
            f_1 = f_list[border - 1]

            dx = x_0 - x_1
            df = f_0 - f_1

        elif deriv_type == 'central':
            x_m1 = x_list[border - 1]
            x_1 = x_list[border + 1]

            f_m1 = f_list[border - 1]
            f_1 = f_list[border + 1]

            dx = x_1 - x_m1
            df = f_1 - f_m1

        aij = df / dx

        if aij != 0.:
            bij = aij * x_list[border] / f_list[border]
        else:
            bij = np.inf

        return aij, bij

        pass

    def analyze(self, problem: OptProblem, n_points=5, deriv_type='right'):
        x0, bounds = problem.get_x0_w_bounds()
        n_params = x0.shape[0]
        x_to_analyze = np.zeros((n_params, n_points, n_params))

        f_history = []
        global_state_history = []

        sense_koefs = np.zeros((n_params, 2))

        for i in range(n_params):
            param_bounds = bounds[i]
            param_linspace = np.linspace(param_bounds[0], param_bounds[1], n_points)
            for n in range(n_points):
                xx = x0.copy()
                xx[i] = param_linspace[n]
                x_to_analyze[i, n, :] = xx

        for i in range(n_params):
            param_linspace = x_to_analyze[i]
            tmp_f_history = []
            tmp_global_state_history = []
            for n in range(n_points):
                x = param_linspace[n]
                f = problem(x)
                problem.callback()
                tmp_f_history.append(f)
                tmp_global_state_history.append(deepcopy(problem.global_state))
            aij, bij = self.compute_coefs(param_linspace[:, i], tmp_f_history, deriv_type)
            sense_koefs[i, :] = aij, bij
            f_history.append(tmp_f_history)
            global_state_history.append(tmp_global_state_history)
        problem.set_x(x0)

        return x_to_analyze, f_history, global_state_history, sense_koefs