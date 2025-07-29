import cffi, os, sys
import numpy as np
from typing import TypedDict



def load_lib():

    HERE = os.path.dirname(__file__)
    if sys.platform.startswith('linux'):
        LIB_FILE_NAME = os.path.abspath(os.path.join(HERE, ".", "compiled", "build", "bin", "lib", "libkontur.so"))
    elif sys.platform.startswith('win32'):
        LIB_FILE_NAME = os.path.abspath(os.path.join(HERE, ".", "compiled", "build", "bin", "libkontur.dll"))
    else:
        raise Exception('Неподдерживаемая платформа')
    ffi = cffi.FFI()

    ffi.cdef(
        '''
    typedef struct csv_st csv;
    
    enum geometry_primitives {
      G_CYLINDR = 1,       //Цилиндр
      G_CONE = 2,          //Конус
      G_REVERSE_OGIVE = 3, //Обратное оживало
      G_OGIVE = 4,         //Оживало
      G_EXPONENT = 5,      //Экспонента
      G_PARABOLIC =6       //Парабола
    };
    
    csv *CSV_New(void);
    void CSV_SetNG(csv *p_csv, const int ng); //Кол-во участков в головной части
    void CSV_SetNH(csv *p_csv, const int nh); //Кол-во участков головной и цилиндрической
                                  // частей (ng или ng+1)
    
    void CSV_SetNK(csv *p_csv, const int nk); //Общее кол-во участков на снаряде
    void CSV_SetNFL(csv *p_csv, const int nfl); //Вид притупления nfl=1 - сферическое,
                                    // nfl= 2..100- другое
    void CSV_SetISIG(csv *p_csv, const int isig); //Не обязательно!
                   //Параметр учета толщины вытеснения пограничного слоя
                   //isig = 0 - учитывается (L <= 7*d) (по умолчанию)
                   //isig = 1 - не учитывается (L > 7*d)
    
    void CSV_SetYInt(csv *p_csv, const double yint); //Высота носика, м
    void CSV_SetDia(csv *p_csv, const double d); //Диаметр снаряда, м
    void CSV_SetHb(csv *p_csv, const double hb); //Высота пояска, м
    void CSV_SetA(csv *p_csv, const double a); //Не обязательно! Скорость звука, м/с.
                                      //(По умолчанию 340,8)
    void CSV_SetRo(csv *p_csv, const double ro); //Не обязательно! Плотность воздуха,
                                     //м/с. (По умолчанию 0,1229)
    void CSV_SetAMU(csv *p_csv, const double amu); //Не обязательно! Динамическая
                       //вязкость воздуха, Н*с/m^2 (По умолчанию 1,825E-6)
    void CSV_SetC2(csv *p_csv, const double c2); //Не обязательно! Шаг сетки по оси X, м
                                     //(По умолчанию 0,02)
    
    void CSV_SetXct(csv *p_csv, const double xct);//Координата центра тяжести от носика, м
    
    void CSV_AddGeom(csv *p_csv, const int num, const int type,
                     const double x1, const double x2,
                     const double r1, const double r2,
                     const double rd, const double exp);
    /* Добавляет/заменяет геометрический примитив
     * при замене нужно переопределить все примитивы!
     * num - Индекс примитива начиная с 0
     * type - Тип примитива (см. geometry_primitives)
     * x1, x2 - Начальная и конечная координата x от носика
     * r1, r2 - Радиус в начальной и конечной точке
     * rd - Радиус, если оживало, м
     * exp - Показатель степени, если экспонента
     */
    
    const char *CSV_CheckError(csv *p_csv); //Проверяет готовность к расчету
                                      //Возвращает описание ошибки или NULL
    
    void CSV_Solve(csv *p_csv, const double mach, const double angle);
    // Определяет геометрические к-нты для заданного числа Маха и угла
    // нутации
    
    void CSV_Solve_Array(csv *p_csv, double *mach_array, double *angle_array, int n_machs, int n_angles,
                        double **tren, double **don, double **voln, double **pois, double **cn, double **cy, 
                        double **xcd, double **cx, double **cyal, double **cmal, double **mxwx, double **mzwx);
    // Определяет геометрические к-нты для массива чисел Маха и углов
    // нутации
    
    double CSV_GetMach(csv *p_csv); //Число маха
    double CSV_GetTren(csv *p_csv); //К-нт силы трения (Cx трен)
    double CSV_GetDon(csv *p_csv);  //К-нт донного сопротивления (Cx дон)
    double CSV_GetVoln(csv *p_csv); //К-нт волнового сопротивления (Cx волн)
    double CSV_GetPois(csv *p_csv); //К-нт сопротивления пояска (Cx пояс)
    double CSV_GetCn(csv *p_csv);   //К-нт нормальной силы (Cn)
    double CSV_GetCy(csv *p_csv);   //К-нт подъемной силы (Cy)
    double CSV_GetXcd(csv *p_csv);  //Положение центра давления от носика, м
    double CSV_GetCx(csv *p_csv);   //К-нт лобового сопротивления (Cx)
    double CSV_GetCyAl(csv *p_csv); //
    double CSV_GetCmAl(csv *p_csv); //
    double CSV_GetMzWz(csv *p_csv);  //
    double CSV_GetMxWx(csv *p_csv); //
    void CSV_Free(csv *p_csv);      //
        '''
    )

    lib = ffi.dlopen(LIB_FILE_NAME)

    return ffi, lib

FFI, KONTUR_LIB = load_lib()

class data(TypedDict):
    ng: float
    nh: float
    nk: float
    nfl: float
    d: float
    hb: float
    xct: float
    yint: float
    geometry_data: list


class KonturSolver:

    name = 'kontur_solver'

    preprocessed_data: data = dict(
        ng=None,
        nh=None,
        nk=None,
        nfl=None,
        d=None,
        hb=None,
        xct=None,
        yint=None,
        geometry_data=None
    )
    def preprocessor(self, data: dict, global_state: dict):

        self.preprocessed_data['ng'] = global_state['mcc_solver']['kontur']['ng']
        self.preprocessed_data['nh'] = global_state['mcc_solver']['kontur']['nh']
        self.preprocessed_data['nk'] = global_state['mcc_solver']['kontur']['nk']
        self.preprocessed_data['nfl'] = global_state['mcc_solver']['kontur']['nfl']
        self.preprocessed_data['d'] = global_state['mcc_solver']['kontur']['d']
        self.preprocessed_data['hb'] = global_state['mcc_solver']['kontur']['hb']
        self.preprocessed_data['xct'] = global_state['mcc_solver']['kontur']['xct']
        self.preprocessed_data['yint'] = global_state['mcc_solver']['kontur']['yint']
        self.preprocessed_data['geometry_data'] = global_state['mcc_solver']['kontur']['geometry_data']


    def run(self, data, global_state):
        p_data = self.preprocessed_data
        solver = KONTUR_LIB.CSV_New()
        KONTUR_LIB.CSV_SetNG(solver, p_data['ng'])
        KONTUR_LIB.CSV_SetNH(solver, p_data['nh'])
        KONTUR_LIB.CSV_SetNK(solver, p_data['nk'])
        KONTUR_LIB.CSV_SetNFL(solver, p_data['nfl'])
        KONTUR_LIB.CSV_SetDia(solver, p_data['d'])
        KONTUR_LIB.CSV_SetHb(solver, p_data['hb'])
        KONTUR_LIB.CSV_SetXct(solver, p_data['xct'])
        KONTUR_LIB.CSV_SetYInt(solver, p_data['yint'])

        for i, primitive in enumerate(p_data['geometry_data']):
            KONTUR_LIB.CSV_AddGeom(solver, i, primitive['type'], primitive['x1'], primitive['x2'],
                                   primitive['r1'], primitive['r2'], primitive['R'], primitive['n'])

        settings = data['settings']['kontur']

        angle_list = np.linspace(settings['alpha_0'], settings['alpha_n'], settings['n_alpha'])
        mach_list = np.linspace(settings['mach_0'], settings['mach_n'], settings['n_mach'])

        n_machs = mach_list.shape[0]
        n_angles = angle_list.shape[0]

        mach_list = np.ascontiguousarray(mach_list, dtype='float64')
        angle_list = np.ascontiguousarray(angle_list, dtype='float64')

        mesh_tren = np.empty((n_angles, n_machs), order='C', dtype='float64')
        mesh_don = np.empty_like(mesh_tren)
        mesh_voln = np.empty_like(mesh_tren)
        mesh_pois = np.empty_like(mesh_tren)
        mesh_cn = np.empty_like(mesh_tren)
        mesh_cy = np.empty_like(mesh_tren)
        mesh_xcd = np.empty_like(mesh_tren)
        mesh_cx = np.empty_like(mesh_tren)
        mesh_cyal = np.empty_like(mesh_tren)
        mesh_cmal = np.empty_like(mesh_tren)
        mesh_mxwx = np.empty_like(mesh_tren)
        mesh_mzwz = np.empty_like(mesh_tren)

        angle_list_ptr = FFI.cast(f'double *', angle_list.ctypes.data)
        mach_list_ptr = FFI.cast(f'double *', mach_list.ctypes.data)

        mesh_tren_ptr = FFI.new(f'double *[{n_angles}]')
        mesh_don_ptr = FFI.new(f'double *[{n_angles}]')
        mesh_voln_ptr = FFI.new(f'double *[{n_angles}]')
        mesh_pois_ptr = FFI.new(f'double *[{n_angles}]')
        mesh_cn_ptr = FFI.new(f'double *[{n_angles}]')
        mesh_cy_ptr = FFI.new(f'double *[{n_angles}]')
        mesh_xcd_ptr = FFI.new(f'double *[{n_angles}]')
        mesh_cx_ptr = FFI.new(f'double *[{n_angles}]')
        mesh_cyal_ptr = FFI.new(f'double *[{n_angles}]')
        mesh_cmal_ptr = FFI.new(f'double *[{n_angles}]')
        mesh_mxwx_ptr = FFI.new(f'double *[{n_angles}]')
        mesh_mzwz_ptr = FFI.new(f'double *[{n_angles}]')

        for i in range(n_angles):
            mesh_tren_ptr[i] = FFI.cast('double *', mesh_tren[i].ctypes.data)
            mesh_don_ptr[i] = FFI.cast('double *', mesh_don[i].ctypes.data)
            mesh_voln_ptr[i] = FFI.cast('double *', mesh_voln[i].ctypes.data)
            mesh_pois_ptr[i] = FFI.cast('double *', mesh_pois[i].ctypes.data)
            mesh_cn_ptr[i] = FFI.cast('double *', mesh_cn[i].ctypes.data)
            mesh_cy_ptr[i] = FFI.cast('double *', mesh_cy[i].ctypes.data)
            mesh_xcd_ptr[i] = FFI.cast('double *', mesh_xcd[i].ctypes.data)
            mesh_cx_ptr[i] = FFI.cast('double *', mesh_cx[i].ctypes.data)
            mesh_cyal_ptr[i] = FFI.cast('double *', mesh_cyal[i].ctypes.data)
            mesh_cmal_ptr[i] = FFI.cast('double *', mesh_cmal[i].ctypes.data)
            mesh_mxwx_ptr[i] = FFI.cast('double *', mesh_mxwx[i].ctypes.data)
            mesh_mzwz_ptr[i] = FFI.cast('double *', mesh_mzwz[i].ctypes.data)


        KONTUR_LIB.CSV_Solve_Array(
            solver, mach_list_ptr, angle_list_ptr, n_machs, n_angles,
            mesh_tren_ptr, mesh_don_ptr, mesh_voln_ptr, mesh_pois_ptr, mesh_cn_ptr, mesh_cy_ptr,
            mesh_xcd_ptr, mesh_cx_ptr, mesh_cyal_ptr, mesh_cmal_ptr, mesh_mxwx_ptr, mesh_mzwz_ptr
        )

        # for i, atk_angl in enumerate(angle_list):
        #     for j, mach in enumerate(mach_list):
        #         KONTUR_LIB.CSV_Solve(solver, mach, atk_angl)
        #         mesh_tren[i, j] = KONTUR_LIB.CSV_GetTren(solver)
        #         mesh_don[i, j] = KONTUR_LIB.CSV_GetDon(solver)
        #         mesh_voln[i, j] = KONTUR_LIB.CSV_GetVoln(solver)
        #         mesh_pois[i, j] = KONTUR_LIB.CSV_GetPois(solver)
        #         mesh_cn[i, j] = KONTUR_LIB.CSV_GetCn(solver)
        #         mesh_cy[i, j] = KONTUR_LIB.CSV_GetCy(solver)
        #         mesh_xcd[i, j] = KONTUR_LIB.CSV_GetXcd(solver)
        #         mesh_cx[i, j] = KONTUR_LIB.CSV_GetCx(solver)
        #         mesh_cyal[i, j] = KONTUR_LIB.CSV_GetCyAl(solver)
        #         mesh_cmal[i, j] = KONTUR_LIB.CSV_GetCmAl(solver)
        #         mesh_mxwx[i, j] = KONTUR_LIB.CSV_GetMxWx(solver)
        #         mesh_mzwz[i, j] = KONTUR_LIB.CSV_GetMzWz(solver)

        global_state[KonturSolver.name] = dict(
            mesh_tren=mesh_tren,
            mesh_don=mesh_don,
            mesh_voln=mesh_voln,
            mesh_pois=mesh_pois,
            mesh_cn=mesh_cn,
            mesh_cy=mesh_cy,
            mesh_xcd=mesh_xcd,
            mesh_cx=mesh_cx,
            mesh_cyal=mesh_cyal,
            mesh_cmal=mesh_cmal,
            mesh_mxwx=mesh_mxwx,
            mesh_mzwz=mesh_mzwz
        )


        global_state[KonturSolver.name] = dict(
            cx_list=mesh_cx[0],
            mach_list=mach_list
        )



if __name__ == '__main__':
    import matplotlib.pyplot as plt

    def print_solver(solver):
        print(
            KONTUR_LIB.CSV_GetMach(solver),
            KONTUR_LIB.CSV_GetTren(solver),
            KONTUR_LIB.CSV_GetDon(solver),
            KONTUR_LIB.CSV_GetVoln(solver),
            KONTUR_LIB.CSV_GetPois(solver),
            KONTUR_LIB.CSV_GetCn(solver),
            KONTUR_LIB.CSV_GetCy(solver),
            KONTUR_LIB.CSV_GetXcd(solver),
            KONTUR_LIB.CSV_GetCx(solver),
            KONTUR_LIB.CSV_GetCyAl(solver),
            KONTUR_LIB.CSV_GetCmAl(solver),
            KONTUR_LIB.CSV_GetMxWx(solver),
            KONTUR_LIB.CSV_GetMzWz(solver),
        )

    def kontur_array(n_machs=100, n_angles=5):
        solver = KONTUR_LIB.CSV_New()
        KONTUR_LIB.CSV_SetNG(solver, 4)
        KONTUR_LIB.CSV_SetNH(solver, 5)
        KONTUR_LIB.CSV_SetNK(solver, 7)
        KONTUR_LIB.CSV_SetNFL(solver, 2)
        KONTUR_LIB.CSV_SetDia(solver, 0.1524)
        KONTUR_LIB.CSV_SetHb(solver, 0.01 * 0.1524)
        KONTUR_LIB.CSV_SetXct(solver, 0.533)
        KONTUR_LIB.CSV_SetYInt(solver, 0.)
        KONTUR_LIB.CSV_AddGeom(solver, 0, KONTUR_LIB.G_CYLINDR, 0., .01, .01, .01, 0., 0.)
        KONTUR_LIB.CSV_AddGeom(solver, 1, KONTUR_LIB.G_CONE, .01, .06, .01, .02, 0., 0.)
        KONTUR_LIB.CSV_AddGeom(solver, 2, KONTUR_LIB.G_CONE, .06, .18, .02, .0425, 0., 0.)
        KONTUR_LIB.CSV_AddGeom(solver, 3, KONTUR_LIB.G_OGIVE, .18, .457, .0425, .0762, 3.22, 0.)
        KONTUR_LIB.CSV_AddGeom(solver, 4, KONTUR_LIB.G_CYLINDR, .457, .712, .0762, .0762, .0, 0.)
        KONTUR_LIB.CSV_AddGeom(solver, 5, KONTUR_LIB.G_CONE, .712, .723, .0762, .0748, .0, 0.)
        KONTUR_LIB.CSV_AddGeom(solver, 6, KONTUR_LIB.G_CONE, .723, .863, .0748, .06675, .0, 0.)

        angle_list = np.linspace(0., 1., n_angles).astype('float64')
        mach_list = np.linspace(0.4, 5, n_machs).astype('float64')

        mach_list = np.ascontiguousarray(mach_list, dtype='float64')
        angle_list = np.ascontiguousarray(angle_list, dtype='float64')

        mach_list = np.ascontiguousarray(mach_list, dtype='float64')
        angle_list = np.ascontiguousarray(angle_list, dtype='float64')

        mesh_tren = np.empty((n_angles, n_machs), order='C', dtype='float64')
        mesh_don = np.empty_like(mesh_tren)
        mesh_voln = np.empty_like(mesh_tren)
        mesh_pois = np.empty_like(mesh_tren)
        mesh_cn = np.empty_like(mesh_tren)
        mesh_cy = np.empty_like(mesh_tren)
        mesh_xcd = np.empty_like(mesh_tren)
        mesh_cx = np.empty_like(mesh_tren)
        mesh_cyal = np.empty_like(mesh_tren)
        mesh_cmal = np.empty_like(mesh_tren)
        mesh_mxwx = np.empty_like(mesh_tren)
        mesh_mzwz = np.empty_like(mesh_tren)

        angle_list_ptr = FFI.cast(f'double *', angle_list.ctypes.data)
        mach_list_ptr = FFI.cast(f'double *', mach_list.ctypes.data)

        mesh_tren_ptr = FFI.new(f'double *[{n_angles}]')
        mesh_don_ptr = FFI.new(f'double *[{n_angles}]')
        mesh_voln_ptr = FFI.new(f'double *[{n_angles}]')
        mesh_pois_ptr = FFI.new(f'double *[{n_angles}]')
        mesh_cn_ptr = FFI.new(f'double *[{n_angles}]')
        mesh_cy_ptr = FFI.new(f'double *[{n_angles}]')
        mesh_xcd_ptr = FFI.new(f'double *[{n_angles}]')
        mesh_cx_ptr = FFI.new(f'double *[{n_angles}]')
        mesh_cyal_ptr = FFI.new(f'double *[{n_angles}]')
        mesh_cmal_ptr = FFI.new(f'double *[{n_angles}]')
        mesh_mxwx_ptr = FFI.new(f'double *[{n_angles}]')
        mesh_mzwz_ptr = FFI.new(f'double *[{n_angles}]')

        for i in range(n_angles):
            mesh_tren_ptr[i] = FFI.cast('double *', mesh_tren[i].ctypes.data)
            mesh_don_ptr[i] = FFI.cast('double *', mesh_don[i].ctypes.data)
            mesh_voln_ptr[i] = FFI.cast('double *', mesh_voln[i].ctypes.data)
            mesh_pois_ptr[i] = FFI.cast('double *', mesh_pois[i].ctypes.data)
            mesh_cn_ptr[i] = FFI.cast('double *', mesh_cn[i].ctypes.data)
            mesh_cy_ptr[i] = FFI.cast('double *', mesh_cy[i].ctypes.data)
            mesh_xcd_ptr[i] = FFI.cast('double *', mesh_xcd[i].ctypes.data)
            mesh_cx_ptr[i] = FFI.cast('double *', mesh_cx[i].ctypes.data)
            mesh_cyal_ptr[i] = FFI.cast('double *', mesh_cyal[i].ctypes.data)
            mesh_cmal_ptr[i] = FFI.cast('double *', mesh_cmal[i].ctypes.data)
            mesh_mxwx_ptr[i] = FFI.cast('double *', mesh_mxwx[i].ctypes.data)
            mesh_mzwz_ptr[i] = FFI.cast('double *', mesh_mzwz[i].ctypes.data)


        KONTUR_LIB.CSV_Solve_Array(
            solver, mach_list_ptr, angle_list_ptr, n_machs, n_angles,
            mesh_tren_ptr, mesh_don_ptr, mesh_voln_ptr, mesh_pois_ptr, mesh_cn_ptr, mesh_cy_ptr,
            mesh_xcd_ptr, mesh_cx_ptr, mesh_cyal_ptr, mesh_cmal_ptr, mesh_mxwx_ptr, mesh_mzwz_ptr
        )

        # print(mesh_cx)

    def kontur(n_machs=100, n_angles=5):
        solver = KONTUR_LIB.CSV_New()
        KONTUR_LIB.CSV_SetNG(solver, 4)
        KONTUR_LIB.CSV_SetNH(solver, 5)
        KONTUR_LIB.CSV_SetNK(solver, 7)
        KONTUR_LIB.CSV_SetNFL(solver, 2)
        KONTUR_LIB.CSV_SetDia(solver, 0.1524)
        KONTUR_LIB.CSV_SetHb(solver, 0.01 * 0.1524)
        KONTUR_LIB.CSV_SetXct(solver, 0.533)
        KONTUR_LIB.CSV_SetYInt(solver, 0.)
        KONTUR_LIB.CSV_AddGeom(solver, 0, KONTUR_LIB.G_CYLINDR, 0., .01, .01, .01, 0., 0.)
        KONTUR_LIB.CSV_AddGeom(solver, 1, KONTUR_LIB.G_CONE, .01, .06, .01, .02, 0., 0.)
        KONTUR_LIB.CSV_AddGeom(solver, 2, KONTUR_LIB.G_CONE, .06, .18, .02, .0425, 0., 0.)
        KONTUR_LIB.CSV_AddGeom(solver, 3, KONTUR_LIB.G_OGIVE, .18, .457, .0425, .0762, 3.22, 0.)
        KONTUR_LIB.CSV_AddGeom(solver, 4, KONTUR_LIB.G_CYLINDR, .457, .712, .0762, .0762, .0, 0.)
        KONTUR_LIB.CSV_AddGeom(solver, 5, KONTUR_LIB.G_CONE, .712, .723, .0762, .0748, .0, 0.)
        KONTUR_LIB.CSV_AddGeom(solver, 6, KONTUR_LIB.G_CONE, .723, .863, .0748, .06675, .0, 0.)

        angle_list = np.linspace(0., 1., n_angles).astype('float64')
        mach_list = np.linspace(0.4, 5, n_machs).astype('float64')

        mesh_tren = np.empty((angle_list.shape[0], mach_list.shape[0]), order='C')
        mesh_don = np.empty_like(mesh_tren)
        mesh_voln = np.empty_like(mesh_tren)
        mesh_pois = np.empty_like(mesh_tren)
        mesh_cn = np.empty_like(mesh_tren)
        mesh_cy = np.empty_like(mesh_tren)
        mesh_xcd = np.empty_like(mesh_tren)
        mesh_cx = np.empty_like(mesh_tren)
        mesh_cyal = np.empty_like(mesh_tren)
        mesh_cmal = np.empty_like(mesh_tren)
        mesh_mxwx = np.empty_like(mesh_tren)
        mesh_mzwz = np.empty_like(mesh_tren)


        for i, atk_angl in enumerate(angle_list):
            # print(f'Угол нутации: {atk_angl}')
            for j, mach in enumerate(mach_list):
                KONTUR_LIB.CSV_Solve(solver, mach, atk_angl)
                # KONTUR_LIB.CSV_GetMach(solver)
                mesh_tren[i, j] = KONTUR_LIB.CSV_GetTren(solver)
                mesh_don[i, j] = KONTUR_LIB.CSV_GetDon(solver)
                mesh_voln[i, j] = KONTUR_LIB.CSV_GetVoln(solver)
                mesh_pois[i, j] = KONTUR_LIB.CSV_GetPois(solver)
                mesh_cn[i, j] = KONTUR_LIB.CSV_GetCn(solver)
                mesh_cy[i, j] = KONTUR_LIB.CSV_GetCy(solver)
                mesh_xcd[i, j] = KONTUR_LIB.CSV_GetXcd(solver)
                mesh_cx[i, j] = KONTUR_LIB.CSV_GetCx(solver)
                mesh_cyal[i, j] = KONTUR_LIB.CSV_GetCyAl(solver)
                mesh_cmal[i, j] = KONTUR_LIB.CSV_GetCmAl(solver)
                mesh_mxwx[i, j] = KONTUR_LIB.CSV_GetMxWx(solver)
                mesh_mzwz[i, j] = KONTUR_LIB.CSV_GetMzWz(solver)




    # test_kontur()
    kontur_array()
