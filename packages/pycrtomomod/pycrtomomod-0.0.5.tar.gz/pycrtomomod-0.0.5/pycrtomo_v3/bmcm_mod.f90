MODULE bmcm_mod
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!$ Collection of subroutines to calculate linearized model
!!!$ uncertainty and resolution matrices for ERT (DC) and EIT (IP)
!!!$
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!$ Copyright by Andreas Kemna 2010
!!!$
!!!$ Created by Roland Martin               30-Jul-2010
!!!$
!!!$ Last changed       RM                  Jul-2010
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


  USE tic_toc ! counts calculation time
  USE alloci , ONLY : sens,sensdc,smatm,ata,ata_reg,cov_m
  USE femmod , ONLY : ldc
  USE elemmod, ONLY : max_nr_element_nodes,espx,espy,nachbar
  USE invmod , ONLY : lfpi,wmatd,wdfak,par
  USE errmod , ONLY : errnr,fetxt
  USE konvmod , ONLY : ltri,lgauss,lam,nx,nz,mswitch,lcov2,lres,lverb,&
       lverb_dat,lelerr,lam_cri
  USE modelmod , ONLY : manz
  USE datmod , ONLY : nanz,wmatdr,wmatd_cri,wmatdp
  USE errmod, ONLY : errnr,fetxt,fprun
  USE sigmamod , ONLY : sigma
  USE pathmod
  USE ompmod, ONLY : CHUNK_0

  IMPLICIT none

  PUBLIC :: buncert
!!!$ this sub controls uncertainty caculation

  PRIVATE :: bata
!!!$ A^HC_d^-1A  -> ata
  PRIVATE :: bata_reg
!!!$ ata + lam*C_m^-1 -> ata_reg
  PRIVATE :: bmcm ! inversion
!!!$ ata_reg^-1   -> cov_m
  PRIVATE :: bres ! MATMUL
!!!$ cov_m * ata -> ata_reg
  PRIVATE :: bmcm2 ! MATMUL
!!!$ ata_reg * cov_m -> ata

CONTAINS

  SUBROUTINE buncert (kanal,lamalt)

!!!$
!!!$ This sub is the control unit of the smatm calculation
!!!$
    INTEGER (KIND = 4 ),INTENT(IN) :: kanal ! kanal is the io unit number
    REAL (KIND(0D0)),INTENT(IN)    :: lamalt ! lambda of the last iteration
!!! for tic_toc
    INTEGER (KIND = 4 )            :: c1

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!$    get time
    CALL TIC(c1)

    WRITE(*,'(a)')'Calculating model uncertainty..'
    WRITE (fprun,'(a)')'Calculating model uncertainty..'
    IF (lfpi) THEN
       WRITE(*,'(a)')' --> resetting lambda of FPI to CRI value'
       WRITE(fprun,'(a)')' --> resetting lambda of FPI to CRI value'
       lam = lam_cri
    ELSE
       WRITE(*,'(a)')' --> taking last good lambda'
       WRITE(fprun,'(a)')' --> taking last good lambda'
       lam = lamalt
    END IF

    WRITE (*,'(/a,G10.3,a/)')'take current lambda ?',lam,&
         ACHAR(9)//':'//ACHAR(9)

    IF (BTEST(mswitch,6)) THEN
       READ (*,*)fetxt
       IF (fetxt/='')READ(fetxt,*)lam
       WRITE (*,*)'No, set lambda to ',lam
    ELSE
       WRITE (*,*)' Yes'
    END IF

    WRITE (fprun,*)'----> taking lam=',lam

    WRITE(*,'(a)')ACHAR(13)//&
         'calculating MCM_1 = (A^TC_d^-1A + C_m^-1)^-1'
    WRITE(fprun,'(a)')'MCM_1 = (A^TC_d^-1A + C_m^-1)^-1'

    IF (lelerr) THEN
       WRITE (*,'(/a/a/)')'++ Resetting error weighting for uncertainty',&
            '  --> Complex error ellipses of CRI'
       wmatd = wmatd_cri
    ELSE IF (lfpi) THEN
       WRITE (*,'(/a/a/)')'++ Resetting error weighting for uncertainty',&
            '  --> Magnitude error of CRI'
       wmatd = wmatdr
    END IF

    ALLOCATE (ata(manz,manz),STAT=errnr)
    IF (errnr /= 0) THEN
       errnr = 97
       RETURN
    END IF
    ata = 0D0

    fetxt = ramd(1:lnramd)//slash(1:1)//'ata.diag'
    CALL bata(kanal) ! A^TC_d^-1A -> ata
    if (errnr.ne.0) RETURN

    ALLOCATE (ata_reg(manz,manz),STAT=errnr)
    IF (errnr /= 0) THEN
       errnr = 97
       RETURN
    END IF
    ata_reg = 0D0

    fetxt = ramd(1:lnramd)//slash(1:1)//'ata_reg.diag'
    CALL bata_reg(kanal) !ata + C_m^-1(lam) -> ata_reg_dc
    if (errnr.ne.0) RETURN

    ALLOCATE (cov_m(manz,manz))
    IF (errnr/=0) THEN
       WRITE (*,'(/a/)')'Allocation problem MCM_1 in bmcmdc'
       errnr = 97
       RETURN
    END IF
    cov_m = 0D0

    CALL bpar

    fetxt = ramd(1:lnramd)//slash(1:1)//'cov1_m.diag'
    CALL bmcm(kanal,lgauss) ! (A^TC_d^-1A + C_m^-1)^-1   -> cov_m_dc
    if (errnr.ne.0) RETURN


    IF (lres) THEN

       fetxt = ramd(1:lnramd)//slash(1:1)//'res_m.diag'

       WRITE(*,'(a)')ACHAR(13)//'calculating RES = '//&
            '(A^TC_d^-1A + C_m^-1)^-1A^TC_d^-1A'
       WRITE(fprun,'(a)')'RES = (A^TC_d^-1A + C_m^-1)^-1A^TC_d^-1A'

       CALL bres(kanal)
       if (errnr.ne.0) RETURN

       IF (lcov2) THEN

          fetxt = ramd(1:lnramd)//slash(1:1)//'cov2_m.diag'

          WRITE(*,'(a)')ACHAR(13)//'calculating MCM_2 = '//&
               '(A^TC_d^-1A + C_m^-1)^-1 A^TC_d^-1A (A^TC_d^-1A + C_m^-1)^-1'
          WRITE(fprun,'(a)')'MCM_2 = (A^TC_d^-1A + C_m^-1)'//&
               '^-1 A^TC_d^-1A (A^TC_d^-1A + C_m^-1)^-1'

          CALL bmcm2(kanal)
          if (errnr.ne.0) RETURN

       END IF              ! lcov2
    END IF                 ! lres

!!! $ may be we ant to write out not only main diagonals before freeing

    IF (ALLOCATED (ata)) DEALLOCATE (ata)
    IF (ALLOCATED (ata_reg)) DEALLOCATE (ata_reg)
    IF (ALLOCATED (cov_m)) DEALLOCATE (cov_m)

    fetxt = 'uncertainty calculation time'
    CALL TOC(c1,fetxt)

  END SUBROUTINE buncert

  SUBROUTINE bata(kanal)
!!!$
!!!$    Unterprogramm berechnet A^HC_d^-1A
!!!$
!!!$    Copyright Andreas Kemna 2009
!!!$    Created by  Roland Martin                            02-Nov-2009
!!!$
!!!$    Last changed      RM                                   20-Feb-2011
!!!$
!!!$.....................................................................
!!!$   PROGRAMMINTERNE PARAMETER:
!!!$   Hilfsvariablen
    INTEGER                                  :: kanal
    INTEGER                                  :: i,j,k
    COMPLEX (KIND(0D0))                      :: cdum
    REAL (KIND(0D0))                         :: dum = 0D0
    REAL(KIND(0d0)),DIMENSION(:),ALLOCATABLE :: dig,dig_fpi    ! contains diagonal of ATA
    REAL (KIND(0D0))                         :: dig_min,dig_max ! MINMAX(diag{ATA})
    INTEGER                                  :: c1
    CHARACTER(80)                            :: csz
    CHARACTER(256)                           :: fname

!!!$....................................................................

!!!$  A^TC_d^-1A

    errnr = 4
    fname = TRIM(fetxt) ! reassign

    fetxt = 'allocating digs'
    ALLOCATE(dig(manz),dig_fpi(manz),STAT=errnr)
    IF (errnr /= 0) THEN
       errnr = 97
       RETURN
    END IF

    ata = 0d0

    CALL TIC(c1)

    IF (ldc) THEN

       DO k=1,manz
          DO j=k,manz ! fills upper triangle (k,j)
             DO i=1,nanz
                ata(k,j) = ata(k,j) + sensdc(i,k) * &
                     sensdc(i,j) * wmatd(i) * DBLE(wdfak(i))
             END DO
             ata(j,k) = ata(k,j) ! fills lower triangle (k,j)
          END DO
          dig(k) = ata(k,k)
       END DO
    ELSE
       DO k=1,manz
          DO j=k,manz ! upper triangle
             cdum = DCMPLX(0d0)
             IF (j==k) dum = 0d0
             DO i=1,nanz
                cdum = cdum + DCONJG(sens(i,k)) * &
                     sens(i,j) * wmatd(i) * DBLE(wdfak(i))

                IF (j==k) dum = dum + DBLE(sens(i,k)) * DBLE(sens(i,j)) * &
                     wmatdp(i)*DBLE(wdfak(i))

             END DO
             ata(k,j) = real(cdum) ! fills upper triangle (k,j)
             ata(j,k) = real(cdum) ! fills lower triangle (j,k)
          END DO
          dig(k) = ata(k,k)
          dig_fpi(k) = dum
       END DO
    END IF

    csz = 'ATA time'
    CALL TOC(c1,csz)

!!!$    get min/max
    dig_min = MINVAL(dig)
    dig_max = MAXVAL(dig)
!!!$    write out
    errnr = 1
    OPEN (kanal,file=TRIM(fname),status='replace',err=999)
    errnr = 4

    WRITE (kanal,*)manz,dig_min,dig_max
    DO i=1,manz
       WRITE (kanal,*)dig(i),LOG10(dig(i))-LOG10(dig_max)
    END DO

    WRITE (*,*)'Max/Min:',dig_max,'/',dig_min
    CLOSE(kanal)

    IF (lfpi) THEN
       WRITE (*,'(/a/)')'Writing out:: '//TRIM(fname)//'_fpi'
       dig_min = MINVAL(dig_fpi)
       dig_max = MAXVAL(dig_fpi)
       errnr = 1
       OPEN (kanal,file=TRIM(fname)//'_fpi',status='replace',err=999)
       errnr = 4

       WRITE (kanal,*)manz
       DO i=1,manz
          WRITE (kanal,*)dig_fpi(i),LOG10(dig_fpi(i))-LOG10(dig_max)
       END DO
       WRITE (kanal,*)'Max/Min:',dig_max,'/',dig_min
       WRITE (*,*)'Max/Min:',dig_max,'/',dig_min
       CLOSE(kanal)
    END IF
    DEALLOCATE (dig,dig_fpi)

    errnr = 0
999 RETURN

  END SUBROUTINE bata

  SUBROUTINE bata_reg(kanal)
!!!$
!!!$    Unterprogramm berechnet A^HC_d^-1A+lam*C_m
!!!$    Fuer beliebige Triangulierung
!!!$
!!!$    Copyright Andreas Kemna
!!!$    Erstellt von Roland Martin                           02-Nov-2009
!!!$
!!!$    Last changed      RM                               31-Mar-2010
!!!$
!!!$.....................................................................
!!!$   PROGRAMMINTERNE PARAMETER:
    INTEGER                        :: kanal ! io number
!!!$   Hilfsvariablen
    INTEGER                        :: i,j,k,ik
    REAL(KIND(0D0)),DIMENSION(:),ALLOCATABLE  :: dig
    REAL(KIND(0D0))                           :: dig_min,dig_max
    INTEGER                                      :: c1
    CHARACTER(80)                                :: csz
!!!$.....................................................................

!!!$  A^TC_d^-1A+lamC_m

    errnr = 1
    open(kanal,file=TRIM(fetxt),status='replace',err=999)
    errnr = 4

    ALLOCATE(dig(manz))

    CALL TIC (c1)

    IF (ltri == 0) THEN

       ata_reg = ata
       DO j=1,manz
        DO i=1,manz

          write(*,'(a,1X,F6.2,A)',advance='no')ACHAR(13)// &
               'ATC_d^-1A+reg/ ',REAL( j * (100./manz)),'%'

          ata_reg(j,j) =  ata(j,j) + lam * smatm(i,1) ! main diagonal

          IF (i+1 < manz) THEN
             ata_reg(i+1,j) = ata(i+1,j) + lam * smatm(i+1,2) ! nebendiagonale in x richtung
             ata_reg(j,i+1) = ata_reg(i+1,j) ! lower triangle
          END IF
          IF (i+nx < manz) THEN
             ata_reg(i+nx,j) = ata(i+nx,j) + lam * smatm(i+nx,3) ! nebendiagonale in z richtung
             ata_reg(j,i+nx) = ata_reg(i+nx,j) ! lower triangle
          END IF
        END DO
          dig(j) = ata_reg(j,j)

       END DO

    ELSE IF (ltri == 3.OR.ltri == 4) THEN

       ata_reg = ata

       DO i=1,manz
          dig (i) = ata(i,i) + lam * smatm(i,1)
          ata_reg(i,i) = dig(i)
       END DO

    ELSE IF (ltri == 1.OR.ltri == 2.OR.(ltri > 4 .AND. ltri < 15)) THEN

       ata_reg = ata ! just copy and fill the other information afterwards

       DO j=1,manz

          write(*,'(a,1X,F6.2,A)',advance='no')ACHAR(13)// &
               'ATC_d^-1A+reg/ ',REAL( j * (100./manz)),'%'

          ata_reg(j,j) = ata(j,j) + lam * smatm(j,max_nr_element_nodes+1) ! main diagonal

          DO k=1,nachbar(j,max_nr_element_nodes+1) ! off diagonal

             ik = nachbar(j,k)

             IF (ik == 0) CYCLE ! check if there actually is a neighbor

             ata_reg(ik,j) = ata(ik,j) + lam * smatm(j,k) ! upper triangle

             ata_reg(j,ik) = ata_reg(ik,j) ! lower triangle

          END DO

          dig(j) = ata_reg(j,j)

       END DO

    ELSE IF (ltri == 15) THEN

       ata_reg= ata + lam * smatm ! for full C_m..w

       DO j=1,manz
          dig(j) = ata_reg(j,j)
       END DO

    END IF

    csz = 'ATA+RTR time'
    CALL TOC(c1,csz)

    dig_min = MINVAL(dig)
    dig_max = MAXVAL(dig)

    WRITE (kanal,*)manz,lam
    DO i=1,manz
       WRITE (kanal,*)dig(i),LOG10(dig(i))
    END DO

    WRITE (kanal,*)'Max/Min:',dig_max,'/',dig_min
    WRITE (*,*)'Max/Min:',dig_max,'/',dig_min

    CLOSE(kanal)

    DEALLOCATE (dig)

    errnr = 0
999 RETURN

  END SUBROUTINE bata_reg

  SUBROUTINE bmcm(kanal,ols)
!!!$
!!!$    Unterprogramm berechnet (einfache) Modell Kovarianz Matrix
!!!$    (A^TC_d^-1A + C_m^-1)^-1
!!!$    Fuer beliebige Triangulierung
!!!$
!!!$    Copyright Andreas Kemna 2009
!!!$    Created by  Roland Martin                            02-Nov-2009
!!!$
!!!$    Last changed      RM                                   20-Feb-2010
!!!$
!!!$.....................................................................
!!!$   PROGRAMMINTERNE PARAMETER:
!!!$   Hilfsvariablen
    INTEGER                                    :: i,kanal,j,c1
    REAL(KIND(0D0)),DIMENSION(:,:),ALLOCATABLE :: work
    REAL(KIND(0D0)),DIMENSION(:),ALLOCATABLE   :: dig
    REAL(KIND(0D0))                            :: dig_min,dig_max
    REAL (KIND(0D0))                           :: dre,dim
    COMPLEX(KIND(0D0))                         :: dsi
    LOGICAL,INTENT(IN),OPTIONAL                :: ols
    CHARACTER(80)                              :: csz
!!!$....................................................................

!!!$  invert (A^TC_d^-1A + C_m^-1)

    errnr = 1

    ALLOCATE (dig(manz)) !dig is a working array and contains main diagonal


!!!$    get time
    CALL TIC(c1)

    cov_m = ata_reg

    IF (.NOT.PRESENT(ols).OR..NOT.ols) THEN !default

       WRITE (*,'(a)',ADVANCE='no')ACHAR(13)//'Factorization...'

       CALL CHOLD(cov_m,dig,manz,errnr,lverb)
       IF (errnr /= 0) THEN
          fetxt='CHOLD mcm :: matrix not pos definite..'
          PRINT*,'Zeile(',abs(errnr),')'
          errnr = 108
          RETURN
       END IF

       csz = 'Factorization time'
       CALL TOC(c1,csz)


       CALL TIC(c1)
       WRITE (*,'(a)',ADVANCE='no')ACHAR(13)//'Inverting...'

       CALL LINVD(cov_m,dig,manz,lverb)

       WRITE (*,'(a)',ADVANCE='no')ACHAR(13)//'Filling lower Cov...'

!!$       !$OMP PARALLEL DEFAULT (none) &
!!$       !$OMP SHARED (cov_m,manz,lverb) &
!!$       !$OMP PRIVATE (i,j)
!!$       !$OMP DO SCHEDULE (GUIDED,CHUNK_0)

       DO i= 1 , manz

          IF (lverb) WRITE (*,'(A,t45,F6.2,A)',ADVANCE='no')&
               ACHAR(13)//'Filling lower/',REAL( i * (100./manz)),'%'

          DO j = 1 , i - 1

             cov_m(i,j) = cov_m(j,i)

          END DO

       END DO

!!$       !$OMP END PARALLEL

       csz = 'Inversion time'
       CALL TOC(c1,csz)


    ELSE
       WRITE (*,'(a)',ADVANCE='no')'Inverting Matrix (Gauss elemination)'

       CALL gauss_dble(cov_m,manz,errnr)

       IF (errnr /= 0) THEN
          fetxt = 'error matrix inverse not found'
          PRINT*,'Zeile::',cov_m(abs(errnr),:)
          PRINT*,'Spalte::',cov_m(:,abs(errnr))
          errnr = 108
          RETURN
       END IF

       csz = 'Inversion time'
       CALL TOC(c1,csz)

    END IF

    IF (lverb) THEN

       ALLOCATE (work(manz,manz),STAT=errnr)
       IF (errnr/=0) THEN
          fetxt = 'Allocation problem WORK in bmcm'
          errnr = 97
          RETURN
       END IF

       !$OMP WORKSHARE
       work = MATMUL(cov_m,ata_reg)
       !$OMP END WORKSHARE

       DO i=1,manz
          IF (ABS(work(i,i) - 1d0) > 0.1) PRINT*,'bad approximation at parameter'&
               ,i,work(i,i)
       END DO
       DEALLOCATE (work)

    END IF

    DO i=1,manz
       dig(i) = cov_m(i,i)
    END DO

    dig_min = MINVAL(dig)
    dig_max = MAXVAL(dig)

!!$In order to find subsequent error expressions for our displayed model parameters, we identify the standard deviation as first order finite difference
!!$\begin{equation}
!!$\Delta:=\sqrt{diag\left\lbrace \MAT{C}_{m^*}^m\left( \lambda \right) \right\rbrace}
!!$\end{equation}
!!$and equate the model parameter within it's error bars:
!!$\begin{equation}
!!$m^*=m(1\pm\Delta)= (\ln{|\sigma|}+i\phi)(1+\Delta)
!!$\end{equation}
!!$From Equation \ref{eq:err_m} we see, that our real-valued covariance matrix error quantities are the same for real and imaginary part of the parameters:
!!$\begin{equation}
!!$\Delta m=\Delta \ln{|\rho|}+i\Delta \phi =\Delta \ln{|\sigma|}+i\Delta \phi\;. \label{eq:d_logm}
!!$\end{equation}
!!$If we now like to equate the errors for real and imaginary part of our complex conductivities, we have to reconsider their definitions.
!!$\begin{align}
!!$\sigma'&=|\sigma|\cos{\phi}\\
!!$\sigma'&=|\sigma|\sin{\phi}\;,
!!$\end{align}
!!$and build the total differential for the real part:
!!$\begin{align}
!!$\MMF{d} \sigma'&=\frac{\partial \sigma'}{\partial |\sigma|}\MMF{d}|\sigma| + \frac{\partial \sigma'}{\partial\phi}\MMF{d}\phi \\
!!$&=\frac{\partial \sigma'}{\partial |\sigma|}\frac{\partial |\sigma|}{\partial \ln{|\sigma|}}\MMF{d}\ln{|\sigma|} +
!!$|\sigma|\sin{\phi}\MMF{d}\phi \\
!!$&= \cos{\phi}|\sigma|\MMF{d}\ln{|\sigma|}+\sin{\phi}|\sigma|\MMF{d}\phi\;.
!!$\end{align}
!!$\begin{equation}
!!$\Delta \sigma'=\Delta |\sigma|\left(\cos{\phi}+\sin{\phi}\right)
!!$\end{equation}
!!$For the imaginary part we find
!!$\begin{align}
!!$\MMF{d} \sigma''&=\frac{\partial \sigma''}{\partial |\sigma|}\MMF{d}|\sigma| + \frac{\partial \sigma''}{\partial\phi}\MMF{d}\phi \\
!!$%&=\frac{\partial \sigma''}{\partial |\sigma|}|\sigma|\Delta\ln{|\sigma|} - |\sigma|\cos{\phi}\Delta\phi \\
!!$&= \sin{\phi}|\sigma|\Delta\ln{|\sigma|}-\cos{\phi}|\sigma|\Delta\phi \\
!!$&=\Delta |\sigma|\left(\sin{\phi}-\cos{\phi}\right)\;.
!!$\end{align}

    errnr = 1
    OPEN (kanal,file=TRIM(fetxt),status='replace',err=999)
    errnr = 4
    WRITE (kanal,*)manz,lam
    DO i=1,manz

       dsi = sigma(i) * SQRT(dig(i))

       dre = DBLE(sigma(i)) * SQRT(dig(i))
       dim = AIMAG(sigma(i)) * SQRT(dig(i))

       WRITE (kanal,*)SQRT(dig(i))*1e2,dre,dim !ABS(REAL(dsi)),ABS(AIMAG(dsi)),dre,dim
    END DO

    WRITE (kanal,*)'Max/Min:',dig_max,'/',dig_min
    WRITE (*,*)'Max/Min:',dig_max,'/',dig_min

    CLOSE(kanal)

    IF (lverb_dat) THEN

       errnr = 1
       open(kanal,file=TRIM(fetxt)//'_full',status='replace',err=999)
       errnr = 4
       DO i = 1, manz
          WRITE (kanal,*)espx(i),espy(i),(cov_m(i,j),j=i,manz)
       END DO

       CLOSE (kanal)
    END IF

    DEALLOCATE (dig)

    errnr = 0
999 RETURN

  END SUBROUTINE bmcm

  SUBROUTINE bres(kanal)
!!!$
!!!$    Unterprogramm berechnet Aufloesungsmatrix
!!!$    Fuer beliebige Triangulierung
!!!$    RES = (A^HC_d^-1A + C_m^-1)^-1 A^HC_d^-1A
!!!$    wobei (A^HC_d^-1A + C_m^-1) bereits invertiert wurde (cov_m)
!!!$
!!!$    Copyright Andreas Kemna 2009
!!!$
!!!$    Created by Roland Martin                            02-Nov-2009
!!!$
!!!$    Last changed      RM                             20-Feb-2010
!!!$.....................................................................
!!!$   PROGRAMMINTERNE PARAMETER:
!!!$   Hilfsvariablen
    INTEGER                                      :: i,j,kanal
    REAL(KIND(0D0)),DIMENSION(:),ALLOCATABLE     :: dig
    REAL(KIND(0D0))                              :: dig_min,dig_max
    INTEGER                                      :: c1
    CHARACTER(80)                                :: csz
!!!$.....................................................................

!!!$  cal!!!$RES = (A^TC_d^-1A + C_m^-1)^-1 A^TC_d^-1A

    errnr = 1
    open(kanal,file=TRIM(fetxt),status='replace',err=999)
    errnr = 4
!!!$    get time
    CALL TIC(c1)

!    !$OMP WORKSHARE
    ata_reg = MATMUL(cov_m,ata) ! that's it...
!    !$OMP END WORKSHARE

    csz = 'MATMUL time'
    CALL TOC(c1,csz)

    ALLOCATE (dig(manz)) !prepare to write out main diagonal

    DO i=1,manz
       dig(i) = ata_reg(i,i)
    END DO

    dig_min = MINVAL(dig)
    dig_max = MAXVAL(dig)

    WRITE (kanal,*) manz, lam, dig_min, dig_max
    DO i=1,manz
       WRITE (kanal,*)abs(dig(i)),LOG10(abs(dig(i)))-LOG10(dig_max)
    END DO

    WRITE (*,*)'Max/Min:',dig_max,'/',dig_min

    CLOSE(kanal)

    IF (lverb_dat) THEN
       errnr = 1
       open(kanal,file=TRIM(fetxt)//'_full',status='replace',err=999)
       errnr = 4
       DO i = 1, manz
          WRITE (kanal,*)espx(i),espy(i),(abs(ata_reg(i,j)),j=i,manz)
       END DO

       CLOSE (kanal)
    END IF

    DEALLOCATE (dig)

    errnr = 0
999 RETURN

  END SUBROUTINE bres

  SUBROUTINE bmcm2(kanal)
!!!$
!!!$    Unterprogramm berechnet Modellkovarianz nach Fehlerfortpflanzung
!!!$    MCM = (A^HC_d^-1A + C_m^-1)^-1 A^HC_d^-1A (A^HC_d^-1A + C_m^-1)^-1
!!!$    Fuer beliebige Triangulierung
!!!$!!!$    Copyright Andreas Kemna/Roland Martin 2009
!!!$    erstellt von Roland Martin                               02-Nov-2009
!!!$
!!!$    Last changed      RM                                   23-Nov-2009
!!!$
    !!!$.........................................................................
    USE alloci
    USE datmod
    USE invmod
    USE modelmod
    USE errmod

    IMPLICIT none

!!!$.....................................................................
!!!$   PROGRAMMINTERNE PARAMETER:
!!!$   Hilfsvariablen
    INTEGER                                      :: kanal
    INTEGER                                      :: i
    REAL(KIND(0D0)),DIMENSION(:),ALLOCATABLE     :: dig
    REAL(KIND(0D0))                              :: dig_min,dig_max
    COMPLEX(KIND(0D0))                           :: dsig
    INTEGER                                      :: c1
    CHARACTER(80)                                :: csz
!!!$.....................................................................
!!!$   vorher wurde schon
!!!$   ata_reg_dc= (A^TC_d^-1A + C_m^-1)^-1 A^TC_d^-1A berechnet
!!!$   cov_m_dc= (A^TC_d^-1A + C_m^-1)^-1


    errnr = 1
    open(kanal,file=TRIM(fetxt),status='replace',err=999)
    errnr = 4

!!!$    get time
    CALL TIC(c1)

!    !$OMP WORKSHARE
    ata = MATMUL (ata_reg,cov_m)
!    !$OMP END WORKSHARE

    csz = 'MATMUL time'
    CALL TOC(c1,csz)

    ALLOCATE (dig(manz))

    DO i=1,manz
       dig(i) = ata(i,i)
    END DO

    dig_min = MINVAL(dig)
    dig_max = MAXVAL(dig)

    WRITE (kanal,*)manz,lam
    DO i=1,manz
       dsig = sigma(i) * SQRT(dig(i))
       WRITE (kanal,*)SQRT(dig(i))*1d2, REAL(dsig), AIMAG(dsig)
    END DO

    WRITE (kanal,*)'Max/Min:',dig_max,'/',dig_min
    WRITE (*,*)'Max/Min:',dig_max,'/',dig_min

    CLOSE(kanal)

    DEALLOCATE (dig)

    errnr = 0

999 RETURN

  END SUBROUTINE bmcm2
END MODULE bmcm_mod
