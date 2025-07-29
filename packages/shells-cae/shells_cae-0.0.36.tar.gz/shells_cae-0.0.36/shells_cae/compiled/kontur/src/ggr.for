      SUBROUTINE GGR(AM,CDON,SNT,STBL,NM,NK)
      IMPLICIT REAL*8(A-H,O-Z)
      DIMENSION AM(39),CDON(39),AK1(7),AK(10),AAM(7),
     *CD(7),CG(7),SNT(17),STBL(70)
      OPEN(UNIT=3,FILE='GG.DAT',STATUS='OLD')
      OPEN(UNIT=2,FILE='OutPut.DAT',STATUS='OLD')
      READ(3,*)HU,DDON,CPG,TG,CN,ETG,SM,NM,NK
      READ(3,*)(AK1(I),I=1,NM)
      READ(3,*)(AK(I),I=1,NK)
      WRITE(2,100)HU,DDON,CPG,TG,CN,ETG,SM,NM,NK
100   FORMAT(2X,'HU=',F8.1,3X,'DDON='F8.3,3X,
     *'CPG=',F6.2,3X,'TG=',F6.2,/
     *3X,'CN=',F4.1,3X,'ETG=',F5.1,3X,'SM=',F8.5,1X,'NM=',I2,3X,
     *'NK=',I2)
      J=0
      EE=0.0001
      DO 200 I=1,39
      IF(DABS(AM(I)-1.0).LE.EE)GO TO 1
      IF(DABS(AM(I)-1.5).LE.EE)GO TO 1
      IF(DABS(AM(I)-2.0).LE.EE)GO TO 1
      IF(DABS(AM(I)-2.5).LE.EE)GO TO 1
      IF(DABS(AM(I)-3.0).LE.EE)GO TO 1
      IF(DABS(AM(I)-3.5).LE.EE)GO TO 1
      IF(DABS(AM(I)-3.8).LE.EE)GO TO 1
      GO TO 2
 1    J=J+1
      AAM(J)=AM(I)
      CD(J)=CDON(I)
2     CONTINUE
200   CONTINUE
      WRITE(2,9)
      WRITE(2,8)(AAM(I),I=1,NM)
      WRITE(2,888)(CD(I),I=1,NM)
      WRITE(2,101)(AK1(I),I=1,NM)
101   FORMAT(2X,'AK1=',10F9.4)
8     FORMAT(2X,' M ='10F9.4)
888   FORMAT(2X,' CD='10F9.4)
      WRITE(2,9)
      WRITE(2,777)(AK(I),I=1,NK)
777   FORMAT(2X,'  M  \ AK=',10F8.5)
      WRITE(2,9)
      JJ=0
      DO 4 N=1,NM
      DO 5 N1=1,NK
      RGG=CPG*(TG+273.0)+HU*ETG
      SD=3.141593*DDON**2/4.0
      TT=288.0*(1.0+0.2*AAM(N)**2)
      AMUG=AK(N1)*RGG/(CN*TT*0.24)
      CG(N1)=AMUG**0.45*AK1(N)*(SD/(SM*AAM(N)**2*0.7)-CD(N))
      JJ=JJ+1
5     STBL(JJ)=CG(N1)
      AM1=AAM(N)
      WRITE(2,300)AM1,(CG(I),I=1,NK)
300   FORMAT(F8.5,3X,10F8.5)
4     CONTINUE
      WRITE(2,9)
9     FORMAT(70('='))
      DO 10 I=1,NK
10    SNT(I)=AK(I)
      NN=NK
      DO 11 I=1,NM
      NN=NN+1
11    SNT(NN)=AAM(I)
      RETURN
      END
