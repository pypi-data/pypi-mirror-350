      SUBROUTINE SCHAPE(X,R,RX999)
      IMPLICIT REAL*8(A-H,O-Z)
      COMMON/TV/SIG,RXX
      COMMON/RX/XR(20,6),G(20),GCH,DM,N,N1(20),IX,I1
      DO 8 I=2,N
      IF(X.GE.XR(I,1).AND.X.LE.XR(I,2)) GO TO 7
    8 END DO
      Return
    7 L=N1(I)
      IF(I1.EQ.I) GO TO 6
      I1=I
      C1=0.D0
      C2=0.D0
      C3=0.D0
      C4=0.D0
      C5=0.D0
      C6=0.D0
      C8=2.D0
      C9=0.D0
      C7=1.D0
      GO TO(1,2,3,4,5,9),L
   1  CONTINUE
    2 C1=(XR(I,2)*XR(I,3)-XR(I,1)*XR(I,4))/(XR(I,2)-XR(I,1))
      C5=(XR(I,4)-XR(I,3))/(XR(I,2)-XR(I,1))
      GO TO 6
    4 CONTINUE
    3 C2=-1.D0
      R2=XR(I,5)**2
      X1=XR(I,1)
      X2=XR(I,2)
      Y1=XR(I,3)
      Y2=XR(I,4)
      S=X2-X1
      C1=-0.5D0*(S*DSQRT(4.D0*R2/(S*S+(Y2-Y1)*(Y2-Y1))-1.D0)-Y1-Y2)
      C3=(Y2-Y1)*(Y2+Y1-2.D0*C1)/S+X2+X1
      C4=R2-C3*C3*0.25D0
      GOTO 6
    9 X1=XR(I,1)
      X2=XR(I,2)
      C1=0.5D0
      C7=-C1
      S1=DSQRT(1.D0-2.D0*XR(I,3))
      S2=DSQRT(1.D0-2.D0*XR(I,4))
      C9=(X2*S1-X1*S2)/(X2-X1)
      C6=(S2-S1)/(X2-X1)
      GO TO 6
    5 C8=XR(I,6)
      IF (XR(I,3).EQ.0.D0) XR(I,3)=1.0D-10
      P1=XR(I,3)**(1.D0/C8)
      P2=XR(I,4)**(1.D0/C8)
      P3=XR(I,2)-XR(I,1)
      C6=(P2-P1)/P3
      C9=(XR(I,2)*P1-XR(I,1)*P2)/P3
   6  S1=(C9+C6*X)**(C8-1.D0)*C7
      C=C5+SIG
      S=DSQRT(C2*X**2+C3*X+C4)
      R=C1+S+C*X+S1*(C9+C6*X)
      RX999=C+C6*C8*S1
      IF(S.EQ.0.D0) RETURN
      RX999=0.5D0*(2.D0*C2*X+C3)/S+RX999
      RETURN
      END
