      SUBROUTINE CSV
      IMPLICIT REAL*8(A-H,O-Z)
      character *12 tx(7),sc*1,sim*78,nos(6)*14
C      real*8 RES(12)
      COMMON/TV/SIG,RXX
      COMMON/LENG/BL,ANL,ALA
      COMMON/IN/ISIG
      COMMON/BASE/CAB,CNB,CMB
      COMMON/BAND/CAP,CNP,CMP,HB
      COMMON/CVP/CXT(240),CNT(240),CMT(240),CPV(21),JA,JB,KF
      COMMON/DISC/R1,PI,I9,JH1,J9,KL
      COMMON/WAVE/CABL,CNBL,CMBL,CAW,CNW,CMW
      COMMON/TAIL1/CXO,CYO,CMO
      COMMON/ICOU/VOLN,SOBS,RJA1,RJA2,ICOUNT,NGOL,NHBS
      COMMON/GEO2/NFL,NN,IPRINT,MAL,MAX,IPR
      COMMON/GEOM1/XB(240),RB(240),RBP(240),C2,BETA
      COMMON/RX/XR(20,6),G(20),GCH,DM,N,N1(20),IX,I1
      COMMON/NNI/NTT(11),NP5,JZT
      COMMON/GEO3/VOVS,AL,YINT,F,RR,RREF,AREF,DLN
      COMMON/VOL/CAF,CNF,CMF,CMX,DIA,RN,AP,XP
      COMMON/PREOBR/PREB(10),RAB1,RAB2,IPE,NPR,NUPR
      COMMON/INPUT_DATA/AINF,RHOINF,AMUINF,CTS,DL,HMAX,DMAX,HUAT,DUAT,
     <DPR,NG,NH,NK
      DIMENSION RAB1(10),RAB2(10),IPN(7),CD(60),AAM(60)
      DIMENSION DCX(60),DCY(60),DXCD(60),DCMX(60),CDON(60),
     <DCML2(60),DCMX2(60)
      DIMENSION AM(50),ETA(44),ALOD(44),AMC(29),CDC(29),rx(60,7)
      data tx/'''  M(1-N3)=''','''CX?(1-N3)=''','''CYA(1-N3)=''',
     <''' MX(1-N3)=''','''MZA(1-N3)=''','''MXO(1-N3)=''',
     <'''MZO(1-N3)='''/,(rx(i,4),i=1,60)/60*0.0d0/
      DATA AMC/0.,0.05,0.1,.15,0.2,.25,0.3,.35,0.4,.45,0.5,.55,0.6,.65,0
     *.7,.75,0.8,.85,0.9,.95,1.,1.05,1.1,1.15,1.2,1.25,1.3,1.35,1.4/
      DATA CDC/1.2,1.2,1.2,1.2,1.2,1.2,1.2,
     *1.22,1.25,1.29,1.35,1.45,1.55,1.66,1.73,1.78,1.81,
     *1.83,1.82,1.81,1.8,1.77,1.75,1.72,1.68,1.65,1.61,1.58,1.53/
      DATA ALOD/1.,1.5,2.,2.5,3.0,3.5,4.,4.5,5.,5.5,6.,6.5,7.,7.5,8.,8.5
     *,9.,9.5,10.,10.5,11.0,11.5,12.,12.5,13.,13.5,14.,14.5,15.,15.5,16.
     *,16.5,17.0,17.5,18.,18.5,19.,19.5,20.,21.,22.,23.,24.,25./
      DATA ETA/0.53,0.554,0.57,0.582,0.593,0.603,0.613,0.62,0.627,0.633,
     *0.64,0.647,0.653,0.658,0.664,0.669,0.674,0.678,0.683,0.688,0.692,0
     *.696,0.7,0.704,0.708,0.712,0.716,0.72,0.724,0.728,0.732,0.736,0.74
     *,0.744,0.748,0.753,0.757,0.761,0.765,.744,.782,.79,.798,.806/
      data jj/11/,nos/'(?????)     ','(?????)       ',
     <'(??????? ???.)','(??????? ??.)','(?????)     ',
     <'(??????)    '/
      OPEN(UNIT=1,FILE='InPut.DAT',STATUS='OLD')
      OPEN(UNIT=2,FILE='Out.DAT')
 106  FORMAT(1X,9H??????? N,I2,5X,7H??? N,I2,5X,9H????? N,I2,5X,3
     *HAl=,F9.4,5X,2HD=,F6.4)
 107  FORMAT(' Mo=',F7.3,2X,'dM =',F7.3,2X,'al =',F7.3,2X,'dal=',F
     *7.3,2X,'Yint =',F7.3)
 1000 FORMAT(6E9.5)
 1001 FORMAT(15x,'?????????? ??????? :'/(I6,3X,4f8.4,2f8.4))
 1002 FORMAT(1X,4HAnl=F8.5,2X,4HAla=F8.5,2X,3HBl=F8.5,2X,4HDln=F8.5)
 2000 FORMAT(1X,3HN?=,I2,2X,3HN?=,I2,2X,3HN?=,I2,2X,4HNFL=,I1,2X,
     *7HIPrint=,I1,2X,4HMal=,I2,2X,
     *4HMax=,I2,2X,4HIpr=,I2,2X,3HC2=,F6.4,2X,
     *2Hf=,F5.3,2X,3HRr=,F8.6)
 1005 FORMAT(10F7.4)
      sim(72:78)='      '
C      write(*,'(1x, "???????? ???? ?????????? ?? ???????.")')
C      write(*,'(1x,a15)') '????????? (y/n)'
C      read(*,'(a1)') sc
      SC='y'
C      RJA1=0.
C      RJA2=0.
C      RXX=0.
C      AP=0.
C      DO 44 I=1,10
C      DO 45 J=1,6
C      XR(I,J)=0.
C  45  END DO
C  44  END DO
C      DO 55 I=1,240
C      CXT(I)=0.
C      CNT(I)=0.
C      CMT(I)=0.
C      XB(I)=0.
C      RB(I)=0.
C      RBP(I)=0.
C  55  END DO
C
C      ???????? MVAR ??? ?? ??? ???? ?????? ?? ????
C      ??? ?? ??????? rewind 1 ?? ?? ???? (?????)
C      ????? ? ?????? ???? ? ? ?? ??! //Y.Pavlov
C
C      READ(1,*) MVAR
C      RREF=0.5
c      PI=3.1415926536
C      AREF=PI*RREF**2
C      DO 15 NP =1,MVAR
      NP=1
      NPR=NP
C      READ(1,*)
C      READ(1,*)
C      if(sc.ne.'n') then
C         rewind 1
C         read(1,*)
C         read(1,'(a72,7x)') sim
C         write(2,*) sim
C         sim(48:78)='(??. ????? ?? ??? InPuT.dat)'
C         write(*,*) sim
C      end if
      NGOL=NG+1
      NHBS=NH+1
      N=NK+1
      IPR=0
      IPP=0
      IPM=0
      INM=0
      DATA IPN/7*0/
C      READ(1,*)
C      if(sc.ne.'n') then
C         rewind 1
C         read(1,*)
C         read(1,*)
C         read(1,'(a72,7x)') sim
C         write(*,*) sim
C         write(2,*) sim
C      end if
      IPP=IPP+1
      IPM=IPM+1
      INM=INM+1
C      READ(1,*) YINT,DIA,HB,AINF,RHOINF,AMUINF,C2,F,CTS,DL
C      READ(1,*)
C      if(sc.ne.'n') then
C         rewind 1
C         read(1,*)
C         read(1,*)
C         read(1,*)
C         read(1,'(a72,7x)') sim
C         write(*,*) sim
C         write(2,*) sim
C      end if
C      open(3,file='cons.dat')
C      write(3,4) DIA,DL
C    4 format(1x,'''DM='' ',f6.4,3x,'''DL='' ',f7.4)
C      READ(1,*) ((XR(I,J),J=1,6),I=2,N)
C      READ(1,*) HMAX,DMAX,HUAT,DUAT,DPR
      dlina=xr(n,2)+YINT
      IF(XR(2,3).LE.1.0D-3) XR(2,3)=0.
      IPR=IPR+1
      DO 15 NIP=1,IPR
      NPR=NIP
      DM=DIA
      NUPR=0
      I1=21
      IF(N1(N).NE.2) GO TO 6
      SLOPE=(XR(N,4)-XR(N,3))/(XR(N,2)-XR(N,1))
      IF(SLOPE.LT.-10.*3.1415926/180.) SLOPE=-.1584
cc
      XR(N,4)=XR(N,3)+(XR(N,2)-XR(N,1))*SLOPE
    6 CONTINUE
      if(sc.ne.'n') then
         do 999 I=2,N
         kkk=N1(I)
         WRITE(sim,'(I6,3x,4f8.4,2f8.4,4x,a14)')
     <   N1(I),(XR(I,J),J=1,6),nos(kkk)
         WRITE(*,*) sim
 999  continue

      end if
      WRITE(2,1001) (N1(I),(XR(I,J),J=1,6),I=2,N)
C      if(sc.ne.'n') then
C         rewind 1
C         do 66 I=2,N+4
C         read(1,*)
C   66    continue
C         read(1,'(a72,7x)') sim
C         WRITE(*,*) sim
C         write(2,*) sim
C      end if
      CXO=0.
      CYO=0.
      CMO=0.
      D4=1.
      IF(IX.EQ.1) D4=DM
      YINT=YINT/D4
      IF(NFL.NE.1) YINT=0.
      DO I=1,N
      PREB(I)=0.
      RAB1(I)=0.
      DO J=1,5
      XR(I,J)=XR(I,J)/D4
      END DO
      END DO
      RR=XR(2,3)
      IX=0
      IF(NIP.EQ.1) DPR=DPR*(XR(INM,2)-XR(INM,1))
      write(2,'(15x,''Ct='',f6.4)') CTS
      ALA=XR(NHBS,2)-XR(NGOL,2)
      BL=XR(N,2)-XR(NHBS,2)
      ANL=XR(NGOL,2)-XR(1,2)+YINT
      DLN=ANL+ALA+BL

      WRITE(2,1002) ANL,ALA,BL,DLN
      WRITE(2,2000) NG,NH,NK,NFL,IPRINT,MAL,MAX,IPR,C2,F,RR
      DO 27 MM=1,MAL
      LSG=0
      LPR=0
      AL=(MM-1)*DUAT+HUAT
      IF(AL.EQ.0.) AL=0.1
      I=NIP-1
      WRITE(2,106) NP,I,MM,AL,DIA
      AL=AL/57.29578D0
      VOVS=HMAX
C
C     Main cycle!!!
C      
C      CALL CSVSTEP(3.1D0, DLN, AL, dlina, RES)
      DO 1 J=1,MAX
      RN=VOVS*AINF*RHOINF/AMUINF
      RE=DM*DLN*RN
      PAL=0.2D0
      SIG=0.046D0*(1.D0+0.0092D0*VOVS**2)**0.88D0/RE**PAL
C      WRITE(*, '(''SIG='',F12.8)') SIG
      IF(ISIG.EQ.0) SIG=0.D0
      IF(LPR.EQ.0) CALL GEOM
      IF(J.GT.1) GO TO 11
      if(sc.eq.'n') WRITE(*,'(1x,''Max?: '')')
      write(2,'(/1x,''MAX'',3x,''TPEH'',3x,''DON'',4x,''VOLN'',3x,
     <''POIS'',4x,''CN'',5x,''CY'',5x,''XCD'',4x,''CX'',4x,''CYAL'',
     <4x,''MZA'',3x,''-MXWX'',3x,''MZWZ'')')
   11 CALL SKBARB
      IF(VOVS.LE.1.001D0) GO TO 62
      IF(VOVS.GT.1.26D0) GO TO 60
      VOV=VOVS
      IF(LSG.EQ.1) GO TO 61
      VOVS=1.D0
      CALL GEOM
      CALL TRANS
      CALL NORMFO
      Q1=1.D0
      P1A=CAW
      P1N=CNW
      P1M=CMW
      VOVS=1.27D0
      CALL GEOM
      CALL HYBRID
      Q2=1.27D0
      P2A=CAW
      P2N=CNW
      P2M=CMW
      VOVS=1.47D0
      CALL GEOM
      CALL HYBRID
      Q3=1.47D0
      P3A=CAW
      P3N=CNW
      P3M=CMW
      LSG=1
   61 VOVS=VOV
      CALL PROD(P1A,P2A,P3A,Q1,Q2,Q3,VOV,CAW,1)
      CALL PROD(P1N,P2N,P3N,Q1,Q2,Q3,VOV,CNW,1)
      CALL PROD(P1M,P2M,P3M,Q1,Q2,Q3,VOV,CMW,1)
      GO TO 5
C
   60 IF(JZT.EQ.0) GO TO 62
      MEX=1
   67 Q1=2.2D0+0.2D0*(1-MEX)
      VOV=VOVS
      IF(LPR.EQ.1) GOTO 63
      VOVS=Q1
      CALL GEOM
      CALL HYBRID
      P1A=CAW
      P1N=CNW
      P1M=CMW
      Q2=2.7D0+0.2D0*(1-MEX)
      VOVS=Q2
      CALL GEOM
      CALL HYBRID
      MEX=MEX+1
      IF(JZT.EQ.1) GOTO 67
      P2A=CAW
      P2N=CNW
      P2M=CMW
      Q3=13.5D0
      VOVS=Q3
      CALL GEOM
      CALL HYBRID
      P3A=CAW
      LPR=1
      P1N=-P1M/P1N
      P2N=-P2M/P2N
      P3A=P3A*1.02D0
      P3M=P2M+(P2M-P1M)*2.5D0
      P3N=P2N+(P2N-P1N)*(4.9D0+20.D0*AL)
   63 VOVS=VOV
      CALL PROD(P1A,P2A,P3A,Q1,Q2,Q3,VOV,CAW,2)
      CALL PROD(P1M,P2M,P3M,Q1,Q2,Q3,VOV,CMW,2)
      CALL PROD(P1N,P2N,P3N,Q1,Q2,Q3,VOV,C5W,2)
      CNW=-CMW/C5W
      GOTO 5
C
   62 IF(VOVS.LT.1.27D0) CALL NORMFO
      IF(VOVS.GE.0.85D0)GO TO 19
      IST=NTT(NGOL)
      THE1=DATAN(RBP(IST))*57.29578D0
      IF(THE1.GE.10.D0)GO TO 51
      CAW=0.D0
      GO TO 5
  51  CAW=0.012D0*(THE1-10.D0)
      GOTO 5
  19  IF(VOVS.LT.1.26D0)GO TO 2
      CALL HYBRID
      GO TO 5
  2   CALL TRANS
    5 CA=CAF+CAB+CAW+CAP+CXO
      CALL INTERP(ALOD,ETA,DLN,ETA1,44,3)
      AMC1=VOVS*DSIN(AL)
      CALL INTERP(AMC,CDC,AMC1,CDC1,29,3)
      S1=CDC1*ETA1*AP/AREF
      CNV=4.75D0*S1*AL**2.8
      CMV=-5.00D0*S1*XP*AL**2.80/(2.D0*RREF)
      IF(AL.GT.0.0175D0) GO TO 52
      CNV=0.
      CMV=0.
  52  CN=CNF+CNB+CNW+CNP+CNV+CYO*AL
      CM=CMF+CMB+CMW+CMP+CMV+CMO*AL
      CY=CN*DCOS(AL)-CA*DSIN(AL)
      CX=CN*DSIN(AL)+CA*DCOS(AL)
      IF(DABS(AL).LT.0.0001D0) GO TO 3
      CMAL=CM/AL
      XCD=-CM/CN
      CNAL=CN/AL
      CYAL=CY/AL
   3  CONTINUE
c
      ddt = dia/dlina
      xcd = xcd * ddt
      cm = cn * (cts-xcd)
      cmal = cnal * (cts - xcd)
      cmx = cmx * ddt**2
      cmzwz = cnal * (cts - xcd)**2
c
      AM(J)=VOVS
      rx(J,1)=VOVS
      CDON(J)=CAB
      DCX(J)=CX
      rx(J,2)=CX
      DCY(J)=CYAL
      rx(J,3)=CYAL
      DXCD(J)=XCD
      DCMX(J)=CMX
      rx(J,5)=CMAL
      DCMX2(J)=CMX*(-1.0d0)
      rx(J,6)=DCMX2(J)
      DCML2(J)=cmzwz
      rx(J,7)=DCML2(J)
      if(sc.ne.'n') then
         jj=jj+1
         if(jj.gt.10) then
            write(*,'(1x,''_'',''MAX'',2(''_''),''Cx??'',
     <      2(''_''),''Cx???'',2(''_''),''Cx??'',4(''_''),
     <      ''Cx'',4(''_''),''CYA'',4(''_''),''MZA'',3(''_''),
     <      ''-MXWX'',3(''_''),''MZWZ'',3(''_''),
     <      ''CXDN'',2(''_''),''Cnal'',4(''_''),''XCD'')')
            jj=0
         end if
         XCD1=XCD*dlina
         write(*,'(f5.2,f6.4,f7.4,f6.4,f7.4,f7.4,f7.4,f7.4,f7.4,
     <f7.4,f7.4,F6.3)')
     <   vovs,caf,caw,cap,cx,CYAL,CMAL,CMX,cmzwz,CAB,CNAL,XCD1
      else
         write(*,'(f3.1,'','')') VOVS
      end if
      write(2,'(f4.2,7f7.4,f7.4,f8.4,3f7.4)')
     <vovs,caf,cab,caw,cap,cn,cy,xcd,cx,cyal,cmal,cmx,cmzwz
      VOVS=VOVS+DMAX
      IF(VOVS.GT.0.9D0.AND.VOVS.LT.1.28D0)VOVS=VOVS-DMAX/2.D0
    1 END DO
C
C     End of main cycle!!!
C      
      IF(IPN(1).NE.0) PRINT 1005,(DCX(Ikk),Ikk=1,MAX)
      IF(IPN(2).NE.0) PRINT 1005,(DCY(Ikk),Ikk=1,MAX)
      IF(IPN(3).NE.0) PRINT 1005,(DXCD(Ikk),Ikk=1,MAX)
  27  END DO
      IF(IPN(5).NE.0) PRINT 1005,(AM(Ikk),Ikk=1,MAX)
      IF(IPN(6).NE.0) PRINT 1000,((XR(Ikk,Jkk),Jkk=1,6),Ikk=2,N)
      IF(IPN(4).NE.0) PRINT 1005,(DCMX(Ikk),Ikk=1,MAX)
      IF(IPR.EQ.1) GO TO 15
      CQ1=0.D0
      IF(IPP.EQ.20) CQ1=0.0087D0
      CQ2=0.D0
      IF(IPP.EQ.21) CQ2=0.0175D0
      CQ3=0.D0
      IF(IPP.EQ.22) CQ3=0.1D0
      DO  I=2,N
         IM=NTT(I)
         IF(N1(I).EQ.3) IM=NTT(I-1)+1
         XR(I,6)=XR(I,6)+CQ3
         RAB1(I)=RBP(IM)+CQ1
      END DO
      RAB2(1)=SLOPE+NIP*CQ2
      IF(IPP.EQ.22) GO TO 15
      PREB(IPP)=DPR
      PREB(IPM)=-PREB(IPP)
      CALL PREBR(2)
   15 Continue
      DO 2277 I=1,MAX

 2277 CONTINUE
C      write(3,7) MAX
C    7 format(10x,'''N3='' ',i2)
C      do j=1,7
C      write(3,'(a12,8f7.4:/(12x,8f7.4:))')
C     <tx(j),(rx(i,j),i=1,MAX)
C      end do
      J=0
      EE=0.0001
      DO 200 I=1,39
      IF(DABS(AM(I)-1.0).LE.EE)GO TO 111
      IF(DABS(AM(I)-1.5).LE.EE)GO TO 111
      IF(DABS(AM(I)-2.0).LE.EE)GO TO 111
      IF(DABS(AM(I)-2.5).LE.EE)GO TO 111
      IF(DABS(AM(I)-3.0).LE.EE)GO TO 111
      IF(DABS(AM(I)-3.5).LE.EE)GO TO 111
      IF(DABS(AM(I)-3.8).LE.EE)GO TO 111
      GO TO 222
  111 J=J+1
      AAM(J)=AM(I)
      CD(J)=CDON(I)
  222 CONTINUE
200   CONTINUE
C      write(3,'(10x,'''''''',''N7='','''''''','' 5'',/'''''''',
C     <''AM(1-N7)='','''''''','' '',5f7.2/'''''''',''CXD(1-N7)'',
C     <'''''''','' '',5f7.4,'' /'')') (AAM(i),i=1,5),(CD(i),i=1,5)

      WRITE(2,107) HMAX,DMAX,HUAT,DUAT,YINT
      END


