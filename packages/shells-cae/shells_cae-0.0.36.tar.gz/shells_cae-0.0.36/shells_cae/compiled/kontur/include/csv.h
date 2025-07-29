#ifndef CSV_H
#define CSV_H

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
                    double **tren, double **don, double **voln, double **pois, double **cn, double **cy, double **xcd, double **cx, double **cyal,
                    double **cmal, double **mxwx, double **mzwx);
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
#endif //CSV_H
