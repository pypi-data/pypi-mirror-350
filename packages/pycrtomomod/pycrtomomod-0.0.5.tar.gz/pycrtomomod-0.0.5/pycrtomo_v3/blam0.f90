!> \file blam0.f90
!> \brief compute the starting regularizazion parameter
!> \details The starting regularization parameter  \f$ \lambda_0 \f$ is determined from
!> - <I>lamnull_cri </I>file in the current directory if llamf <I> modulo </I> 2 = 1 and \f$ nz \neq -1\f$ in <I>crmod.cfg</I> 
!> - \f$\max(nanz,manz) \f$ the maximum of either the nr of model parameters and the number of measurements if llamf <I> modulo </I> 2 = 1 and \f$ nz = -1 \f$
!> - else (the common way): Kemna (2000): Following the suggestion of Newman and Alumbaugh (1997), an adequate starting value \f$ \lambda_0 \f$ at the first inverse iteration step may be estimated from the row sums of the matrix product \f$ A^H W_d^H W_d A \f$. Such a choice properly scales the regularizing term \f$ \lambda W_m^T W_m \f$ at the beginning of the inversion process. However, whereas Newman and Alumbaugh (1997) use the maximum absolute row value which occurs, for the problem considered herein five times the corresponding mean value has been found to be sufficiently large. Taking in addition the smoothing parameters \f$ \alpha_x \f$ and \f$ \alpha_z \f$ into account, it is
!> \f[ \lambda_0 = \frac{2}{\alpha_x + \alpha_z} \frac{5}{M} \sum_{m=1}^M {\left| 4 \sum_{j=1}^M {\sum_{i=1}^N {\frac{\bar a _{im} a_{ij}}{\bar \epsilon_i \epsilon_i}}}\right|}, \f]
!> where \f$ \bar {} \f$ denotes complex conjugation.
!> @author Andreas Kemna
!> @date 02/20/1997, last change 03/07/2003
SUBROUTINE blam0()

!     Unterprogramm zum Bestimmen des Start-Regularisierungsparameters.

!     Andreas Kemna                                            20-Feb-1997
!     Letzte Aenderung   07-Mar-2003

!.....................................................................

  USE alloci
  USE femmod
  USE datmod
  USE invmod
  USE modelmod
  USE konvmod

  IMPLICIT NONE


!.....................................................................

!     PROGRAMMINTERNE PARAMETER:

!     Hilfsvariablen
  COMPLEX (KIND(0D0)) ::  cdum
  REAL (KIND(0D0))    ::  dum

  REAL (KIND(0D0)),ALLOCATABLE , DIMENSION(:) :: jtj

!     Indexvariablen
  INTEGER (KIND = 4)  ::  i,j,k,ic

!.....................................................................

!     Start-Regularisierungsparameter bestimmen

! for fixed lambda set the values according to preset fixed lamfix
  IF (( BTEST(llamf,0) .OR. (lamnull_cri > EPSILON(lamnull_cri)) ) .AND..NOT. &
       lfpi ) THEN
     IF (nz==-1) THEN ! this is a special switch, but only taken for 
!! CRI/DC
        lammax = MAX(REAL(manz),REAL(nanz))
        WRITE (*,'(a,t5,a,G12.4)')ACHAR(13),'taking easy lam_0 ',lammax
     ELSE
        lammax = DBLE(lamnull_cri)
        WRITE (*,'(a,t5,a,G12.4)')ACHAR(13),'-> presetting lam0 CRI',lammax
     END IF
     RETURN
  ELSE IF ( BTEST(llamf,0) .OR. (lamnull_fpi > EPSILON(lamnull_fpi)) ) THEN
     lammax = DBLE(lamnull_fpi)
     WRITE (*,'(a,t5,a,G12.4)')ACHAR(13),'-> presetting lam0 FPI',lammax
     RETURN
  END IF


  ALLOCATE (jtj(manz))

  jtj = 0d0;ic = 0

  
  IF (ldc) THEN

     !$OMP PARALLEL DEFAULT(none) PRIVATE (dum) &
     !$OMP SHARED (manz,nanz,sensdc,wmatd,wdfak,jtj,lverb,ic)
     !$OMP DO SCHEDULE (GUIDED)

     DO j=1,manz
        IF (lverb) THEN
           !$OMP ATOMIC
           ic = ic + 1
           
           WRITE(*,'(a,t70,F6.2,A)',advance='no')ACHAR(13)//&
                'blam0/ ',REAL( ic * (100./manz)),'%'
        END IF
        dum = 0d0

        DO i=1,nanz
           DO k=1,manz
              dum = dum + sensdc(i,j) * sensdc(i,k) * &
                   wmatd(i)*DBLE(wdfak(i))
           END DO

        END DO

        jtj(j) = DABS(dum)
        
     END DO

     !$OMP END PARALLEL

  ELSE IF (lfpi) THEN

     !$OMP PARALLEL DEFAULT(none) PRIVATE (dum) &
     !$OMP SHARED (manz,nanz,sens,wmatd,wdfak,jtj,lverb,ic)
     !$OMP DO SCHEDULE (GUIDED)
     DO j=1,manz
        IF (lverb) THEN
           !$OMP ATOMIC
           ic = ic + 1
           
           WRITE(*,'(a,t70,F6.2,A)',advance='no')ACHAR(13)//&
                'blam0/ ',REAL( ic * (100./manz)),'%'
        END IF

        dum = 0d0

        DO i=1,nanz
           DO k=1,manz
              dum = dum + DBLE(sens(i,j)) * DBLE(sens(i,k)) * &
                   wmatd(i)*DBLE(wdfak(i))
           END DO
        END DO

        jtj(j) = DABS(dum)

     END DO
     !$OMP END PARALLEL

  ELSE

     !$OMP PARALLEL DEFAULT(none) PRIVATE (cdum) &
     !$OMP SHARED (manz,nanz,sens,wmatd,wdfak,jtj,lverb,ic)
     !$OMP DO SCHEDULE (GUIDED)
     DO j=1,manz

        
        IF (lverb) THEN
           !$OMP ATOMIC
           ic = ic + 1
           
           WRITE(*,'(a,t70,F6.2,A)',advance='no')ACHAR(13)//&
                'blam0/ ',REAL( ic * (100./manz)),'%'
        END IF

        cdum = dcmplx(0d0)

        DO i=1,nanz
           DO k=1,manz
              cdum = cdum + dconjg(sens(i,j)) * sens(i,k) * &
                   dcmplx(wmatd(i)*DBLE(wdfak(i)))
           END DO
        END DO
        
        jtj(j) = cdabs(cdum)

     END DO
     !$OMP END PARALLEL

  END IF

  lammax = SUM(jtj)/DBLE(manz)

  DEALLOCATE (jtj)

  lammax = lammax * 2d0/(alfx+alfz)
!     ak Default
  lammax = lammax * 5d0
  WRITE (*,'(a,t5,a,G12.4,t60)')ACHAR(13),'found lam_0 ',lammax

!     ak Synthetic Example (JoH)
!     ak        lammax = lammax * 1d1

!     ak MinFrac
!     ak        lammax = lammax * 5d1

!     ak Test
!     ak        lammax = lammax * 1d1

!     ak AAC
!     ak        lammax = lammax * 5d0
  RETURN
END SUBROUTINE blam0
