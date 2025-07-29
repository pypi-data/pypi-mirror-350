import cffi
import os
import numpy as np
import sys
from typing import Sequence, Union
from .solvers_abc import ABCSolver

def load_lib():
    HERE = os.path.dirname(__file__)
    if sys.platform.startswith('linux'):
        LIB_FILE_NAME = os.path.abspath(os.path.join(HERE, ".", "compiled", "build", "bin", "lib", "libpenetrationlib.so"))
    elif sys.platform.startswith('win32'):
        LIB_FILE_NAME = os.path.abspath(os.path.join(HERE, ".", "compiled", "build", "bin", "libpenetrationlib.dll"))
    else:
        raise Exception('Неподдерживаемая платформа')
    ffi = cffi.FFI()
    ffi.cdef(
        '''
        typedef struct material{\n
        double sigma;\n
        double rho;\n
        double C;\n
        double a;\n
        double lambda;\n
        } material;
        '''
    )
    ffi.cdef(
        '''
        typedef struct hedge{\n
        material mat;\n
        double E;\n
        double nu;\n
        double lambda1;\n
        double A;\n
        double gamma;\n
        } hedge;
        '''
    )
    ffi.cdef(
        '''
        typedef struct kernel{\n
        material mat;\n
        double c_zv;\n
        double da;\n
        double la;\n
        double vc;\n
        } kernel;
        '''
    )

    ffi.cdef(
        '''
        typedef struct pen_prob{\n
        double u_0;\n
        double d;\n
        double r_g;\n
        } pen_prob;
        '''
    )
    ffi.cdef(
        '''
        void set_hedge_material(\n
        hedge *ahedge,\n
        double sigma,\n
        double rho,\n
        double a,\n
        double lambda\n
        );
        '''
    )
    ffi.cdef(
        '''
        void set_kernel_material(\n
        kernel *akernel,\n
        double sigma,\n
        double rho,\n
        double a,\n
        double lambda\n
        );
        '''
    )

    ffi.cdef(
        '''
        void init_hedge(\n
        hedge *ahedge,\n
        double E,\n
        double nu,\n
        double lambda1\n
        );
        '''
    )
    ffi.cdef(
        '''
        void init_kernel(\n
        kernel *akernel,\n
        double c_zv,\n
        double da,\n
        double la,\n
        double vc\n
        );
        '''
    )

    ffi.cdef(
        '''
        void compute_penetration(\n
        double *y_s,\n
        pen_prob *prob,\n
        kernel *akernel,\n
        hedge *ahedge,\n
        double tstep,\n
        double tmax\n
        );
        '''
    )

    ffi.cdef(
        '''
        void dense_compute_penetration(\n
        double *y_s,\n
        int *ntsteps,\n
        pen_prob *prob,\n
        kernel *akernel,\n
        hedge *ahedge,\n
        double tstep,\n
        double tmax\n
        );
        '''
    )

    bal_lib = ffi.dlopen(LIB_FILE_NAME)
    return ffi, bal_lib

FFI, PEN_LIB = load_lib()

class AlTateSolver(ABCSolver):
    name = 'al_tate_solver'

    preprocessed_data = dict(
        hedge_sigma=None,
        hedge_rho=None,
        hedge_c0=None,
        hedge_b0=None,
        kernel_sigma=None,
        kernel_rho=None,
        kernel_c0=None,
        kernel_b0=None,

        hedge_E=None,
        hedge_nu=None,
        hedge_lambd=None,

        kernel_c_zv=None,
        kernel_da=None,
        kernel_la=None,
        kernel_vc=None,

    )

    def run(self, data: dict, global_state: dict):

        p_data = self.preprocessed_data
        kernel = FFI.new('kernel *')
        hedge = FFI.new('hedge *')
        prob = FFI.new('pen_prob *')

        al_tate_settings = data['settings'][AlTateSolver.name]

        tstep = al_tate_settings['tstep']
        tmax = al_tate_settings['tmax']
        n_tsteps = FFI.new('int *')
        n_tsteps[0] = int(tmax / tstep)

        PEN_LIB.set_hedge_material(
            hedge,
            p_data['hedge_sigma'], p_data['hedge_rho'],
            p_data['hedge_c0'], p_data['hedge_b0']
        )

        PEN_LIB.set_kernel_material(
            kernel,
            p_data['kernel_sigma'], p_data['kernel_rho'],
            p_data['kernel_c0'], p_data['kernel_b0']
        )

        PEN_LIB.init_hedge(hedge,
                           p_data['hedge_E'],
                           p_data['hedge_nu'],
                           p_data['hedge_lambd']
                           )

        PEN_LIB.init_kernel(kernel, p_data['kernel_c_zv'],
                            p_data['kernel_da'], p_data['kernel_la'], p_data['kernel_vc'])


        y_s = np.zeros((4, n_tsteps[0]), order='F', dtype=np.float64)
        y_s_ptr = FFI.cast("double*", y_s.__array_interface__['data'][0])
        PEN_LIB.dense_compute_penetration(
            y_s_ptr, n_tsteps, prob, kernel, hedge, tstep, tmax
        )

        y_s = y_s[:, :n_tsteps[0]-1]
        t_s = np.linspace(0., tstep * n_tsteps[0], n_tsteps[0] - 1)

        global_state[AlTateSolver.name] = dict(
            t_array=t_s,
            x_array=y_s[0],
            l_array=y_s[1],
            v_array=y_s[2],
            u_array=y_s[3],
            u_v_array=y_s[2] - y_s[3]
        )