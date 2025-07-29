#include <math.h>
#include <stdio.h>
#include "csv.h"
#include "structs.h"

#ifndef SQR
#define SQR(x) pow((x), 2.)
#endif

double alod[] = {1.,1.5,2.,2.5,3.0,3.5,4.,4.5,5.,5.5,6.,6.5,7.,7.5,8.,
     8.5,9.,9.5,10.,10.5,11.0,11.5,12.,12.5,13.,13.5,14.,14.5,15.,15.5,
     16.,16.5,17.0,17.5,18.,18.5,19.,19.5,20.,21.,22.,23.,24.,25.};

double eta[] = {0.53,0.554,0.57,0.582,0.593,0.603,0.613,0.62,0.627,
     0.633,0.64,0.647,0.653,0.658,0.664,0.669,0.674,0.678,0.683,0.688,
     0.692,0.696,0.7,0.704,0.708,0.712,0.716,0.72,0.724,0.728,0.732,
     0.736,0.74,0.744,0.748,0.753,0.757,0.761,0.765,.744,.782,.79,.798,
     .806};

double amc[] = {0.,0.05,0.1,.15,0.2,.25,0.3,.35,0.4,.45,0.5,.55,0.6,.65,
                .7,.75,0.8,.85,0.9,.95,1.,1.05,1.1,1.15,1.2,1.25,1.3,
                1.35,1.4};

double cdc[] = {1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.22,1.25,1.29,1.35,1.45,
                1.55,1.66,1.73,1.78,1.81,1.83,1.82,1.81,1.8,1.77,1.75,
                1.72,1.68,1.65,1.61,1.58,1.53};

void csvstep_(double *vovs, double *dln, double *al, double *dlina, 
              double *results){
  double gvovs = geo3_.vovs;
  geo3_.vovs = *vovs;
  double gal = geo3_.al;
  geo3_.al = *al; //Угол нутации в радианах!!!
  double AINF = input_data_.ainf;
  double RHOINF = input_data_.rhoinf;
  double AMUINF = input_data_.amuinf;
  double DM = vol_.dia;
  double DLN = *dln;  
  vol_.rn = (*vovs)*AINF*RHOINF/AMUINF;
  if(in_.isig){ //Толщина вытеснения пограничного слоя не учитывается L > 7*d
    double RE=DM*DLN*vol_.rn;
    tv_.sig=0.046*pow((1. + 0.0092*SQR(*vovs)), 0.88)/pow(RE, 0.2);
  } else { //Толщина вытеснения пограничного слоя учитывается L <= 7*d
    tv_.sig=0.;
  }
  geom_();
  skbarb_();
  if(*vovs < 1.001){
    normfo_();
    if(*vovs >= 0.85){
      trans_();
    } else {
      int ist=nni_.ntt[icou_.ngol - 1];
      double the1= atan(geom1_.rbp[ist - 1])*57.29578;
      if(the1 < 10.){
        wave_.caw = 0.;
      } else {
        wave_.caw = 0.012*(the1-10.);
      }
    }
  } else if(*vovs > 1.26){
    if(nni_.jzt == 0){
      hybrid_();
    } else {
      int MEX = 1;
      double Q1;
      double Q2;
      double P1A;
      double P1N;
      double P1M;
      do{
        Q1=2.2 + 0.2*(1-MEX);
        geo3_.vovs=Q1;
        geom_();
        hybrid_();
        P1A=wave_.caw;
        P1N=wave_.cnw;
        P1M=wave_.cmw;
        Q2=2.7 + 0.2*(1-MEX);
        geo3_.vovs=Q2;
        geom_();
        hybrid_();
        MEX++;
      } while (nni_.jzt == 1);
      double P2A=wave_.caw;
      double P2N=wave_.cnw;
      double P2M=wave_.cmw;
      double Q3=13.5;
      geo3_.vovs=Q3;
      geom_();
      hybrid_();
      double P3A=wave_.caw;
      P1N=-P1M/P1N;
      P2N=-P2M/P2N;
      P3A=P3A*1.02;
      double P3M=P2M+(P2M-P1M)*2.5;
      double P3N=P2N+(P2N-P1N)*(4.9+20.*geo3_.al);
      geo3_.vovs = *vovs;
      int i = 2;
      prod_(&P1A, &P2A, &P3A, &Q1, &Q2, &Q3, vovs, &wave_.caw,&i);
      prod_(&P1M, &P2M, &P3M, &Q1, &Q2, &Q3, vovs, &wave_.cmw,&i);
      double C5W;
      prod_(&P1N, &P2N, &P3N, &Q1, &Q2, &Q3, vovs, &C5W,&i);
      wave_.cnw=-wave_.cmw/C5W;
    }
  } else { //Скорость от 1 до 1.25 Маха
    geo3_.vovs=1.;
    geom_();
    trans_();
    normfo_();
    double Q1 =1.;
    double P1A=wave_.caw;
    double P1N=wave_.cnw;
    double P1M=wave_.cmw;
    geo3_.vovs=1.27;
    geom_();
    hybrid_();
    double Q2=1.27;
    double P2A=wave_.caw;
    double P2N=wave_.cnw;
    double P2M=wave_.cmw;
    geo3_.vovs=1.47;
    geom_();
    hybrid_();
    double Q3=1.47;
    double P3A = wave_.caw;
    double P3N = wave_.cnw;
    double P3M = wave_.cmw;
    geo3_.vovs = *vovs;
    int i = 1;
    prod_(&P1A, &P2A, &P3A, &Q1, &Q2, &Q3, vovs, &wave_.caw, &i);
    prod_(&P1N, &P2N, &P3N, &Q1, &Q2, &Q3, vovs, &wave_.cnw, &i);
    prod_(&P1M, &P2M, &P3M, &Q1, &Q2, &Q3, vovs, &wave_.cmw, &i);
  }
  double ca = vol_.caf + base_.cab + wave_.caw + band_.cap + tail1_.cxo;
  double eta1;
  int numEta = sizeof(eta)/sizeof(double); //44
  int j = 3;
  interp_(alod, eta, dln, &eta1, &numEta, &j);
  double amc1 = (*vovs)*sin(geo3_.al);
  double cdc1;
  int numAmc = sizeof(amc)/sizeof(double); //29
  interp_(amc, cdc, &amc1, &cdc1, &numAmc, &j);
  double s1=cdc1*eta1*vol_.ap/geo3_.aref;
  double cnv;
  double cmv;
  if(geo3_.al > 0.0175){
    double powal = pow(geo3_.al, 2.8);
    cnv = 4.75*s1*powal;
    cmv = -5.*s1*vol_.xp*powal/(2.*geo3_.rref);
  } else {
    cnv = 0.;
    cmv = 0.;
  }
  double cn = vol_.cnf + base_.cnb + wave_.cnw + band_.cnp + cnv +
              tail1_.cyo*geo3_.al;
  double cm = vol_.cmf + base_.cmb + wave_.cmw + band_.cmp + cmv +
              tail1_.cmo*geo3_.al;
  double cy = cn*cos(geo3_.al) - ca*sin(geo3_.al);
  double cx = cn*sin(geo3_.al) + ca*cos(geo3_.al);
  double cmal=.0, xcd=.0, cnal=.0, cyal=.0;
  if(fabs(geo3_.al) >= 0.0001){
    cmal=cm/geo3_.al;
    xcd=-cm/cn;
    cnal=cn/geo3_.al;
    cyal=cy/geo3_.al;
  }
  double ddt = vol_.dia/(*dlina);
  xcd = xcd*ddt;
  cm = cn*(input_data_.cts - xcd);
  cmal = cnal*(input_data_.cts - xcd);
  double cmx = vol_.cmx*SQR(ddt);
  double cmzwz = cnal*SQR(input_data_.cts - xcd);
  // FILE *file = fopen("res.txt", "w");
  // if(file){
  //   fprintf(file, "Mach:%g\nTren:%g\nDon:%g\nVoln:%g\nPois:%g\nCn:%g\n"
  //           "Cy:%g\nXcd:%g\nCx:%g\nCyal:%g\nMza:%g\n-Mxwx:%g\n"
  //           "Mzwz:%g", geo3_.vovs, vol_.caf, base_.cab, wave_.caw,
  //           band_.cap, cn, cy, xcd, cx, cyal, cmal, cmx, cmzwz);
  //   fclose(file);
  // }
  results[0] = vol_.caf;
  results[1] = base_.cab;
  results[2] = wave_.caw;
  results[3] = band_.cap;
  results[4] = cn;
  results[5] = cy;
  results[6] = xcd;
  results[7] = cx;
  results[8] = cyal;
  results[9] = cmal;
  results[10] = cmx;
  results[11] = cmzwz;
  geo3_.vovs = gvovs;
  geo3_.al = gal;
}
