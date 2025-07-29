#include <stdlib.h>
#include <stdio.h>
#include "csv.h"
#include "structs.h"
#include "strings.h"

#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

struct csv_st{
  int initialized;
  int calledSetYInt;
  int calledSetHb;
  double dln;
  double dlina;
  double mach;
  double angle;
  double results[12];
};

csv *CSV_New(){
  csv *ret = calloc(1, sizeof(csv));
  input_data_.ainf = 0.;
  input_data_.rhoinf = 0.;
  input_data_.amuinf = 0.;
  geom1_.c2 = 0.;
  return ret;
}

void CSV_SetNG(csv *p_csv, const int ng){
  input_data_.ng = ng;
}

void CSV_SetNH(csv *p_csv, const int nh){
  input_data_.nh = nh;
}

void CSV_SetNK(csv *p_csv, const int nk){
  input_data_.nk = nk;
}

void CSV_SetNFL(csv *p_csv, const int nfl){
  if(nfl > 0 || nfl <= 100){
    geo2_.nfl = nfl;
  }
}

void CSV_SetISIG(csv *p_csv, const int isig){
  if(isig == 0 || isig == 1){
    in_.isig = isig;
  }
}

void CSV_SetYInt(csv *p_csv, const double yint){
  if(yint >= 0.){
    geo3_.yint = yint;
    p_csv->calledSetYInt = 1;
  }
}

void CSV_SetDia(csv *p_csv, const double d){
  if(d > 0){
    vol_.dia = d;
  }
}

void CSV_SetHb(csv *p_csv, const double hb){
  if(hb >= 0.){
    band_.hb = hb;
    p_csv->calledSetHb = 1;
  }
}

void CSV_SetA(csv *p_csv, const double a){
  if(a > 0.){
    input_data_.ainf = a;
  }
}

void CSV_SetRo(csv *p_csv, const double ro){
  if(ro > 0.){
    input_data_.rhoinf = ro/9.80665;
  }
}

void CSV_SetAMU(csv *p_csv, const double amu){
  if(amu >= 0.){
    input_data_.amuinf = amu;
  }
}

void CSV_SetC2(csv *p_csv, const double c2){
  if(c2 >= 0.015 && c2 <= 0.02){
    geom1_.c2 = c2;
  }
}

void CSV_SetXct(csv *p_csv, const double xct){
  if(xct > 0.){
    input_data_.cts = xct;
  }
}

void CSV_AddGeom(csv *p_csv, const int num, const int type,
                 const double x1, const double x2,
                 const double r1, const double r2,
                 const double rd, const double exp){
  p_csv->initialized = 0;
  rx_.n1[num+1] = type;
  rx_.xr[0][num+1] = x1;
  rx_.xr[1][num+1] = x2;
  rx_.xr[2][num+1] = r1;
  rx_.xr[3][num+1] = r2;
  rx_.xr[4][num+1] = rd;
  rx_.xr[5][num+1] = exp;
}

const char *ERRORS[] = {
  "You must use SetNG function!",
  "You must use SetNH function!",
  "NH must be equal NG or greater on 1!",
  "You must use SetNK function!",
  "NK must be equal or greater NH!",
  "You must use proper value in SetNFL funftion!",
  "You must use SetYInt function!",
  "You must use SetDia function!",
  "You must use SetHb function!",
  "You must use SetXct function!",
  "You must use AddGeom function for primitive %d!"
};

char ERROR_STR[50];

const char *CSV_CheckError(csv *p_csv){
  if(input_data_.ng == 0) {
    return ERRORS[0];
  }
  if(input_data_.nh == 0) {
    return ERRORS[1];
  }
  if(input_data_.nh < input_data_.ng ||
     input_data_.nh > input_data_.ng + 1){
    return ERRORS[2];
  }
  if(input_data_.nk == 0){
    return ERRORS[3];
  }
  if(input_data_.nk < input_data_.nh){
    return ERRORS[4];
  }
  if(geo2_.nfl < 1 || geo2_.nfl > 100){
    return ERRORS[5];
  }
  if(!p_csv->calledSetYInt){
    return ERRORS[6];
  }
  if(vol_.dia == 0.){
    return ERRORS[7];
  }
  if(!p_csv->calledSetHb){
    return ERRORS[8];
  }
  if(input_data_.cts <= 0.){
    return ERRORS[9];
  }
  for(int i=0; i<input_data_.nk; i++){
    if(rx_.n1[i+1] == 0){
      snprintf(ERROR_STR, 50, ERRORS[10], i);
      return ERROR_STR;
    }
  }
  return NULL;
}

static void Initialization(csv *p_csv){
  icou_.rja1 = 0.;
  icou_.rja2 = 0.;
  tv_.rxx = 0.;
  vol_.ap = 0.;
  for(int i = 0; i < 240; i++){
    cvp_.cxt[i] = 0.;
    cvp_.cnt[i] = 0.;
    cvp_.cmt[i] = 0.;
    geom1_.xb[i] = 0.;
    geom1_.rb[i] = 0.;
    geom1_.rbp[i] = 0.;
  }
  geo3_.rref = 0.5;
  disc_.pi = M_PI;
  geo3_.aref = M_PI*0.25;
  band_.hb = band_.hb/vol_.dia;
  rx_.n1[0] = 0;
  if(input_data_.ainf == 0.){
    input_data_.ainf = 340.8;
  }
  if(input_data_.rhoinf == 0){
    input_data_.rhoinf = 0.1229;
  }
  if(input_data_.amuinf == 0.){
    input_data_.amuinf = 0.000001825;
  }
  if(geom1_.c2 == 0.){
    geom1_.c2 = 0.02;
  }
  geo3_.f = 0.95;
  p_csv->dlina = rx_.xr[1][input_data_.nk] + geo3_.yint;
  if(geo2_.nfl == 1){
    geo3_.yint /= vol_.dia;
  } else {
    geo3_.yint = 0.;
  }
  //p_csv->dln = p_csv->dlina/vol_.dia;
  p_csv->initialized = 1;
  //
    preob_.npr = 1;
    icou_.ngol = input_data_.ng + 1;
    icou_.nhbs = input_data_.nh + 1;
    rx_.n = input_data_.nk + 1;
    geo2_.ipr = 1;
    if(rx_.xr[2][1] < 1.E-3){
      rx_.xr[2][1] = 0.;
    }
    rx_.dm = vol_.dia;
    preob_.nupr = 0;
    rx_.i1 = 21;
    tail1_.cxo = 0.;
    tail1_.cyo = 0.;
    tail1_.cmo = 0.;
    for(int i = 0; i < rx_.n; i++){
      preob_.preb[i]=0.;
      preob_.rab1[i]=0.;
    }
  //
  for(int n = 1; n <= input_data_.nk; n++){
    for(int i = 0; i < 5; i++){
      rx_.xr[i][n] /= vol_.dia;
    }
  }
  geo3_.rr = rx_.xr[2][1];
  rx_.ix = 0;
  input_data_.dpr *= (rx_.xr[1][0] - rx_.xr[0][0]);
  //Относительная длина цилиндрической части
  leng_.ala = rx_.xr[1][input_data_.nh] - rx_.xr[1][input_data_.ng];
  //Относительная длина запоясковой части
  leng_.bl = rx_.xr[1][input_data_.nk] - rx_.xr[1][input_data_.nh];
  //Относительная длина головной части
  leng_.anl = rx_.xr[1][input_data_.ng] - rx_.xr[1][0] + geo3_.yint;
  p_csv->dln = leng_.ala + leng_.bl + leng_.anl; //Длина снаряда в калибрах
  geo3_.dln = p_csv->dln;
}

void csvstep_(double *vovs, double *dln, double *al, double *dlina,
              double *results);

void CSV_Solve(csv *p_csv, const double mach, const double angle){
  if(!p_csv->initialized){
    Initialization(p_csv);
  }
  p_csv->mach = mach;
  double angle_r;
  if(angle < 0.1){
    angle_r = 0.1*M_PI/180.;
  } else {
    angle_r = angle*M_PI/180.;
  }
  csvstep_(&p_csv->mach, &p_csv->dln, &angle_r, &p_csv->dlina,
           p_csv->results);
}

void CSV_Solve_Array(csv *p_csv, double *mach_array, double *angle_array, int n_machs, int n_angles,
                    double **tren, double **don, double **voln, double **pois, double **cn, double **cy, double **xcd, double **cx, double **cyal,
                    double **cmal, double **mxwx, double **mzwx){

  for (int i=0;i<n_angles;i++){
    for (int j=0;j<n_machs;j++){
      CSV_Solve(p_csv, mach_array[j], angle_array[i]);
      tren[i][j] = CSV_GetTren(p_csv);
      don[i][j] = CSV_GetDon(p_csv);
      voln[i][j] = CSV_GetVoln(p_csv);
      pois[i][j] = CSV_GetPois(p_csv);
      cn[i][j] = CSV_GetCn(p_csv);
      cy[i][j] = CSV_GetCy(p_csv);
      xcd[i][j] = CSV_GetXcd(p_csv);
      cx[i][j] = CSV_GetCx(p_csv);
      cyal[i][j] = CSV_GetCyAl(p_csv);
      cmal[i][j] = CSV_GetCmAl(p_csv);
      mxwx[i][j] = CSV_GetMxWx(p_csv);
      mzwx[i][j] = CSV_GetMzWz(p_csv);
      }
  }
}

double CSV_GetMach(csv *p_csv){
  return p_csv->mach;
}

double CSV_GetTren(csv *p_csv){
  return p_csv->results[0];
}

double CSV_GetDon(csv *p_csv){
  return p_csv->results[1];
}

double CSV_GetVoln(csv *p_csv){
  return p_csv->results[2];
}

double CSV_GetPois(csv *p_csv){
  return p_csv->results[3];
}

double CSV_GetCn(csv *p_csv){
  return p_csv->results[4];
}

double CSV_GetCy(csv *p_csv){
  return p_csv->results[5];
}

double CSV_GetXcd(csv *p_csv){
  return p_csv->results[6];
}

double CSV_GetCx(csv *p_csv){
  return p_csv->results[7];
}

double CSV_GetCyAl(csv *p_csv){
  return p_csv->results[8];
}

double CSV_GetCmAl(csv *p_csv){
  return p_csv->results[9];
}

double CSV_GetMxWx(csv *p_csv){
  return p_csv->results[10];
}

double CSV_GetMzWz(csv *p_csv){
  return p_csv->results[11];
}

void CSV_Free(csv *p_csv){
  free(p_csv);
}
