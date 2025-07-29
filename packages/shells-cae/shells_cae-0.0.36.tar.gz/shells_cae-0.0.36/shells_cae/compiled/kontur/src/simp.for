      SUBROUTINE SIMP
      IMPLICIT REAL*8(A-H,O-Z)
      COMMON/GEOM1/XB(240),RB(240),RBP(240),C2,BETA
      COMMON/CVP/CXT(240),CNT(240),CMT(240),CPV(21),JA,JB,KF
      COMMON/DIS2/SUM1,SUM2,SUM3,SUM4,SUM5,SUM6
      SUM1=0.D0
      SUM2=0.D0
      SUM3=0.D0
      DO 2 I=JA,JB
      F1=CXT(I)
      G=CNT(I)
      G1=CMT(I)
      IF(I.EQ.JA) GO TO 4
      H=(RB(I)-RB(I-1))/2.D0
      H1=(XB(I)-XB(I-1))/2.D0
      SUM1=SUM1+H*(SF1+F1)
      SUM2=SUM2+H1*(SG+G)
      SUM3=SUM3+H1*(SG1+G1)
    4 SF1=F1
      SG=G
      SG1=G1
  2   END DO
      RETURN
      END
