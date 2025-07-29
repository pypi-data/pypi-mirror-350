      SUBROUTINE DISCO
      IMPLICIT REAL*8(A-H,O-Z)
      COMMON/GEOM1/XB(240),RB(240),RBP(240),C2,BET
      COMMON/DATA1/C(240),C1(240),B(240),C3
      COMMON/DFO/FIO,FIOX,FIOR,FIOXX,FIOXR,FIORR
      COMMON/DF1/FI1,FI1X,FI1R,XIOX,XIOR
      COMMON/DISC/R1,PI,I,JH,J,KL
      REAL *8 K
      BETA=BET
      CT=C(JH)
      C1T=C1(JH)
      BT=B(JH)
      X=XB(I)-XB(JH-1)+BETA*RB(JH-1)
      T=BETA*RB(I)/X
      IF(T.GT.0.999999D0) T=0.999999D0
      T2=T**2
      TP1=1.D0+T
      CAP=DSQRT((1.D0-T)/TP1)
      CALL DCEL(K,E,CAP)
      A=DSQRT(2.D0*T*RB(JH)/(RB(I)*TP1))/PI
      A1=A*X*TP1
      A2=A/(X*(1.D0-T))
      A3=4.D0*DSQRT(RB(JH)*TP1*0.5D0/(T*RB(I)))/(3.D0*PI)
      F1X=-4.D0*A1*(K-E)
      F1XX=-2.D0*A*K
      F2XX=A2*(K-E)
      F1R=4.D0*BETA*A1*(E/T-K)/3.D0
      F2XR=BETA*A2*(E/T-K)
      F1XR=2.D0*BETA*A*(TP1*E/T-K)
      IF(T.LT.0.9999D0) GO TO 1
      SR8=0.125D0/RB(I)
      F1X=0.D0
      F1R=0.D0
      F1XX=-1.D0
      F2XX=SR8/BETA
      F2XR=3.D0*SR8
      F1XR=BETA
    1 IF(KL.EQ.3) GO TO 3
      F1=-8.D0*A1*X*((3.D0+T)*K-4.D0*E)/9.D0
      F1RR=-2.D0*BETA**2*A*(2.D0*TP1*E/T2-(2.D0-T)*K/T)/3.D0
      F2RR=-BETA**2*A2*((2.D0-T2)*E/T2-(2.D0-T)*K/T)
      F4=2.D0*A3*X*(E-T*K)/BETA
      F4X=3.D0*A3*(E-T*K/TP1)/BETA
      F4R=-2.D0*A3*(E/T-(2.D0-T)*0.5D0*K/TP1)
      IF(T.LT.0.9999D0) GO TO 2
      F1=0.D0
      F1RR=-BETA**2
      F2RR=-7.D0*BETA*SR8
      F4=0.D0
      F4X=1.D0/BETA
      F4R=-1.D0
    2 CONTINUE
      FIO=FIO+CT*(F1+F1X)
      FIOX=FIOX+CT*(F1X+F1XX)
      FIOR=FIOR+CT*(F1R+F1XR)
      FIOXX=FIOXX+CT*(F1XX+F2XX)
      FIOXR=FIOXR+CT*(F1XR+F2XR)
      FIORR=FIORR+CT*(F1RR+F2RR)
      FI1=FI1+BT*F4
      FI1X=FI1X+BT*F4X
      FI1R=FI1R+BT*F4R
      IF(KL.EQ.2) RETURN
    3 XIOX=XIOX+C1T*(F1X+F1XX)+C3*F2XX
      XIOR=XIOR+C1T*(F1R+F1XR)+C3*F2XR
      RETURN
      END
