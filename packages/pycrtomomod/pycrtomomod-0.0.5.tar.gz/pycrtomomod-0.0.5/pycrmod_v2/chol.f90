!> \file chol.f90
!> \brief Cholesky decomposition of the stiffness matrix A
!> \details Cholesky decomposition of the stiffness matrix A on the allocated memory of A. The algorithm closely follows <I>CHOBNDN</I> in Schwarz (1991).
!> @author Andreas Kemna
!> @date 10/11/1993

subroutine chol(a_chol)

!     Cholesky-Zerlegung der positiv definiten Matrix 'a'; erfolgt auf dem
!     Platz von 'a', d.h. bei Auftreten eines Fehlers ist gegebene Matrix
!     'a' zerstoert.

!     ( Vgl. Subroutine 'CHOBNDN' in Schwarz (1991) )

!     Andreas Kemna                                            11-Oct-1993
!     Letzte Aenderung   07-Mar-2003

!.....................................................................

  USE alloci
  USE elemmod
  USE errmod
  USE ompmod

  IMPLICIT none


!.....................................................................

!     PROGRAMMINTERNE PARAMETER:
!> stiffness matrix A
  COMPLEX (KIND(0D0)),DIMENSION(*) :: a_chol
  
!     Hilfsvariablen
  INTEGER (KIND = 4)  ::     idi,i0,ij,j0
  INTEGER (KIND = 4)  ::     m1,fi
  COMPLEX (KIND(0D0)) ::  s

!     Indexvariablen
  INTEGER (KIND = 4)  ::     i,j,k

!.....................................................................

  m1 = mb+1

  do i=1,sanz
     idi = i*m1
     fi  = max0(1,i-mb)
     i0  = idi-i
     
     do j=fi,i
        
        ij = i0+j
        j0 = j*mb
        s  = a_chol(ij)

        do k=fi,j-1
           s = s - a_chol(i0+k)*a_chol(j0+k)
        END do

        if (j.lt.i) then

           a_chol(ij) = s / a_chol(j*m1)

        else

           if (cdabs(s).le.0d0) then
              fetxt = ' '
              errnr = 28
              GOTO 1000
           end if

           a_chol(idi) = cdsqrt(s)

        end if

     END do
  END do
  errnr = 0
  return

!:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

!     Fehlermeldungen

1000 return

end subroutine chol
