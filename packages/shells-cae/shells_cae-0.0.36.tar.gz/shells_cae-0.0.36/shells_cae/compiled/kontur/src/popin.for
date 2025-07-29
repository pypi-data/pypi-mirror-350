      SUBROUTINE POPIN
      IMPLICIT REAL*8(A-H,O-Z)
      COMMON/DISC/R1,PI,I,JH,J,KL
      COMMON/CVP/CXT(240),CNT(240),CMT(240),CPV(21),JA,JB,KF
      COMMON/GEOM1/XB(240),RB(240),RBP(240),C2,BETA
      DF=PI/(KF-1.)
      F1=0.D0
      F2=0.D0
      DO 1 IJ=1,KF
      S=3.D0+(-1.D0)**IJ
      IF(IJ.EQ.1.OR.IJ.EQ.KF) S=1.D0
      S1=S*CPV(IJ)
      F1=F1+S1
      F2=F2+S1*DCOS((IJ-1)*DF)
 1    END DO
      S=RB(I)*DF/3.D0
      CXT(I)=F1*S
      CNT(I)=F2*S
      CMT(I)=F2*(XB(I)+RB(I)*RBP(I))*S
      RETURN
      END
