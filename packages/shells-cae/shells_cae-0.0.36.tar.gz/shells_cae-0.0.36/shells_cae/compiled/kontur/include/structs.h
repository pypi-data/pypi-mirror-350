#ifndef STRUCTS_H
#define STRUCTS_H

extern struct {
  double sig, rxx;
} tv_;

extern struct {
  double bl, anl, ala;
} leng_;

extern struct {
  int isig; ////Параметр учета толщины вытеснения пограничного слоя (0 - учитывается (L <= 7*d), 1 - не учитывается(L > 7*d))
} in_;

extern struct {
  double cab, cnb, cmb;
} base_;

extern struct {
  double cap, cnp, cmp;
  double hb; //Высота пояска в клб
} band_;

extern struct {
  double cxt[240], cnt[240], cmt[240], cpv[21];
  int ja, jb, kf;
} cvp_;

extern struct {
  double r1, pi;
  int i9, jh1, kl;
} disc_;

extern struct {
  double cabl, cnbl, cmbl, caw, cnw, cmw;
} wave_;

extern struct {
  double cxo, cyo, cmo;
} tail1_;

extern struct {
  double voln, sobs, rja1, rja2;
  int icount, ngol, nhbs;
} icou_;

extern struct {
  int nfl; // Вид притупления nfl=1 - сферическое nfl=2..100 - другое
  int nn;
  int iprint; // Печать распределения давления по корпусу снаряда (1 - есть, 0 - нет)
  int mal; // Колличество вариантов по углу атаки
  int max; // Колличество вариантов по числу Маха
  int ipr;
} geo2_;

extern struct {
  double xb[240], rb[240], rbp[240];
  double c2; // Коэффициент, определяющий размеры расчетной сетки по коор-
             // динате X. (C2=0.015-0.02)
  double beta;
} geom1_;

extern struct {
  double xr[6][20]; /*двухмерный массив чисел
  xr(1,i)=x1 -координата начала участка
  xr(2,i)=x2 -координата конца участка
  xr(3,i)=r1 -радиус начала участка
  xr(4,i)=r2 -радиус конца участка
  xr(5,i)=rож-радиус оживала
  xr(6,i)=n  -показатель степени */
  double g[20], gch, dm;
  int n;
  int n1[20]; //Массив параметров, соответствующих каждому участку корпуса
              //n1[0] - не задается! Массив начинать с элемента n1[1]
              //1 - цилиндр
              //2 - конус
              //3 - оживало обратное
              //4 - оживало прямое
              //5 - степень
              //6 - парабола
  int ix; //Координаты ix=0 - в калибрах, ix=1 - в метрах
  int i1;
} rx_;

extern struct {
  int ntt[11], np5, jzt;
} nni_;

extern struct {
  double vovs, al;
  double yint; //высота шарового сегмента, при сферическом затуплении снаряда
               //в метрах или калибрах в соответствии с IX
  double f; //Константа глубокого понимания аэродинамики (f=0.95)
  double rr, rref, aref, dln;
} geo3_;


extern struct {
  double caf, cnf, cmf, cmx, dia, rn, ap, xp;
} vol_;

extern struct {
  double preb[10], rab1[10], rab2[10];
  int ipe; //параметр печати (IPE=1 - на печать выдается X, R,dR/dX; IPE=0 - нет печати)
  int npr, nupr;
} preob_;

extern struct {
  double ainf; // Скорость звука м/с
  double rhoinf; // Плотность воздуха, кг/м^3
  double amuinf; // Динамическая вязкость воздуха, Н*с/m^2
  double cts; // Положение центра тяжести от носика, м
  double dl; // Длина снаряда, м
  double hmax; // Начальное число Маха
  double dmax; // Приращение числа Маха
  double huat; // Начальный угол атаки
  double duat; // Приращение угла атаки
  double dpr; // Коэффициент, определяющий величину приращения участка, т.е.
              // приращение X=(XR(INM,2)-XR(INM,1))*DPR
  int ng; //Кол-во участков головной части снаряда
  int nh; //Кол-во участков головной части и цилиндрической части (либо ng, либо ng+1)
  int nk; //Кол-во участков по всему снаряду (nk <=10!!!)
} input_data_;

//Процедуры используемые контуром
void geom_(void);
void skbarb_(void);
void trans_(void);
void normfo_(void);
void hybrid_(void);
void prod_(double *Y1, double *Y2, double *Y3, double *X1, double *X2,
           double *X3, double *CM, double *P, int *I);
void interp_(double *TX, double *TY, double *X, double *Y, 
             int *N, int *J);

#endif //STRUCTS_H
