from cffi import FFI

ffi = FFI()
ffi.cdef(\"""
typedef struct {
    const double* mach_array;
    const double* cx0_array;
    const double* cx2_array;
    const double* cya_array;
    const double* cn_array;
    const double* mxwx_array;
    const double* mza_array;
    const double* mzwz_array;
    int array_len;
} BallisticsCoeffs;

int solve_trajectory(
    const double* y0,
    double t0,
    double t_end,
    double dt,
    const BallisticsCoeffs* coeffs,
    double d, double L, double A, double B, double q,
    double*** result_arrays,
    int* result_length
);
\""")

dll = ffi.dlopen("./ballistics_solver.dll")
print("DLL loaded.")