      SUBROUTINE PROD(Y1,Y2,Y3,X1,X2,X3,CM,P,I)
      IMPLICIT REAL*8(A-H,O-Z)
      S12=X1-X2
      S13=X1-X3
      S23=X2-X3
      IF(I.EQ.2) GOTO3
      Q1=Y1
      Q2=Y2
      Q3=Y3
      GOTO2
  3   Q1=Y1*X1
      Q2=Y2*X2
      Q3=Y3*X3
  2   A=(Q1*S23-Q2*S13+Q3*S12)/(S12*S13*S23)
      B=(Q3-Q2)/S23+A*(X2+X3)
      C=Q3-A*X3**2+B*X3
      P=A*CM**2-B*CM+C
      IF(I.EQ.2) P=P/CM
      RETURN
      END
