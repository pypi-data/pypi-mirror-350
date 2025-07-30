!> \file choldc.f90
!> \brief Cholesky decomposition of the stiffness matrix A for the DC case
!> \details Cholesky decomposition of the stiffness matrix A on the allocated memory of A. The algorithm closely follows <I>CHOBNDN</I> in Schwarz (1991).
!> @author Andreas Kemna
!> @date 10/11/1993

SUBROUTINE choldc(a_chol)

!!!$  Cholesky-Zerlegung der positiv definiten Matrix 'adc'; erfolgt auf dem
!!!$  Platz von 'adc', d.h. bei Auftreten eines Fehlers ist gegebene Matrix
!!!$    'adc' zerstoert.

!!!$   ( Vgl. Subroutine 'CHOBNDN' in Schwarz (1991) )

!!!$   Andreas Kemna                                            11-Oct-1993
!!!$   Letzte Aenderung   07-Mar-2003

!!!$.....................................................................

  USE alloci
  USE elemmod
  USE errmod

  IMPLICIT NONE


!!!$.....................................................................
  REAL (KIND(0D0)),DIMENSION(*)    ::  a_chol

!!!$     PROGRAMMINTERNE PARAMETER:

!!!$     Hilfsvariablen
  INTEGER (KIND = 4)  ::     idi,i0,ij,j0
  INTEGER (KIND = 4)  ::     m1,fi
  REAL (KIND(0D0))    ::     s

!!!$     Indexvariablen
  INTEGER (KIND = 4)  ::     i,j,k

!!!$.....................................................................

  m1 = mb+1

  DO i=1,sanz

     idi = i*m1
     fi  = max0(1,i-mb)
     i0  = idi-i

     DO j=fi,i

        ij = i0+j
        j0 = j*mb
        s  = a_chol(ij)

        DO k=fi,j-1
           s = s - a_chol(i0+k)*a_chol(j0+k)
        END DO

        IF (j.LT.i) THEN

           a_chol(ij) = s / a_chol(j*m1)

        ELSE

           IF (s.LE.0d0) THEN
              fetxt = ' '
              errnr = 28
              RETURN
           END IF

           a_chol(idi) = dsqrt(s)

        END IF

     END DO

  END DO

  errnr = 0

!!!$:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

!!!$     Fehlermeldungen

END SUBROUTINE choldc
