import cffi, os, sys
import numpy as np
from typing import TypedDict



def load_lib():

    HERE = os.path.dirname(__file__)
    if sys.platform.startswith('linux'):
        LIB_FILE_NAME = os.path.abspath(os.path.join(HERE, ".", "spin73", "libspinner.so"))
    elif sys.platform.startswith('win32'):
        LIB_FILE_NAME = os.path.abspath(os.path.join(HERE, ".", "compiled", "spin73", "libspinner.dll"))
    else:
        raise Exception('Неподдерживаемая платформа')
    ffi = cffi.FFI()

    ffi.cdef('''
    typedef struct spiner_data sdata;

    sdata *SPN_Init(void);

    int SPN_Count(
      sdata *sd,
      const double VL,
      const double VN,
      const double VB,
      const double DM,
      const double OR,
      const double BD,
      const double BM,
      const double VCG,
      const double D
    );

    double GetTranslCoefs(sdata *sd, const int rawnum, double *coefs);
    int SPN_WriteResults(sdata *sd, char *FileName);
    int SPN_WriteTranslResults(sdata *sd, char *FileName);
    void SPN_Free(sdata *sd);
    ''')

    lib = ffi.dlopen(LIB_FILE_NAME)

    return ffi, lib

FFI, SPIN73_LIB = load_lib()

class Spin73Data(TypedDict):
    D: float
    VL: float
    DM: float
    VN: float
    VB: float
    VCG: float
    BD: float
    BM: float
    OR: float

class Spin73Solver:

    name = 'spin73_solver'

    preprocessed_data: Spin73Data = dict(
        D=None,
        VL=None,
        DM=None,
        VN=None,
        VB=None,
        VCG=None,
        BD=None,
        BM=None,
        OR=None
    )

    def check_geometry(self):
        '''


        '''
        D=self.preprocessed_data['D']
        VL=self.preprocessed_data['VL']
        DM=self.preprocessed_data['DM']
        VN=self.preprocessed_data['VN']
        VB=self.preprocessed_data['VB']
        VCG=self.preprocessed_data['VCG']
        BD=self.preprocessed_data['BD']
        BM=self.preprocessed_data['BM']
        OR=self.preprocessed_data['OR']

        errors = ''
        try:
            if D <= 0:
                errors = errors + "Не выполняется условие D>0\n"
                D = 0.0000001
        except ValueError:
            errors = errors + "Неверное значение D\n"

        try:
            if VL/D > 10. or VL/D < 2.5:
                errors = errors + "Не выполняется условие 2.5*D < VL < 10*D\n"
        except ValueError:
            errors = errors + "Неверное значение VL\n"

        try:
            if DM/D > 0.35 or DM/D < 0:
                errors = errors + "Не выполняется условие 0 < DM < 0.35*D\n"
        except ValueError:
            errors = errors + "Неверное значение DM\n"

        try:
            if VN/D > 5.5 or VN/D < 1.2:
                errors = errors + "Не выполняется условие 1.2*D < VN < 5.5*D\n"
        except ValueError:
            errors = errors + "Неверное значение VN\n"

        try:
            if VB/D > 2.0 or VB/D < 0.0:
                errors = errors + "Не выполняется условие 0 < VB < 2*D\n"
        except ValueError:
            errors = errors + "Неверное значение VB\n"

        try:
            if VCG < 0 or VCG > VL:
                errors = errors + "Не выполняется условие 0 < VCG < VL\n"
            else:
                self.preprocessed_data['VCG'] = VL - VCG # Цент масс от носика
        except ValueError:
            errors = errors + "Неверное значение VCG\n"

        try:
            if BD/D > 1.06 or BD/D < 1.0:
                errors = errors + "Не выполняется условие D < BD < 1.06*D\n"
        except ValueError:
            errors = errors + "Неверное значение BD\n"

        try:
            BM = float(BM)
        except ValueError:
            errors = errors + "Неверное значение BOOM\n"

        try:
            OR = float(OR)
        except ValueError:
            errors = errors + "Неверное значение OR\n"

        if errors:
            raise Exception(f'В геометрии обнаружены следующие ошибки:\n{errors}')

    def preprocessor(self, data: dict, global_state: dict):
        self.preprocessed_data['D'] = global_state['mcc_solver']['spin73']['D']
        self.preprocessed_data['VL'] = global_state['mcc_solver']['spin73']['VL']
        self.preprocessed_data['DM'] = global_state['mcc_solver']['spin73']['DM']
        self.preprocessed_data['VN'] = global_state['mcc_solver']['spin73']['VN']
        self.preprocessed_data['VB'] = global_state['mcc_solver']['spin73']['VB']
        self.preprocessed_data['VCG'] = global_state['mcc_solver']['spin73']['VCG']
        self.preprocessed_data['BD'] = global_state['mcc_solver']['spin73']['BD']
        self.preprocessed_data['BM'] = global_state['mcc_solver']['spin73']['BM']
        self.preprocessed_data['OR'] = global_state['mcc_solver']['spin73']['OR']



    def run(self, data, global_state):
        self.check_geometry()
        D=self.preprocessed_data['D']
        VL=self.preprocessed_data['VL']
        DM=self.preprocessed_data['DM']
        VN=self.preprocessed_data['VN']
        VB=self.preprocessed_data['VB']
        VCG=self.preprocessed_data['VCG']
        BD=self.preprocessed_data['BD']
        BM=self.preprocessed_data['BM']
        OR=self.preprocessed_data['OR']

        sdata = SPIN73_LIB.SPN_Init()

        res = SPIN73_LIB.SPN_Count(sdata,
                                   VL,
                                   VN,
                                   VB,
                                   DM,
                                   OR,
                                   BD,
                                   BM,
                                   VCG,
                                   D)
        if res:
            mach_array = []
            spin73res = dict(
                Cx=[],
                Cx2=[],
                Cn=[],
                Mza=[],
                MzWz=[],
                MxWx=[],
            )
            row = FFI.new("double[10]")
            for i in range(17):
                mach = SPIN73_LIB.GetTranslCoefs(sdata, i, row)
                spin73res['Cx'].append(row[0])
                spin73res['Cx2'].append(row[1])
                spin73res['Cn'].append(row[2])
                spin73res['Mza'].append(row[3])
                spin73res['MzWz'].append(row[4])
                spin73res['MxWx'].append(row[5])
                mach_array.append(mach)
            global_state[self.name] = {'mach': mach_array, 'results': spin73res}
        else:
            raise Exception('Неизвестная ошибка')





if __name__ == '__main__':
    from eb_solver import _ExternalBallistics3DSolver
    preprocessed_data: Spin73Data = dict(
        D=100,
        VL=506.6,
        DM=27,
        VN=260,
        VB=35,
        VCG=180,
        BD=103,
        BM=0,
        OR=800
    )

    solver = Spin73Solver()
    solver.preprocessed_data = preprocessed_data

    gl_state = {}

    solver.run({}, gl_state)

    d = 0.1
    eta = 25

    v0 = 250
    theta0 = np.deg2rad(24.06)
    omega_0 = (2 * np.pi * v0) / (eta * d)
    psi_0 = 0.0

    Cx = gl_state[Spin73Solver.name]['results']['Cx']
    Cx02 = gl_state[Spin73Solver.name]['results']['Cx2']
    Cn = gl_state[Spin73Solver.name]['results']['Cn']
    Mza = gl_state[Spin73Solver.name]['results']['Mza']
    MxWx = gl_state[Spin73Solver.name]['results']['MxWx']
    mach = gl_state[Spin73Solver.name]['mach']

    ext_bal_solver = _ExternalBallistics3DSolver(
        q=15.6,
        d=0.1,
        L=0.5066,
        A=0.022,
        v0=v0,
        theta0=theta0,
        omega0=omega_0,
        psi0=psi_0,
        cx=lambda _mach, _delta: np.interp(_mach, mach, Cx) + np.interp(_mach, mach, Cx02) * _delta**2,
        cya=lambda _mach, _delta: np.interp(_mach, mach, Cn),
        mxwx=lambda _mach: np.interp(_mach, mach, MxWx),
        mza=lambda _mach: np.interp(_mach, mach, Mza),
    )

    sol = ext_bal_solver.solve()
