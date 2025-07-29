!> \file rsigma.f90
!> \brief read model conductivity file.
!> \details Read model conductivity file and store it in the complex format \f$ \sigma = \frac{1}{| \rho |} \exp^{\i \varphi} \f$
!> @author Andreas Kemna 
!> @date 10/11/1993


SUBROUTINE rsigma(kanal,datei)

!     Unterprogramm zum Einlesen der Widerstandsverteilung aus 'datei'.

!     Andreas Kemna                                            20-Dec-1993
!     Letzte Aenderung   07-Nov-1997

!.....................................................................

  USE make_noise
  USE alloci,ONLY:rnd_r,rnd_p
  USE femmod
  USE invmod
  USE sigmamod
  USE modelmod
  USE elemmod
  USE errmod
  USE konvmod

  IMPLICIT NONE

!.....................................................................

!     EIN-/AUSGABEPARAMETER:

!> unit number
  INTEGER (KIND=4) ::    kanal

!> filename
  CHARACTER (80)   ::    datei

!.....................................................................
! FUNCTION
  INTEGER :: set_ind_ref_grad

!     PROGRAMMINTERNE PARAMETER:

!     Hilfsvariablen
  INTEGER (KIND=4) ::     i,idum,ifp1,ifp2
  REAL(KIND(0D0))  ::     bet,pha,eps_r,eps_p,bet_ref,pha_ref
! Pi
  REAL (KIND(0D0)) ::    pi
!.....................................................................
  pi = dacos(-1d0)

  lw_ref = .FALSE.
  lam_ref = -1d0 
  lam_ref_sw = 0

!     'datei' oeffnen
  fetxt = datei

  errnr = 1
  OPEN(kanal,file=TRIM(fetxt),status='old',err=999)

  errnr = 3
  IF (lnsepri) THEN
     PRINT*,''
     CALL get_unit(ifp1)
     PRINT*,'iseedpri / std. err.',iseedpri,modl_stdn
     OPEN (ifp1,FILE='tmp.mynoise_mprior_rho',STATUS='replace')
     WRITE (*,'(A)',advance='no')' Initializing noise '
     ALLOCATE (rnd_r(elanz))
     CALL Random_Init(iseedpri)
     DO i=1,elanz
        rnd_r(i) = Random_Gauss()
     END DO
     IF (.NOT.ldc) THEN
        CALL get_unit(ifp2)
        OPEN (ifp2,FILE='tmp.mynoise_mprior_phase',STATUS='replace')
        ALLOCATE (rnd_p(elanz))
        CALL Random_Init(-iseedpri)
        DO i=1,elanz
           rnd_p(i) = Random_Gauss()
        END DO
     END IF
     PRINT*,''
  END IF

!     Anzahl der Messwerte lesen
! also check if we may use individual errors or not
!!! Failsafe read in one line

  READ(kanal,*,END=11,err=11) idum,lw_ref,lam_ref,lam_ref_sw
  WRITE (*,'(a)',ADVANCE='no')'Successful I/O of all reference regu options'
  IF (lw_ref) THEN
     IF (lam_ref_sw == 1) WRITE(*,'(a)')&
          '  -> vertical gradient'
     IF (lam_ref_sw == 2) WRITE(*,'(a)')&
          '  -> horizontal gradient'
  END IF
  GOTO 12
11 IF (lam_ref < 0d0) lam_ref = 1d0 
  BACKSPACE (kanal)
  
12 IF (lw_ref) THEN
     

     ALLOCATE (ind_ref_grad(manz)) ! which is in fact manz for now
     
     ind_ref_grad = 0

     PRINT*,'---> Reference model regularization '
     IF (lam_ref <= EPSILON(REAL(lam_ref))) THEN
        lam_ref = 0d0 ! so, what again is zero ??
     END IF
     PRINT*,'     lambda ref (factor)=',lam_ref
  END IF

!     Ggf. Fehlermeldung
  IF (idum.NE.elanz) THEN
     fetxt = ' '
     errnr = 47
     GOTO 1000
  END IF
  


!     Betrag und Phase (in mrad) des komplexen Widerstandes einlesen
  DO i=1,elanz
     
     IF (lw_ref) THEN
!!$        IF (ldc) THEN
!!$           READ(kanal,*,END=1001,err=1002) bet,pha,bet_ref,w_ref_re(mnr(i))
!!$           pha_ref = 0d0
!!$        ELSE
        READ(kanal,*,END=1001,err=1002) bet,pha,bet_ref,eps_r,pha_ref,eps_p
        w_ref_re(mnr(i)) = eps_r * eps_r ! make std err -> variance
        w_ref_im(mnr(i)) = eps_p * eps_p ! std err -> variance
        pha_ref = 1d-3 * pha_ref ! mRad -> Rad
!!$        END IF
     ELSE
        READ(kanal,*,END=1001,err=1000) bet,pha
     END IF

     pha      = 1d-3*pha

     IF (lprior) THEN 
        !     set prior model ...             
        IF (bet0 <= 0. .OR. &
             (.NOT.ldc.AND.dabs(pha0).GT.1d3*pi)) THEN
           fetxt = 'starting model incorrect '
           errnr = 91
           GOTO 999
        END IF

        IF (bet > 0d0) THEN  
           !     TODO: meaningful phase check.. 
           IF (lnsepri) THEN
              eps_r = 1d-2*modl_stdn * bet
              WRITE(ifp1,'(3(G14.4,1X))',ADVANCE='no')rnd_r(i),eps_r,bet
              bet = bet + rnd_r(i) * eps_r
              WRITE(ifp1,'(G14.4)')bet
              IF (.NOT. ldc) THEN
                 eps_p = 1d-2*modl_stdn*dabs(pha)
                 WRITE(ifp2,'(3(G14.4,1X))',ADVANCE='no')rnd_p(i),eps_p,pha
                 pha = pha + rnd_p(i) * eps_p
                 WRITE(ifp2,'(G14.4)')pha
              END IF
           END IF
           sigma(i) = dcmplx(dcos(pha)/bet,-dsin(pha)/bet)
!    hier koennte mittelung passieren
           m0(mnr(i)) = cdlog(sigma(i))
        ELSE                
           !     or let it stay at zero and take background cond
           sigma(i) = dcmplx( dcos(pha0/1d3)/bet0 , -dsin(pha0/1d3)/bet0 )
           m0(mnr(i)) = DCMPLX(0d0)
        END IF

     ELSE

!     Ggf. Fehlermeldung
        IF (bet.LT.1d-12) THEN
           fetxt = ' '
           errnr = 11
           GOTO 999
        END IF

!     Komplexe Leitfaehigkeit bestimmen
        sigma(i) = dcmplx(dcos(pha)/bet,-dsin(pha)/bet)

     END IF

! >> RM ref model regu
     IF (.NOT.lw_ref) CYCLE ! next i 
     IF (w_ref_re(mnr(i)) > EPSILON(eps_r)) THEN

! variance -> inverse weighting        
        w_ref_re(mnr(i)) = 1d0/w_ref_re(mnr(i))

! assign m_ref = \ln(|\sigma|) + i \phi(\sigma) 
!              = -\ln(|\rho|) - i\phi(\rho) 
!              = - (\ln(|\rho|)+i\phi(\rho)
! for \phi(z) = Im(z) / Re(z), z\inC

        m_ref(mnr(i)) = -DCMPLX(DLOG(bet_ref),pha_ref)
        IF (w_ref_im(mnr(i)) > EPSILON(eps_p)) THEN
           w_ref_im(mnr(i)) = 1d0/w_ref_im(mnr(i))
        ELSE ! force zero
           w_ref_im(mnr(i)) = 0D0
        END IF

        ind_ref_grad(i) = set_ind_ref_grad(i)

     ELSE
        m_ref(mnr(i)) = DCMPLX(0d0)

     END IF
! << RM ref model regu

  END DO

!     'datei' schliessen
  CLOSE(kanal)

  IF (lw_ref .AND. lam_ref_sw > 0) THEN
     OPEN (kanal,FILE='tmp.ind_ref',STATUS='replace')
     DO i = 1,elanz
        IF (ind_ref_grad(i) /= 0) WRITE (kanal,*) &
             i,ind_ref_grad(i),REAL(espx(i)),REAL(espy(i)),&
             REAL(espx(ind_ref_grad(i))),REAL(espy(ind_ref_grad(i)))
     END DO
     CLOSE (kanal)
  END IF
!  IF (lw_ref .AND. (lam_ref_sw > 0)) CALL set_ind_ref_grad2

  IF (lnsepri) THEN
     CLOSE (ifp1)
     IF (.NOT.ldc) CLOSE(ifp2)
  END IF

  errnr = 0
  RETURN

!:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

!     Fehlermeldungen

999 RETURN

1000 CLOSE(kanal)
  RETURN

1001 CLOSE(kanal)
  errnr = 2
  RETURN

1002 CLOSE(kanal)
  fetxt = 'reference assignment failed'
  errnr = 2
  RETURN

END SUBROUTINE rsigma

INTEGER FUNCTION set_ind_ref_grad(i)

  USE elemmod
  USE konvmod, ONLY: lam_ref_sw

  IMPLICIT NONE

  INTEGER :: k,nik
  INTEGER,INTENT(IN) :: i
  REAL(KIND(0d0)) :: ax,ay

  set_ind_ref_grad = 0

  DO k = 1, nachbar(i,max_nr_element_nodes + 1) ! check all neighboring elements
     
     nik = nachbar(i,k)
     
     IF (nik == 0) CYCLE ! if it is not a neighbor.. skip it
!!! else check the element number
     ax = ABS(espx(i) - espx(nik)) ! center point differences
! for vertical gradient, this needs to be smaller than the grid distance
     ay = ABS(espy(i) - espy(nik)) ! center point differences
     
     
     IF ( ((lam_ref_sw == 1) .AND. &
          (ax >= grid_minx .OR. espy(nik) > espy(i))) .OR. &
          ((lam_ref_sw == 2) .AND. &
          (ay >= grid_miny .OR. espx(nik) < espx(i))) ) CYCLE
     
     set_ind_ref_grad = nik
     
  END DO

END FUNCTION  set_ind_ref_grad

SUBROUTINE set_ind_ref_grad2
  USE sigmamod
  USE modelmod
  USE elemmod
  USE errmod
  USE elemmod
  USE konvmod, ONLY: lam_ref_sw

  IMPLICIT NONE

  INTEGER :: i,k,nik
  INTEGER :: ifp
  REAL(KIND(0d0)) :: ax,ay


  PRINT*,'setting ind_ref_grad'
  CALL get_unit(ifp)
  OPEN (ifp,FILE='tmp.ind_ref',STATUS='replace')

  DO i = 1,elanz

     DO k = 1, nachbar(i,max_nr_element_nodes + 1) ! check all neighboring elements

        nik = nachbar(i,k)

        IF (nik == 0) CYCLE ! if it is not a neighbor.. skip it
!!! else check the element number
        ax = ABS(espx(i) - espx(nik)) ! center point differences
! for vertical gradient, this needs to be smaller than the grid distance
        ay = ABS(espy(i) - espy(nik)) ! center point differences
        

!!$        IF (lam_ref_sw == 1 ) THEN ! vertical gradient
!!$           IF (ax < grid_minx) THEN ! if the points are at the same profile coordinate
!!$!!! There are just two or less more pints: 
!!$! one above and one below
!!$              PRINT*,i,nachbar(i,k)
!!$              IF (espy(nachbar(i,k)) < espy(i)) THEN ! is the point is _below_ the other..
!!$! save its number
!!$                 ind_ref_grad(i) = nachbar(i,k)
!!$              END IF
!!$           END IF
!!$        ELSE
!!$           IF (ay < grid_miny) THEN ! if the points are at the same profile coordinate
!!$              IF (espx(nachbar(i,k)) > espx(i)) THEN ! i the point is _below_ the other..
!!$                 ind_ref_grad(i) = nachbar(i,k)
!!$              END IF
!!$           END IF
!!$
!!$        END IF


! shorter XOR variant

        IF ( ((lam_ref_sw == 1) .AND. &
             (ax >= grid_minx .OR. espy(nik) > espy(i))) .OR. &
             ((lam_ref_sw == 2) .AND. &
             (ay >= grid_miny .OR. espx(nik) < espx(i))) ) CYCLE

        ind_ref_grad(i) = nik
        
     END DO

     IF (ind_ref_grad(i) /= 0) THEN
        WRITE (ifp,*) i,ind_ref_grad(i),REAL(espx(i)),&
             REAL(espy(i)),REAL(espx(ind_ref_grad(i))),REAL(espy(ind_ref_grad(i)))
     ELSE
        WRITE (ifp,*) nachbar(i,max_nr_element_nodes + 1),i,ind_ref_grad(i),REAL(espx(i)),REAL(espy(i))
     END IF


  END DO

  CLOSE (ifp)


END SUBROUTINE set_ind_ref_grad2
