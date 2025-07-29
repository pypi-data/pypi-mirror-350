/*
 * C header for using KONTUR function
 */

#ifndef KONTUR_H
#define KONTUR_H
#define kontur kontur_

void kontur(
  float *l1,  //Калибр, м
  float *l2,  //Ширина пояска, м
  float *l3,  //Угол запояскового конуса, рад.
  float *l4,  //Осевое смещение оживала, м
  float *l5,  //Плотность воздуха, кг/м3
  float *l6,  //Диаметр притупления носика, м
  float *l7,  //Диаметр основания взрывателя, м
  float *l8,  //Высота носика, м
  float *l9,  //Высота взрывателя, м
  float *l10, //Высота оживала, м
  float *l11, //Длина цилиндрической части, м
  float *l12, //Длина запояскового конуса, м
  float *l13, //Число Маха
  float *l14, //Начальный угол атаки, град
  float *l15  //Cx
);

#endif KONTUR_H
