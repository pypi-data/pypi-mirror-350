      SUBROUTINE GEOM
      IMPLICIT REAL*8(A-H,O-Z)
      DIMENSION RAB1(10),RAB2(10)
      COMMON/ICOU/VOLN,SOBS,RJA1,RJA2,ICOUNT,NGOL,NHBS
      COMMON/GEO2/NFL,NN,IPRINT,MAL,MAX,IPR
      COMMON/GEOM1/XB(240),RB(240),RBP(240),C2,BETA
      COMMON/RX/XR(20,6),G(20),GCH,DM,N,N1(20),IX,I1
      COMMON/NNI/NTT(11),NP5,JZT
      COMMON/GEO3/VOVS,AL,YINT,O,RR,RREF,AREF,DLN
      COMMON/DISC/R1,PI,I9,JH1,J9,KL
      COMMON/DIS2/SUM1,SUM2,SUM3,SUM4,SUM5,SUM6
      COMMON/VOL/CAF,CNF,CMF,CMX,DIA,RN,AP,XP
      COMMON/WAVE/CABL,CNBL,CMBL,CAW,CNW,CMW
      COMMON/PREOBR/PREB(10),RAB1,RAB2,IPE,NPR,NUPR
      COMMON/CVP/CXT(240),CNT(240),CMT(240),CPV(21),JA,JB,KF
      UKST=0.125D0
      NP5=15
      C3=C2
      BETA=DSQRT(DABS(VOVS**2-1.D0))
      KF=11
      IF(BETA.LE.0.5D0) BETA=0.5D0
      JZT=0
      JA=1
      JB=NP5
      BET1=BETA
      IF(BET1.GT.1.D0) BET1=1.D0
      CABL=0.D0
      CNBL=0.D0
      CMBL=0.D0
      F=O-AL*0.1D0
      IF(RR.LE.1.0D-6) GO TO 5
      IF(NFL.NE.1) GO TO 3
      H1=YINT/(NP5-1.)
      DO 4 J=1,NP5
      XB(J)=-YINT+H1*(J-1)
      RB(J)=DSQRT(DABS((XB(J)+YINT)*(RR**2-XB(J)*YINT)/YINT))
      IF(RB(J).LE.1.0D-10) RB(J)=1.0D-10
      RBP(J)=(RR**2/YINT-2.D0*XB(J)-YINT)/(2.D0*RB(J))
  4   END DO
  3   IF(VOVS.GT.1.26D0)CALL NEWT
      IF(NFL.NE.1.OR.VOVS.LE.1.26) GO TO 5
      CALL SIMP
      CABL=2.D0*SUM1/AREF
      CNBL=-2.D0*SUM2/AREF
      CMBL=SUM3/(AREF*RREF)
  5   CONTINUE
      S1=XR(2,1)+1.0D-10
      CALL SCHAPE(S1,R1,DRB)
      TETT=DATAN(DRB)
      XM=-RR/0.7D0
      TETX=0.4795D0
      IF(VOVS.GT.2.D0)TETX=F*DASIN(1.D0/VOVS)
      IF(TETX.LT.TETT) TETX=TETT
      STX=DSIN(TETX)
      CTX=DCOS(TETX)
      TNX=STX/CTX
      YM=0.5D0*XM*(TNX+DRB)+RR
      K=1
      XB(1)=XM-YM/TNX
      RB(1)=0.D0
      RBP(1)=TNX
      IF(RR.LT.1.0D-6) GO TO 40
      XB(2)=XM
      RB(2)=YM
      RBP(2)=TNX
      EC=RR
      EB=DRB
      EA=(TNX-DRB)/(2.D0*XM)
      VOV=VOVS
      IF(VOVS.LE.1.19D0)VOV=1.0001D0
      E=16.D0/VOV**2
      IF(E.LT.3.D0)E=3.D0
      S2=0.7D0
  43  S1=S2*(TETX/0.5236D0)**2/VOV**E
      DO 42 K=3,100
      A=K-2.D0
      S3=XB(K-1)+RB(K-1)*DSQRT(A)*S1
      RB(K)=EA*S3**2+EB*S3+EC
      RBP(K)=2.D0*EA*S3+EB
      XB(K)=S3
      IF(S3.GE.0.D0) GO TO 40
   42 END DO
      S2=1.2D0*S2
      GO TO 43
   40 EP=1.0D-10
      NTT(1)=K-1
      J1=2
   46 C3=1.2D0*C3
      K=NTT(1)
      DO 10 J=J1,N
      K=K+1
      IJ=0
      I1=11
      XB(K)=XR(J,1)
      CALL SCHAPE(XB(K)+EP,RB(K),RBP(K))
      IF(J.GT.2) RB(K)=RB(K-1)
   11 K=K+1
      IJ=IJ+1
      C5=IJ*C3
      IF(K.GT.240) GO TO 46
      P1=C5*BET1*RB(K-1)
      IF(P1.GT.UKST) P1=UKST
      XB(K)=XB(K-1)+P1
      IF(K.EQ.2) XB(2)=0.005D0+XB(1)
      IF(XB(K).GE.XR(J,2)) GO TO 7
      CALL SCHAPE(XB(K),RB(K),RBP(K))
      GO TO 11
    7 CONTINUE
      XB(K)=XR(J,2)
      CALL SCHAPE(XB(K)-EP,RB(K),RBP(K))
      NTT(J)=K
  10  END DO
      NN=NTT(N)
      SUM3=0.D0
      SUM4=0.D0
      SUM1=PI*(YINT**2+RR**2)
      C22=0.D0
      IF(RJA1.EQ.0.) RJA1=0.37D0*DLN
      PRMX=0.D0
      SUM2=PI*YINT*(3.D0*RR**2+YINT**2)/6.D0
      DO 1 J=2,N
      JB=NTT(J)-1
      JA=NTT(J-1)+1
      DO 1 I=JA,JB
      XI=XB(I)
      XI1=XB(I+1)
      RI=RB(I)
      DX=XI1-XI
      RI1=RB(I+1)
      SUM3=SUM3+DX*(RI+RI1)
      SUM4=SUM4+DX*(XI1*RI1+XI*RI)
      SUM2=SUM2+PI/2.D0*DX*(RI**2+RI1**2)
      IF(J.EQ.NGOL) VOLN=SUM2
      C22=C22+2.D0*DX*(XI*RI*RI+XI1*RI1*RI1)
      IF(J.EQ.NHBS) VOLN1=SUM2
      S1=DABS(RBP(I))
      IF(PRMX.LT.S1) PRMX=S1
      SUM1=SUM1+PI*DX*(RI*DSQRT(1.D0+RBP(I)**2)+RI1*DSQRT
     *(1.D0+RBP(I+1)**2))
  1   Continue
      C22=4.D0*(DLN-RJA1/DIA)*SUM2/PI-C22
      CMQ=-4.D0*(4.D0*RB(NN)**2*RJA1/DIA+C22)
      SOBS=SUM1
      AB=SUM3
      XP=SUM4/SUM3
      RJA2=CMQ
      IF(IPE.EQ.0) NUPR=NPR
      IF(IPE.EQ.0.OR.NPR.EQ.NUPR) GO TO 14
      NUPR=NPR
  14  CONTINUE
      FI=DATAN(PRMX)/F
      SNFI=DSIN(FI)
      IF(SNFI.LE.1.D0/VOVS.AND.VOVS.LE.3.D0)GOTO2
      JZT=1
      SUM6=1./SNFI
      IF(SUM6.GT.3.D0) SUM6=3.0D0
      JA=NTT(1)+1
      JB=NN
      SUM6=SUM6*0.98D0
  2   IF(JZT.EQ.1) CALL NEWT
      RETURN
      END
