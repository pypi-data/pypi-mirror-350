MODULE brough_mod
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!$ Collection of subroutines calculate model roughness term
!!!$ for different regularizations
!!!$ 
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!$ Copyright by Andreas Kemna 2010
!!!$
!!!$ Created by Roland Martin               30-Jul-2010
!!!$
!!!$ Last changed       RM                  Jul-2010
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

  USE alloci , ONLY : smatm
  USE invmod , ONLY : lfpi,par,m0
  USE konvmod , ONLY : ltri,nx,nz,lprior,rough
  USE modelmod , ONLY : manz
  USE elemmod, ONLY : max_nr_element_nodes,nachbar
  USE errmod , ONLY : errnr,fetxt
  USE datmod , ONLY : nanz

  IMPLICIT none

  PUBLIC :: brough
!!!$ controls which smatm to use

PRIVATE :: broughreg
!!!$ uses smatm of smooth regularization for regular grids (sparse smatm)
PRIVATE :: broughtri
!!!$ uses smatm for unstructured grids (recommended). this is (sparse smatm)
!!!$ used for MGS/TV regu as well..
PRIVATE :: broughlma
!!!$ smatm for Levenberg or Levenberg-Marquardt (diagonal smatm)
PRIVATE :: broughsto
!!!$ smatm for stochastical regu (full M^2 matrix)

CONTAINS

  SUBROUTINE brough

!!!$   Roughness bestimmen
      IF (ltri == 0) THEN
         CALL broughreg()
      ELSE IF (ltri == 1.OR.ltri == 2.OR.&
           (ltri > 4 .AND. ltri < 15)) THEN
         CALL broughtri
      ELSE IF (ltri == 3.OR.ltri == 4) THEN
         CALL broughlma
      ELSE IF (ltri == 15) THEN
         CALL broughsto
      END IF

  END SUBROUTINE brough

  subroutine broughreg()

!!!$   Unterprogramm zum Belegen der Leitfaehigkeit und zum Bestimmen der
!!!$   Rauhigkeit.
!!!$
!!!$   Andreas Kemna                                            12-Apr-1996
!!!$   Letzte Aenderung   15-Jan-2001
!!!$
!!!$.....................................................................
!!!$   PROGRAMMINTERNE PARAMETER:

!!!$   Hilfsvariablen
    INTEGER ::     i
    COMPLEX(KIND(0D0)) ::    cdum
!!!$   cdum describes (R^TR)m
!!!$.....................................................................

!!!$   Roughness bestimmen
    rough = 0d0

    do i=1,manz
       cdum = dcmplx(0d0)

!!!$   diff+<
       if (.not.lprior) then
!!!$   diff+>
          if (i.gt.1) &
         cdum = dcmplx(smatm(i-1,2))*par(i-1)
          if (i.lt.manz) &
         cdum = cdum + dcmplx(smatm(i,2))*par(i+1)
          if (i.gt.nx) &
               cdum = cdum + dcmplx(smatm(i-nx,3))*par(i-nx)
          if (i.lt.manz-nx+1) &
         cdum = cdum + dcmplx(smatm(i,3))*par(i+nx)

          cdum = cdum + dcmplx(smatm(i,1))*par(i)

          if (lfpi) then
             rough = rough + dimag(cdum)*dimag(par(i))
          else
             rough = rough + dble(cdum*dconjg(par(i)))
          end if
!!!$   diff+<
       else
          if (i.gt.1) &
               cdum = dcmplx(smatm(i-1,2)) * (par(i-1) - m0(i-1))
          if (i.lt.manz) &
               cdum = cdum + dcmplx(smatm(i,2)) * (par(i+1) - m0(i+1))
          if (i.gt.nx) &
               cdum = cdum + dcmplx(smatm(i-nx,3)) * (par(i-nx) - m0(i-nx))
          if (i.lt.manz-nx+1) &
               cdum = cdum + dcmplx(smatm(i,3)) * (par(i+nx) - m0(i+nx))
          
          cdum = cdum + dcmplx(smatm(i,1))*(par(i)-m0(i))
          
          if (lfpi) then
             rough = rough + dimag(cdum) * dimag(par(i) - m0(i))
          else
             rough = rough + dble(cdum*dconjg(par(i) - m0(i)))
          end if
       end if
!!!$   diff+>
    end do

  END subroutine broughreg

  SUBROUTINE broughtri()
!!!$
!!!$   Belegen der Leitfaehigkeit und zum Bestimmen der Rauhigkeit...
!!!$   Fuer beliebige Triangulierung
!!!$
!!!$   Andreas Kemna                                            12-Apr-1996
!!!$
!!!$   Letzte Aenderung                                         29-Jul-2009
!!!$
!!!$.....................................................................
!!!$  PROGRAMMINTERNE PARAMETER:
!!!$  Hilfsvariablen
    INTEGER ::     i,j
    COMPLEX(KIND(0D0)) ::    cdum
!!!$ cdum describes (R^TR)m
!!!$.....................................................................
!!!$  Roughness bestimmen
    rough = 0d0
    IF (.NOT. lprior) THEN
       DO i=1,manz
          cdum = dcmplx(0d0)
          DO j=1,max_nr_element_nodes
             IF (nachbar(i,j) /= 0) cdum = cdum + &
                  DCMPLX(smatm(i,j)) * par(nachbar(i,j))
          END DO
          cdum = cdum + dcmplx(smatm(i,max_nr_element_nodes+1)) * par(i)
          IF (lfpi) THEN
             rough = rough + dimag(cdum) * dimag(par(i))
          ELSE
             rough = rough + dble(cdum * dconjg(par(i)))
          END IF
       END DO
    ELSE 
       DO i=1,manz
          cdum = dcmplx(0d0)
          DO j=1,max_nr_element_nodes
             IF (nachbar(i,j) /= 0) cdum = cdum + &
                  DCMPLX(smatm(i,j)) * &
                  (par(nachbar(i,j)) - m0(nachbar(i,j)))
          END DO
          cdum = cdum + dcmplx(smatm(i,max_nr_element_nodes+1)) * (par(i) - m0(i))
          IF (lfpi) THEN
             rough = rough + dimag(cdum) * dimag(par(i) - m0(i))
          ELSE
             rough = rough + dble(cdum * dconjg(par(i) - m0(i)))
          END IF
       END DO
    END IF

  END SUBROUTINE broughtri

  SUBROUTINE broughlma
!!!$
!!!$   Unterprogramm zum Belegen der Leitfaehigkeit und zum Bestimmen der
!!!$   Rauhigkeit fuer Levenberg-Marquardt 
!!!$
!!!$   Copyright by Andreas Kemna 2010
!!!$   
!!!$   Andreas Kemna / Roland Martin                            24-Feb-2010
!!!$
!!!$   Letzte Aenderung   RM                                    24-Feb-2010
!!!$
!!!$.....................................................................
!!!$   PROGRAMMINTERNE PARAMETER:
!!!$   Hilfsvariablen
    INTEGER ::     i,j
    COMPLEX(KIND(0D0)) ::    cdum
!!!$.....................................................................
!!!$   Roughness bestimmen

    rough = 0d0

    DO j=1,manz
       IF (.NOT. lprior) THEN

          cdum = DCMPLX(smatm(j,1)) * par(j)

          IF (lfpi) THEN

             rough = DIMAG(cdum) * SUM(DIMAG(par))

          ELSE

             rough = DBLE(cdum) * REAL(SUM(DCONJG(par)))

          END IF

       ELSE

          cdum = DCMPLX(smatm(j,1)) * (par(j)-m0(j))

          IF (lfpi) THEN

             DO i=1,manz
                rough = rough + dimag(cdum)*dimag(par(i)-m0(i))
             END DO
          ELSE
             DO i=1,manz
                rough = rough + dble(cdum*dconjg(par(i)-m0(i)))
             END DO
          END IF
       END IF

    END DO

  END SUBROUTINE broughlma

  SUBROUTINE broughsto
!!!$
!!!$   Unterprogramm zum Belegen der Leitfaehigkeit und zum Bestimmen der
!!!$   Rauhigkeit. 
!!!$   Angepasst an die neue Regularisierungsmatrix (stoch. Kovarianzmatrix).
!!!$   
!!!$   Copyright by Andreas Kemna 2009
!!!$   
!!!$   Andreas Kemna / Roland Martin                            10-Jun-2009
!!!$   
!!!$   Letzte Aenderung   RM                                    30-Jun-2009
!!!$   
!!!$.....................................................................
!!!$   PROGRAMMINTERNE PARAMETER:
!!!$   Hilfsvariablen
    COMPLEX(KIND(0D0)),DIMENSION(:),ALLOCATABLE :: parh
!!!$   parh: Parameter-Hilfsvektor (R^TR)m bzw (C_m^-1)m
!!!$.....................................................................
!!!$   Roughness bestimmen
    
    IF (.NOT. ALLOCATED(parh)) ALLOCATE (parh(manz),STAT=errnr)
    IF (errnr/=0) THEN
       fetxt = 'Allocation problem parh in proughsto'
       WRITE (*,'(/a/)')TRIM(fetxt)
       errnr = 97
       RETURN
    END IF
 
    IF (.NOT. lprior) THEN

       !$OMP WORKSHARE
       parh = MATMUL(par,DCMPLX(smatm))
       !$OMP END WORKSHARE

       IF (lfpi) THEN
          rough = DOT_PRODUCT(DIMAG(parh),DIMAG(par))
       ELSE
          rough = DOT_PRODUCT(DBLE(parh),REAL(DCONJG(par)))
       END IF

    ELSE

       !$OMP WORKSHARE
       parh = MATMUL((par - m0),DCMPLX(smatm))
       !$OMP END WORKSHARE

       IF (lfpi) THEN
          rough = DOT_PRODUCT(DIMAG(parh),DIMAG(par - m0))
       ELSE
          rough = DOT_PRODUCT(DBLE(parh),REAL(DCONJG(par - m0)))
       END IF

    END IF

    IF (ALLOCATED (parh)) DEALLOCATE (parh)

  END SUBROUTINE broughsto

END MODULE brough_mod
