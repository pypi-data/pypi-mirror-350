!!!$     diff-        subroutine kont1(delem,delectr,dstrom,drandb)
!!!$     diff+<
SUBROUTINE kont1(delem,delectr,dstrom,drandb,dd0,dm0,dfm0,lagain)
!!!$     diff+>

!!!$     Unterprogramm zur Ausgabe der Kontrollvariablen.

!!!$     Andreas Kemna                                            16-Apr-1996
!!!$     Letzte Aenderung   16-Jul-2007

!!!$.....................................................................

  USE variomodel
  USE femmod
  USE datmod
  USE cjgmod
  USE sigmamod
  USE modelmod
  USE elemmod
  USE wavenmod
  USE randbmod
  USE errmod
  USE konvmod
  USE pathmod
  USE get_ver,ONLY : version

  IMPLICIT NONE

!!!$.....................................................................
!!!$     EIN-/AUSGABEPARAMETER:

!!!$     Dateinamen
  CHARACTER (80)  :: delem,delectr,dstrom,dd0,dm0,dfm0,drandb
  LOGICAL :: lagain
  REAL(KIND(0D0)) :: Ix,Iy

  fetxt = ramd(1:lnramd)//slash(1:1)//'inv.ctr'
  OPEN(fpinv,file=TRIM(fetxt),status='old',POSITION='append',err=999)


!!!$     HEADER AUSGEBEN
10 FORMAT (l1,t20,a)
11 FORMAT (g11.5,t20,a)
12 FORMAT (I8,t20,a)
13 FORMAT (t1, a3, t5,a3,t11,a8,t23,a8,t34,a8,t46,a8,t58,a8,&
       t69,a8,t81,a8,t93,a8,t105,a8,t117,a10)
14 FORMAT (t1, a3, t5,a3,t11,a8,t23,a8,t34,a8,t46,a8,t58,a8,&
       t69,a8,t81,a8,t93,a8,t105,a10)


  WRITE (fpinv,'(a)')'##'
  WRITE (fpinv,'(a)')'## Complex Resistivity Tomography (CRTomo)'
  WRITE (fpinv,'(a)')'##'
  WRITE (fpinv,'(a)')'## Git-Branch '//TRIM(version(1))
  WRITE (fpinv,'(a)')'## Git-ID     '//TRIM(version(2))
  WRITE (fpinv,'(a)')'## Compiler   '//TRIM(version(4))
  WRITE (fpinv,'(a)')'## OS         '//TRIM(version(5))
  WRITE (fpinv,'(a)')'##'
  WRITE (fpinv,'(a)')'## Created  '//TRIM(version(3))
  WRITE (fpinv,'(a)')'##'
  WRITE (fpinv,'(a)')''

  IF (mswitch /= 0) THEN
     WRITE(fpinv,12,err=999)mswitch,'#  mswitch'
  ELSE
     WRITE(fpinv,'(a)',err=999) '***FILES***'
  END IF

  WRITE(fpinv,'(a)',err=999) TRIM(delem)//' # FEM grid'
  WRITE(fpinv,'(a)',err=999) TRIM(delectr)//' # Electrodes'
  WRITE(fpinv,'(a)',err=999) TRIM(dstrom)//' # Measurements'
  WRITE(fpinv,'(a)',err=999) TRIM(ramd)//' # Inversion results'
!!!$     diff+<
  WRITE(fpinv,10,err=999) ldiff.OR.lprior,&
       '! difference inversion or (m - m_{prior})'
  WRITE(fpinv,'(a)',err=999) TRIM(dd0)
  WRITE(fpinv,'(a)',err=999) TRIM(dm0)
  WRITE(fpinv,'(a)',err=999) TRIM(dfm0)
!!!$     diff+>
  IF (lnsepri) THEN
     WRITE (fpinv,*,err=999) iseedpri,modl_stdn
  ELSE
     WRITE(fpinv,'(a)',err=999) '***PARAMETERS***'
  END IF
  WRITE(fpinv,12,err=999) nx,'! nx-switch or # cells in x-direction'
  WRITE(fpinv,12,err=999) nz,'! nz-switch or # cells in z-direction'
  WRITE(fpinv,11,err=999) alfx,'! smoothing parameter in x-direction'
  WRITE(fpinv,11,err=999) alfz,'! smoothing parameter in z-direction'
  WRITE(fpinv,12,err=999) itmax,'! max. # inversion iterations'
!!!$     ak        write(fpinv,'(g11.5,t18,a15)',err=999) nrmsdm,'! min. data RMS'
  WRITE(fpinv,10,err=999) ldc,'! DC inversion ?'
!!!$     ak        write(fpinv,'(l1,t18,a23)',err=999) lsr,'! singularity removal ?'
  WRITE(fpinv,10,err=999) lrobust,'! robust inversion ?'
!!!$     ak        write(fpinv,'(l1,t18,a33)',err=999) lpol,
!!!$     ak     1           '! automatic polarity adjustment ?'
  WRITE(fpinv,10,err=999) lfphai,'! final phase improvement ?'
  WRITE(fpinv,11,err=999) stabw0,'! rel. resistance error level (%)'// &
       '  (parameter A1 in err(R) = A1*abs(R) + A2)'
  WRITE(fpinv,11,err=999) stabm0,'! min. abs. resistance error (ohm)'// &
       ' (parameter A2 in err(R) = A1*abs(R) + A2)'
  WRITE(fpinv,11,err=999) stabpA1,&
       '! phase error model parameter A1 (mrad/ohm^B) '// &
       '(in err(pha) = A1*abs(R)**B + A2*abs(pha) + A3)'
  WRITE(fpinv,11,err=999) stabpB, &
       '! phase error model parameter B  (-)          '// &
       '(in err(pha) = A1*abs(R)**B + A2*abs(pha) + A3)'
  WRITE(fpinv,11,err=999) stabpA2, &
       '! phase error model parameter A2 (%)          '// &
       '(in err(pha) = A1*abs(R)**B + A2*abs(pha) + A3)'
  WRITE(fpinv,11,err=999) stabp0, &
       '! phase error model parameter A3 (mrad)       '// &
       '(in err(pha) = A1*abs(R)**B + A2*abs(pha) + A3)'
  WRITE(fpinv,10,err=999) lrho0,'! homogeneous background resistivity ?'
  WRITE(fpinv,11,err=999) bet0,'! background magnitude (ohm*m)'
  WRITE(fpinv,11,err=999) pha0,'! background phase (mrad)'
  WRITE(fpinv,10,err=999) lagain,'! Another dataset?'
  WRITE(fpinv,12,err=999) swrtr,'! 2D (=0) or 2.5D (=1)'
  WRITE(fpinv,10,err=999) lsink,'! fictitious sink ?'
  WRITE(fpinv,12,err=999) nsink,'! fictitious sink node number'
  WRITE(fpinv,10,err=999) lrandb2,'! boundary values ?'
  WRITE(fpinv,'(a)',err=999) TRIM(drandb)
  IF (BTEST(llamf,0)) THEN
     IF (BTEST(llamf,1)) THEN
        WRITE (fpinv,'(I2)') ltri + 2**5 + 2**6
     ELSE
        WRITE (fpinv,'(I2)') ltri + 2**5
     END IF
  ELSE
     WRITE (fpinv,'(I2)') ltri
  END IF
  WRITE (fpinv,'(I2)',err=999) ltri
  IF (BTEST(ltri,5)) WRITE (fpinv,*,err=999) lamfix
  IF (ltri > 4 .AND. ltri < 15) WRITE (fpinv,*,err=999) betamgs
  IF ( lnse ) WRITE (fpinv,*,err=999) iseed
100 FORMAT (a,t39,l1)
101 FORMAT (a,t30,g10.5)
102 FORMAT (a,t30,I8)

  WRITE(fpinv,'(/a)',err=999)'***Model stats***'
  WRITE(fpinv,102,err=999)'# Model parameters',manz
  WRITE(fpinv,102,err=999)'# Data points',nanz
  WRITE(fpinv,100,err=999)'Add data noise ?',lnse
  WRITE(fpinv,100,err=999)'Couple to Err. Modl?',.NOT.lnse2
  WRITE(fpinv,102,err=999)'    seed',iseed
  WRITE(fpinv,101,err=999)'    Variance',nstabw0
  WRITE(fpinv,100,err=999)'Add model noise ?',lnsepri
  WRITE(fpinv,102,err=999)'    seed',iseedpri
  WRITE(fpinv,101,err=999)'    Variance',modl_stdn
  WRITE(fpinv,'(/a)',err=999)'******** Regularization Part *********'
  WRITE(fpinv,100,err=999)'Prior regualrization',lprior
  WRITE(fpinv,100,err=999)'Reference regualrization',lw_ref
  IF (lw_ref) THEN
     IF (lam_ref_sw == 1) WRITE(fpinv,'(a)',err=999)&
          '  -> vertical gradient'
     IF (lam_ref_sw == 2) WRITE(fpinv,'(a)',err=999)&
          '  -> horizontal gradient'
     WRITE(fpinv,101,err=999)'  global regularization strength',lam_ref
  END IF
  WRITE(fpinv,101,err=999)'Regularization-switch',ltri
  WRITE(fpinv,100,err=999)'Regular grid smooth',(ltri==0)
  WRITE(fpinv,100,err=999)'Triangular regu',(ltri==1)
  WRITE(fpinv,100,err=999)'Triangular regu2',(ltri==2)
  WRITE(fpinv,100,err=999)'Levenberg damping',(ltri==3)
  WRITE(fpinv,100,err=999)'Marquardt damping',(ltri==4)
  WRITE(fpinv,100,err=999)'Minimum grad supp',(ltri==5)
  WRITE(fpinv,100,err=999)'MGS beta/sns1 (RM)',(ltri==6)
  WRITE(fpinv,100,err=999)'MGS beta/sns2 (RM)',(ltri==7)
  WRITE(fpinv,100,err=999)'MGS beta/sns1 (RB)',(ltri==8)
  WRITE(fpinv,100,err=999)'MGS beta/sns2 (RB)',(ltri==9)
  WRITE(fpinv,100,err=999)'TV (Huber)',(ltri==10)

  IF (ltri>4.AND.ltri<15)&
       WRITE(fpinv,101,err=999)'  Stabilizer beta',betamgs

  !  WRITE(fpinv,100,err=999)'Stochastic regu',(ltri==15)

  IF (ltri == 15) THEN
     CALL get_vario (Ix,Iy,fetxt,1) ! get covariance..
     WRITE (fpinv,'(a)',err=999)'Covariance regu ('//TRIM(fetxt)//')'
     WRITE (*,'(a)')ACHAR(9)//'Covariance ('//TRIM(fetxt)//')'
  END IF

  IF (lvario) THEN
     WRITE (fpinv,'(a)',err=999)'Caculate experimental Variogram::'
     WRITE (fpinv,'(a,I4)',err=999)ACHAR(9)//'nx-switch  : ',nx
     CALL get_vario (Ix,Iy,fetxt,0) ! get korrelation lengths
     WRITE (fpinv,'(2(a,F5.2))',ERR=999)ACHAR(9)// &
          'Correlation lengths Ix/Iy',Ix,'/',Iy
     WRITE (*,'(2(a,F5.2),a)')ACHAR(9)// &
          'Correlation lengths (I{x,y}) (',Ix,'/',Iy,') [m]'
     WRITE (fpinv,'(a)',err=999)ACHAR(9)// &
          'Variogram ('//TRIM(fetxt)//')'
     WRITE (*,'(a)')ACHAR(9)//'Variogram ('//TRIM(fetxt)//')' 
  END IF

  WRITE(fpinv,100,err=999)'Fixed lambda?',BTEST(llamf,0)
  IF (BTEST(llamf,0)) WRITE (fpinv,101,err=999)'Lambda=',lamfix
  IF (BTEST(llamf,1)) WRITE(fpinv,100,err=999)'Cooling lambda?',&
       BTEST(llamf,1)

  IF (nz<0) THEN
     WRITE(fpinv,'(a)',err=999,ADVANCE='no')'Taking easy lam_0 : '
     IF (nz<-1) WRITE(fpinv,*,err=999) -REAL(nz)
     IF (nz==-1) WRITE(fpinv,*,err=999)MAX(REAL(manz),REAL(nanz))
  END IF

  WRITE(fpinv,'(/a,I6)',err=999)'******** Additional output *********'
  WRITE(fpinv,101,err=999)'mswitch',mswitch
  WRITE(fpinv,100,err=999)'Read start model?',lstart
  WRITE(fpinv,100,err=999)'Write coverage?',lsens
  WRITE(fpinv,100,err=999)'Write MCM 1?',lcov1
  WRITE(fpinv,100,err=999)'Write resolution?',lres
  WRITE(fpinv,100,err=999)'Write MCM 2?',lcov2
  WRITE(fpinv,100,err=999)'Using Gauss ols?',lgauss
  WRITE(fpinv,100,err=999)'Forcing negative phase?',lphi0
  WRITE(fpinv,100,err=999)'Calculate sytop?',lsytop
  WRITE(fpinv,100,err=999)'Verbose?',lverb
  WRITE(fpinv,100,err=999)'Error Ellipses?',lelerr
  WRITE(fpinv,100,err=999)'Restart FPI with homogenous phase?',lffhom
  WRITE(fpinv,'(l1,t18,a20)',err=999) lindiv,'! individual error ?'

  WRITE(fpinv,'(/a)',err=999) '***FIXED***'

  IF (swrtr.EQ.1) THEN
     WRITE(fpinv,'(a,t50,i2)',err=999) ' # wavenumbers :',kwnanz
     WRITE(fpinv,'(a,t50,g11.5,t62,a1)',err=999)&
          ' Inverse Fourier transform range :',amin,'m'
     WRITE(fpinv,'(t50,g11.5,t62,a1)',err=999) amax,'m'
  END IF
  IF (lsytop) THEN
     WRITE(fpinv,'(a,t50,g11.5)',err=999) &
          ' -- Sytop [m] :',sytop
  END IF
  IF (.NOT.lrho0.AND..NOT.lstart) THEN
     bet0 = cdabs(dcmplx(1d0)/sigma0)
     pha0 = 1d3*datan2(dimag(dcmplx(1d0)/sigma0),DBLE(dcmplx(1d0)/sigma0))
     WRITE(fpinv,'(a,t50,g11.5,t62,a5)',err=999) &
          ' Background resistivity :',bet0,'ohm*m'
     WRITE(fpinv,'(t50,g11.5,t62,a4)',err=999)pha0,'mrad'
  END IF
  WRITE(fpinv,'(a,t50,l1)',err=999)' Force negative phase ?',lphi0
  WRITE(fpinv,'(a16,t50,l1)',err=999) ' Ratio dataset ?',lratio
  IF (lrobust.OR.lfphai) WRITE(fpinv,'(a13,t50,g11.5)',err=999)&
       ' Min. L1 norm',l1min
  WRITE(fpinv,'(a,t50,g11.5)',err=999)&
       ' Min. rel. decrease of data RMS :',mqrms
  WRITE(fpinv,'(a,t50,g11.5)',err=999)&
       ' Min. steplength              :',stpmin
  WRITE(fpinv,'(a,t50,g11.5)',err=999)&
       ' Min. stepsize (||\delta m||) :',bdmin
  WRITE(fpinv,'(a,t50,g11.5)',err=999)&
       ' Min. error in relaxation :',eps
  WRITE(fpinv,'(a,t50,i5)',err=999)&
       ' Max. # relaxation iterations :',ncgmax
  WRITE(fpinv,'(a,t50,i3)',err=999)&
       ' Max. # regularization steps :',nlam
  WRITE(fpinv,'(a,t50,g11.5)',err=999)' Initial step factor :',fstart
  WRITE(fpinv,'(a,t50,g11.5)',err=999)' Final   step factor :',fstop
  WRITE(fpinv,*,err=999)
  WRITE(fpinv,'(a48,a48,a13)',err=999)&
       '------------------------------------------------',&
       '------------------------------------------------',&
       '-------------'
  WRITE(fpinv,*,err=999)
!!!$     Robuste Inversion
  IF (lrobust) THEN
     WRITE(fpinv,13,err=999)'ID','it.','data RMS','stepsize',&
          ' lambda ',' roughn.','CG-steps',' mag RMS',' pha RMS',&
          '- # data','L1-ratio','steplength'
  ELSE
     WRITE(fpinv,14,err=999)&
          'ID','it.','data RMS','stepsize',' lambda ',' roughn.',&
          'CG-steps',' mag RMS',' pha RMS','- # data','steplength'
  END IF
  WRITE(fpinv,*,err=999)

!!!$     'inv.ctr' schliessen
  CLOSE(fpinv)

  errnr = 0
  RETURN

!!!$:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

!!!$     Fehlermeldungen

999 RETURN

END SUBROUTINE kont1
