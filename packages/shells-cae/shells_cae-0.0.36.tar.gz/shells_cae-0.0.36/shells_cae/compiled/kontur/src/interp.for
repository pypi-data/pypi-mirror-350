      SUBROUTINE INTERP(TX,TY,X,Y,N,J)
      IMPLICIT REAL*8(A-H,O-Z)
      DIMENSION TX(N),TY(N)
      N1=N-2
      DO 1 I=J,N1
      IF(X.LE.TX(I)) GO TO 2
   1  END DO
      I=N1
   2  CALL INTER5(X,TX(I-2),TX(I-1),TX(I),TX(I+1),TX(I+2),TY(I-2),TY(I-1
     *),TY(I),TY(I+1),TY(I+2),Y)
      RETURN
      END
