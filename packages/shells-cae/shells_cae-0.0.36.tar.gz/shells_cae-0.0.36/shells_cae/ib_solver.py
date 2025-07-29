import numpy as np
import cffi, os, sys

__all__ = ['ThermoInternalBallisticsSolver']

class TooMuchPowderError(Exception):
    def __str__(self):
        return "Слишком много пороха"

class TooMuchTimeError(Exception):
    def __str__(self):
        return "Превышено максимальное время процесса"

def load_lib():
    HERE = os.path.dirname(__file__)
    if sys.platform.startswith('linux'):
        LIB_FILE_NAME = os.path.abspath(os.path.join(HERE, ".", "compiled", "build", "bin", "lib", "libsintbal.so"))
    elif sys.platform.startswith('win32'):
        LIB_FILE_NAME = os.path.abspath(os.path.join(HERE, ".", "compiled", "build", "bin", "libsintbal.dll"))
    else:
        raise Exception('Неподдерживаемая платформа')
    ffi = cffi.FFI()
    ffi.cdef(
        '''
        typedef struct barrel{\n
        double d;\n
        double q;\n
        double s;\n
        double w0;\n
        double l_d;\n
        double l_k;\n
        double l0;\n
        double kf;\n
        } barrel;
        '''
    )
    ffi.cdef(
        '''
        typedef struct ibproblem{\n
        barrel artsystem;\n
        double p0;\n
        double pv;\n
        double ig_mass;\n
        double t0;\n
        double v0;\n
        double p_av_max;\n
        double p_sn_max;\n
        double p_kn_max;\n
        double psi_sum;\n
        double eta_k;\n
        int status;
        } ibproblem;
        '''
    )
    ffi.cdef(
        '''
        typedef struct powder{\n
        double om;\n
        double ro;\n
        double f_powd;\n
        double ti;\n
        double jk;\n
        double alpha;\n
        double theta;\n
        double zk;\n
        double kappa1;\n
        double lambda1;\n
        double mu1;\n
        double kappa2;\n
        double lambda2;\n
        double mu2;\n
        double gamma_f;\n
        double gamma_jk;\n
        } powder;
        '''
    )
    ffi.cdef(
        '''
        void set_problem(\n
        ibproblem *problem,\n
        double p0,\n
        double pv,\n
        double ig_mass,\n
        double t0\n
        );
        '''
    )
    ffi.cdef(
        '''
        void set_barrel(\n
        ibproblem *problem,\n
        double d,\n
        double q,\n
        double s,\n
        double w0,\
        double l_d,\n
        double l_k,\n
        double l0,\n
        double kf\n
        );
        '''
    )
    ffi.cdef(
        '''
        void add_powder(\n
        int n_powd,\n
        powder *powd_array,\n
        int i,\n
        double om,\n
        double ro,\n
        double f_powd,\n
        double ti,\n
        double jk,\n
        double alpha,\n
        double theta,\n
        double zk,\n
        double kappa1,\n
        double lambda1,\n
        double mu1,\n
        double kappa2,\n
        double lambda2,\n
        double mu2,\n
        double gamma_f,\n
        double gamma_jk\n
        );
        '''
    )
    ffi.cdef(
        '''
        void count_ib(ibproblem *ibp, int n_powd, powder *charge, double tstep, double tend);
        '''
    )
    ffi.cdef(
        '''
        void dense_count_ib(ibproblem *ibp, int n_powd, powder *charge, double tstep, double tend,\n
        int *n_tsteps, double *y_array, double *pressure_array);
        '''
    )
    bal_lib = ffi.dlopen(LIB_FILE_NAME)
    return ffi, bal_lib

FFI, BAL_LIB = load_lib()

class ThermoInternalBallisticsSolver:

    name = 'thermo_ib_solver'

    preprocess_data = dict(
        d=None,
        q=None,
        S=None,
        W0=None,
        l_d=None,
        khi=None,
        Kf=None,
        P0=None,
        PV=None,
        ig_mass=None,
        T0=None,
    )

    def preprocessor(self, data: dict, global_state: dict):

        raise NotImplementedError()

    def run(self, data: dict, global_state: dict):

        powders: dict = data['powders'] # Словарь с порохами (ключи марки/id, значения - словарь с характеристиками)

        # self._preprocessor(data, global_state) # Словарь с настройками задачи (орудие + давление/масса воспламенителя, давление форсироания, температура МЗ, шаг по времени, время расчета)

        ib_data = self.preprocess_data

        ib_settings: dict = data['settings'][ThermoInternalBallisticsSolver.name] # Словарь с доп настройками задачи (давление/масса воспламенителя, давление форсироания, температура МЗ, шаг по времени, время расчета)

        n_powd = len(powders)
        new_problem = FFI.new('ibproblem *')
        powd_array = FFI.new(f'powder[{n_powd}]')

        P0 = ib_data.get('P0', 30e6)
        PV = ib_data.get('PV', 4e6)
        ig_mass = ib_data.get('ig_mass', 0.)
        T0 = ib_data.get('T0', 15.)

        tstep = ib_settings.get('tstep', 1e-5)
        tmax = ib_settings.get('tmax', 1.)

        n_tsteps = FFI.new('int *')
        n_tsteps[0] = int(tmax/tstep)

        BAL_LIB.set_problem(new_problem,
                            P0,
                            PV,
                            ig_mass,
                            T0)

        d = ib_data['d']
        q = ib_data['q']
        S = ib_data['S']
        W0 = ib_data['W0']
        l_d = ib_data['l_d']
        l_k = W0 / (S * ib_data['khi'])
        l_0 = W0 / S
        Kf = ib_data['Kf']

        for i, powd in enumerate(powders.values(), start=1):
            BAL_LIB.add_powder(
                n_powd, powd_array, i,
                powd['om'], powd['rho'], powd['f_powd'], powd['Ti'],
                powd['Jk'], powd['alpha'], powd['theta'],
                powd['Zk'], powd['kappa1'], powd['lambd1'], powd['mu1'], powd['kappa2'], powd['lambd2'], powd['mu2'],
                powd['gamma_f'], powd['gamma_Jk']
            )

        BAL_LIB.set_barrel(new_problem, d, q, S, W0, l_d, l_k, l_0, Kf)

        y_array = np.empty((2 + n_powd, n_tsteps[0]), dtype=np.float64, order='F')
        pressure_array = np.empty((3, n_tsteps[0]), dtype=np.float64, order='F')

        y_array_ptr = FFI.cast("double*", y_array.__array_interface__['data'][0])
        pressure_array_ptr = FFI.cast("double*", pressure_array.__array_interface__['data'][0])

        BAL_LIB.dense_count_ib(new_problem, n_powd, powd_array, tstep, tmax, n_tsteps, y_array_ptr, pressure_array_ptr)

        calc_status = new_problem[0].status

        if calc_status == 0:
            y_array = y_array[:, :n_tsteps[0]]
            pressure_array = pressure_array[:, :n_tsteps[0]]
            ts = np.linspace(0., tstep * n_tsteps[0], n_tsteps[0])
            lk_indexes = np.argmin(1.0 - y_array[2:], axis=1)

            res_dict = dict(
                v0=new_problem[0].v0,
                p_sn_max=new_problem[0].p_sn_max,
                p_av_max=new_problem[0].p_av_max,
                p_kn_max=new_problem[0].p_kn_max,
                psi_sum=new_problem[0].psi_sum,
                eta_k=new_problem[0].eta_k,
                p_av_array=pressure_array[0],
                p_sn_array=pressure_array[1],
                p_kn_array=pressure_array[2],
                t_array=ts,
                v_array=y_array[0],
                l_array=y_array[1],
                psi_array=y_array[2:],
                lk_indexes=lk_indexes
            )

            global_state[ThermoInternalBallisticsSolver.name] = res_dict

        if calc_status == 1:
            raise TooMuchPowderError()
        elif calc_status == 2:
            raise TooMuchTimeError()

