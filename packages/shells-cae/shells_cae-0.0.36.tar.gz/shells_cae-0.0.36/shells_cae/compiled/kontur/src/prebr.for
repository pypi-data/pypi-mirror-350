      SUBROUTINE PREBR(J1)
      IMPLICIT REAL*8(A-H,O-Z)
      DIMENSION RAB1(10),RAB2(10)
      COMMON/PREOBR/PREB(10),RAB1,RAB2,IPE,NPR,NUPR
      COMMON/RX/XR(20,6),G(20),GCH,DM,N,N1(20),IX,I1
      S=XR(J1,1)
      DO 1 I=J1,N
      S=S+XR(I,2)-XR(I,1)+PREB(I)
      XR(I,2)=S
1     END DO
      DO 2 I=J1,N
      XR(I,1)=XR(I-1,2)
      IF(N1(I).EQ.4.OR.N1(I).EQ.3) GO TO 3
      GO TO 2
    3 Q=XR(I,2)-XR(I,1)
      S=XR(I,4)-XR(I,3)
      TET=DATAN(RAB1(I))
      SNT=DSIN(TET)
      CST=DCOS(TET)
      XR(I,5)=(S**2+Q**2)/(2.D0*(S*CST-Q*SNT))
    2 END DO
      IF(N1(N).EQ.2) XR(N,4)=XR(N,3)+RAB2(1)*(XR(N,2)-XR(N,1))
      RETURN
      END
