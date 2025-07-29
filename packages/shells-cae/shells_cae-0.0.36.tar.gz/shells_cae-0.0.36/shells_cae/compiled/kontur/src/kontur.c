//Реализация программы Контур на языке Си-99
#include <stdlib.h>
#include <stdio.h>
#include "structs.h"
#include "csv.h"

#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

#define SQR(x) ((x)*(x))

// void csv_(void);
static void InitFortranCommonBlocks(void);
static void SetGeometry(void);
static void CSVTest(void);

int main(int argc, char *argv[]){
  CSVTest();
  InitFortranCommonBlocks();
  SetGeometry();
  // csv_();
  return 0;
}

static void InitFortranCommonBlocks(void){
  for(int i = 0; i < 10; i++){
    for(int j = 0; j < 6; j++){
      rx_.xr[j][i] = 0.;
    }
  }
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
  geo3_.aref = M_PI*SQR(0.5);
}

static void SetPrimitive(const int i,
                         const enum geometry_primitives type,
                         const double x1, const double x2,
                         const double r1, const double r2,
                         const double R, const double n){
  rx_.n1[i+1] = type;
  rx_.xr[0][i+1] = x1;
  rx_.xr[1][i+1] = x2;
  rx_.xr[2][i+1] = r1;
  rx_.xr[3][i+1] = r2;
  rx_.xr[4][i+1] = R;
  rx_.xr[5][i+1] = n;
}

static void SetGeometry(){
  input_data_.ng = 4;
  input_data_.nh = 5;
  input_data_.nk = 7;
  geo2_.mal = 3;
  geo2_.max = 15;
  geo2_.nfl = 2;
  geo2_.iprint = 0;
  in_.isig = 0;
  rx_.ix = 1;
  rx_.n1[0] = 0;
  SetPrimitive(0, G_CYLINDR, .0,    .01,    .01,    .01,  .0,   .0);
  SetPrimitive(1, G_CONE,    .01,   .06,    .01,    .02,  .0,   .0);
  SetPrimitive(2, G_CONE,    .06,   .18,    .02,  .0425,  .0,   .0);
  SetPrimitive(3, G_OGIVE,   .18,  .457,  .0425,  .0762,  3.22, .0);
  SetPrimitive(4, G_CYLINDR, .457, .712,  .0762,  .0762,  .0,   .0);
  SetPrimitive(5, G_CONE,    .712, .723,  .0762,  .0748,  .0,   .0);
  SetPrimitive(6, G_CONE,    .723, .863,  .0748,  .06675, .0,   .0);
  //preob_.ipe = 0;
  geo3_.yint = 0.;
  vol_.dia = 0.1524;
  band_.hb = 0.01;
  input_data_.ainf = 340.8;
  input_data_.rhoinf = 0.1229;
  input_data_.amuinf = 0.000001825;
  geom1_.c2 = 0.02;
  geo3_.f = 0.95;
  input_data_.cts = 0.533;
  input_data_.dl = 0.863;
  input_data_.hmax = 0.6;
  input_data_.dmax = 0.2;
  input_data_.huat = 0.;
  input_data_.duat = 1.;
  //input_data_.dpr = 0.;
}


static void PrintFixWidth(FILE *file, const double val, const int width){
  char str[width];
  int pr = snprintf(str, width, "%g", val);
  for(int i = pr; i < width-1; i++){
    str[i] = ' ';
  }
  str[width-1] = '\0';
  fprintf(file, "%s  ", str);
}

const char TITLE[] = "Mach  Tren       Don        Voln         "
"Pois          Cn         Cy         Xcd        Cx         "
"CyAl       CmAl       MxWx          MzWz\n";

static void OutTitle(FILE *file){
  fputs(TITLE, file);
}

static void OutMachString(csv *solver, FILE *file){
  PrintFixWidth(file, CSV_GetMach(solver), 5);
  PrintFixWidth(file, CSV_GetTren(solver), 10);
  PrintFixWidth(file, CSV_GetDon(solver), 10);
  PrintFixWidth(file, CSV_GetVoln(solver), 12);
  PrintFixWidth(file, CSV_GetPois(solver), 13);
  PrintFixWidth(file, CSV_GetCn(solver), 10);
  PrintFixWidth(file, CSV_GetCy(solver), 10);
  PrintFixWidth(file, CSV_GetXcd(solver), 10);
  PrintFixWidth(file, CSV_GetCx(solver), 10);
  PrintFixWidth(file, CSV_GetCyAl(solver), 10);
  PrintFixWidth(file, CSV_GetCmAl(solver), 10);
  PrintFixWidth(file, CSV_GetMxWx(solver), 13);
  PrintFixWidth(file, CSV_GetMzWz(solver), 10);
  fputs("\n", file);
}

static void CSVTest(void){
  csv *solver = CSV_New();
  CSV_SetNG(solver, 4);
  CSV_SetNH(solver, 5);
  CSV_SetNK(solver, 7);
  CSV_SetNFL(solver, 2);
  CSV_SetDia(solver, 0.1524);
  CSV_SetHb(solver, 0.01*0.1524);
  CSV_SetXct(solver, 0.533);
  CSV_SetYInt(solver, 0.);
  CSV_AddGeom(solver, 0, G_CYLINDR, 0.,   .01,  .01,   .01,    0.,   0.);
  CSV_AddGeom(solver, 1, G_CONE,    .01,  .06,  .01,   .02,    0.,   0.);
  CSV_AddGeom(solver, 2, G_CONE,    .06,  .18,  .02,   .0425,  0.,   0.);
  CSV_AddGeom(solver, 3, G_OGIVE,   .18,  .457, .0425, .0762,  3.22, 0.);
  CSV_AddGeom(solver, 4, G_CYLINDR, .457, .712, .0762, .0762,  .0,   0.);
  CSV_AddGeom(solver, 5, G_CONE,    .712, .723, .0762, .0748,  .0,   0.);
  CSV_AddGeom(solver, 6, G_CONE,    .723, .863, .0748, .06675, .0,   0.);
  const char *err = CSV_CheckError(solver);
  if(err){
    printf("%s\n", err);
    exit(1);
  }
  FILE *file = fopen("CSV.txt", "w");
  if(file){
    for(double angle = 0.; angle < 2.1; angle += 1.){
      fprintf(file, "Angle = %g\n", angle);
      OutTitle(file);
      double mach = 0.6;
      while(mach < 3.11){
        if(mach>0.8 && mach<1.21){
          mach -= 0.1;
        }
        CSV_Solve(solver, mach, angle);
        OutMachString(solver, file);
        mach += 0.2;
      }
    }
    fclose(file);
  } else {
    printf("Error! Can't open file CSV.txt\n");
  }
  CSV_Free(solver);
}
