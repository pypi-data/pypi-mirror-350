      SUBROUTINE INTER5(X,X1,X2,X3,X4,X5,F1,F2,F3,F4,F5,F)
      IMPLICIT REAL*8(A-H,O-Z)
      A1=(X-X2)*(X-X3)*(X-X4)*(X-X5)
      A2=(X-X1)*(X-X3)*(X-X4)*(X-X5)
      A3=(X-X1)*(X-X2)*(X-X4)*(X-X5)
      A4=(X-X1)*(X-X2)*(X-X3)*(X-X5)
      A5=(X-X1)*(X-X2)*(X-X3)*(X-X4)
      D1=(X1-X2)*(X1-X3)*(X1-X4)*(X1-X5)
      D2=(X2-X1)*(X2-X3)*(X2-X4)*(X2-X5)
      D3=(X3-X1)*(X3-X2)*(X3-X4)*(X3-X5)
      D4=(X4-X1)*(X4-X2)*(X4-X3)*(X4-X5)
      D5=(X5-X1)*(X5-X2)*(X5-X3)*(X5-X4)
      C1=A1/D1
      C2=A2/D2
      C3=A3/D3
      C4=A4/D4
      C5=A5/D5
      F=C1*F1+C2*F2+C3*F3+C4*F4+C5*F5
      RETURN
      END
