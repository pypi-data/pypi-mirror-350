import cffi
import os
import numpy as np
import sys
from typing import Sequence, Union

__all__ = ['McDragSolver']

def load_lib():
    HERE = os.path.dirname(__file__)

    ffi = cffi.FFI()
    if sys.platform.startswith('linux'):
        LIB_FILE_NAME = os.path.abspath(os.path.join(HERE, ".", "compiled", "build", "bin", "lib", "libmcdrag.so"))
    elif sys.platform.startswith('win32'):
        LIB_FILE_NAME = os.path.abspath(os.path.join(HERE, ".", "compiled", "build", "bin", "libmcdrag.dll"))
    else:
        raise Exception('Неподдерживаемая платформа')

    ffi.cdef(
        '''
        typedef struct shell{
        double d;
        double L;
        double h_l;
        double b_l;
        double m_d;
        double b_d;
        double bs_d;
        double hs_p;
        double t_r;
        int bl_code;
        } shell;

        void set_shell_geo(
        shell *ashell,
        double d,
        double L,
        double h_l,
        double b_l,
        double m_d,
        double b_d,
        double bs_d,
        double hs_p,
        int bl_code
        );

        double cdsf(double M, shell *ashell);
        double cdrb(double M, shell *ashell);
        double cdb(double M, shell *ashell);
        double cdbt(double M, shell *ashell);
        double cdh(double M, shell *ashell);
        double cd0(double M, shell *ashell);

        void get_aerodynamics(
        double *M,
        int n_machs,
        shell *ashell,
        double *cd0_array,
        double *cdh_array,
        double *cdbt_array,
        double *cdb_array,
        double *cdrb_array,
        double *cdsf_array
        );
        '''
    )

    bal_lib = ffi.dlopen(LIB_FILE_NAME)
    return ffi, bal_lib

FFI, MCDRAGLIB = load_lib()

class McDragSolver:
    name = 'mcdrag_solver'

    preprocessed_data = dict(
        d=None,
        L=None,
        h_l=None,
        b_l=None,
        m_d=None,
        b_d=None,
        bs_d=None,
        hs_p=None
    )

    def _get_fortran_shell(self, bl_code):
        ashell = FFI.new('shell *ashell')

        d = self.preprocessed_data['d']

        if not d:
            raise ValueError('Не заполнена геометрия')

        L = self.preprocessed_data['L']
        h_l = self.preprocessed_data['h_l']
        b_l = self.preprocessed_data['b_l']
        m_d = self.preprocessed_data['m_d']
        b_d = self.preprocessed_data['b_d']
        bs_d = self.preprocessed_data['bs_d']
        hs_p = self.preprocessed_data['hs_p']

        MCDRAGLIB.set_shell_geo(
            ashell,
            d,
            L / d,
            h_l / d,
            b_l / d,
            m_d / d,
            b_d / d,
            bs_d / d,
            hs_p,
            bl_code
        )

        return ashell

    def preprocessor(self, data: dict, global_state: dict):

        shell_size = data['shell_size']

        self.preprocessed_data.update(
            d=data['gun_char']['d'] * 1e3,
            L=max(global_state['geometry_solver']['corpus_coord'][0])* 1e3,
            h_l=(shell_size['R8'] + shell_size['R27'])* 1e3,
            b_l = (shell_size['R1'] + shell_size['R2'])* 1e3,
            m_d = shell_size['R28'] * 2. * 1e3,
            b_d = shell_size['R17'] * 2.* 1e3,
            bs_d = global_state['geometry_solver']['corpus_coord'][1, 1] * 2* 1e3,
            hs_p = global_state['geometry_solver']['hs_p']
        )

    def run(self, data: dict, global_state: dict):
        # Считает аэродинамику
        mcdrag_settings = data['settings']['mcdrag']
        n_machs = mcdrag_settings['n_machs']
        MN = mcdrag_settings['MN']
        M0 = mcdrag_settings['M0']
        bl_code = mcdrag_settings['bl_code']

        m_step = (MN - M0) / n_machs

        ashell = self._get_fortran_shell(bl_code)

        mach_array = np.array([i * m_step for i in range(1, n_machs + 1)], order='F', dtype=np.float64)
        cd0_array = np.zeros(n_machs, order='F', dtype=np.float64)
        cdh_array = np.zeros(n_machs, order='F', dtype=np.float64)
        cdbt_array = np.zeros(n_machs, order='F', dtype=np.float64)
        cdb_array = np.zeros(n_machs, order='F', dtype=np.float64)
        cdrb_array = np.zeros(n_machs, order='F', dtype=np.float64)
        cdsf_array = np.zeros(n_machs, order='F', dtype=np.float64)

        mach_array_ptr = FFI.cast("double*", mach_array.__array_interface__['data'][0])
        cd0_array_ptr = FFI.cast("double*", cd0_array.__array_interface__['data'][0])
        cdh_array_ptr = FFI.cast("double*", cdh_array.__array_interface__['data'][0])
        cdbt_array_ptr = FFI.cast("double*", cdbt_array.__array_interface__['data'][0])
        cdb_array_ptr = FFI.cast("double*", cdb_array.__array_interface__['data'][0])
        cdrb_array_ptr = FFI.cast("double*", cdrb_array.__array_interface__['data'][0])
        cdsf_array_ptr = FFI.cast("double*", cdsf_array.__array_interface__['data'][0])

        MCDRAGLIB.get_aerodynamics(
            mach_array_ptr,
            n_machs,
            ashell,
            cd0_array_ptr,
            cdh_array_ptr,
            cdbt_array_ptr,
            cdb_array_ptr,
            cdrb_array_ptr,
            cdsf_array_ptr
        )

        global_state[McDragSolver.name] = dict(
            cx_list=cd0_array,
            mach_list=mach_array
        )


